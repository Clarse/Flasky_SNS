#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/4/17
from flask import Blueprint

main = Blueprint('main', __name__)


from . import errors, views
