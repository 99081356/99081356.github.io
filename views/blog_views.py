from flask import request, redirect, url_for, render_template, flash
from models.blog import Post, db
from markdown2 import Markdown
from flask_login import current_user, login_required
from forms.forms import PostForm
from markdown import markdown

markdown_converter = Markdown()


def index():
    posts = Post.query.all()
    return render_template('blog_index.html', posts=posts)


def post(post_id):
    post = Post.query.get_or_404(post_id)
    post.content = markdown_converter.convert(post.content)
    return render_template('blog_post.html', post=post)


def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data)
        db.session.add(post)
        db.session.commit()
        flash('你的博客已发布！')
        return redirect(url_for('blog_controller.blog_index'))
    return render_template('new_post.html', title='创建博客', form=form, post=form.data)


def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('你的博客已更新！')
        return redirect(url_for('blog_controller.blog_index'))
    return render_template('edit_post.html', title='编辑博客', form=form, post=post)


def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('你的博客已删除！')
    return redirect(url_for('blog_controller.blog_index'))
