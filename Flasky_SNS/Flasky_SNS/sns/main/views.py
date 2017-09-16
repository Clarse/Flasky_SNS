#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/4/17
from flask import session, flash, render_template, redirect, url_for
from datetime import datetime
from .forms import NameForm
from sns import db
from ..models import User, Role
from . import main


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    name = session.get('name')
    if form.validate_on_submit():
        users = User.query.filter_by(username=form.name.data).first()
        if users is None:
            session['know'] = False
            flash('You are not already in our system. Please sign in!')
            # if app.config['FLASKY_ADMIN']:
            #     send_email(app.config['FLASKY_ADMIN'], 'New User', 'mail/new_user', user=users)
        else:
            session['know'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('.user'))
    return render_template('index.html', current_time=datetime.utcnow(), form=form, name=name)


@main.route('/count/<numb>')
def count(numb):
    numb = int(numb)
    numb = [i for i in range(numb)]
    print(numb)
    return render_template('count.html', numb=numb)


@main.route('/usr')
def user():
    return render_template('user.html', name=session.get('name'), known=session.get('know', False))