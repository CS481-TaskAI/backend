from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
                                            #URI to connect to db -- database must exist before
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:my-secret-pw@localhost:3306/taskai"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    return app



