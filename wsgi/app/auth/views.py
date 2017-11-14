#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

from flask import render_template, redirect, request, url_for, flash, abort, g
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import User, Check_Pass
from ..email import send_email
from .forms import LoginForm, RelialveForm, PwdForm

@auth.route('/login', methods=['GET', 'POST'])
def login():
    authform = LoginForm()
    if authform.validate_on_submit():
        user = User.query.filter_by(Email=authform.email.data).first()
        if user is not None and user.verify_password(authform.password.data):
            login_user(user, authform.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', authform=authform)

@auth.route('/relialve/<PaSS>', methods=['GET', 'POST'])
def relialve(PaSS):
    relialveform = RelialveForm()
    if Check_Pass(PaSS):
        if relialveform.validate_on_submit():
            user = User(Email=relialveform.email.data, Username=relialveform.username.data, Password=relialveform.password.data, Role_id=relialveform.role_id.data)
            db.session.add(user)
            db.session.commit()
            flash(u'用户注册成功')
        return render_template('auth/relialve.html', relialveform=relialveform)
    abort(404)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route('/pwd/<int:user_id>', methods=['GET', 'POST'])
@login_required
def pwd(user_id):
    user = User.query.get(user_id)
    pwdform = PwdForm()
    if pwdform.validate_on_submit():
        if user.verify_password(pwdform.old_pwd.data):
            user.Password = pwdform.new_pwd.data
            db.session.commit()
            flash(u'密码修改成功')
        else:
            flash(u'原密码错误')
    return render_template('auth/pwd.html', pwdform=pwdform, user=user)
    
