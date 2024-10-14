"""Blogly application."""


from models import db, connect_db, User, Post, Tag
from flask import Flask, request, redirect, render_template, flash, session
#from flask_debugtoolbar import DebugToolbarExtension
#from sqlalchemy.sql import text





app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly' #connects to blogly database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True #shows sql when running objects or app.
app.config['SECRET_KEY'] = "secretKey"



#toolbar = DebugToolbarExtension(app)


connect_db(app) #connect app to db 
db.create_all() #create database

@app.route('/hello')
def hello():
    return "Hello There!" #test

@app.route('/')
def home():
    """homepage redirects to users list"""

    return redirect('/users')

@app.route('/users')
def user_list():
    users = User.query.order_by(User.first_name, User.last_name).all()

    return render_template('/users/index.html', users = users)

@app.route('/users/new', methods = ["GET"])
def new_user():
    """makes add form for users"""

    return render_template('/users/new.html')


@app.route("/users/new", methods = ["POST"])  
def add_new_user():
    """add submitted user and redirect back to user index"""
    new_user = User(first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                image_url=request.form['image_url'] or None
)   #takes persons submitted info and below, adds new user to session and committs it, adding them to list/ table

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users") 


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """show user person clicked on from list"""
    user = User.query.get_or_404(user_id)
    return render_template('/users/show.html', user = user) #user will be anchor tags and clicking on them will send them to specific user page.

@app.route('/users/<int:user_id>/edit')
def show_edit(user_id):
    """show from to edit user"""
    user = User.query.get_or_404(user_id)

    return render_template('users/edit.html', user = user) #using user id to send person to edit user page

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def edit_user(user_id):
    """take provided input and add user to list"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    return redirect('/users') #edit user taking input and adding it to list/table


@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    """handles deleting user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users') #delete using using delete forms, a post method and requires user input




#--------------------------------------------------



@app.route('/users/<int:user_id>/posts/new')
def set_up_post_form(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    """show form at add post for that user"""
    return render_template('posts/new.html', user=user, tags = tags)



@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def handle_post(user_id):
    """handle post form"""
    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post = Post(title = request.form['title'],
                content = request.form['content'],
                user = user,
                tags = tags) #you need the tags they selected.

    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """show post, show buttons to edit and delete post"""
    
    post = Post.query.get_or_404(post_id)

    return render_template('posts/show.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """show form to edit post"""
    post = Post.query.get_or_404(post_id)#grab post by it's id.
    tags = Tag.query.all() #display all tags so user can select any of them for their post.

    return render_template('posts/edit.html', post=post, tags = tags) #show edit.html page for specific post from user and show all tags.



@app.route('/posts/<int:post_id>/edit', methods = ["POST"])
def edit_post(post_id):
    """handle form to edit post"""

    post = Post.query.get_or_404(post_id) #grab post by it's id.
    post.title = request.form['title'] #grab and push submitted title.
    post.content = request.form['content'] #grab and push submitted content.

    tag_ids = [int(num) for num in request.form.getlist('tags')] #request all tags selected.
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all() #add selected tags to this specific post.

        
    db.session.add(post) #add post to database.
    db.session.commit() #commit changes to database.
    return redirect(f'/users/{post.user_id}') #redirect to this specific post from this specific user.

@app.route('/posts/<int:post_id>/delete', methods = ["POST"])
def delet_post(post_id):
    """delete post and return to user with posts page"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')


#-----------------------------------


@app.route('/tags')
def get_tags():
    """list all tags"""
    
    tags = Tag.query.all() #retrieve all tags from Tag model


    return render_template('/tags/index.html', tags = tags)


@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """show details about a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('/tags/show.html', tag = tag)


@app.route('/tags/new')
def new_tag():
    """show form to make new tag"""

    posts = Post.query.all()

    return render_template('/tags/new.html', posts = posts)


@app.route('/tags/new', methods = ["POST"]) #look at this one again
def post_new_tag():
    """handle new tag form"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts = posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit')
def edit_tag(tag_id):
    """show form to edit existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all() #getting all tags for specific post


    return render_template('tags/edit.html', posts = posts, tag = tag)


@app.route('/tags/<int:tag_id>/edit', methods = ["POST"])
def post_edit_tag(tag_id):
    """handle form to edit existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    

    post_ids = [int(num) for num in request.form.getlist('posts')]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all() 

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/delete', methods = ['POST'])
def delete_tag(tag_id):
    """delete existing tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')