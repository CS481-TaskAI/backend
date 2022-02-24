from server.flask_app.app import db, create_app
from getRecords import Get
from addRecords import Add
from deleteRecords import Delete
from flask import Flask, request, jsonify
import json

app = create_app()

get = Get(app)
add = Add(app)
delete = Delete(app)

#--------------------Get and Post routes------------------------------------------

# Will take the username and password and authenticate
# Returns user id
# Post will attempt to create database records if email or username don't exist
@app.route('/user', methods = ['GET', 'POST'])
def login_signup():
    #here we will pass take the id from the request and pull 
    #the records using the id
    pass

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
        # rest of the attributes
        # then,
        # add users with these parameters

    obs = get.getUserTasks(2)
    list_of_dicts = to_list_dict(obs)
    return jsonify(list_of_dicts)

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

if __name__ == '__main__':

    app.run(debug=True)