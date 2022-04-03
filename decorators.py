#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from functools import wraps
from flask import redirect, url_for, session, flash

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'tgid' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return redirect(url_for('login'))

    return wrap