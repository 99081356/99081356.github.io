# models/blog.py
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Post(db.Model):
    # 定义Post类，继承自db.Model

    id = db.Column(db.Integer, primary_key=True)
    # 定义id列，类型为db.Integer，为主键
    title = db.Column(db.String(100), nullable=False)
    # 定义title列，类型为db.String(100)，不可为空
    content = db.Column(db.Text, nullable=False)
    # 定义content列，类型为db.Text，不可为空
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.now)
    # 定义date_posted列，类型为db.DateTime，不可为空，默认值为当前时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    # 定义updated_at列，类型为db.DateTime，默认值为当前时间，每次更新时自动更新为当前时间
    # 定义一个tags属性，用来表示和这个文章关联的标签
    tags = db.relationship('Tag', secondary='post_tags', lazy='subquery', backref=db.backref('posts', lazy=True))


def __repr__(self):
    return f"Post('{self.title}', '{self.date_posted}')"


# 定义__repr__方法，用于打印Post对象时显示的内容

class Tag(db.Model):
    # 标签的ID
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 标签的名称
    name = db.Column(db.String(100), unique=True, nullable=False)


class PostTags(db.Model):
    # 定义PostLabel类，作为关联表post和tag的中间表
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    # 定义tag_id，类型为db.Integer，外键为tag表的id，主键为True
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

    def __repr__(self):
        # 定义__repr__方法，用于打印PostLabel类的信息
        return f"PostTags(post_id={self.post_id}, label_id={self.tag_id})"
