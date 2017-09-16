#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/4/17
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'inc<STDIO.H>=-04'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    FLAKSY_MAIL_SUBJECT_PREFIX = '[Flasky]'
    FLASKY_MAIL_SENDER = 'Flasky Admin<bloodyevo@163.com>'
    FLAKSY_ADMIN = os.environ.get('FLASKY_ADMIN') or 'Flasky Admin'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'bloodyevo@163.com'
    MAIL_PASSWORD = 'Asdf123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or (
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite'))


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URL = os.environ.get('TEST_DATABASE_URL') or (
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')
    )


class ProducingConfig(Config):
    SQLALCHEMY_DATABASE_URL = os.environ.get('Producing_DATABASE_URL') or (
        'sqlite:///' + os.path.join(basedir, 'date-pro.sqlite')
    )


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'Producing': ProducingConfig,

    'default': DevelopmentConfig
}
