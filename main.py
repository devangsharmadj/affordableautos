#!/usr/bin/python3

from flask import (
  Flask, 
  render_template,
  redirect,
  url_for,
  abort,
  request,
  flash,
  session
)
from cars import cars
import os
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func



basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "OwnEF6OddTe1LUJPOIyvRghMjwxUwqir"
db = SQLAlchemy(app)
@app.route('/')
def index():
  return render_template("index.html")

@app.route('/index.html')
def home():
  return render_template("index.html")


@app.route('/inventory.html')
def inventory():
  return render_template("inventory.html", cars=cars)


@app.route('/<model>.html')
def car(model):
  car = {}
  for i in cars:
    if i['model'].lower() == model.lower():
      car = i
  return render_template("cars2.html", i=car)

@app.route('/about.html')
def about():
  return render_template("about.html", cars=cars)

@app.route('/terms.html')
def terms():
  return render_template("terms.html")
  
@app.route('/contact.html', methods=['GET', 'POST'])
def contact():
  if request.method == "POST":
    post = Post(subject=request.form['subject'], message=request.form['message'],
                       email=request.form['email'])
    db.session.add(post)
    db.session.commit()
    return render_template('thanks.html')
  else:
    return render_template("contact.html")

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if request.method == "GET":
        return render_template("chatbot.html")
    if request.method == "POST":
        user_input = request.form["user_input"]
        response = chatbot.get_response(user_input)
        return render_template("chatbot.html", response=response)

@app.route('/messages.html')
def messages():
  return render_template('messages.html', posts=Post.query.all())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    bio = db.Column(db.Text)

    def __repr__(self):
        return f'<Student {self.subject}>'

@app.route('/team.html')
def team():
  return render_template('team.html')

if __name__ == "__main__":
  app.run(host='0.0.0.0', port=81)
