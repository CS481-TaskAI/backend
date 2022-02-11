from server.models import User
from server import db, create_app

app = create_app()

def addUser(idIn, usernameIn, emailIn, passwordIn):
    if ((not isinstance(idIn, int)) or (not isinstance(usernameIn, str)) or # makes sure input is correct datatypes
        (not isinstance(emailIn, str)) or (not isinstance(passwordIn, str))):
        print('Bad input!')
        return
    with app.app_context():
        newUser = User(id=idIn, username=usernameIn, email=emailIn, password=passwordIn)
        db.session.add(newUser)
        db.session.commit()
    
# example implementation
addUser(3, 'asdf', 'qwer@gmail.com', 'asdf')

