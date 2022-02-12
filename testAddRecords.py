from server.models import *
from server import db, create_app

import addRecords

app = create_app()

addRecords.addUser('asdf', 'qwer@gmail.com', 'asdf')

