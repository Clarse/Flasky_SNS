#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/14/17
from flask import Blueprint


auth = Blueprint('auth', __name__)


from . import views
