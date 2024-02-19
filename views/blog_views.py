from flask import request, redirect, url_for, render_template, flash, jsonify, json
from models.blog import Post, db, Tag
from markdown2 import Markdown
from flask_login import current_user, login_required
from forms.forms import PostForm, checkForm
from markdown import markdown
import re
from docx import Document

# 创建Markdown对象
markdown_converter = Markdown()


# 定义首页路由，展示所有博客文章
def index():
    posts = Post.query.all()
    # 统计所有标签的频率
    all_tags = [tag for post in list(posts) for tag in post.tags]
    # 使用一个字典来存储每个标签的频率
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
    return render_template('blog_index.html', posts=posts, tags=json_tags)


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


# 定义常用工具路由
# 定义常用工具路由
def common_tools():
    form = checkForm()

    if form.validate_on_submit():
        # 创建一篇文章
        if request.method == 'POST':
            # 如果请求中没有文件部分

            # 获取文件
            file = form.file.data
            # if file not in request.files:
            #     # 返回首页模板，并传递消息
            #     return render_template('tools.html', form=form, message='No file part')
            # 如果文件名称为空
            if file.name == '':
                # 返回首页模板，并传递消息
                return render_template('tools.html', form=form, message='未上传文件！')
            # 如果文件存在
            if file:
                # 获取要搜索的图表号
                figure_number_to_search = form.key_word.data
                keyword = re.split(r'\r\n', figure_number_to_search)
                # 如果图表号为空
                if not figure_number_to_search:
                    # 返回首页模板，并传递消息
                    return render_template('tools.html', form=form, message='请输入需要检索的词！')
                # 创建文档对象
                doc = Document(file)
                message = []
                matches = []
                results = []
                details = []
                # 遍历文档中的每个段落，如果keyword命中，则返回message没有问题，如果有未命中的keyword，则指出哪个keyword没有命中
                for key_word in keyword:
                    # 初始化出现次数
                    occurrences = 0
                    if key_word:
                        # 遍历文档段落
                        for para_index, para in enumerate(doc.paragraphs):
                            # 如果图表号在段落文本中
                            if key_word in para.text:
                                # 累加出现次数
                                occurrences += para.text.count(key_word)
                                # 获取段落中的字符索引
                                start_char = para.text.find(key_word)
                                # 记录匹配项的位置信息
                                matches.append({
                                    '段落': para_index + 1,  # 段落编号，从1开始
                                    '开始字符': start_char + 1,  # 开始字符索引
                                    '结束字符': start_char + len(keyword)  # 结束字符索引
                                })

                        if occurrences == 0:
                            results.append(key_word)
                            details.append(f"关键词：'{key_word}'在文中未出现！")
                        else:
                            details.append(f"关键词：'{key_word}'在文中出现 {occurrences} 次，具体出现位置为：{matches}。")
                            matches.clear()
                if len(results) == 0:
                    message.append("结论：说明书附图和附图中的图号一一对应！")
                else:
                    message.append(f"结论：说明书附图和附图中的图号无法一一对应，存在问题的附图图号为:'{results}'！")
                    # 返回首页模板，并传递消息
                return render_template('tools.html', form=form, message=message, details=details, title='常用工具')
    return render_template('tools.html', form=form, title='常用工具')
