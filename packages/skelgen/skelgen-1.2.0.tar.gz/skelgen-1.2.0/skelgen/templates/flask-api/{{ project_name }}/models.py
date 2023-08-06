"""
Some example SQLAlchemy models.

In this case, we define a person model
with a one-to-many relationship to a thing model.

One person can have multiple things, and a thing has one person
associated with it.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))

    things = db.relationship('Thing', backref='person', lazy=True)


class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)
