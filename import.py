import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine('postgresql://postgres:fizzzyme@localhost:5432/project1')
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    for isbn,title,author,year in reader:
        db.execute("INSERT INTO books(isbn_no,title,author,year) VALUES (:isbn,:title,:author,:year)",
                    {"isbn":isbn,"title":title,"author":author,"year":year})
    db.commit()
    print('Task Performed')

if __name__ == "__main__":
    main()