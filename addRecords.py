from server.flask_app.models import *
from datetime import date
import MySQLdb

# MySQLdb._exceptions.OperationalError
# MySQLdb._exceptions.IntegrityError

class Add():

    def __init__(self, app):
        self.app = app
        
    # return value of all functions below is true if success, false if failure

    # db auto assigns and increments id, no need to explicitly assign id
    def addUser(self, u_username, u_email, u_password):
        with self.app.app_context():
            try:
                newUser = User(username=u_username, email=u_email, password=u_password)
                db.session.add(newUser)
                db.session.commit()
                return True
            except:
                return False
        

    # u_id is used to create user project link
    def addProject(self, p_title, p_description, u_id):
        with self.app.app_context():
            try:
                newProj = Project(title=p_title, description=p_description)
                db.session.add(newProj)
                db.session.flush() # flush so we can access the id of the new entry
                p_id = newProj.id
                db.session.commit()
                self.addUserProjectLink(u_id, p_id) # create user-project link with user and newly created project
                return True
            except:
                return False

    #   Need to know user id and project id before adding task
    def addTask(self, u_id, p_id, desc, due, priority_in, class_in, timing_in):
        with self.app.app_context():
            try:
                newTask = Task(user_id=u_id, project_id=p_id, description=desc, 
                        date_due=due, priority=priority_in, classification=class_in,
                        timing=timing_in)
                db.session.add(newTask)
                db.session.commit()
                return True
            except:
                return False

    # called by addProject or when adding user to existing project
    def addUserProjectLink(self, u_id, p_id):
        with self.app.app_context():
            try:
                newLink = UserProjectLink(user_id=u_id, project_id=p_id)
                db.session.add(newLink)
                db.session.commit()
                return True
            except:
                return False
            
    def addContact(self, u_id, f_id):
        with self.app.app_context():
            try:
                newContact = Contact(user_id=u_id, friend_id=f_id)
                db.session.add(newContact)
                db.session.commit()
                return True
            except:
                return False
