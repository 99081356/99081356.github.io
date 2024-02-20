from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired
from flask_flatpages import FlatPages
from markdown import markdown


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
    # 定义一个title字段，类型为StringField，必填
    file = FileField('文件', validators=[DataRequired()])
    # 定义一个content字段，类型为TextAreaField，必填
    key_word = TextAreaField('关键词', validators=[DataRequired()])
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
