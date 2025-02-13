import os
import requests

from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError


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
    url = f"{API_BASE_URL}/{bible_id}"
    headers = {
        "api-key": key
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")  # Prints the response data
        print(response.status_code, response.text)
        data = None 
        
    return render_template('home.html', data=data)


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



