from server.models import *
from server import db, create_app


#TODO: encapsulate data sent to these functions into objects


app = create_app()


# db auto assigns and increments id, no need to explicitly assign id
def addUser(usernameIn, emailIn, passwordIn):
    if ((not isinstance(usernameIn, str)) or # makes sure input is correct datatypes
        (not isinstance(emailIn, str)) or (not isinstance(passwordIn, str))):
        print('Bad input!')
        return
    with app.app_context():
        newUser = User(username=usernameIn, email=emailIn, password=passwordIn)
        db.session.add(newUser)
        db.session.commit()

# u_id is used to create user project link
def addProject(p_title, p_description, u_id):

    with app.app_context():
        newProj = Project(title=p_title, description=p_description)
        db.session.add(newProj)
        # flush so we can access the id of the new entry
        db.session.flush()
        p_id = newProj.id
        db.session.commit()

        # create user-project link with user and newly created project
        addUserProjectLink(u_id, p_id)

#   Need to know user id and project id before adding task
#   Caller of this method needs that info from frontend request.
def addTask(u_id, p_id, desc, due, priority_in, class_in, timing_in):

    with app.app_context():
        newTask = Task(user_id=u_id, project_id=p_id, description=desc, 
                       date_due=due, priority=priority_in, classification=class_in,
                       timing=timing_in)
        db.session.add(newTask)
        db.session.commit()

# called by addProject
def addUserProjectLink(u_id, p_id):

    with app.app_context():
        newLink = UserProjectLink(user_id=u_id, project_id=p_id)
        db.session.add(newLink)
        db.session.commit()
