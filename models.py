"""SQLAlchemy models for MyDailyBread."""

from datetime import datetime

from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User Information"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    username = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # Relationships
    favorites = db.relationship("Favorite", backref="user", lazy=True, cascade="all, delete")
    journals = db.relationship("Journal", backref="user", lazy=True, cascade="all, delete")
    
    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def __repr__(self):
        return f"<User {self.username}"
    

class Favorite(db.Model):
    """Favorite verses model."""

    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False
    )

    bible_id = db.Column(
        db.String(100),
        nullable=False
    )
    book_id = db.Column(
        db.String(100),
        nullable=False
    )
    chapter = db.Column(
        db.Integer,
        nullable=False
    )
    verse = db.Column(
        db.Integer,
        nullable=False
    )
    reference = db.Column(
        db.String(200),
        nullable=False
    )
    text = db.Column(
        db.String(255),
        nullable=False
    )
    
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    def __repr__(self):
        return f"<Favorite {self.reference} by User {self.user_id}>"
    
class Journal(db.Model):
    """Journal Entries model."""

    __tablename__ = "journals"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    entry_date = db.Column(
        db.Date,
        nullable=False,
        default=datetime.utcnow
    )

    title = db.Column(
        db.String(100),
        nullable=False
    )
    
    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Journal {self.title} by User {self.user_id}"
    



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
