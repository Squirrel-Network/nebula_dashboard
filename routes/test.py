#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, render_template,request, session, url_for, redirect
from decorators import login_required
from database.repository.users import UsersRepository
from database.repository.groups import GroupsRepository

route_test = Blueprint('route_test', __name__)

@route_test.route('/test', methods=['GET', 'POST'])
@login_required
def test():
	tg_id = int(session['tgid'])
	get_owners = UsersRepository().getOwnerById(tg_id)
	get_article = GroupsRepository().get_article()
	title = request.form.get('title')
	lang = request.form.get('lang')
	a = request.form.get('valore_editor')
	if request.method == 'GET':
		return render_template("test.html", owner = get_owners, data=get_article)
	if request.method == 'POST':
		if a is not None:
			data = [(title.lower(), lang, a)]
			GroupsRepository().insert_article(data)
		return redirect(url_for('route_test.test'))
