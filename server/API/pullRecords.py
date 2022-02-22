from server.flask_app.models import *
#from start_server import app, db
from datetime import date
import MySQLdb

class Get():

    def __init__(self, app):
        self.app = app

    # get all user projects given user id
    def getUserProjects(self, u_id):
        with self.app.app_context():
            records = db.session.query(Project).join(UserProjectLink).filter(UserProjectLink.user_id==u_id)
            listed = records.all()
            return listed

    # get all of a projects users, given project id
    def getProjectUsers(self, p_id):
        with self.app.app_context():
            records = db.session.query(User).join(UserProjectLink).filter(UserProjectLink.user_id==p_id)
            listed = records.all()
            return listed    

    # gets all tasks associated with a user
    def getUserTasks(self, u_id):
        with self.app.app_context():
            records = db.session.query(Task).filter_by(user_id=u_id)
            listed = records.all()
            return listed