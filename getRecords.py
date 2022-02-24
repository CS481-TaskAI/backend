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
    
    # returns an int list containing all the contacts of a user
    def getContacts(self, u_id):
        with self.app.app_context():
            contacts = db.session.query(Contact).filter_by(user_id=u_id).all()
            friends = []
            for contact in contacts:
                friends.append(contact.friend_id)
            return friends
        
    def getUser(self, u_username, u_password):
        with self.app.app_context():
            return db.session.query(User).filter_by(username=u_username,password=u_password).first()
        
    def getUserId(self, u_username):
        with self.app.app_context():
            try:
                user = db.session.query(User).filter_by(username=u_username).first()
                return user.id
            except AttributeError: # user = None
                return 0
        
    def getProjectId(self, p_title):
        with self.app.app_context():
            try:
                project = db.session.query(Project).filter_by(title=p_title).first()
                return project.id
            except AttributeError: # project = None
                return 0