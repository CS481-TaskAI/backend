from server.models import *
from server import db, create_app

import addRecords
import pullRecords
import deleteRecords

app = create_app()

# addRecords.addUser(1, 'qwer@gmail.com', 'asdf')

# addRecords.addProject('asdf', 'asdf', 'asdf')
'''
addRecords.addUser('asdf1', 'asdf1', 'asdf1')

addRecords.addUser('asdf2', 'asdf2', 'asdf2')

addRecords.addProject('proj1', 'do stuff 1', 1)

addRecords.addProject('proj2', 'do stuff 2', 2)

addRecords.addProject('proj3', 'do stuff 3', 1)

addRecords.addTask(2, 2, 'asdf', '2022-02-20', 1, 'asdf', 'asdf')
'''
deleteRecords.deleteProject(2)


