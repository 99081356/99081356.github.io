# models/blog.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

