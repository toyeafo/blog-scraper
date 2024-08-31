from flask import Flask, render_template, request
from markupsafe import escape
from db import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html', message="Welcome to the home page")

@app.route('/about/<name>')
def home_with_name(name):
    return render_template('about.html', name=f"{escape(name)}")

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit', methods=['POST'])
def submit():
    user = User(id=1, 
                name=request.form['name'],
                email=request.form['email'],
                message=request.form['message'],
            )
    db.session.add(user)
    db.session.commit()
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    return f"Hello, {name}. Your email is {email} and the message left is {message}"

if __name__ == '__main__':
    app.run(debug=True)