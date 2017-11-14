#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017 - fxlovely <fxlovely@outlook.com>

import os
from datetime import datetime
from flask import render_template, session, redirect, url_for, request, current_app, flash, send_from_directory, g

from . import main

from .. import db
from ..models import MessageDb, NewsDb, ProductDb, CaseDb
from ..email import send_email

from flask_login import login_required, current_user

from ..decorators import admin_required, super_admin_required

from .forms import MessageForm, ManageForm, ReSubmitForm
from .. import photos, videos

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('about.html')

@main.route('/news')
def news():
    return render_template('news.html', newshtml=NewsDb.query.order_by(NewsDb.NSubTime.desc()).all())

@main.route('/products')
def products():
    page = request.args.get('page', 1, type=int)
    pagination = ProductDb.query.order_by(ProductDb.id).paginate(page, per_page=6, error_out=False)
    return render_template('products.html', pagination=pagination, page=page)

@main.route('/cases')
def cases():
    page = request.args.get('page', 1, type=int)
    pagination = CaseDb.query.order_by(CaseDb.id).paginate(page, per_page=6, error_out=False)
    return render_template('cases.html', pagination=pagination, page=page)

@main.route('/details/<item>/<int:item_id>')
def details(item, item_id):
    if item == 'news':
        return render_template('details.html', news_details=NewsDb.query.get(item_id))
    elif item == 'products':
        return render_template('details.html', products_details=ProductDb.query.get(item_id))
    elif item == 'cases':
        return render_template('details.html', cases_details=CaseDb.query.get(item_id))
    else:
        abort(404)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    messageform = MessageForm()
    if messageform.validate_on_submit():
        messagedb = MessageDb(MName=messageform.name.data, MPhone=messageform.phone.data, MEmail=messageform.mail.data, MContent=messageform.content.data)
        db.session.add(messagedb)
	db.session.commit()
	flash(u'谢谢，留言已提交！')
	send_email(current_app.config['MAIL_ADMIN'], '网站新留言', current_app.config['MAIL_TEMPLATE_DIR'], messagedb=messagedb)
    return render_template('contact.html', messageform=messageform)

@main.route('/manage', methods=['GET', 'POST'])
@login_required
def manage():
    page = request.args.get('page', 1, type=int)
    if page == 1:
        img = 'NULL'
        video = 'NULL'
        manageform = ManageForm()
        if manageform.validate_on_submit():
            if manageform.item.data == 1:
                if manageform.img.data:
                    img = photos.save(manageform.img.data, name=manageform.img.data.filename)
                if manageform.video.data:
                    video = videos.save(manageform.video.data, name=manageform.video.data.filename)
                db.session.add(NewsDb(NTitle=manageform.name.data, NText=manageform.text.data, NImg=img, NVideo=video, user_id=current_user.id))
                db.session.commit()
                flash(u'新闻已添加')
            elif manageform.item.data == 2:
                if manageform.img.data:
                    img = photos.save(manageform.img.data, name=manageform.img.data.filename)
                db.session.add(ProductDb(PName=manageform.name.data, PText=manageform.text.data, PImg=img, user_id=current_user.id))
                db.session.commit()
                flash(u'产品信息已添加')
            elif manageform.item.data == 3:
                if manageform.img.data:
                    img = photos.save(manageform.img.data, name=manageform.img.data.filename)
                db.session.add(CaseDb(CName=manageform.name.data, CText=manageform.text.data, CImg=img, user_id=current_user.id))
                db.session.commit()
                flash(u'业绩信息已添加')
        return render_template('manage.html', manageform=manageform, page=page)
    elif page == 0:
        return render_template('manage.html', messagehtml=MessageDb.query.order_by(MessageDb.MSubTime.desc()).all(), \
            newshtml=NewsDb.query.order_by(NewsDb.NSubTime.desc()), producthtml=ProductDb.query.order_by(ProductDb.PSubTime.desc()), \
                casehtml=CaseDb.query.order_by(CaseDb.CSubTime.desc()), page=page)
    
@main.route('/delete/<dbname>/<items>')
@login_required
@super_admin_required
def delete(dbname, items):
    if dbname == 'MessageDb':
        message = MessageDb.query.get(items)
        db.session.delete(message)
        db.session.commit()
        flash(u'一条留言信息已删除')
        return redirect(url_for('main.manage', page=0))
    elif dbname == 'NewsDb':
        news = NewsDb.query.get(items)
        if news.NImg != 'NULL':
            os.remove(photos.path(news.NImg))
        if news.NVideo != 'NULL':
            os.remove(videos.path(news.NVideo))
        db.session.delete(news)
        db.session.commit()
        flash(u'一条新闻信息已删除')
        return redirect(url_for('main.manage', page=0))
    elif dbname == 'ProductDb':
        products = ProductDb.query.get(items)
        if products.PImg != 'NULL':
            os.remove(photos.path(products.PImg))
        db.session.delete(products)
        db.session.commit()
        flash(u'一条产品信息已删除')
        return redirect(url_for('main.manage', page=0))
    elif dbname == 'CaseDb':
        cases = CaseDb.query.get(items)
        if cases.CImg != 'NULL':
            os.remove(photos.path(cases.CImg))
        db.session.delete(cases)
        db.session.commit()
        flash(u'一条业绩信息已删除')
        return redirect(url_for('main.manage', page=0))
    else:
        abort(403)
        
