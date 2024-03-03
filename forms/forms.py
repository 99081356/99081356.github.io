from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


# 定义一个PostForm类，继承FlaskForm和CSRFProtect
class PostForm(FlaskForm, CSRFProtect):
    # 定义一个title字段，类型为StringField，必填
    title = StringField('标题', validators=[DataRequired()])
    # 定义一个content字段，类型为TextAreaField，必填
    content = TextAreaField('内容', validators=[DataRequired()])
    # 定义一个tags字段，类型为StringField
    tags = StringField('标签')
    # 定义一个submit字段，类型为SubmitField
    submit = SubmitField('提交')


# 定义一个checkForm类，继承FlaskForm和CSRFProtect
class checkForm(FlaskForm, CSRFProtect):
    # # 定义wor文件输入框
    # word_file = FileField('wor文件')
    # # 定义pdf文件输入框
    # pdf_file = FileField('pdf文件')
    # 定义文本输入框
    text_to_check = TextAreaField('待检查文本', validators=[DataRequired()])
    # 定义一个content字段，类型为TextAreaField，必填
    key_words = TextAreaField('关键词', validators=[DataRequired()])
    # 定义一个submit字段，类型为SubmitField
    submit = SubmitField('提交')


# 定义一个textCmpForm类，继承FlaskForm和CSRFProtect
class textCmpForm(FlaskForm, CSRFProtect):
    # 原始
    text_orgin = TextAreaField('原始文字', validators=[DataRequired()])
    # 对比
    text_cmp = TextAreaField('对比文字', validators=[DataRequired()])
    # 定义一个submit字段，类型为SubmitField
    submit = SubmitField('提交')

# 定义标签Form类，继承FlaskForm和CSRFProtect
class TagForm(FlaskForm, CSRFProtect):
    # 定义一个title字段，类型为StringField，必填
    name = StringField('标签名称', validators=[DataRequired()])
    # 定义一个submit字段，类型为SubmitField
    submit = SubmitField('提交')


class SearchForm(FlaskForm, CSRFProtect):
    # 定义一个title字段，类型为StringField，必填
    keyword = StringField('关键词', validators=[DataRequired()])
    # 定义一个submit字段，类型为SubmitField
    submit = SubmitField('搜索')