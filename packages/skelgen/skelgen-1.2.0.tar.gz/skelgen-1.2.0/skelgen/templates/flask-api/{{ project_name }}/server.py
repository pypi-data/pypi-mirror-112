import flask
from flask_cors import CORS
from {{ project_name }}.settings import Settings
from {{ project_name }}.views import api
from {{ project_name }}.version import VERSION
from {{ project_name }}.models import db
from {{ project_name }}.schemas import ma

app = flask.Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = Settings.UPLOAD_SIZE_MAX
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{{ project_name }}.db'
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
with app.app_context():
    db.create_all()

CORS(app)

@app.route("/")
def root():
    return f"{{ project_name }} version {VERSION}"

app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    app.run(port=5000) # Dev server
