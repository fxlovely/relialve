#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>


import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, '/migrations/db_repository')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    UPLOADED_PHOTOS_DEST = os.environ.get('OPENSHIFT_DATA_DIR') + 'uploads'
    UPLOADED_PHOTOS_ALLOW = tuple('jpg jpe jpeg png gif svg bmp IMG JPG PNG'.split())
    UPLOADED_VIDEOS_DEST = os.environ['OPENSHIFT_DATA_DIR'] + 'uploads'
    UPLOADED_VIDEOS_ALLOW = tuple('mp4 MP4 mov MOV'.split())
    
    
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'fxlovely@outlook.com'
    MAIL_PASSWORD = 'relialve1024'
    MAIL_SENDER = 'fxlovely<fxlovely@outlook.com>'
    MAIL_SUBJECT_PREFIX = '[Relialve]'
    MAIL_ADMIN = 'xye@rlb-v.com'
    MAIL_TEMPLATE_DIR = '/mail/send_mail'
    
    @staticmethod
    def init_app(app):
        pass
