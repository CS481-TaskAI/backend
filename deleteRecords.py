from server.models import *
from server import db, create_app
from datetime import date
import MySQLdb

app = create_app()

# delete user, deletes all the user project links too
def deleteUser(u_id):
    with app.app_context():
        # first deleting the links to this user
        projectLinks = db.session.query(UserProjectLink).filter_by(user_id=u_id).all() # later make all
        for link in projectLinks:
            db.session.delete(link)
        # deleting this user's tasks
        tasks = db.session.query(Task).filter_by(user_id=u_id).all() # later make all
        for task in tasks:
            db.session.delete(task)
        # now deleting the actual project
        user = db.session.query(User).filter_by(id=u_id).first()
        db.session.delete(user)
        db.session.commit()

# delete project, deletes all the project's user project links first
def deleteProject(p_id):
    with app.app_context():
        # first deleting the links to this project
        projectLinks = db.session.query(UserProjectLink).filter_by(project_id=p_id).all() # later make all
        for link in projectLinks:
            db.session.delete(link)
        # deleting this project's tasks
        tasks = db.session.query(Task).filter_by(project_id=p_id).all() # later make all
        for task in tasks:
            db.session.delete(task)
        # now deleting the actual project
        project = db.session.query(Project).filter_by(id=p_id).first()
        db.session.delete(project)
        db.session.commit()

# delete task
def deleteTask(t_id):
    with app.app_context():
        task = db.session.query(Task).filter_by(id=t_id).first()
        db.session.delete(task)
        db.session.commit()

# delete individual user project link
def deleteUserProjectLink(u_id, p_id):
    with app.app_context():
        userProjectLink = db.session.query(UserProjectLink).filter_by(project_id=p_id, user_id=u_id).first()
        db.session.delete(userProjectLink)
        db.session.commit()