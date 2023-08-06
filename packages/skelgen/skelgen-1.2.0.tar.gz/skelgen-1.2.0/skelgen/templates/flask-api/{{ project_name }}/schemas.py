"""
Marshmallow schemas.

These schemas intelligently handle automatically
serializing the models into usable datatypes.
"""
from datetime import time
from marshmallow import fields, pprint
from flask_marshmallow import Marshmallow
from {{ project_name }}.models import Person, Thing, db

ma = Marshmallow()

class ThingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Thing
        sqla_session = db.session
        include_fk = True

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        sqla_session = db.session

    things = ma.List(ma.Nested(ThingSchema))
