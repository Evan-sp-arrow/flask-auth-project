from flask import Flask, render_template, request, redirect, url_for, session
from db_setup import db, User   # Import your DB setup and model
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)


app.secret_key = 'your_secret_key'  # Required for using sessions


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Home route – login page
@app.route('/')
def home():
    return render_template('login.html')

# Handle login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):

        session['username'] = username  # Store username in session
        return redirect(url_for('dashboard'))
    else:
        message = "Invalid username or password."
        return render_template('login.html', message=message)
    

# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            message = "Username already exists. Please choose another."
            return render_template('signup.html', message=message)

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        message = "Signup successful! You can now log in."
        return render_template('login.html', message=message)

    # 👇 This was missing — return signup page for GET request
    return render_template('signup.html')


# Dashboard route
@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    return f"<h2>Welcome to the dashboard, {username}!</h2>"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
