import flask
from {{ project_name }}.version import VERSION
from flask_restful import Resource, Api
from {{ project_name }}.models import Person, Thing, db
from {{ project_name }}.schemas import PersonSchema, ThingSchema

api = flask.Blueprint("api", __name__)
rest_api = Api(api)

@api.route("/", methods=["GET"])
def root():
    """
    Return 200 OK status with some server info.
    """
    return f"{{ project_name }} {VERSION}"

class PersonView(Resource):
    def get(self, person_id=None):
        if person_id is None:
            model = Person.query.all()
            data = PersonSchema(many=True).dump(model)
        else:
            model = Person.query.get(person_id)
            data = PersonSchema().dump(model)
        return data

    def post(self, person_id=None):
        data = PersonSchema().load(flask.request.get_json())
        if person_id is None:
            model = Person(**data)
            db.session.add(model)
        else:
            model = Person.query.filter_by(id=person_id).first()
            model.update(data)
        db.session.commit()
        return PersonSchema().dump(model)

    def put(self, person_id=None):
        return self.post(self, person_id)

    def delete(self, thing_id=None):
        model = Thing.query.filter_by(id=thing_id).first()
        db.session.delete(model)
        db.session.commit()


class ThingView(Resource):
    def get(self, thing_id=None):
        if thing_id is None:
            model = Thing.query.all()
            data = ThingSchema(many=True).dump(model)
        else:
            model = Thing.query.get(thing_id)
            data = ThingSchema().dump(model)
        return data

    def post(self, thing_id=None):
        data = ThingSchema().load(flask.request.get_json())
        if thing_id is None:
            model = Thing(**data)
            db.session.add(model)
        else:
            model = Thing.query.filter_by(id=thing_id).first()
            model.update(data)
        db.session.commit()
        return ThingSchema().dump(model)

    def put(self, thing_id=None):
        return self.post(self, thing_id)

    def delete(self, thing_id=None):
        model = Thing.query.filter_by(id=thing_id).first()
        db.session.delete(model)
        db.session.commit()


rest_api.add_resource(PersonView, "/person", "/person/<int:person_id>")
rest_api.add_resource(ThingView, "/thing", "/thing/<int:thing_id>")
