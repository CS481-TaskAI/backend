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

#This the is route to the basic url
#Demo will print
@app.route('/')
def index():
    
    resp = get.getUserTasks(2)
    answer = resp[0].to_str()
    print(answer)

    
    
    return answer

# Once the user has been authenticated they will be redirected
# to this function with their username and id
@app.route('/home', methods = ['GET', 'POST'])
def homePage():
    #here we will pass take the id from the request and pull 
    #the records using the id
    pass

# The users project page, here they will need all of their tasks
# regarding the project.
# They can create new tasks
@app.route('/projects', methods = ['GET', 'POST'])
def projectsPage():
    pass



if __name__ == '__main__':

    app.run(debug=True)