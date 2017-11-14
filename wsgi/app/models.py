#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from markdown import markdown
#import bleach
from flask import current_app, request, url_for
from flask_login import UserMixin, AnonymousUserMixin
#from app.exceptions import ValidationError
from . import db, login_manager

'''
class Relialve(UserMixin, db.Model):
    __tablename__ = 'relialve'
    id = db.Column(db.Integer, primary_key=True)
    Email = db.Column(db.String(64), unique=True, index=True)
    Username = db.Column(db.String(64), unique=True, index=True)
    Password_Hash = db.Column(db.String(128))
    
    def verify_password(self, Password):
        return check_password_hash(self.Password_Hash, Password)
    
    def Password(self, Password):
        self.Password_Hash = generate_password_hash(Password)
    
    def __repr__(self):
        return '<User %r>' % (self.Username)
'''

def Check_Pass(pWd):
    PassHash = generate_password_hash('fxlovely0415')
    return check_password_hash(PassHash, pWd)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column('User_id', db.Integer, primary_key=True)
    Email = db.Column(db.String(64), unique=True, index=True)
    Username = db.Column(db.String(64), unique=True, index=True)
    Password_Hash = db.Column(db.String(128))
    Role_id = db.Column(db.Integer)
    Registered_on = db.Column(db.DateTime, default=datetime.utcnow)
    news = db.relationship('NewsDb', backref='user', lazy='dynamic')
    products = db.relationship('ProductDb', backref='user', lazy='dynamic')
    cases = db.relationship('CaseDb', backref='user', lazy='dynamic')
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    @property
    def Password(self):
        raise AttributeError('password is not a readable attribute')

    @Password.setter
    def Password(self, Password):
        self.Password_Hash = generate_password_hash(Password)

    def verify_password(self, Password):
        return check_password_hash(self.Password_Hash, Password)
    
    def __repr__(self):
        return '<User %r>' % (self.Username)
    
@login_manager.user_loader
###加载用户的回调函数接收以Unicode字符串形式表示的用户标示符
###如果能找到用户，这个函数必须返回用户对象，否则返回None。
def load_user(User_id):
    return User.query.get(int(User_id))

class MessageDb(db.Model):
    __tablename__ = 'messages'
    id = db.Column('Message_id', db.Integer, primary_key=True)
    MName = db.Column(db.String(60), unique=True, index=True)
    MPhone = db.Column(db.String(60))
    MEmail = db.Column(db.String)
    MContent = db.Column(db.String)
    MSubTime = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, **kwargs):
        super(MessageDb, self).__init__(**kwargs)
        
    def __repr__(self):
        return '<MessageDb %r>' % (self.MName)
        
class ProductDb(db.Model):
    __tablename__ = 'products'
    id = db.Column('Product_id', db.Integer, primary_key=True)
    PName = db.Column(db.String(60), unique=True, index=True)
    PText = db.Column(db.String)
    PImg = db.Column(db.String)
    PSubTime = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.User_id'))
    
    def __init__(self, **kwargs):
        super(ProductDb, self).__init__(**kwargs)
        
    def __repr__(self):
        return '<ProductDb %r>' % (self.PName)
    
class NewsDb(db.Model):
    __tablename__ = 'news'
    id = db.Column('News_id', db.Integer, primary_key=True)
    NTitle = db.Column(db.String(60), unique=True, index=True)
    NText = db.Column(db.String)
    NImg = db.Column(db.String)
    NVideo = db.Column(db.String)
    NSubTime = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.User_id'))
    
    def __init__(self, **kwargs):
        super(NewsDb, self).__init__(**kwargs)
        
    def __repr__(self):
        return '<NewsDb %r>' % (self.NTitle)
    
class CaseDb(db.Model):
    __tablename__ = 'cases'
    id = db.Column('Case_id', db.Integer, primary_key=True)
    CName = db.Column(db.String(60), unique=True, index=True)
    CText = db.Column(db.String)
    CImg = db.Column(db.String)
    CSubTime = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.User_id'))
    
    def __init__(self, **kwargs):
        super(CaseDb, self).__init__(**kwargs)
    
    def __repr__(self):
        return '<CaseDb %r>' % (self.CName)
