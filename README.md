Capstone Project One - MyDailyBread
DEPLOYED AT

GOAL OF APPLICATION
The project is a Bible app called MyDailyBread that allows users to explore and engage with the Bible in an interactive and personalized way. It will provide features such as login authentication, a searchable Bible, favorite verse storage, and tracking of daily reading with optional notes. The app aims to serve as a spiritual and organizational tool for its users.

APP FEATURES
Features implented inlcude the following:

User profile acccount: This allows the user to create their own account. With an account you can update you preferences, user details, and store a list of your favorite verses.
Scripture search: This feature allows any site visitor to search the Bible. They can either search for a whole chapter at a time, a single verse or a collection of verses.
Verse-of-the-day: This feature, despite it's name will give you two new "random" verses from the Bible everytime you visit the homepage. If you are logged in, you can click a heart icon to add those verses to your favorites.
Favorites tab: This feature allows a logged in user to view their saved list of favorite passages from the Bible. They can delete or add to their list on this page.
Memory Game tab: This feature allows any site visitor to play a game! The game is proven to help with memorization. The game begins once the user has selected a verse to memorize.
Compare tab: This feature allows any site visitor to view two translations of the Bible at the same time. This is helpful since translations can vary in the style of english used. A user can select a chapter form the Bible, and two translations of choice will be displayed for the user to read.
Search bar: This feature allows any site visitor to type in a keyword like "love" or "David". A list of passages containing those words will be displayed for the user to browse
USER FLOW
When visiting the site, the user will be brough to the home page where they can see the verses of the day and option to search the Bible. They can also navigate to the Memory Game or Compare tabs where they can either play a game with a verse from the Bible or compare different translations of the Bible, respectively. If the user clicks on the Favorites tab, they will be redirected to the sign up screen. Upon successful account creation, they will be redirected to the Favorites tab that they were trying to access. Here they can search for verses and add it to their favorites list. If the user cliks on their username, they can add details to their account and set a default translation for the whole site to use. Once done browsing the site, the user could then logout using the link in the nav bar.

TECH STACK USED
The following tech stack was used for this project: Python, Flask, PostreSQL, JavaScript, SQLAlchemy, Jinja, RESTful APIs, HTML, CSS, WTForms, Boostrap, and Bcrypt

API
This project uses the Bolls Bible API. It contains text from the Bible and allows the user to fetch specific information such as keywords or a particular chapter/verse. No authentication is required. https://bolls.life/api/

SETUP
To get this application running, make sure you do the following in the Terminal:

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
createdb upwordV4
flask run
TESTS
Information on how to run tests can be found at the top of the test files.

NOTES
Please leave a comment for any future features you would like to see implemented.