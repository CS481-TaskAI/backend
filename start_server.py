from server.flask_app.app import db, create_app
from server.API.pullRecords import Get
from server.API.addRecords import Add
from server.API.deleteRecords import Delete
from flask import Flask, request, jsonify
import json

app = create_app()
db.init_app(app)

get = Get(app)
add = Add(app)
delete = Delete(app)


@app.route('/')
def index():
    
    return 'hello there'

if __name__ == '__main__':

    app.run(debug=True)