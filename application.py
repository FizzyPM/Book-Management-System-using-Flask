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
    db.execute("INSERT INTO cur_user (f_name,l_name,cur_username) VALUES (:fname, :lname ,:uname)",
            {"fname": user.fname, "lname": user.lname,"uname":user.username})
    db.commit()
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

@app.route("/book/<string:book_title>")
def details(book_title):
    dbook = db.execute("SELECT * FROM books WHERE title = :title", {"title": book_title}).fetchone()
    rate=db.execute("SELECT * FROM ratings WHERE isbn=:isbn",{"isbn":dbook.isbn_no} ).fetchall()
    db.execute("INSERT INTO cur_book (cur_isbn,cur_tite) VALUES (:isbn, :title)",
            {"isbn": dbook.isbn_no, "title": dbook.title})
    db.commit()
    return render_template("details.html", dbook=dbook,rate=rate)

@app.route("/rated",methods=["POST"])
def rated():
    rating = request.form.get("rating")
    comment = request.form.get("comment")
    cur=db.execute("SELECT * FROM cur_user").fetchone()
    cbook=db.execute("SELECT * FROM cur_book").fetchone()
    db.execute("INSERT INTO ratings (uname,isbn,rating,review) VALUES (:uname, :isbn ,:rating,:review)",
            {"uname": cur.cur_username, "isbn": cbook.cur_isbn,"rating":rating,"review":comment})
    db.commit()
    return render_template("success.html")