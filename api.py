from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from flask_jwt_extended import jwt_required, create_access_token
from flasgger import swag_from
from .models import db, Blogpost, User

api = Blueprint('api', __name__)

# Routes definitions
@api.post('/signup')
@swag_from('swagger/signup.yml')
def signup():
    username = request.json.get('username', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    if not username or not email or not password:
        return jsonify({"error": "Missing username, email, or password"}), 400
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already exists"}), 409
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email address already exists"}), 409
    new_user = User(username=username, email=email)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    access_token = create_access_token(identity=username)
    return jsonify({"message": "User created successfully", "access_token": access_token}), 201

@api.post('/login')
@swag_from('swagger/login.yml')
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401
    access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
    return jsonify(access_token=access_token), 200

@api.get('/getblogs')
@jwt_required()
@swag_from('swagger/getblogs.yml')
def get_blogs():
    blogs = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    serialized_blogs = [{
        'id': blog.id,
        'title': blog.title,
        'subtitle': blog.subtitle,
        'author': blog.author,
        'date_posted': blog.date_posted.isoformat(),
        'content': blog.content
    } for blog in blogs]
    return jsonify(serialized_blogs)

@api.get('/getblog/<int:blog_id>')
@jwt_required()
@swag_from('swagger/getblog.yml')
def get_blog(blog_id):
    blog = Blogpost.query.filter_by(id=blog_id).one_or_none()
    if not blog:
        return jsonify({"error": "Blog post not found"}), 404
    serialized_blog = {
        'id': blog.id,
        'title': blog.title,
        'subtitle': blog.subtitle,
        'author': blog.author,
        'date_posted': blog.date_posted.isoformat(),
        'content': blog.content
    }
    return jsonify(serialized_blog), 200

@api.post('/addblog')
@jwt_required()
@swag_from('swagger/addblog.yml')
def add_blog():
    data = request.json
    title = data.get('title')
    subtitle = data.get('subtitle')
    author = data.get('author')
    content = data.get('content')
    if not all([title, subtitle, author, content]):
        return jsonify({"error": "Missing required fields"}), 400
    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    return jsonify({"message": "Blog post added successfully", "post_id": post.id}), 201

@api.put('/updateblog/<int:post_id>')
@jwt_required()
@swag_from('swagger/updateblog.yml')
def update_blog(post_id):
    data = request.json
    title = data.get('title')
    subtitle = data.get('subtitle')
    author = data.get('author')
    content = data.get('content')
    if not all([title, subtitle, author, content]):
        return jsonify({"error": "Missing required fields"}), 400
    post = Blogpost.query.get(post_id)
    if not post:
        return jsonify({"error": "Blog post not found"}), 404
    post.title = title
    post.subtitle = subtitle
    post.author = author
    post.content = content
    db.session.commit()
    return jsonify({"message": "Blog post updated successfully", "post_id": post_id}), 200

@api.delete('/deleteblog/<int:post_id>')
@jwt_required()
@swag_from('swagger/deleteblog.yml')
def delete_blog(post_id):
    post = Blogpost.query.get(post_id)
    if not post:
        return jsonify({"error": "Blog post not found"}), 404
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Blog post deleted successfully", "post_id": post_id}), 204
