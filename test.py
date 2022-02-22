from server.flask_app.models import *
from server.flask_app.app import db, create_app
from pullRecords import Get
from addRecords import Add
from deleteRecords import Delete

app = create_app()

get = Get(app)
add = Add(app)
delete = Delete(app)

# addRecords.addUser(1, 'qwer@gmail.com', 'asdf')

# addRecords.addProject('asdf', 'asdf', 'asdf')
''' '''
add.addUser('asdf1', 'asdf1', 'asdf1')

add.addUser('asdf2', 'asdf2', 'asdf2')

add.addProject('proj1', 'do stuff 1', 1)

add.addProject('proj2', 'do stuff 2', 2)

add.addProject('proj3', 'do stuff 3', 1)

add.addTask(2, 2, 'asdf', '2022-02-20', 1, 'asdf', 'asdf')

# deleteRecords.deleteProject(2)


