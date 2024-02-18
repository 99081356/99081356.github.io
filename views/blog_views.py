from flask import request, redirect, url_for, render_template, flash
from models.blog import Post, db, Tag
from markdown2 import Markdown
from flask_login import current_user, login_required
from forms.forms import PostForm
from markdown import markdown

# 创建Markdown对象
markdown_converter = Markdown()


# 定义首页路由，展示所有博客文章
def index():
    posts = Post.query.all()
    return render_template('blog_index.html', posts=posts)


# 定义文章路由，根据文章id展示单篇文章
def post(post_id):
    post = Post.query.get_or_404(post_id)
    # 将文章内容转换为Markdown格式
    post.content = markdown_converter.convert(post.content)
    return render_template('blog_post.html', post=post)


# 定义新建文章路由，新建一篇文章
def new_post():
    form = PostForm()
    tags = Tag.query.all()
    tags_selected = request.form.getlist('tags')
    # 如果表单提交成功
    if form.validate_on_submit():
        # 创建一篇文章
        post = Post(title=form.title.data, content=form.content.data)
        for tag_id in tags_selected:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)
        # 添加到数据库
        db.session.add(post)
        db.session.commit()
        # 提示信息
        flash('你的博客已发布！')
        # 重定向到首页
        return redirect(url_for('blog_controller.blog_index'))
    return render_template('new_post.html', title='创建博客', form=form, post=form.data, tags=tags)


# 定义编辑文章路由，编辑一篇文章
def edit_post(post_id):
    # 根据post_id获取博客
    post = Post.query.get_or_404(post_id)
    # 获取博客表单
    form = PostForm(obj=post)
    # 获取标签
    tags = Tag.query.all()
    # 获取选中的标签
    tags_selected = request.form.getlist('tags')
    # 如果表单提交成功
    if form.validate_on_submit():
        # 更新博客标题和内容
        post.title = form.title.data
        post.content = form.content.data
        # 移除博客原有的标签
        for tag in tags:
            if tag in post.tags:
                post.tags.remove(tag)
                # 更新数据库
                db.session.commit()
        # 添加新的标签
        for tag_id in tags_selected:
            tag = Tag.query.get(tag_id)
            post.tags.append(tag)
            # 更新数据库
            db.session.commit()

        # 提示信息
        flash('你的博客已更新！')
        # 重定向到首页
        return redirect(url_for('blog_controller.blog_index'))
    return render_template('edit_post.html', title='编辑博客', form=form, post=post, tags=tags)


# 定义删除文章路由，删除一篇文章
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    # 从数据库删除
    db.session.delete(post)
    db.session.commit()
    # 提示信息
    flash('你的博客已删除！')
    # 重定向到首页
    return redirect(url_for('blog_controller.blog_index'))
