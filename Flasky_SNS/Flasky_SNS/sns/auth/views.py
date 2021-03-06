#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/14/17
from flask import render_template, flash, redirect, url_for, request, session
from . import auth
from ..models import User, Role
from .. import db
from flask_login import login_user, login_required, logout_user
from .forms import *
from ..mails import send_mail
from flask_login import current_user


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint[:5] != 'auth.' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = None
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/secret')
@login_required
def secret():
    return 'Only authenticated users are allowed'


@auth.route('/register', methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data,
                    role_id=Role.query.filter_by(name='User').first().id)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_mail(user.email, 'Confirm Your Account', 'auth/email/confirm', user=user, token=token)
        flash('An confirmation email has been sent to you by email.')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm/<token>', methods=['POST', 'GET'])
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired')
    return redirect(url_for('main.index'))


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, 'Confirm Your Account', 'auth/email/confirm', user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email')
    return redirect(url_for('main.index'))


@auth.route('/change-password', methods=['POST', 'GET'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.oldpwd.data):
            current_user.password = form.newpwd.data
            db.session.add(current_user)
            flash('Your password has been updated')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid Password')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['POST', 'GET'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetReuquestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generet_reset_token()
            send_mail(user.email, 'Reset Your Password', 'auth/email/reset_password',
                      user=user,
                      token=token,
                      next=request.args.get('next'))
            flash('An email with instructions to reset your password has been sent to you')
            return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['POST', 'GET'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change-email', methods=['POST', 'GET'])
@login_required
def change_email_request():
    form = ChangeEmailForm
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generet_change_email_token(new_email)
            send_mail(new_email, 'Confirm Your Email Address',
                      'auth/mail/change_email', user=current_user,
                      token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to your new email address.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
        return render_template('auth/change_email.html')


@auth.route('/change-email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Your email address has already been changed')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))
