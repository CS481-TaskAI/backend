from server.models import *
from server import db, create_app
from datetime import date
import MySQLdb

app = create_app()

# get all user projects given user id
def getUserProjects(u_id):
    with app.app_context():
        records = db.session.query(Project).join(UserProjectLink).filter(UserProjectLink.user_id==u_id)
        listed = records.all()
        return listed

# get all of a projects users, given project id
def getProjectUsers(p_id):
    with app.app_context():
        records = db.session.query(User).join(UserProjectLink).filter(UserProjectLink.user_id==p_id)
        listed = records.all()
        return listed    

# gets all tasks associated with a user
def getUserTasks(u_id):
    with app.app_context():
        records = db.session.query(Task).filter_by(user_id=u_id)
        listed = records.all()
        return listed