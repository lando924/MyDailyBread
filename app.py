import os
import requests, random

from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup

from api import key
# from forms import UserAddForm, LoginForm, EditUserForm
from models import db, connect_db



CURR_USER_KEY = "curr_user"
API_BASE_URL = "https://api.scripture.api.bible/v1/bibles"


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///mydailybread'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = "it's a secret"

toolbar = DebugToolbarExtension(app)

connect_db(app)

app.app_context().push()


##############################################################################
# User signup/login/logout:

# @app.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])

#     else:
#         g.user = None


# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]



##############################################################################
# General user routes:

@app.route('/', methods=['GET'])
def home_route():
    """Fetch King James Version (KJV) Bible data and render it"""

    bible_id = "de4e12af7f28f599-02"
    headers = {
        "api-key": key
    }
    
    try:
        # Step 1: fetch all books
        books_url = f"{API_BASE_URL}/{bible_id}/books"
        books_response = requests.get(books_url, headers=headers)
        books_response.raise_for_status()
        books = books_response.json().get("data", [])

        if not books:
            return render_template('home.html', data=None)

        # Step 2: pick a random book
        random_book = random.choice(books)
        book_id = random_book["id"]


        # Step 3: get all chapters from book
        chapters_url = f"{API_BASE_URL}/{bible_id}/books/{book_id}/chapters"
        chapters_response = requests.get(chapters_url, headers=headers)
        chapters_response.raise_for_status()
        chapters = chapters_response.json().get("data", [])

        if not chapters:
            return render_template('home.html', data=None)
        
        # Step 4: Pick a random chapter
        random_chapter = random.choice(chapters)
        chapter_id = random_chapter["id"]

        # Step 5: fetch the verse text   
        verses_url = f"{API_BASE_URL}/{bible_id}/chapters/{chapter_id}/verses"
        verses_response = requests.get(verses_url, headers=headers)
        verses_response.raise_for_status()
        verses = verses_response.json().get("data", [])
       
        if not verses:
            return render_template('home.html', data=None)
        
        # Step 6: Pick a random verse
        random_verse = random.choice(verses)
        verse_id = random_verse["id"]

        # Step 7: Fetch the full verse text
        verse_text_url = f"{API_BASE_URL}/{bible_id}/verses/{verse_id}"
        verse_text_response = requests.get(verse_text_url, headers=headers)
        verse_text_response.raise_for_status()
        verse_data = verse_text_response.json()

        if "data" in verse_data and "content" in verse_data["data"]:
            soup = BeautifulSoup(verse_data["data"]["content"], "html.parser")
            clean_text = soup.get_text(" ", strip=True)
            verse_data["data"]["content"] = clean_text
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        verse_data = None

    return render_template('home.html', data=verse_data)


@app.route('/books', methods=['GET'])
def get_books():
    """Fetch and display all books from the King James Version."""

    bible_id = "de4e12af7f28f599-02"
    url = f"{API_BASE_URL}/{bible_id}/books"
    headers = {"api-key": key}

    try:
        response = requests.get(url, headers=headers)
        print(f"Request URL: {url}")
        print(f"Rsponse Status Code: {response.status_code}")

        response.raise_for_status()
        books_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching books: {e}")
        books_data = None

    return render_template('books.html', books=books_data.get("data", []))



@app.route('/chapters', methods=['GET'])
def get_chapters():
    """Fetch and display all chapters from the King James Version."""

    bible_id = "de4e12af7f28f599-02"
    book_id = "LUK"
    url = f"{API_BASE_URL}/{bible_id}/books/{book_id}/chapters"
    headers = {"api-key": key}

    try:
        response = requests.get(url, headers=headers)
        print(f"Request URL: {url}")
        print(f"Rsponse Status Code: {response.status_code}")

        response.raise_for_status()
        chapters_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching books: {e}")
        chapters_data = None

    return render_template('chapters.html', chapters=chapters_data.get("data", []))



