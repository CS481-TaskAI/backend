from server.flask_app.models import *
from server.flask_app.app import db, create_app
from getRecords import Get
from addRecords import Add
from deleteRecords import Delete
from modifyRecords import Modify

app = create_app()

get = Get(app)
add = Add(app)
delete = Delete(app)
modify = Modify(app)

# addRecords.addUser(1, 'qwer@gmail.com', 'asdf')

# addRecords.addProject('asdf', 'asdf', 'asdf')
'''
add.addUser('asdf1', 'asdf1', 'asdf1')

add.addUser('asdf2', 'asdf2', 'asdf2')

add.addProject('proj1', 'do stuff 1', 1)

add.addProject('proj2', 'do stuff 2', 2)

add.addProject('proj3', 'do stuff 3', 1)

add.addTask(2, 2, 'asdf', '2022-02-20', 1, 'asdf', 'asdf')
'''
# delete.deleteProject(2)

# projects = get.getUserProjects(1)
# print(projects)

# modify.modifyProject(1, 'proj asdf', 'do stuff asdf')

# modify.modifyTask(1, 'qwer', 2022-2-22, 3, 'qewr', 'asdf')

# modify.markTaskCompleted(1)

p_id = get.getProjectId('proj1')
print(p_id)


