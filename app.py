from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# Initialize the SQLAlchemy object
db = SQLAlchemy(app) 

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to add a user to the database
@app.route('/add_user/<username>')
def add_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return f'User {username} added!'

# Route to list all users in the database
@app.route('/users')
def list_users():
    users = User.query.all()
    return '<br>'.join([f'User: {user.username}' for user in users])

#displays list of users in json
@app.route('/users_json')
def list_users_json():
    users = User.query.all()
    return jsonify([{'username': user.username} for user in users])

# Route to delete a user from the database
@app.route('/remove_user/<username>')
def delete_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return f'User {username} deleted!'
    else:
        return f'User {username} not found!'

# Route to modify a user's username in the database
@app.route('/modify_user/<current_username>/<new_username>')
def modify_user(current_username, new_username):
    user = User.query.filter_by(username=current_username).first()
    if user:
        user.username = new_username
        db.session.commit()
        return f'Username updated from \'{current_username}\' to \'{new_username}\'!'
    else:
        return f'User \'{current_username}\' not found!'

if __name__ == '__main__':
    app.run(debug=True)
