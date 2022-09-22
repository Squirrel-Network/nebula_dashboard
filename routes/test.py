#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, render_template,request, session
from decorators import login_required
from database.repository.users import UsersRepository
from database.repository.groups import GroupsRepository

route_test = Blueprint('route_test', __name__)

@route_test.route('/test', methods=['GET', 'POST'])
@login_required
def test():
	tg_id = int(session['tgid'])
	get_owners = UsersRepository().getOwnerById(tg_id)
	lang = request.form.get('lang')
	a = request.form.get('valore_editor')
	if a is not None:
		data = [(lang,a)]
		GroupsRepository().insert_article(data)
	return render_template("test.html", owner = get_owners)
