from server.flask_app.models import *
from datetime import date
import MySQLdb

class Get():

    def __init__(self, app):
        self.app = app

    # get all user projects given user id
    def getUserProjects(self, u_id):
        with self.app.app_context():
            userProjects = db.session.query(Project).join(UserProjectLink).filter(UserProjectLink.user_id==u_id).all()
            if not userProjects:
                return 0
            else:
                return userProjects

    # get all of a projects users, given project id
    def getProjectTeam(self, p_id):
        with self.app.app_context():
            team = db.session.query(User).join(UserProjectLink).filter(UserProjectLink.project_id==p_id).all()
            if not team:
                return 0
            else:
                return team
            
    # get all of a tasks users, given task id
    def getTaskTeam(self, t_id):
        with self.app.app_context():
            team = db.session.query(User).join(UserTaskLink).filter(UserTaskLink.task_id==t_id).all()
            if not team:
                return 0
            else:
                return team

    # get all tasks of a project.
    def getProjectTasks(self, p_id):
        with self.app.app_context():
            tasks = db.session.query(Task).filter_by(project_id=p_id).all()
            if not tasks:
                return 0
            else:
                return tasks
        
    # gets all tasks associated with a user
    def getUserTasks(self, u_id):
        with self.app.app_context():
            userTasks = db.session.query(Task).join(UserTaskLink).filter(UserTaskLink.user_id==u_id).all()
            if not userTasks:
                return 0
            else:
                return userTasks
    
    # returns an int list containing all the contacts of a user
    def getContacts(self, u_id):
        with self.app.app_context():
            contacts = db.session.query(Contact).filter_by(user_id=u_id).all()
            friends = []
            for contact in contacts:
                friends.append(contact.friend_id)
            if not friends:
                return 0
            else:
                return friends

    # returns contacts information given their id 
    def getSafeContact(self, c_id):
        with self.app.app_context():
            try:
                contact = db.session.query(User).filter_by(user_id=c_id).first()
                c = contact.as_dict()
                return {"username": c["username"], "id": c["id"], "email": c["email"],
                        "firstname": c["firstname"], "lastname": c["lastname"], "bio": c["bio"]}
            except AttributeError: # user = None
                return 0

            
        
    def getUser(self, u_username, u_password):
        with self.app.app_context():
            try:
                usr = db.session.query(User).filter_by(username=u_username).first()
                if usr.password != u_password:
                    return 0
                return usr
            except AttributeError: # user = None
                return 0
            
      
    # for login
    def getUserByEmail(self, u_email, u_password):
        with self.app.app_context():
            try:
                usr = db.session.query(User).filter_by(email=u_email).first()
                if usr.password != u_password:
                    return 0
                return usr
            except AttributeError: # user = None
                return 0
        
    def getUserId(self, u_username):
        with self.app.app_context():
            try:
                user = db.session.query(User).filter_by(username=u_username).first()
                return user.id
            except AttributeError: # user = None
                return 0
    
    def getUserIdByEmail(self, u_email):
        with self.app.app_context():
            try:
                user = db.session.query(User).filter_by(email=u_email).first()
                return user.email
            except AttributeError: # user = None
                return 0
        
    def getProjectId(self, p_title):
        with self.app.app_context():
            try:
                project = db.session.query(Project).filter_by(title=p_title).first()
                return project.id
            except AttributeError: # project = None
                return 0