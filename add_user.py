# add_user.py
from flask import Flask
from db_setup import db, User  # Updated: import db and User only
from werkzeug.security import generate_password_hash  # Added: for hashing password

# This block runs inside the Flask app context
app = Flask(__name__)  # Create temporary Flask app for setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()  # Ensure tables exist
    # Check if user already exists
    if not User.query.filter_by(username='forest').first():
        hashed_password = generate_password_hash('forest1234')  # Added: hash the password
        new_user = User(username='forest', password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        print("User added successfully!")
    else:
        print("User already exists!")
