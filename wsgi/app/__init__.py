#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_mail import Mail
from flask_login import LoginManager
from config import Config


bootstrap = Bootstrap()
db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'basic'
login_manager.login_view = 'auth.login'
photos = UploadSet('photos')
videos = UploadSet('videos')

from .models import *
    
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Config.init_app(app)
    
    bootstrap.init_app(app)
    db.app = app
    db.init_app(app)
    #from .models import *
    db.create_all()
    
    mail.init_app(app)
    
    login_manager.init_app(app)

    configure_uploads(app, photos)
    configure_uploads(app, videos)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    return app
