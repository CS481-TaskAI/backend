from server.flask_app.app import db
from datetime import datetime
import json

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(20), unique = True)
    email = db.Column(db.String(30), unique = True)
    password = db.Column(db.String(30))

    def __repr__(self):
        dictionary = {'id':self.id, 'username':self.username, 'email':self.email}
        return json.dumps(dictionary, indent = 3)

class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(20))
    description = db.Column(db.String(120))

    def __repr__(self):
        dictionary = {'id':self.id, 'title':self.title, 'description':self.description}
        return json.dumps(dictionary, indent = 3)

class Task(db.Model):
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id)) # ForeignKey
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id)) # ForeignKey
    description = db.Column(db.String(120))
    date_assigned = db.Column(db.Date, default = datetime.utcnow)
    date_due = db.Column(db.Date)
    priority = db.Column(db.Integer)
    classification = db.Column(db.String(10))
    timing = db.Column(db.String(10)) #Not what type timing should be
    status = db.Column(db.Boolean, default = False) #False = not completed

    def toJSON(self):
        return json.dumps(self, sort_keys=True, indent=4)

    def __repr__(self):
        dictionary = {'id':self.id, 'description':self.description, 'assigned':str(self.date_assigned),
                       'due':str(self.date_due), 'priority':self.priority, 'classification':self.classification,
                        'timing':self.timing, 'status':self.status}
        return json.dumps(dictionary, indent = 3)
        
                


class UserProjectLink(db.Model):
    __tablename__ = 'user_project_link'
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    project_id = db.Column(db.Integer, db.ForeignKey(Project.id))

    # proxy objects for accessing members through foreign keys
    # user = db.relationship('User', db.ForeignKey(User.id))
    # project = db.relationship('Project', db.ForeignKey(Project.id))



    