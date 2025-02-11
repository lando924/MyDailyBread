# Capstone Project One - MyDailyBread


## GOAL OF APPLICATION
The project is a Bible app called MyDailyBread that allows users to explore and engage with the Bible in an interactive and personalized way. It will provide features such as login authentication, a searchable Bible, favorite verse storage, and tracking of daily reading with optional notes. The app aims to serve as a spiritual and organizational tool for its users.

## APP FEATURES
Features implented inlcude the following:
- User profile acccount: This allows the user to create their own account. With an account you can update you preferences, user details, and store a list of your favorite verses.
- Scripture search: This feature allows any site visitor to search the Bible. They can either search for a whole chapter at a time, a single verse or a collection of verses. 
- Verse-of-the-day: This feature, despite it's name will give you two new "random" verses from the Bible everytime you visit the homepage. If you are logged in, you can click a heart icon to add those verses to your favorites. 
- Favorites tab: This feature allows a logged in user to view their saved list of favorite passages from the Bible. They can delete or add to their list on this page. 
- Search bar: This feature allows any site visitor to type in a keyword like "love" or "David". A list of passages containing those words will be displayed for the user to browse

## USER FLOW
The app is designed for individuals of all ages and backgrounds who are interested in studying or exploring the Bible. This may include religious practitioners, students, and spiritual seekers looking for a simple, accessible way to interact with the Bible.

## TECH STACK USED
The following tech stack was used for this project: 

- Frontend: HTML, CSS, Bootstrap, JavaScript
- Backend: Python, Flask, Bcrypt, WTForms, Jinja, SQLAlchemy, RESTful API from https://docs.api.bible/
- Database: PostgreSQL


## API
This project uses the API.Bible. It contains text from the Bible and allows the user to fetch specific information such as keywords or a particular chapter/verse. No authentication is required. https://scripture.api.bible/

## SETUP
To get this application running, make sure you do the following in the Terminal:

-python3 -m venv venv
-source venv/bin/activate
-pip3 install -r requirements.txt
-createdb mydailybread
-flask run

## TESTS
Information on how to run tests can be found at the top of the test files.

## NOTES
Please leave a comment for any future features you would like to see implemented.