from server.models import *
from server import db, create_app
from datetime import date
import MySQLdb

#TODO: functions currently print the query, do something more useful with it

app = create_app()

# get all user projects given user id
def getUserProjects(u_id):
    with app.app_context():
        print(UserProjectLink.query.with_entities(UserProjectLink.project_id).filter_by(user_id=u_id).all())

# get all of a projects users, given project id
# def getProjectUsers(p_id):
    