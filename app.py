from flask import Flask, render_template, request, jsonify
from db_setup import db, User
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


app = Flask(__name__)

# JWT configuration
app.config['JWT_SECRET_KEY'] = 'supersecretkey123'

app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=1)  # Token expires in 1 minute for testing

jwt = JWTManager(app)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# ------------------ ROUTES ------------------

@app.route('/')
def home():
    return render_template('login.html')


# LOGIN — accepts JSON instead of form
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()   # JSON input from JavaScript

    username = data.get('username')  #extract username and password
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):

        access_token = create_access_token(identity=username)

        return jsonify({
            "message": "Login successful",
            "token": access_token
        }), 200

    return jsonify({"message": "Invalid username or password"}), 401



# SIGNUP (same as before)
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return render_template('signup.html',
                                   message="Username already exists.")

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)

        db.session.add(new_user) #prepare to add new user
        db.session.commit() #commit to database #save changes permanently

        return render_template('login.html',
                               message="Signup successful! You can now log in.")

    return render_template('signup.html')



# ----------------------------
# DASHBOARD (HTML page only)
# ----------------------------
# NOTE: This route no longer returns JSON.
# It only loads the HTML page.
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template("dashboard.html")   # Now loads HTML



# --------------------------------------------------
# PROTECTED API that requires JWT (returns the data)
# --------------------------------------------------
# IMPORTANT:
# JavaScript in dashboard.html will call this endpoint
# and send token in Authorization header.
@app.route('/api/dashboard-data', methods=['GET'])
@jwt_required()
def dashboard_data():
    current_user = get_jwt_identity()
    return jsonify({
        "message": f"Welcome to the dashboard, {current_user}!"
    })



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
