"""Blogly application."""

from flask import Flask, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'bestpasswordever'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


connect_db(app)

@app.route('/')
def home_page():
    """Show home page(for now just all users)"""

    return redirect('/users')

@app.route('/users')
def all_users():
    """Showing all users"""

    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def new_user_form():

    return render_template('new_users.html')


@app.route('/users/new', methods=['POST'])
def create_new_user():
    first = request.form['first_name']
    last = request.form['last_name']
    image = request.form['image_url']
    image = image if image else None

    new_user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')

@app.route('/users/<int:id>')
def user_details(id):
    user = User.query.get_or_404(id)

    return render_template('user_details.html', user=user)


@app.route('/users/<int:id>/edit')
def edit_user_form(id):
    user = User.query.get_or_404(id)

    return render_template('user_edit.html', user=user)

@app.route('/users/<int:id>/edit', methods=["POST"])
def edit_user(id):
    first = request.form['first_name']
    last = request.form['last_name']
    image = request.form['image_url']
    image = image if image else None

    user = User.query.get(id)
    user.first_name = first
    user.last_name = last
    user.image_url = image

    db.session.add(user)
    db.session.commit()

    return redirect(f'/users/{user.id}')

@app.route('/users/<int:id>/delete')
def delete_user(id):
    """Deleting a user"""
    User.query.filter_by(id=id).delete()
    db.session.commit()

    return redirect('/')

