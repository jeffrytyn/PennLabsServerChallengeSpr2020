from flask import request
from flask_restful import Resource
from models.user import UserModel
import bcrypt


class User(Resource):
    @classmethod
    def get(cls, username):
        user = UserModel.find_by_name(username)
        if user:
            return user.json(), 200
        return {"message": "No such user exists"}, 400

class UserSignUp(Resource):
    @classmethod
    def post(cls):
        args = request.get_json()
        if 'password' not in args or 'username' not in args:
            return {"message": "Missing password or username"}, 400

        user = UserModel.find_by_name(args['username'])
        if user:
            return {"message": "user exists"}, 400
        user = UserModel(args['username'], args['password'])
        user.save_to_db()
        return user.json(), 200


class FavoriteClub(Resource):
    @classmethod
    def post(cls, club_name):
        data = request.get_json()
        if 'username' not in data or 'password' not in data:
            return {"message": "Must specify username to favorite club"}, 400
        user = UserModel.find_by_name(data['username'])
        pw_encode = data['password'].encode()
        if user:
            if bcrypt.checkpw(pw_encode, user.password):
                return user.fav_club_toggle(club_name), 200
            return {"message": "Incorrect password"}, 200
        else:
            return {"message": "No such user exists"}, 400