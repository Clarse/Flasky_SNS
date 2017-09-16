#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/12/17
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class NameForm(FlaskForm):
    name = StringField('what\'s your name?', validators=[DataRequired()])
    submit = SubmitField('submit')
