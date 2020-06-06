from flask_restful import Resource
from flask import request
from models.club import ClubModel, TagModel


class Clubs(Resource):

    @classmethod
    def get(cls):
        clubs = ClubModel.find_all()
        if clubs:
            return {'clubs': [club.json() for club in clubs]}, 200
        else:
            return {'message': "No clubs present"}, 200

    @classmethod
    def post(cls):
        args = request.get_json()
        if 'name' not in args:
            return {"message": "Must include club name"}, 401
        if ClubModel.find_by_name(args['name']):
            return {'message': "Club with that name already exists"}, 400
        if 'description' not in args:
            description = ""
        else:
            description = args['description']
        club = ClubModel(name=args['name'], description=description)

        if 'tags' in args:
            for tag in args['tags']:
                new_tag = TagModel.find_by_name(tag)
                if not new_tag:
                    new_tag = TagModel(tag)
                    new_tag.add_to_db()
                new_tag.clubs.append(club)
                club.add_tag(new_tag)

        club.save_to_db()
        return club.json(), 200