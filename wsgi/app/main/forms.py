#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


from .. import photos, videos

'''
class UploadForm(FlaskForm):

    #一个简单的上传表单
    # 文件field设置为‘必须的’，过滤规则设置为‘photos’
    upload = FileField('image:', validators=[FileRequired(), FileAllowed(photos, 'you can upload images only!')])
    submit = SubmitField('ok')
'''

class MessageForm(FlaskForm):
    name = StringField(u'姓名', validators=[DataRequired()])
    phone = StringField(u'手机', validators=[DataRequired()])
    mail = StringField(u'邮件', validators=[DataRequired()])
    content = StringField(u'内容', validators=[DataRequired()])
    submit = SubmitField(u'提交')

class ManageForm(FlaskForm):
    item = SelectField(u'管理项目', choices = [(1, u'新闻'), (2, u'产品'), (3, u'业绩')], coerce=int)
    name = StringField(u'标题', validators=[DataRequired()])
    text = StringField(u'内容', validators=[DataRequired()])
    img = FileField(u'图片', validators=[FileAllowed(photos, 'you can upload images only!')])
    video = FileField(u'视频', validators=[FileAllowed(videos, 'you can upload videos only!')])
    submit = SubmitField(u'提交')
    
class ReSubmitForm(FlaskForm):
    name = StringField(u'标题', validators=[DataRequired()])
    text = StringField(u'内容', validators=[DataRequired()])
    img = FileField(u'图片', validators=[FileAllowed(photos, 'you can upload images only!')])
    video = FileField(u'视频', validators=[FileAllowed(videos, 'you can upload videos only!')])
    submit = SubmitField(u'确认修改')
