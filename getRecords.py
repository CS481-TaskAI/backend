from server.flask_app.models import *
from datetime import date
import MySQLdb

class Get():

    def __init__(self, app):
        self.app = app

    # get all user projects given user id
    def getUserProjects(self, u_id):
        with self.app.app_context():
            return db.session.query(Project).join(UserProjectLink).filter(UserProjectLink.user_id==u_id).all()

    # get all of a projects users, given project id
    def getProjectUsers(self, p_id):
        with self.app.app_context():
            return db.session.query(User).join(UserProjectLink).filter(UserProjectLink.project_id==p_id).all()

    # gets all tasks associated with a user
    def getUserTasks(self, u_id):
        with self.app.app_context():
            return db.session.query(Task).filter_by(user_id=u_id).all()
        
    def getUserId(self, u_username):
        with self.app.app_context():
            user = db.session.query(User).filter_by(username=u_username).first()
            return user.id
        
    def getProjectId(self, p_title):
        with self.app.app_context():
            project = db.session.query(Project).filter_by(title=p_title).first()
            return project.id
    