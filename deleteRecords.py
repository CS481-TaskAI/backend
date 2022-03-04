from server.flask_app.models import *
from datetime import date
import MySQLdb

class Delete():

    def __init__(self, app):
        self.app = app
        
    # return value of all functions below is true if success, false if failure

    # delete user, deletes all the user project links too
    def deleteUser(self, u_id):
        with self.app.app_context():
            try:
                # first deleting the links to this user
                projectLinks = db.session.query(UserProjectLink).filter_by(user_id=u_id).all() # later make all
                for link in projectLinks:
                    db.session.delete(link)
                # deleting this user's contacts
                contacts = db.session.query(Contact).filter_by(user_id=u_id).all() # later make all
                for contact in contacts:
                    db.session.delete(contact)
                # deleting this user's tasks links
                taskLinks = db.session.query(UserTaskLink).filter_by(user_id=u_id).all() # later make all
                for link in taskLinks:
                    db.session.delete(link)
                # now deleting the actual project
                user = db.session.query(User).filter_by(id=u_id).first()
                db.session.delete(user)
                db.session.commit()
                return True
            except:
                return False

    # delete project, deletes all the project's user project links first
    def deleteProject(self, p_id):
        with self.app.app_context():
            try:
                # first deleting the user links to this project
                projectLinks = db.session.query(UserProjectLink).filter_by(project_id=p_id).all()
                for link in projectLinks:
                    db.session.delete(link)
                # deleting this project's tasks
                tasks = db.session.query(Task).filter_by(project_id=p_id).all()
                for task in tasks:
                    db.session.delete(task)
                # now deleting the actual project
                project = db.session.query(Project).filter_by(id=p_id).first()
                db.session.delete(project)
                db.session.commit()
                return True
            except:
                return False

    # delete task
    def deleteTask(self, t_id):
        with self.app.app_context():
            try:
                # first deleting the links to this task
                taskLinks = db.session.query(UserTaskLink).filter_by(task_id=t_id).all()
                for link in taskLinks:
                    db.session.delete(link)
                # now deleting the actual task
                task = db.session.query(Task).filter_by(id=t_id).first()
                db.session.delete(task)
                db.session.commit()
                return True
            except:
                return False

    # delete individual user project link
    def deleteUserProjectLink(self, u_id, p_id):
        with self.app.app_context():
            try:
                userProjectLink = db.session.query(UserProjectLink).filter_by(project_id=p_id, user_id=u_id).first()
                db.session.delete(userProjectLink)
                db.session.commit()
                return True
            except:
                return False
            
    # delete individual contact
    def deleteContact(self, u_id, f_id):
        with self.app.app_context():
            try:
                contact = db.session.query(Contact).filter_by(user_id=u_id, friend_id=f_id).first()
                db.session.delete(contact)
                contactReverse = db.session.query(Contact).filter_by(user_id=f_id, friend_id=u_id).first()
                db.session.delete(contactReverse)
                db.session.commit()
                return True
            except:
                return False
            
    