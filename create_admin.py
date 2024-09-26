from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash
import random
import string

def generate_random_password(length=12):
    characters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    password = ''.join(random.choice(characters) for i in range(length))
    return password

app = create_app()

with app.app_context():
    username = input("Enter admin username: ")
    password = input("Enter the password: ")
    print("Password", password)
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_admin = User(username=username, password_hash=hashed_password)
    
    db.session.add(new_admin)
    db.session.commit()
    
    print(f"Admin user '{username}' created with password: {password}")
