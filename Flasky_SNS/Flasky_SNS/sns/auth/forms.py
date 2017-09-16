#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/28/17
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 64)])
    remember_me = BooleanField('Keep me login')
    submit_field = SubmitField('Login')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 24), Regexp(
            '^[A-Za-z][A-za-z0-9_.]*$', 0,
            'Usernames must have only letters, '
            'numbers, dots or underscores.')])
    password = PasswordField('Password', validators=[
        DataRequired(), Length(6, 18), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), Length(6, 18)])
    submit_field = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email address already in use')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use.')


class ChangePasswordForm(FlaskForm):
    oldpassword = PasswordField('Old Password', validators=[DataRequired(), Length(6, 18)])
    newpassword = PasswordField('New Password', validators=[
        DataRequired(), Length(6, 18), EqualTo('newpassword2', message='Password must match.')])
    newpassword2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 18)])
    submit_field = SubmitField('Confirm')


class PasswordResetReuquestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])

    submit = SubmitField('Reset Password')


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(1, 64)])

    password = PasswordField('New Password', validators=[
        DataRequired(), Length(6, 18), EqualTo('password2', message='Password must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(6, 18)])
    submit = SubmitField('Reset Password')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown Email Address')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Update Email Address')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already in use')
