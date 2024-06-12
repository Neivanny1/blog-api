from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from datetime import datetime
from models import db, Blogpost


api = Blueprint('api', __name__)

@api.get('/getblogs')
def index():
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

@api.get('/about')
def about():
    return render_template('about.html')

@api.get('/getblog/<int:blog_id>')
def get_blog(blog_id):
    blog = Blogpost.query.filter_by(id=blog_id).one()
    serialized_blog = {
        'id': blog.id,
        'title': blog.title,
        'subtitle': blog.subtitle,
        'author': blog.author,
        'date_posted': blog.date_posted.isoformat(),
        'content': blog.content
    }
    return jsonify(serialized_blog)

@api.route('/delete')
def delete():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('delete.html', posts=posts)


'''
Post a blog
'''
@api.post('/addblog')
def addblog():
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

'''
Update blog
'''
@api.put('/updateblog/<int:post_id>')
def updatepost(post_id):
    data = request.json
    title = data.get('title')
    subtitle = data.get('subtitle')
    author = data.get('author')
    content = data.get('content')
    if title is None or subtitle is None or author is None or content is None:
        return jsonify({"error": "Missing required fields"}), 400
    post = Blogpost.query.get(post_id)
    if post is None:
        return jsonify({"error": "Post not found"}), 404
    post.title = title
    post.subtitle = subtitle
    post.author = author
    post.content = content
    db.session.commit()
    sts = {
        "status": "SUCCESS",
        "Code": 200,
        "Message": "Post updated successfully",
        "post_id": post_id,
        "title": title,
        "subtitle": subtitle,
        "author": author,
        "content": content
    }
    return jsonify(sts), 200

'''
Delete blog
'''
@api.delete('/deleteblog/<int:post_id>')
def deleteblog(post_id):
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