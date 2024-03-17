from flask import Blueprint, request, render_template
from views.blog_views import index, post, new_post, edit_post, delete_post
from views.common_tools import key_word_check, text_cmp
from views.tag_control import tags_show,new_tag, edit_tag, delete_tag
from views.pdf_reader import pdf_show,get_remote_pdf
from es.es import search

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
@blog_controller.route('/keyword_check_tool', methods=['GET', 'POST'])
def keyword_check_tool():
    # 调用common_tools函数
    return key_word_check()


@blog_controller.route('/text_cmp_tool', methods=['GET', 'POST'])
def text_cmp_tool():
    # 调用common_tools函数
    return text_cmp()


@blog_controller.route('/tags_show', methods=['GET', 'POST'])
def tags_show_page():
    # 调用common_tools函数
    return tags_show()

# 定义编辑文章页的路由，支持GET和POST请求，post_id为文章的id
@blog_controller.route('/new_tag', methods=['GET', 'POST'])
def new_tag_page():
    # 调用edit_post函数，传入post_id
    return new_tag()



# 定义编辑文章页的路由，支持GET和POST请求，post_id为文章的id
@blog_controller.route('/edit_tag/<int:tag_id>', methods=['GET', 'POST'])
def edit_tag_page(tag_id):
    # 调用edit_post函数，传入post_id
    return edit_tag(tag_id)


# 定义删除文章页的路由，支持GET和POST请求，post_id为文章的id
@blog_controller.route('/delete_tag/<int:tag_id>', methods=['GET', 'POST'])
def delete_tag_page(tag_id):
    # 调用delete_post函数，传入post_id
    return delete_tag(tag_id)


@blog_controller.route('/search', methods=['GET', 'POST'])
def es_search():
    # 调用new_post函数
    return search()

@blog_controller.route('/pdf', methods=['GET', 'POST'])
def pdf():
    # 调用new_post函数
    return pdf_show()

@blog_controller.route('/remote_pdf', methods=['GET', 'POST'])
def get_pdf():
    # 调用new_post函数
    return get_remote_pdf()