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

#TODO: /add_user_to_task
#      /add_user_to_project
#      /remove_user_from_task
#      /remove_user_from_project
#      finish /modify_tasks


# Will take the username and password and authenticate
# Returns user id
# Post will attempt to create database records if email or username don't exist
@app.route('/user', methods = ['GET', 'POST'])
def login_signup():

    if request.is_json:
        # Parse the JSON into a Python dictionary
        req = request.get_json()
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400
    
    #SIGN UP
    if request.method == 'POST':    
        username = req["username"]
        email = req["email"]
        password = req["password"]
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
    #username = req["username"]
    email = request.form["email"]
    password = req["password"]
    #if  get.getUserId(username) == 0:
    #    return jsonify({"error": "Username does not exist."})

    # TODO: enable logining in by email instead of username
    if get.getUserIdByEmail(email) == 0:
        return jsonify({"error": "Username or Email are incorrect"})
        
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
    
    if request.is_json:
        # Parse the JSON into a Python dictionary
        req = request.get_json()
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400
   

    #CREATE PROJECT
    if request.method == 'POST':
        u_id = req["user_id"]
        title = req["title"]
        desc = req["description"]
        print('posting a project to db\t')
        if not add.addProject(title, desc, u_id):
            return jsonify({"error": "Could not create Project."})
    
    print("after ")
    #GET ALL USER PROJECTS
    u_id = req['user_id']
    projects = get.getUserProjects(u_id)
    if projects == 0:
        return {}
    dict_of_projects = to_list_dict(projects)
    print(dict_of_projects)
    return jsonify(dict_of_projects), 200




#Returns all tasks given a user_id
#Creates task if all parameters valid, returns tasks
@app.route('/tasks', methods = ['GET', 'POST'])
def tasks():

    if request.is_json:
        # Parse the JSON into a Python dictionary
        req = request.get_json()
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400
    
    #CREATE TASK
    if request.method == 'POST':
        u_id = req["user_id"]
        p_id = req["project_id"]
        desc = req["description"]
        due = req["date_due"]
        classification = req["classification"]
        timing = req["timing"]
        try:
            priority = req["priority"]
        except KeyError:
            priority = 3

        # call to Machine Learning module
        # returns priority, reassigns priority to new one
        if not add.addTask(u_id, p_id, desc, due, priority, classification, timing):
            return jsonify({"error": "Could not add task."}) 
    
    #GET ALL USER TASKS
    u_id = req["user_id"]
    tasks = get.getUserTasks(u_id)
    if tasks == 0:
        return {}
    dict_of_tasks = to_list_dict(tasks)
    return jsonify(dict_of_tasks)

#Returns all contacts given user_id
#creates contact given contact username
@app.route("/contacts", methods = ['GET', 'POST'])
def contacts():

    if request.is_json:
        # Parse the JSON into a Python dictionary
        req = request.get_json()
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

    #CREATE CONTACT
    if request.method == 'POST':
        u_id = req["user_id"]
        c_username = req["contact_username"]
        c_id = get.getUserId(c_username)
        if c_id == 0:
            return jsonify({"error": "No such user by that username."})
        if not add.addContact(u_id, c_id):
            return jsonify({"error": "Could not add contact."})

    #GET ALL CONTACTS
    u_id = req["user_id"]
    contacts = get.getContacts(u_id)
    dict_of_contacts = to_list_dict(contacts)
    return jsonify(dict_of_contacts)

#--------------------Update and Delete routes---------------------------------------

#Modify or delete Projects, reroutes to associated Get route
@app.route('/mod_projects', methods = ['PUT', 'DELETE'])
def update_projects():

    if request.is_json:
        # Parse the JSON into a Python dictionary
        req = request.get_json()
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400
    
    #DELETE PROJECT
    if request.method == 'DELETE':
        p_id = req["project_id"]
        if not delete.deleteProject(p_id):
            return jsonify({"error": "Could not delete project."})
        return {}

    #MODIFY PROJECT
    if request.method == 'PUT':
        p_id = req["project_id"]
        title = req["title"]
        desc = req["description"]
        if not modify.modifyProject(p_id, title, desc):
            return jsonify({"error": "Could not modify project."})
        return {}


#Modify or delete Tasks, reroutes to associated Get route
@app.route('/mod_tasks', methods = ['PUT', 'DELETE'])
def update_tasks():

    if request.is_json:
        # Parse the JSON into a Python dictionary
        req = request.get_json()
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400

    # if either, afterwards reroute to GET /tasks
    #re
    return {}

#Modify or delete Contacts, reroutes to associated Get route
@app.route("/mod_contacts", methods = ['DELETE'])
def update_contacts():

    if request.is_json:
        # Parse the JSON into a Python dictionary
        req = request.get_json()
    else:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400
    
    #DELETE CONTACT
    u_id = req["user_id"]
    c_id = req["contact_id"]
    if not delete.deleteContact(u_id, c_id):
        return jsonify({"error": "Could not delete contact."})

    return {}
    


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