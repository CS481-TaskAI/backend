from server.flask_app.app import db, create_app
from getRecords import Get
from addRecords import Add
from deleteRecords import Delete
from modifyRecords import Modify
from flask import Flask, request, redirect, url_for, jsonify
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
            return jsonify({"error": "Username already taken."})
        elif get.getUserIdByEmail(email) != 0:
            return jsonify({"error": "There already exists an account with this email address."})

        if not isValidEmail(email):
            return jsonify({"error": "Enter a valid email address."})
        if not isValidUsername(username):
            return jsonify({"error": "Username should be 20 characters or less"})
        if not isValidPW(password):
            return jsonify({"error": "Password should be at least 8 characters and no more than 30 characters"})
        
        if not add.addUser(username, email, password):
            return jsonify({"error": "Oops. Something went wrong..."})   

    #LOG IN
    username = request.form["username"]
    #email = request.form["email"]
    password = request.form["password"]
    if  get.getUserId(username) == 0:
        return jsonify({"error": "Username does not exist."})

    # TODO: enable logining in by email instead of username
    #elif get.getUserIdByEmail(email) == 0:
        #return jsonify({"error": "Username or Email are incorrect"})
        
    #at this point username is valid, need to validate password
    usr = get.getUser(username, password)
    if usr == 0:
        return jsonify({"error": "Incorrect password."})
        pass 
    usr_dict = to_list_dict(usr)
    return jsonify(usr_dict)
    
# Returns all projects given a user_id
# Creates project if all parameters valid, returns projects
@app.route('/projects', methods = ['GET', 'POST'])
def projects():
    
    #CREATE PROJECT
    if request.method == 'POST':
        u_id = request.form["user_id"]
        title = request.form["title"]
        desc = request.form["description"]
        if not add.addProject(title, desc, u_id):
            return jsonify({"error": "Could not create Project."})
    
    #GET ALL USER PROJECTS
    u_id = request.form["user_id"]
    projects = get.getUserProjects(u_id)
    dict_of_projects = to_list_dict(projects)
    return jsonify(dict_of_projects)


#Returns all tasks given a user_id
#Creates task if all parameters valid, returns tasks
@app.route('/tasks', methods = ['GET', 'POST'])
def tasks():
    
    #CREATE TASK
    if request.method == 'POST':
        u_id = request.form["user_id"]
        p_id = request.form["project_id"]
        desc = request.form["description"]
        due = request.form["date_due"]
        classification = request.form["classification"]
        timing = request.form["timing"]
        if not add.addTask(u_id, p_id, desc, due, classification, timing):
            return jsonify({"error": "Could not add task."}) 
    
    #GET ALL USER TASKS
    u_id = request.form["user_id"]
    obs = get.getUserTasks(u_id)
    dict_of_tasks = to_list_dict(obs)
    return jsonify(dict_of_tasks)

#Returns all contacts given user_id
#creates contact given contact username
@app.route("/contacts", methods = ['GET', 'POST'])
def contacts():

    #CREATE CONTACT
    if request.method == 'POST':
        u_id = request.form["user_id"]
        c_username = request.form["contact_username"]
        c_id = get.getUserId(c_username)
        if c_id == 0:
            return jsonify({"error": "No such user by that username."})
        if not add.addContact(u_id, c_id):
            return jsonify({"error": "Could not add contact."})

    #GET ALL CONTACTS
    u_id = request.form["user_id"]
    contacts = get.getContacts(u_id)
    dict_of_contacts = to_list_dict(contacts)
    return jsonify(dict_of_contacts)

#--------------------Update and Delete routes---------------------------------------

#Modify or delete Projects, reroutes to associated Get route
@app.route('/mod_projects', methods = ['PUT', 'DELETE'])
def update_projects():
    
    #DELETE PROJECT
    if request.method == 'DELETE':
        p_id = request.form["project_id"]
        if not delete.deleteProject(p_id):
            return jsonify({"error": "Could not delete project."})
        return redirect(url_for('/projects'))

    #MODIFY PROJECT
    if request.method == 'PUT':
        p_id = request.form["project_id"]
        title = request.form["title"]
        desc = request.form["description"]
        if not modify.modifyProject(p_id, title, desc):
            return jsonify({"error": "Could not modify project."})
        return redirect(url_for('/projects'))


#Modify or delete Tasks, reroutes to associated Get route
@app.route('/mod_tasks', methods = ['PUT', 'DELETE'])
def update_tasks():
    # if either, afterwards reroute to GET /tasks
    #re
    return redirect(url_for('/tasks'))

#Modify or delete Contacts, reroutes to associated Get route
@app.route("/mod_contacts", methods = ['DELETE'])
def update_contacts():
    
    #DELETE CONTACT
    u_id = request.form["user_id"]
    c_id = request.form["contact_id"]
    if not delete.deleteContact(u_id, c_id):
        return jsonify({"error": "Could not delete contact."})

    return redirect(url_for('/contacts'))
    


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

def isValidUsername(username):
    return (len(username) < 21 and len(username) > 0)

if __name__ == '__main__':

    app.run(debug=True)