@main.route('/resubmit/<dbname>/<int:items>', methods=['GET', 'POST'])
@login_required
@admin_required
def resubmit(dbname, items):
    img = 'NULL'
    video = 'NULL'
    resubform = ReSubmitForm()
    if dbname == 'NewsDb':
        news = NewsDb.query.get(items)
        if resubform.validate_on_submit():
            if resubform.img.data:
                img = photos.save(resubform.img.data, name=resubform.img.data.filename)
            if resubform.video.data:
                video = videos.save(resubform.video.data, name=resubform.video.data.filename)
            #db.session.add(NewsDb(id=items, NTitle=resubform.name.data, NText=resubform.text.data, NImg=img, NVideo=video, user_id=current_user.id))
            #NewsDb.query.filter(id==items).update({'NTitle': resubform.name.data, 'NText': resubform.text.data, 'NImg': img, 'NVideo': video, 'user_id': current_user.id})
            news.NTitle=resubform.name.data
            news.NText=resubform.text.data
            news.NImg=img
            news.NVideo=video
            news.user_id=current_user.id
            db.session.commit()
            flash(u'新闻信息已修改')
        return render_template('resubmit.html', resubform=resubform, newshtml=news)
    elif dbname == 'ProductDb':
        products = ProductDb.query.get(items)
        if resubform.validate_on_submit():
            if resubform.img.data:
                img = photos.save(resubform.img.data, name=resubform.img.data.filename)
            #db.session.add(ProductDb(id=items, PName=resubform.name.data, PText=resubform.text.data, PImg=img, user_id=current_user.id))
            products.PName=resubform.name.data
            products.PText=resubform.text.data
            products.PImg=img
            products.user_id=current_user.id
            db.session.commit()
            flash(u'产品信息已修改')
        return render_template('resubmit.html', resubform=resubform, producthtml=products)
    elif dbname == 'CaseDb':
        cases = CaseDb.query.get(items)
        if resubform.validate_on_submit():
            if resubform.img.data:
                img = photos.save(resubform.img.data, name=resubform.img.data.filename)
            #db.session.add(CaseDb(id=items, CName=resubform.name.data, CText=resubform.text.data, CImg=img, user_id=current_user.id))
            cases.CName=resubform.name.data
            cases.CText=resubform.text.data
            cases.CImg=img
            cases.user_id=current_user.id
            db.session.commit()
            flash(u'业绩信息已修改')
        return render_template('resubmit.html', resubform=resubform, casehtml=cases)
    else:
        abort(403)

'''
@main.route('/test-upload', methods = ['GET', 'POST'])
def test_upload():
    uploadform = UploadForm()
    url = None
    
    if uploadform.validate_on_submit():
        filename = form.upload.data.filename
        url = photos.save(form.upload.data, name=filename)
    return render_template('test-upload.html', uploadform=uploadform, url=url)

@main.route('/test-message', methods=['GET', 'POST'])
def test_message():
    name = None
    phone = None
    mail = None
    content = None
    messageform = MessageForm()
    
    if messageform.validate_on_submit():
        name = messageform.name.data
        phone = messageform.phone.data
        mail = messageform.mail.data
        content = messageform.content.data
    return render_template('test-message.html', messageform=messageform, name=name, phone=phone, mail=mail, content=content)

@main.route('/test-sql', methods=['GET', 'POST'])
def test_sql():
    name = None
    phone = None
    mail = None
    content = None
    messageform = MessageForm()
    
    if messageform.validate_on_submit():
        name = messageform.name.data
        phone = messageform.phone.data
        mail = messageform.mail.data
        content = messageform.content.data
        messagedb = MessageDb(name, phone, mail, content)
        db.session.add(messagedb)
	db.session.commit()
	flash('Message has been submited')
    return render_template('test-message.html', messageform=messageform, name=name, phone=phone, mail=mail, content=content, messagehtml = MessageDb.query.order_by(MessageDb.SubTime.desc()).all())

@main.route('/test-mail', methods=['GET', 'POST'])
def test_mail():
    name = None
    phone = None
    mail = None
    content = None
    messageform = MessageForm()
    
    if messageform.validate_on_submit():
        name = messageform.name.data
        phone = messageform.phone.data
        mail = messageform.mail.data
        content = messageform.content.data
        messagedb = MessageDb(name, phone, mail, content)
        db.session.add(messagedb)
	db.session.commit()
	flash('Message has been submited')
	send_email(current_app.config['MAIL_ADMIN'], '新留言', current_app.config['MAIL_TEMPLATE_DIR'], messagedb=messagedb)
    return render_template('test-message.html', messageform=messageform, name=name, phone=phone, mail=mail, content=content, messagehtml = MessageDb.query.order_by(MessageDb.SubTime.desc()).all())
'''
