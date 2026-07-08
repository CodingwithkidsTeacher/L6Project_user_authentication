from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.secret_key = "My Secret"

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
        
posts = [
    {
        'author': 'Cool Coder',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'Oct. 1, 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'Oct. 5, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
  user= ''

  if "username" in session:
    user = session['username']
 
  return render_template('home.html', posts=posts, user=user)

@app.route("/about")
def about():
  user = ''

  if "username" in session:
    user = session['username']
  
  return render_template('about.html', user=user, title="About")

@app.route("/login", methods=['POST', 'GET'])
def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first() 

    if user and (password == user.password):
        session['username'] = username
        return redirect("/")
    else:
      return render_template("login.html", user='', error = "Invalid username or password")
  else:
    return render_template("login.html", user='')

@app.route("/signup", methods=['POST', 'GET'])
def signup():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password=request.form["confirm-password"]

    if password != confirm_password:
      return render_template("signup.html", user='', error="Passwords do not match!")

    user = User.query.filter_by(username=username).first() 

    if user:
        return render_template("signup.html", user='', error = "Username already exists.")

    new_user = User(username=username, password=password)
    
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect("/login")
  else:
    return render_template('signup.html', user='')

@app.route("/logout")
def logout():
  session.pop('username', None)
  return render_template('home.html', user='', posts=posts)


if __name__ == "__main__":
  db.create_all()
  app.run(host='0.0.0.0', port=8080)
