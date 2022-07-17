#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, render_template,request
from decorators import login_required

route_test = Blueprint('route_test', __name__)

@route_test.route('/test', methods=['GET', 'POST'])
@login_required
def test():
	a = request.form.get('valore_editor')
	print(a)
	return render_template("test.html")
