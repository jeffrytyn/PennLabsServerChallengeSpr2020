from db import db
from flask_sqlalchemy import event
import bcrypt
from models.club import ClubModel

user_favorites = db.Table('user_favorites',
                          db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                          db.Column('club_id', db.Integer, db.ForeignKey('clubs.id'))
                          )


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(100), unique=False, nullable=False)
    clubs = db.relationship('club.ClubModel', secondary=user_favorites,
                            backref=db.backref('favorited_by', lazy='dynamic'), lazy='dynamic')

    def __init__(self, username, password):
        self.username = username
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode(), salt)
        self.password = hashed

    def json(self):
        return {
            "username": self.username,
            "favorited_clubs": [club.json() for club in self.clubs.all()]
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def favorited_club(self, club):
        return self.clubs.filter(user_favorites.c.club_id == club.id).count() > 0

    def fav_club_toggle(self, club_name):
        club = ClubModel.find_by_name(club_name)
        if club:
            if self.favorited_club(club):
                self.clubs.remove(club)
                club.favorite_count -= 1
            else:
                self.clubs.append(club)
                club.favorite_count += 1
            db.session.commit()
            return club.json()
        else:
            return {"message": "No club with name {} exists".format(club_name)}

    @classmethod
    def find_by_name(cls, username):
        return cls.query.filter_by(username=username).first()

@event.listens_for(UserModel.__table__, 'after_create')
def put_first_user(target, connection, **kw):
    db.session.add(UserModel('jen', 'password'))
    db.session.commit()