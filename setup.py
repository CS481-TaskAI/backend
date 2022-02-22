#Connects with mysql container and creates tables

#SQLAlchemy
from server.flask_app.models import *
from server.flask_app.app import db, create_app
db.create_all(app=create_app())
    