from flask import request, redirect, url_for, render_template, flash, jsonify, json
from models.blog import Post, db, Tag
from markdown2 import Markdown
from flask_login import current_user, login_required
from forms.forms import PostForm, checkForm, textCmpForm
from markdown import markdown
import re
from docx import Document
from difflib import HtmlDiff


# 定义常用工具路由
def file_cmp():
    form = checkForm()

    if form.validate_on_submit():
        # 创建一篇文章
        if request.method == 'POST':
            # 如果请求中没有文件部分

            # 获取文件
            file = form.file.data
            # if file not in request.files:
            #     # 返回首页模板，并传递消息
            #     return render_template('file_cmp_tool.html', form=form, message='No file part')
            # 如果文件名称为空
            if file.name == '':
                # 返回首页模板，并传递消息
                return render_template('file_cmp_tool.html', form=form, message='未上传文件！')
            # 如果文件存在
            if file:
                # 获取要搜索的图表号
                figure_number_to_search = form.key_word.data
                keyword = re.split(r'\r\n', figure_number_to_search)
                # 如果图表号为空
                if not figure_number_to_search:
                    # 返回首页模板，并传递消息
                    return render_template('file_cmp_tool.html', form=form, message='请输入需要检索的词！')
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
                return render_template('file_cmp_tool.html', form=form, message=message, details=details,
                                       title='常用工具')
    return render_template('file_cmp_tool.html', form=form, title='常用工具')


# import fitz  # PyMuPDF
# import re
# # 打开PDF文件
# pdf_path = "X波段宽频带圆极化阵列天线研究（终稿）.pdf"
# pdf_document = fitz.open(pdf_path)
#
# # 关键字列表
# keywords = ["李晋琳", "X波段"]
#
# pattern = re.compile(r'图\s*\d+\.?\d*')
#
# results = []
# # 正则表达式模式
# # 遍历PDF中的每一页
# for page_number in range(len(pdf_document)):
#     page = pdf_document[page_number]
#     text = page.get_text()
#     metches = pattern.findall(text)
#     for metch in metches:
#         if metch not in results:
#             results.append(metch)
#     # # 遍历每个关键字
#     # for keyword in keywords:
#     #     # 搜索关键字
#     #     text_instances = page.search_for(keyword)
#     #     # 遍历找到的关键字实例
#     #     for inst in text_instances:
#     #         # 去重查找结果
#     #         # 创建一个矩形区域来高亮关键字
#     #         highlight = page.add_highlight_annot(inst)
#     #         # 设置高亮的颜色，这里使用红色
#     #         highlight.set_colors({'stroke': (1, 0, 0)})
#     #         highlight.update()
#     #         break  # 只高亮第一个实例，然后跳出循环
#
# # 保存修改后的PDF文件
# pdf_document.saveIncr()
#
# pdf_document.close()
#
# # # 遍历PDF中的每一页
# # for page_number in range(len(pdf_document)):
# #     page = pdf_document[page_number]
# #     # 获取页面上的所有注释
# #     annots = page.annots()
# #     # 遍历所有注释
# #     for annot in annots:
# #         # 检查注释类型是否为高亮
# #         if annot.type == 8:  # 2 是高亮注释的类型代码
# #             # 删除高亮注释
# #             page.removeAnnot(annot)
# # # 保存修改后的PDF文件
# # pdf_document.saveIncr()
# # pdf_document.close()


def text_cmp():
    form = textCmpForm()
    diff_result = None
    if form.validate_on_submit():
        # 创建一篇文章
        if request.method == 'POST':
            # 获取原始文本
            text_orgin = form.text_orgin.data
            # 获取对比文本
            text_cmp = form.text_cmp.data
            diff_result = HtmlDiff().make_file(text_orgin.splitlines(), text_cmp.splitlines(), context=True)
            # 如果原始文本与对比文本不一致
            return render_template('text_cmp_tool.html', diff_result=diff_result, form=form)
    return render_template('text_cmp_tool.html', diff_result=diff_result, form=form)
