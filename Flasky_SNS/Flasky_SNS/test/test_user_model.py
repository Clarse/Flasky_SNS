#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by evo on 8/12/17
import unittest
from sns import create_app, db
from sns.models import User


class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_setter(self):
        u = User(password='cat')
        self.assertFalse(u.password is None)

    def test_password_getter(self):
        u = User(password='cat')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='cat')
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('ohters'))

    def test_password_salts_are_random(self):
        u = User(password='cat')
        u2 = User(password='dog')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_valid_confirmation_token(self):
        u = User(password='cat')
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertTrue(u.confirm(token))

    def test_invalid_confirmation_token(self):
        u = User(password = 'cat')
        u2 = User(password = 'dog')
        db.session.add(u)
        db.session.add(u2)
        db.session.commit()
        token = u.generate_confirmation_token()
        self.assertFalse(u2.confirm(token))