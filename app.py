from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for sessions

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
bootstrap = Bootstrap(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(250))
    phone = db.Column(db.String(50))
    role = db.Column(db.String(20), nullable=False, default='user')
    pickupdate = db.Column(db.String(50))
    wastetype = db.Column(db.String(100))
    crew_id = db.Column(db.Integer, db.ForeignKey('crew.id'), nullable=True)  # Foreign key reference
    location = db.Column(db.String(250))
    subscription = db.Column(db.String(50))

    crew = db.relationship('Crew', back_populates='members')

    def __init__(self, firstname, lastname, email, password, address=None, phone=None, role='user', pickupdate=None, wastetype=None, crew_id=None, location=None, subscription=None):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = generate_password_hash(password)
        self.address = address
        self.phone = phone
        self.role = role
        self.pickupdate = pickupdate
        self.wastetype = wastetype
        self.crew_id = crew_id
        self.location = location
        self.subscription = subscription

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# Crew model
class Crew(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    pickupdate = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(250), nullable=False)

    members = db.relationship('User', back_populates='crew', cascade='all, delete-orphan')

    def __init__(self, name, pickupdate, location):
        self.name = name
        self.pickupdate = pickupdate
        self.location = location


# Create the database tables
with app.app_context():
    db.create_all()


# Routes and Views

# Landing page route
@app.route('/')
def home():
    return render_template('home.html')


# Error handling 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Error handling 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# Home route
@app.route('/dashboard')
def index():
    if 'name' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['name'] = user.firstname
            session['role'] = user.role  # Store user role in session
            flash('Login successful!', 'success')
            return redirect(url_for('profile', name=user.firstname))
        else:
            flash('Incorrect password or email!', 'danger')
    return render_template('login.html', title='Login')


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists!', 'danger')
        else:
            new_user = User(firstname=firstname, lastname=lastname, email=email, password=password)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Registration')


# Logout route
@app.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('role', None)  # Remove user role from session on logout
    flash('Logged out!', 'success')
    return redirect(url_for('login'))


# User route
@app.route('/user/<name>', methods=['GET', 'POST'])
def profile(name):
    if 'name' not in session or session['name'] != name:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(firstname=name).first()  # Assuming name refers to firstname

    if not user:
        flash('User not found!', 'danger')
        return redirect(url_for('index'))  # Redirect to a different page (e.g., homepage)

    # Now you have the user object, proceed with rendering the template
    return render_template('profile.html', user=user)  # Use profile.html for displaying profile


@app.route('/edit_user/<int:id>', methods=['POST'])
def edit_user(id):
    if request.method == 'POST':
        # Retrieve user information from the form
        firstname = request.form['editFirstname']
        lastname = request.form['editLastname']
        pickupdate = request.form['editPickupdate']
        wastetype = request.form['editWastetype']
        crew_id = request.form['editCrew']
        phone = request.form['editPhone']
        location = request.form['editLocation']
        subscription = request.form['editSubscription']

        # Find the user in the database by ID
        user = User.query.get(id)

        # Update the user information
        user.firstname = firstname
        user.lastname = lastname
        user.pickupdate = pickupdate
        user.wastetype = wastetype
        user.crew_id = crew_id
        user.phone = phone
        user.location = location
        user.subscription = subscription

        # Commit changes to the database
        db.session.commit()

        # Flash a success message
        flash('User information updated successfully!', 'success')

        # Redirect to the clients page
        return redirect(url_for('clients'))


# Clients route
@app.route('/clients')
def clients():
    # TODO: Implement the sessions for admins only
    if 'role' not in session or session['role'] != 'user':
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    # Fetch all users from the database
    users = User.query.all()
    crews = Crew.query.all()

    return render_template('clients.html', title='Clients', users=users, crews=crews)


# Crews route
@app.route('/crews')
def crews():
    if 'role' not in session or session['role'] != 'user':
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    crews = Crew.query.all()

    return render_template('crews.html', title='Crews', crews=crews)


# Add Crew route
@app.route('/add_crew', methods=['POST'])
def add_crew():
    if request.method == 'POST':
        name = request.form['name']
        pickupdate = request.form['pickupdate']
        location = request.form['location']

        new_crew = Crew(name=name, pickupdate=pickupdate, location=location)
        db.session.add(new_crew)
        db.session.commit()

        flash('Crew added successfully!', 'success')

        return redirect(url_for('crews'))


# Edit Crew route
@app.route('/edit_crew/<int:id>', methods=['POST'])
def edit_crew(id):
    if request.method == 'POST':
        crew = Crew.query.get(id)
        crew.name = request.form['editName']
        crew.pickupdate = request.form['editPickupdate']
        crew.location = request.form['editLocation']

        db.session.commit()

        flash('Crew information updated successfully!', 'success')

        return redirect(url_for('crews'))


# Delete Crew route
@app.route('/delete_crew/<int:id>', methods=['POST'])
def delete_crew(id):
    if request.method == 'POST':
        crew = Crew.query.get(id)
        if crew:
            db.session.delete(crew)
            db.session.commit()
            flash('Crew deleted successfully!', 'success')
        else:
            flash('Crew not found!', 'danger')
    return redirect(url_for('crews'))


# edit profile
@app.route('/edit_profile/<int:id>', methods=['GET', 'POST'])
def edit_profile(id):
    if 'name' not in session or session['name'] != User.query.get(id).firstname:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = User.query.get(id)

    if request.method == 'POST':
        # Retrieve user information from the form
        firstname = request.form['editFirstname']
        lastname = request.form['editLastname']
        phone = request.form['editPhone']
        wastetype = request.form['editWastetype']

        # Update the user information
        user.firstname = firstname
        user.lastname = lastname
        user.phone = phone
        user.wastetype = wastetype

        # Commit changes to the database
        db.session.commit()

        # Flash a success message
        flash('Profile information updated successfully!', 'success')

        # Redirect back to the profile page
        return redirect(url_for('profile', name=user.firstname))  # Redirect to profile

    return render_template('edit_profile.html', user=user)


if __name__ == "__main__":
    app.run(debug=True)
