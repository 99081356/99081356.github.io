from flask import Flask
from controllers.blog_controller import blog_controller
from models.blog import db
from flask_sqlalchemy import SQLAlchemy
from markdown2 import Markdown
from flask_wtf import CSRFProtect
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = '3.1415926'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite'
db.init_app(app)
CSRFProtect(app)

# 确保应用程序上下文已经激活
with app.app_context():
    # 创建所有表
    db.create_all()
# Initialize Markdown converter
markdown_converter = Markdown()
app.register_blueprint(blog_controller)
# Register the filter
app.jinja_env.filters['markdown'] = lambda text: markdown_converter.convert(text)


if __name__ == '__main__':
    app.run(debug=True)
