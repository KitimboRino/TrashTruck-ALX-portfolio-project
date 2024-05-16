from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)

# Error handling 400
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Error handling 500
@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Login route
@app.route('/login')
def login():
    return render_template('login.html', title='Login')

# Register route
@app.route('/register')
def register():
    return render_template('register.html', title='Registeration')

# User route
@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

# Home route
@app.route('/home')
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