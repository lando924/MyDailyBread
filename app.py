import requests, random

from flask import Flask, render_template, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from bs4 import BeautifulSoup

from api import key
from forms import UserAddForm, LoginForm
from models import db, connect_db, User, Favorite, Journal



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

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create a new user and add to DB. Redirect to home page.

    If form not valid, presnet form.

    If there is already a user with that username: flash message and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/users/signup.html', form=form)
        
        do_login(user)

        return redirect("/")
    
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login"""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", "danger")
    
    return render_template('/users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handle user logout"""

    do_logout()
    flash("You have successfully logged out.", "session")
    return redirect("/login")




##############################################################################
# General user routes:

@app.route('/', methods=['GET'])
def home_route():
    """Fetch Bible data and render it"""

    bible_id = "9879dbb7cfe39e4d-01"
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
            return render_template('home.html', data=None, books={})

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
        return render_template('home.html', data=None, books=[])

    return render_template('home.html', data=verse_data, books=books)

@app.route('/verse', methods=['GET'])
def search_verse():
    """Handles scripture search"""

    book = request.args.get("book")
    chapter = request.args.get("chapter")
    verse1 = request.args.get("verse1")
    verse2 = request.args.get("verse2")

    if not book or not chapter:
        flash("Book and Chapter are required.", "warning")
        return redirect('/')
    
    # 
    verse_range = f"{verse1}-{verse2}" if verse1 and verse2 else verse1
    reference = f"{book} {chapter}:{verse_range}" if verse_range else f"{book} {chapter}"


    bible_id = "9879dbb7cfe39e4d-01"
    url = f"{API_BASE_URL}/{bible_id}/chapters/{chapter}/verse"
    headers = {"api_key": key}
    response = requests.get(url, headers=headers)

    return render_template('/users/search.html')
    


############################################################################
# Favorite routes:

# @app.route('/favorites/add_favorite/<int:verse_id', methods=['POST'])
# def user_favorites(verse_id):
#     """favorite/unfavorite a verse"""

#     if not g.user:
#         flash("You must be logged in to like!", "danger")
#         return redirect("/")
    
#     verse = 
    
    

# @app.route('/favorites/<int:user_id>')
# def show_favorites(user_id):
#     """shows users favorites"""

#     user


@app.route('/books', methods=['GET'])
def get_books():
    """Fetch and display all books from the King James Version."""

    bible_id = "9879dbb7cfe39e4d-01"
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


##############################################################################
# Journal routes:

@app.route('/chapters', methods=['GET'])
def get_chapters():
    """Fetch and display all chapters from the King James Version."""

    bible_id = "9879dbb7cfe39e4d-01"
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



