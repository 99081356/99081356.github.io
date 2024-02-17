from flask import Blueprint, request, render_template
from views.blog_views import index, post, new_post, edit_post, delete_post

blog_controller = Blueprint('blog_controller', __name__)


@blog_controller.route('/')
def blog_index():
    return index()


@blog_controller.route('/<int:post_id>')
def blog_post(post_id):
    return post(post_id)


@blog_controller.route('/new_post', methods=['GET', 'POST'])
def new_post_page():
    return new_post()


@blog_controller.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post_page(post_id):
    return edit_post(post_id)


@blog_controller.route('/delete_post/<int:post_id>', methods=['GET', 'POST'])
def delete_post_page(post_id):
    return delete_post(post_id)
