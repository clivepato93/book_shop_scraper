import sqlite3 
import requests
from bs4 import BeautifulSoup

rating=["One","Two","Three","Four","Five"]

def book_name(book):
    return book("a")[1]["title"]

def book_price(book):
    return book.find(class_="price_color").get_text()[2:]

def book_rating(book):
    return rating.index(book.find("p")['class'][-1])+1

def collect_books():
    book_data=[]
    # Request URL
    link=requests.get("https://books.toscrape.com/catalogue/category/books/horror_31/index.html")
    # Initialise BS
    soup=BeautifulSoup(link.text,"html.parser")
    # Extract Data we Want
    books=soup.find_all(class_="product_pod")
    for book in books:
        name=book_name(book)
        price=book_price(book)
        rank=book_rating(book)
        book_data.append((name,float(price),rank))
    return book_data

    # Save data to database
def database_books():
    conn=sqlite3.connect('books_db.db')
    c=conn.cursor()
    c.execute("CREATE TABLE horror_books (title TEXT, price REAL, rating INTEGER);")
    c.executemany(f"INSERT INTO horror_books VALUES (?,?,?)",collect_books())
    conn.commit()
    conn.close()

collect_books()
database_books()