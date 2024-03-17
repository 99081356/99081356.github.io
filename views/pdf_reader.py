import json

from flask import Flask, render_template,request
import base64
import requests
app = Flask(__name__)


@app.route('/pdf_show')
def pdf_show():
    return render_template('pdf_reader.html')  # 展示PDF的页面


# @app.route('/pdf')
# def get_pdf():
#
#     # 读取PDF文件
#     with open('激活.pdf', 'rb') as f:
#         pdf_data = f.read()
#     # 转码为base64
#     pdf_base64 = base64.b64encode(pdf_data).decode('utf-8')
#     # 返回base64字符串
#     return pdf_base64

@app.route('/remote_pdf')
def get_remote_pdf():
    # 目标URL
    url = 'http://106.15.248.252:8000/api/pdf/jh.pdf'
    # 读取PDF文件
    # 添加常见的请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    # 发送GET请求
    pdf_base64 = requests.get(url, headers=headers).content.decode('utf-8')
    json_data = json.loads(pdf_base64)['pdf_base64']
    # 返回base64字符串
    return json_data


