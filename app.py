from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)


users = {}


# Error handling 400
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
@app.route('/login', method=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name in users and users[name]['password'] == password:
            session['name'] = name
            flash('Login successful!', 'success')
            return redirect(url_for ('profile', name=name))
        else:
            flash('Incorrect password or name!', 'danger')
    return render_template('login.html', title='Login')

# Register route
@app.route('/register', method=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        if name in users:
            flash('Name already exists!', 'danger')
        else:
            users[name] = {'email': email, 'password': password}
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Registration')

# Logout route
@app.route('/logout')
def logout():
    session.pop('name', None)
    flash('Logged out!', 'success')
    return redirect(url_for('index'))

# User route
@app.route('/user/<name>', method=['GET', 'POST'])
def profile(name):
    if 'name' not in session or session['name'] != name:
        flash('Access denied!', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        address = request.form.get('address')
        phone = request.form.get('phone')
        if address:
            users[name]['address'] = address
        if phone:
            users[name]['phone'] = phone
        flash('Profile updated!', 'success')
    return render_template('user.html', name=name)

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
