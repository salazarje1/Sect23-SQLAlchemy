"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, func


db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):

    __tablename__ = 'users'


    id = db.Column(
        db.Integer, 
        primary_key=True, 
        autoincrement=True
    )

    first_name = db.Column(
        db.String(30),
        nullable=False
    )

    last_name = db.Column(
        db.String(30),
        nullable=False
    )

    image_url = db.Column(
        db.Text(), 
        default=str('https://eastlakeohio.com/wp-content/uploads/2022/01/no-image-eastlake-300x300.jpg')
    )


class Post(db.Model):

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    post_title = db.Column(db.String(50), default='No Title')

    post_content = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    post = db.relationship('User', backref='posts')