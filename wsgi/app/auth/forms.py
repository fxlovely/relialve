#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, BooleanField, SelectField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),Email()])
    password = PasswordField(u'密码', validators=[Required()])
    remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')
    
class RelialveForm(FlaskForm):
    username = StringField(u'用户名', validators=[Required()])
    email = StringField(u'电子邮件', validators=[Required(), Length(1, 64),Email()])
    password = PasswordField(u'初始密码', validators=[Required()])
    role_id = SelectField(u'角色', choices = [(1, u'员工'), (7, u'管理员'), (9, u'超级管理员')], coerce=int)
    submit = SubmitField(u'注册')
    
    def validate_email(self, field):
        if User.query.filter_by(Username=field.data).first():
            raise ValidationError('Email already registered')
        
    def validate_username(self,field):
        if User.query.filter_by(Username=field.data).first():
            raise ValidationError('Username already in use')

class PwdForm(FlaskForm):
    old_pwd = PasswordField(u'原密码', validators=[Required()])
    new_pwd = PasswordField(u'新密码', validators=[Required()])
    c_new_pwd = PasswordField(u'确认密码', validators=[Required(), EqualTo('new_pwd', message='Passwords must match.')])
    submit = SubmitField(u'确认修改')
