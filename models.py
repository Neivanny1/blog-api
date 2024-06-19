from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    date_edited = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    edited_by = db.Column(db.String(20), nullable=True)
    content = db.Column(db.Text)
    def __repr__(self):
        return f'<Blogpost {self.id}>'
