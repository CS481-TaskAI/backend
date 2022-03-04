from server.flask_app.models import *
from datetime import date
import MySQLdb

class Modify():

    def __init__(self, app):
        self.app = app
        
    # return value of all functions below is true if success, false if failure

    # updates information of the user with the given id, to the given parameters
    def modifyUser(self, u_id, u_username, u_email, u_password, u_bio):
        with self.app.app_context():
            try:
                user = db.session.query(User).filter_by(id=u_id).first()
                user.username = u_username
                user.email = u_email
                user.password = u_password
                user.bio = u_bio
                db.session.commit()
                return True
            except:
                return False
     
    # updates information of the user with the given id, to the given parameters
    def modifyProject(self, p_id, p_title, p_description):
        with self.app.app_context():
            try:
                project = db.session.query(Project).filter_by(id=p_id).first()
                project.title = p_title
                project.description = p_description
                db.session.commit()
                return True
            except:
                return False
       
    # updates information of the task with the given id, to the given parameters
    def modifyTask(self, t_id, desc, due, priority_in, class_in, timing_in):
        with self.app.app_context():
            try:
                task = db.session.query(Task).filter_by(id=t_id).first()
                task.description = desc
                task.due_date = due
                task.priority = priority_in
                task.classification = class_in
                task.timing = timing_in
                db.session.commit()
                return True
            except:
                return False
            
    # mark task as completed
    def markTaskCompleted(self, t_id):
        with self.app.app_context():
            try:
                task = db.session.query(Task).filter_by(id=t_id).first()
                task.status = True
                db.session.commit()
                return True
            except:
                return False