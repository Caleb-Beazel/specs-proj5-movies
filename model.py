"""Models for movie ratings app."""
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    email = db.Column(db.String(255), unique = True)
    password = db.Column(db.String(255))

    # ratings = a list of Rating objects.

    def __repr__(self):
        return f'User: id = {self.user_id} | email = {self.email}'

class Movie(db.Model):

    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    title = db.Column(db.String)
    overview = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    poster_path = db.Column(db.String)

    # ratings = a list of Rating objects.

    def __repr__(self):
        return f' Movie: "{self.title}" | release date: {self.release_date} | id: {self.movie_id}'


class Rating(db.Model):

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    score = db.Column(db.Integer)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.movie_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))

    movie = db.relationship("Movie", backref="ratings")
    user = db.relationship("User", backref="ratings")

    def __repr__(self):
        return f"<> Rating rating_id = {self.rating_id}, score = {self.score} <>"


def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
