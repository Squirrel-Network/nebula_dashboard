#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
import os
from flask import Blueprint, render_template,request, session, url_for, redirect, flash
from decorators import login_required
from werkzeug.utils import secure_filename
from database.repository.users import UsersRepository
from database.repository.groups import GroupsRepository

route_crm = Blueprint('route_crm', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'static/img/uploads'
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@route_crm.route('/crm', methods=['GET', 'POST'])
@login_required
def crm():
	tg_id = int(session['tgid'])
	get_owners = UsersRepository().getOwnerById(tg_id)
	get_article = GroupsRepository().get_article()
	title = request.form.get('title')
	lang = request.form.get('lang')
	a = request.form.get('valore_editor')
	if request.method == 'GET':
		return render_template("crm.html", owner = get_owners, data=get_article)
	if request.method == 'POST':
		file = request.files['file']

		if file.filename == '':
			return '''
				<!doctype html>
				<h1>You have not selected any files, please select a file!</h1>
				<a href="https://nebula.squirrel-network.online/crm">Return to previous page</a>
				'''
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(UPLOAD_FOLDER, filename))
		else:
			return '''
			    <!doctype html>
			    <h1>Unauthorized file extension uses <code>.jpg, .jpeg, .png</code></h1>
			    <a href="https://nebula.squirrel-network.online/crm">Return to previous page</a>
			    '''
		if a is not None:
			data = [(title.lower(), lang, a)]
			GroupsRepository().insert_article(data)

		return redirect(url_for('route_crm.crm'))
