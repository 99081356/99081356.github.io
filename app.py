from flask import Flask
from controllers.blog_controller import blog_controller
from models.blog import db
from flask_sqlalchemy import SQLAlchemy
from markdown2 import Markdown
from flask_wtf import CSRFProtect
import os

# 创建Flask应用
app = Flask(__name__)
# 设置密钥
app.config['SECRET_KEY'] = '3.1415926'

# 设置数据库连接
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite'
# 初始化数据库
db.init_app(app)
# 初始化CSRF保护
CSRFProtect(app)

# 确保应用程序上下文已经激活
with app.app_context():
    # 创建所有表
    db.create_all()

# 初始化Markdown转换器
markdown_converter = Markdown()
# 注册蓝本
app.register_blueprint(blog_controller)
# 注册过滤器
app.jinja_env.filters['markdown'] = lambda text: markdown_converter.convert(text)

if __name__ == '__main__':
    # 运行应用
    app.run(debug=True)
