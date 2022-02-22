from server.flask_app.models import *
from datetime import date
import MySQLdb

class Modify():

    def __init__(self, app):
        self.app = app

    # get all user projects given user id
    # def getUserProjects(self, u_id):
        # with self.app.app_context():