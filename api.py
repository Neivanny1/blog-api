from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from datetime import datetime
from models import db, Blogpost


api = Blueprint('api', __name__)

@api.get('/index')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    serialized_posts = [{
        'id': post.id,
        'title': post.title,
        'subtitle': post.subtitle,
        'author': post.author,
        'date_posted': post.date_posted.isoformat(),
        'content': post.content
    } for post in posts]
    return jsonify(serialized_posts)

@api.get('/about')
def about():
    return render_template('about.html')

@api.get('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    serialized_post = {
        'id': post.id,
        'title': post.title,
        'subtitle': post.subtitle,
        'author': post.author,
        'date_posted': post.date_posted.isoformat(),
        'content': post.content
    }
    return jsonify(serialized_post)

@api.route('/delete')
def delete():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('delete.html', posts=posts)

@api.post('/addpost')
def addpost():
    data = request.json
    title = data.get('title')
    subtitle = data.get('subtitle')
    author = data.get('author')
    content = data.get('content')

    if title is None or subtitle is None or author is None or content is None:
        return jsonify({"error": "Missing required fields"}), 400

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    db.session.add(post)
    db.session.commit()
    post_id = post.id

    sts = {
        "status": "SUCCESS",
        "Code": 201,
        "Message": "Post added successfully",
        "post_id": post_id,
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "content": content
    }
    return jsonify(sts), 201

@api.delete('/deletepost/<int:post_id>')
def deletepost(post_id):
    post = Blogpost.query.get(post_id)
    if post:
        db.session.delete(post)
        db.session.commit()
        return jsonify({
            "status": "SUCCESS",
            "Code": 204,
            "Message": "Post deleted successfully"
        }), 204
    else:
        return jsonify({
            "status": "ERROR",
            "Code": 404,
            "Message": "Post not found"
        }), 404