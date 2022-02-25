from server.flask_app.app import db, create_app
from getRecords import Get
from addRecords import Add
from deleteRecords import Delete
from modifyRecords import Modify
from flask import Flask, request, jsonify
import json

app = create_app()

#-----------------API Accesser Initialization-------------------------------------
get = Get(app)
add = Add(app)
delete = Delete(app)
modify = Modify(app)

#--------------------Get and Post routes------------------------------------------

# Will take the username and password and authenticate
# Returns user id
# Post will attempt to create database records if email or username don't exist
@app.route('/user', methods = ['GET', 'POST'])
def login_signup():
    
    #SIGN UP
    if request.method == 'POST':    
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        if get.getUserId(username) != 0:
            #return error code, username taken
            pass
        elif get.getUserIdByEmail(email) != 0:
            #return error code, email taken
            pass
        
        #if validEmail(email) and validUsername(username):
        #add.addUser(username, email, password)      

    #LOG IN
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    if  get.getUserId(username) == 0:
        #return error code , no such username
        pass
    elif get.getUserIdByEmail(email) == 0:
        #return error code , no such email
        pass
    #at this point username is valid, need to validate password
    usr = get.getUser(username, password)
    if usr == 0:
        #return error code, wrong password
        pass 
    usr_dict = to_list_dict(usr)
    return jsonify(usr_dict)
    

#checkCreds (username , password) -> if match return the record, if not None


# Returns all projects given a user_id
# Creates project if all parameters valid, returns projects
@app.route('/projects', methods = ['GET', 'POST'])
def projects():
    pass

#Returns all tasks given a user_id
#Creates task if all parameters valid, returns tasks
@app.route('/tasks', methods = ['GET', 'POST'])
def tasks():
    
    if request.method == 'POST':
        u_id = request.form["user_id"]
        p_id = request.form["project_id"]
        desc = request.form["description"]
        due = request.form["date_due"]
        classification = request.form["classification"]
        timing = request.form["timing"]
        if not add.addTask(u_id, p_id, desc, due, classification, timing):
            #return an error code 
            pass
    u_id = request.form["user_id"]
    obs = get.getUserTasks(u_id)
    dict_of_tasks = to_list_dict(obs)
    return jsonify(dict_of_tasks)

#Returns all contacts given user_id
#creates contact given contact username
@app.route("/contact", methods = ['GET', 'POST'])
def contacts():
    # if either, after reroute to GET /c
    pass

#--------------------Update and Delete routes---------------------------------------

#Modify or delete Projects, reroutes to associated Get route
@app.route('/mod_projects', methods = ['PUT', 'DELETE'])
def update_projects():
    # if either, afterwards reroute to GET /projects
    pass

#Modify or delete Tasks, reroutes to associated Get route
@app.route('/mod_tasks', methods = ['PUT', 'DELETE'])
def update_tasks():
    # if either, afterwards reroute to GET /tasks
    #re
    pass

#Modify or delete Contacts, reroutes to associated Get route
@app.route("/mod_contact", methods = ['PUT', 'DELETE'])
def update_contacts():
    pass


#-------------------Utility--------------------------------------------------
# Takes list of db records and converts to list of dictionaries
# returns list of dictionaries
def to_list_dict(obs):
    my_list = []
    for rec in obs:
        my_list.append(rec.as_dict())
    return my_list

def isValidEmail(email):
    if (len(email) < 3):
        return False
    num = email.count("@")
    if (num != 1):
        return False
    if (email[0] == '@' or email[len(email) - 1] == '@'):
        return False
    return True

def isValidPW(password):
    return (len(password) >= 8 and len(password) <= 30)

if __name__ == '__main__':

    app.run(debug=True)