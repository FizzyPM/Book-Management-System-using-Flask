import os

from flask import Flask, session, redirect, url_for, escape, request,render_template
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine('postgresql://postgres:fizzzyme@localhost:5432/project1')
db = scoped_session(sessionmaker(bind=engine))

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return redirect(url_for('search'))
    return redirect(url_for('signup'))

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/account",methods=["POST"])
def account():
    fname = request.form.get("firstname")
    lname = request.form.get("lastname")
    username = request.form.get("username")
    password = request.form.get("password")
    db.execute("INSERT INTO users (fname,lname,username,password) VALUES (:fname, :lname ,:uname,:pass)",
            {"fname": fname, "lname": lname,"uname":username,"pass":password})
    db.commit()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        password=request.form['password']
        try:
            user = db.execute("SELECT * FROM users WHERE username = :username", {"username": session['username'] }).fetchone()
            if(user.password != password):
                return render_template("error.html",message="Wrong Password")
        except:
            return render_template("error.html",message="Please fill the signup page !")
        return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))

app.secret_key = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

@app.route("/search")
def search():
    user=session['username']
    return render_template("search.html",user=user)

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
    temp2=db.execute("DELETE FROM cur_book")
    dbook = db.execute("SELECT * FROM books WHERE title = :title", {"title": book_title}).fetchone()
    rate=db.execute("SELECT * FROM ratings WHERE isbn=:isbn",{"isbn":dbook.isbn_no} ).fetchall()
    db.execute("INSERT INTO cur_book (cur_isbn,cur_tite) VALUES (:isbn, :title)",
            {"isbn": dbook.isbn_no, "title": dbook.title})
    db.commit()
    res=requests.get("https://www.goodreads.com/book/review_counts.json?key=Op3LFpWFhCjos35VapSw&isbns="+dbook.isbn_no)
    data=res.json()
    rating=data["books"][0]["average_rating"]
    return render_template("details.html", dbook=dbook,rate=rate,rating=rating)

@app.route("/rated",methods=["POST"])
def rated():
    rating = request.form.get("rating")
    comment = request.form.get("comment")
    cbook=db.execute("SELECT * FROM cur_book").fetchone()
    try:
        db.execute("INSERT INTO ratings (uname,isbn,rating,review) VALUES (:uname, :isbn ,:rating,:review)",
                {"uname":session['username'], "isbn": cbook.cur_isbn,"rating":rating,"review":comment})
        db.commit()
    except:
         return render_template("alreadyrated.html")
    return render_template("success.html")