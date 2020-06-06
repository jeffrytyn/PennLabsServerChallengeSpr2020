from db import db

import os
from flask import Flask
from flask_restful import Api
from resources.club import Clubs
from resources.user import User, FavoriteClub, UserSignUp
from models.user import UserModel
from scraper import *  # Web Scraping utility functions for Online Clubs with Penn.


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

api.add_resource(Clubs, '/api/clubs')
api.add_resource(User, '/api/user/<string:username>')
api.add_resource(UserSignUp, '/api/signup')
api.add_resource(FavoriteClub, '/api/<string:club_name>/favorite')

if __name__ == '__main__':
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run()

