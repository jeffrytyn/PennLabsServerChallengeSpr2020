from db import db

tag_identifier = db.Table('tag_identifier',
                          db.Column('club_id', db.Integer, db.ForeignKey('clubs.id')),
                          db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                          )


class ClubModel(db.Model):
    __tablename__ = "clubs"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(200), unique=False, nullable=True)
    favorite_count = db.Column(db.Integer, unique=False, autoincrement=False, nullable=False)
    tags = db.relationship('TagModel', secondary=tag_identifier, #look into primary/secondary joins
                           backref=db.backref('clubs', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, description, favorite_count=0):
        self.name = name
        self.description = description
        self.favorite_count = favorite_count

    def json(self):
        return {"name": self.name,
                "description": self.description,
                "tags": [tag.name for tag in self.tags.all()],
                "favorite_count": self.favorite_count}

    # add tag to relationship
    def add_tag(self, tag):
        if not self.has_tag(tag):
            self.tags.append(tag)

    # looks for items in the association table that have the left side foreign key set to the self user,
    # and the right side set to the tag argument
    def has_tag(self, tag):
        return self.tags.filter(tag_identifier.c.tag_id == tag.id).count() > 0

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  #SELECT * FROM tablename WHERE name=name LIMIT 1

    @classmethod
    def find_all(cls):
        return cls.query.all()


class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))

    def __init__(self, name):
        self.name = name

    def add_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()  #SELECT * FROM tablename WHERE name=name LIMIT 1