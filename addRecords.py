from server.flask_app.models import *
from datetime import date
import MySQLdb

#TODO: encapsulate data sent to these functions into objects

# MySQLdb._exceptions.OperationalError
# MySQLdb._exceptions.IntegrityError

class Add():

    def __init__(self, app):
        self.app = app

    # db auto assigns and increments id, no need to explicitly assign id
    def addUser(self, u_username, u_email, u_password):
        # if ((not isinstance(u_username, str)) or # makes sure input is correct datatypes
            # (not isinstance(u_email, str)) or (not isinstance(u_password, str))):
            # print('Bad input!')
            # return
        
        with self.app.app_context():
            newUser = User(username=u_username, email=u_email, password=u_password)
            db.session.add(newUser)
            db.session.commit()
        

    # u_id is used to create user project link
    def addProject(self, p_title, p_description, u_id):
        # if ((not isinstance(p_title, str)) or (not isinstance(p_description, str)) or (not isinstance(u_id, int))):
            # print('Bad input!')
            # return
        try:
            with self.app.app_context():
                newProj = Project(title=p_title, description=p_description)
                db.session.add(newProj)
                db.session.flush() # flush so we can access the id of the new entry
                p_id = newProj.id
                db.session.commit()
                self.addUserProjectLink(u_id, p_id) # create user-project link with user and newly created project
        except MySQLdb._exceptions.OperationalError:
            print('Bad input!')

    #   Need to know user id and project id before adding task
    #   Caller of this method needs that info from frontend request.
    def addTask(self, u_id, p_id, desc, due, priority_in, class_in, timing_in):
        with self.app.app_context():
            newTask = Task(user_id=u_id, project_id=p_id, description=desc, 
                        date_due=due, priority=priority_in, classification=class_in,
                        timing=timing_in)
            db.session.add(newTask)
            try:
                db.session.commit()
            except MySQLdb._exceptions.OperationalError:
                print('Bad input!')

    # called by addProject or when adding user to existing project
    def addUserProjectLink(self, u_id, p_id):
        try:
            with self.app.app_context():
                newLink = UserProjectLink(user_id=u_id, project_id=p_id)
                db.session.add(newLink)
                db.session.commit()
        except MySQLdb._exceptions.OperationalError:
            print('Bad input!')
            
    def addContact(self, u_id, f_id):
        with self.app.app_context():
                newContact = Contact(user_id=u_id, friend_id=f_id)
                db.session.add(newContact)
                db.session.commit()
