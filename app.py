from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Add a secret key for sessions

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(150), nullable=False)
    lastname = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(250))
    phone = db.Column(db.String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Create the database tables
with app.app_context():
    db.create_all()

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
            new_user = User(firstname=firstname, lastname=lastname, email=email)
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
    flash('Logged out!', 'success')
    return redirect(url_for('login'))

# User route
@app.route('/user/<name>', methods=['GET', 'POST'])
def profile(name):
    if 'name' not in session or session['name'] != name:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(firstname=name).first()
    if request.method == 'POST':
        address = request.form.get('address')
        phone = request.form.get('phone')
        if address:
            user.address = address
        if phone:
            user.phone = phone
        db.session.commit()
        flash('Profile updated!', 'success')
    return render_template('profile.html', user=user)

# Home route
@app.route('/')
def home():
    return render_template('home.html', title='Home')

# Clients route
@app.route('/clients')
def clients():
    return render_template('clients.html', title='Clients')

# Crews route
@app.route('/crews')
def crews():
    return render_template('crews.html', title='Crews')

if __name__ == "__main__":
    app.run(debug=True)
