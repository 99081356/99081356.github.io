from flask import request, redirect, url_for, render_template, flash
from flask_paginate import Pagination, get_page_parameter

from forms.forms import TagForm
from models.blog import db, Tag


def tags_show():
    per_page = 10  # 每页显示10条记录
    page = request.args.get(get_page_parameter(), type=int, default=1)
    start = (page - 1) * per_page
    end = start + per_page

    get_tags = Tag.query.all()
    tags = get_tags[start:end]
    # 计算总页数
    total = len(get_tags)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')
    return render_template('tags_show.html', tags=tags, pagination=pagination, page=page)


def new_tag():
    form = TagForm()
    # 如果表单提交成功
    if form.validate_on_submit():
        # 创建一个标签
        tag = Tag(name=form.name.data)
        # 添加到数据库
        db.session.add(tag)
        db.session.commit()
        # 提示信息
        flash('你的标签已添加！')
        # 重定向到首页
        return redirect(url_for('blog_controller.tags_show_page'))
    return render_template('new_tag.html', title='创建标签', form=form)


# 定义编辑标签路由，编辑标签
def edit_tag(tag_id):
    # 根据tag_id获取tag
    tag = Tag.query.get_or_404(tag_id)
    # 获取博客表单
    form = TagForm(obj=tag)
    # 如果表单提交成功
    if form.validate_on_submit():
        # 更新标签名称
        tag.name = form.name.data
        db.session.commit()
        # 提示信息
        flash('你的标签已更新！')
        # 重定向到首页
        return redirect(url_for('blog_controller.tags_show_page'))
    return render_template('edit_tags.html', title='编辑标签', form=form, tag=tag)


# 定义删除标签路由，删除标签
def delete_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)
    # 从数据库删除
    db.session.delete(tag)
    db.session.commit()
    # 提示信息
    flash('你的标签已删除！')
    # 重定向到首页
    return redirect(url_for('blog_controller.tags_show_page'))
