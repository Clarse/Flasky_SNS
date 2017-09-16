#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/4/17
from flask import render_template
from . import main


@main.errorhandler(404)
def page_not_found(e):
    render_template('404.html'), 404


@main.errorhandler(500)
def internal_server_error(e):
    render_template('500.html'), 500
