from flask import Blueprint, request, render_template
from views.blog_views import index, post, new_post, edit_post, delete_post
from views.common_tools import common_tools

blog_controller = Blueprint('blog_controller', __name__)


# 定义博客首页的路由
@blog_controller.route('/')
def blog_index():
    # 调用index函数
    return index()


# 定义博客文章页的路由，post_id为文章的id
@blog_controller.route('/<int:post_id>')
def blog_post(post_id):
    # 调用post函数，传入post_id
    return post(post_id)


# 定义新建文章页的路由，支持GET和POST请求
@blog_controller.route('/new_post', methods=['GET', 'POST'])
def new_post_page():
    # 调用new_post函数
    return new_post()


# 定义编辑文章页的路由，支持GET和POST请求，post_id为文章的id
@blog_controller.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post_page(post_id):
    # 调用edit_post函数，传入post_id
    return edit_post(post_id)


# 定义删除文章页的路由，支持GET和POST请求，post_id为文章的id
@blog_controller.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post_page(post_id):
    # 调用delete_post函数，传入post_id
    return delete_post(post_id)


# 定义博客首页的路由
@blog_controller.route('/tools', methods=['GET', 'POST'])
def tools():
    # 调用common_tools函数
    return common_tools()
