from server.flask_app.app import db, create_app
from server.flask_app.models import *
from getRecords import Get
from addRecords import Add
from deleteRecords import Delete
from modifyRecords import Modify
from priorityAssignment import getRecPriority
from flask import Flask, request, redirect, url_for, jsonify
from datetime import datetime, date
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
@app.route('/login', methods = ['POST'])
def login():

    if request.method != 'POST': 
        return "/login accepts POST method only.", 400
    if not request.is_json:
        # The request body wasn't JSON so return a 400 HTTP status code
        return "Request was not JSON", 400
    
    #SIGN UP
    req = request.get_json()
   
    #username = req["username"]
    email = req["email"]
    password = req["password"]
    
    if get.getUserIdByEmail(email) == 0:
        return jsonify({"error": "Email is incorrect"})
        
    #at this point username is valid, need to validate password
    usr = get.getUserByEmail(email, password)
    if usr == 0:
        return jsonify({"error": "Incorrect password."})
    
    usr_dict = usr.as_dict()
    usr_clean = {"username": usr_dict["username"], "id": usr_dict["id"], "email": usr_dict["email"], "bio": usr_dict["bio"]}
    return jsonify(usr_clean)


# Will take the username and password and authenticate
# Returns user id
# Post will attempt to create database records if email or username don't exist
@app.route('/signup', methods = ['POST'])
def signup():

    if request.method != 'POST': 
        return "/signup accepts POST method only.", 400
    if not request.is_json:
        return "Request was not JSON", 400
    
    #SIGN UP
    req = request.get_json()

    bio = req["bio"]
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
    
    if not add.addUser(username, email, password, bio):
        return jsonify({"error": "Oops. Something went wrong..."})   
    return {}
                        
# Returns all projects given a user_id
# Creates project if all parameters valid, returns projects
@app.route('/projects', methods = ['GET', 'POST'])
def projects():
    
    
   
    #CREATE PROJECT
    if request.method == 'POST':

        if not request.is_json:
            return "Request was not JSON", 400
        req = request.get_json()

        u_id = req["user_id"]
        title = req["title"]
        desc = req["description"]
        print('posting a project to db\t')
        if not add.addProject(title, desc, u_id):
            return jsonify({"error": "Could not create Project."})
        return {}
    
    
    #GET ALL USER PROJECTS
    u_id = request.args.get('user_id')
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
    
    #CREATE TASK
    if request.method == 'POST':

        if not request.is_json:
            return "Request was not JSON", 400
    
        req = request.get_json()

        u_id = req["user_id"]
        p_id = req["project_id"]
        desc = req["description"]
        due = req["date_due"] # string "YYYY-MM-DD"
        classification = req["classification"]
        classification = classification.lower()
        diff = req["difficulty"]
        #status = false    handled by db

        #classification ([0, 1, 2] = [communication, process, logistics]), 
        # difficulty ([0, 1, 2, 3]=[Easy, Medium, Hard, Extreme])

        classifier = class_int[classification]
        difficult = diff_int[diff]

        #try:
        #    priority = req["priority"]
        #except KeyError:
        #    priority = 3

        # call to Machine Learning module, returns priority
        # string for due, int for classification and diff
        priority = getRecPriority(date.today(), strToDate(due), classifier, difficult) 
        
        if not add.addTask(u_id, p_id, desc, due, priority, classification, diff):
            return jsonify({"error": "Could not add task."}) 
        return {}
    
    
    my_args = request.args.to_dict()
    print(my_args)
    
    u_id = request.args.get('user_id')
    p_id = request.args.get('project_id')

    
    print(f"\nUSER id : {u_id}\nPROJECT id: {p_id} ")
    my_tasks = get.getUserTasks(u_id)
    #NO TASKS FOR THIS USER
    if my_tasks == 0:
        return {}
    #IF NO p_id PROVIDED, LIST ALL USER TASKS
    if p_id is None:
        dict_of_tasks = to_list_dict(my_tasks)
        return jsonify(dict_of_tasks)
    
    all_p_tasks = get.getProjectTasks(p_id)
    if all_p_tasks == 0:
        return {}

    combined = common(to_list_dict(my_tasks), to_list_dict(all_p_tasks))
    print(combined)
    if len(combined) > 0:
        return jsonify(combined)
    #NO TASKS IN THIS PROJECT
    else:
        return {}

 

#Returns all contacts given user_id
#creates contact given contact username
@app.route("/contacts", methods = ['GET', 'POST'])
def contacts():

    #CREATE CONTACT
    if request.method == 'POST':

        if not request.is_json:
            return "Request was not JSON", 400
    
        req = request.get_json()

        u_id = req["user_id"]
        c_username = req["contact_username"]
        c_id = get.getUserId(c_username)
        if c_id == 0:
            return jsonify({"error": "No such user by that username."})
        if not add.addContact(u_id, c_id):
            return jsonify({"error": "Could not add contact."})
        return {}

    #GET ALL CONTACTS
    u_id = request.args.get('user_id')
    contact_ids = get.getContacts(u_id)
    if len(contact_ids) == 0:
        return {}
    else:
        contacts = []
        for con in contact_ids:
            contacts.append(get.getSafeContact(con))
        return jsonify(contacts)

#/add_user_to_project
@app.route("/add_user_to_project", methods = ['POST'])
def joinProject():
    pass

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

def common(lst1, lst2): 

    print("in common\n")
    print(lst1)
    print(lst2)

    t_ids = []
    for ob in lst1:
        t_ids.append(ob["id"])
    
    print(t_ids)
    final = []
    for ob in lst2:
        if ob["id"] in t_ids:
            final.append(ob)
    return final

#classification ([0, 1, 2] = [communication, process, logistics]), 
#difficulty ([0, 1, 2, 3]=[Easy, Medium, Hard, Extreme])

class_int = {'communication': 0, 'process': 1, 'logistics': 2}
diff_int = {'easy': 0, 'medium': 1, 'hard': 2, 'extreme': 3}

# returns boolean for if two users are contacts
def isContact(self, u_id, f_id):
    with self.app.app_context():
        contacts = db.session.query(Contact).filter_by(user_id=u_id,friend_id=f_id).all()
        if contacts:
            return True
        else:
            return False

def isValidBio(bio):
    return (len(bio) < 281 and len(bio) > 0)

# "YYYY-MM-DD" to date object
def strToDate(str):
    tokens = str.split('-')
    nums = list()
    for token in tokens:
        nums.append(int(token))
    return date(nums[0], nums[1], nums[2])

if __name__ == '__main__':

    app.run(debug=True)