import os

from flask import Flask, session,render_template,request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('postgresql://postgres:fizzzyme@localhost:5432/project1')
db = scoped_session(sessionmaker(bind=engine))

@app.route("/")
def signup():
    return render_template("signup.html")

@app.route("/create",methods=["POST"])
def create():
    fname = request.form.get("firstname")
    lname = request.form.get("lastname")
    username = request.form.get("username")
    password = request.form.get("password")
    db.execute("INSERT INTO users (fname,lname,username,password) VALUES (:fname, :lname ,:uname,:pass)",
            {"fname": fname, "lname": lname,"uname":username,"pass":password})
    db.commit()
    return render_template("success.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/search",methods=["POST"])
def search():
    username = request.form.get("username")
    password = request.form.get("password")
    if db.execute("SELECT * FROM users WHERE username = :username", {"username": username}).rowcount == 0:
        return render_template("error.html",message="No such user with that username.")
    user = db.execute("SELECT * FROM users WHERE username = :username", {"username": username }).fetchone()
    if(user.password != password):
        return render_template("error.html",message="Wrong Password")
    return render_template("success.html")

@app.route("/bsearch")
def bsearch():
    return render_template("bsearch.html")

@app.route("/book",methods=["POST"])
def book():
    title = request.form.get("title")
    isbn = request.form.get("isbn")
    author = request.form.get("author")
    if isbn is None:
        isbn=''
    if title is None:
        title=''
    if author is None:
        author=''
    curbooks=db.execute("SELECT * FROM books WHERE title LIKE :title AND author LIKE :author AND isbn_no LIKE :isbn ",{"title": title+'%',"author": author+'%',"isbn": isbn+'%'} ).fetchall()
    return render_template("books.html", curbooks=curbooks)
