from . import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    email = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(30))

class Project(db.Model):
    __tablename__ = 'project'
    project_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20))
    description = db.Column(db.String(120))

class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    project_id = db.Column(db.Integer, db.ForeignKey(Project.project_id))
    description = db.Column(db.String(120))
    date_assigned = db.Column(db.Date, default = datetime.utcnow)
    date_due = db.Column(db.Date)
    priority = db.Column(db.Integer)
    classification = db.Column(db.String(10))
    timing = db.Column(db.String(10)) #Not what type timing should be
    status = db.Column(db.Boolean, default = False) #False = not completed

class UserProjectLink(db.Model):
    __tablename__ = 'user_project_link'
    user_id = db.Column(db.Integer, db.ForeignKey(User.user_id), primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey(Project.project_id), primary_key = True)

    #proxy objects for accessing members through foreign keys
    user = db.relationship('User', db.ForeignKey(User.user_id))
    project = db.relationship('Project', db.ForeignKey(Project.project_id))