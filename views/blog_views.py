from flask import request, redirect, url_for, render_template, flash, json
from flask_paginate import Pagination, get_page_parameter
from markdown2 import Markdown

from es.es import sync_data_to_es, search
from forms.forms import PostForm, SearchForm
from models.blog import Post, db, Tag

# 创建Markdown对象
markdown_converter = Markdown()


# 定义首页路由，展示所有博客文章
def index():
    # sync_data_to_es()
    per_page = 10  # 每页显示10条记录
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page

    get_posts = Post.query.all()
    posts = get_posts[start:end]
    # 计算总页数
    total = len(get_posts)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    # return render_template('index.html', data=current_data, pagination=pagination, page=page)
    # 统计所有标签的频率
    all_tags = [tag for post in list(posts) for tag in post.tags]
    # 使用字典来存储每个标签的频率
    tags_freq = {}
    for tag in all_tags:
        if tag in tags_freq:
            tags_freq[tag] += 1
        else:
            tags_freq[tag] = 1
    # 对字典进行排序，以便按频率显示标签
    # sorted_tags = sorted(tag_freq.items(), key=lambda x: x[1], reverse=True)
    array_tags = []
    for tag in tags_freq:
        tag_name = tag.name
        tag_freq = tags_freq[tag]
        array_tags.append({"tag_name": tag_name, "tag_freq": tag_freq})
    json_tags = json.dumps(array_tags)
    return render_template('blog_index.html', posts=posts, tags=json_tags, pagination=pagination, page=page)


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
