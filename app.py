#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
import hashlib
import hmac
import time
from flask import Flask, render_template, request,redirect, session, url_for
from flask_login import login_required
from decorators import login_required
from utilities import string_generator
from database.repository.users import UsersRepository
from database.repository.groups import GroupsRepository

app = Flask(__name__)

app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

# openssl aes-256-cbc -d -in config.py.enc -out config.py -pass env:CONFIGPASS
# openssl aes-256-cbc -in config.py -out config.py.enc -pass env:CONFIGPASS


@app.route('/')
@app.route("/home")
@app.route("/index")
def index():
	return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
	tg_id = int(session['tgid'])
	row = UsersRepository().getById(tg_id)
	if row:
		if row['enable'] == 1:
			groups = GroupsRepository().get_groups(tg_id)
			return render_template('dashboard.html', data=groups)
		else:
			return 'Non sei abilitato! Contatta un amministratore'
	else:
		return redirect(url_for('login'))

@app.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
	if request.method == 'GET':
		tg_id = int(session['tgid'])
		db_data = (tg_id, id)
		row = GroupsRepository().get_groups_options(db_data)
		get_tpnu = GroupsRepository().get_type_no_username_cat()
		return render_template("edit.html",data=row,tpnu=get_tpnu)
	if request.method == 'POST':
		tg_id = int(session['tgid'])
		db_data = (tg_id, id)
		rules_button = request.form.get('updateoptions')
		if rules_button is not None:
			#Database Record
			record_welcome = 'welcome_text'
			record_rules = 'rules_text'
			record_tpnu = 'type_no_username'
			record_checkbox_no_photo = 'set_user_profile_picture'
			record_checkbox_welcome = 'set_welcome'
			record_checkbox_arabic = 'set_arabic_filter'
			#Data Arrived by <form>
			form = request.form
			checkbox_photo = form.get('userphoto') if form.get('userphoto') is not None else 0
			checkbox_welcome = form.get('welcomeswitch') if form.get('welcomeswitch') is not None else 0
			checkbox_arabic_filter = form.get('arabicfilter') if form.get('arabicfilter') is not None else 0

			data_welcome = [(form['welcome'],id)]
			data_rules = [(form['rules'],id)]
			data_tpnu = [(int(form['tpnuselect']),id)]
			data_checkbox_photo = [(int(checkbox_photo),id)]
			data_checkbox_welcome = [(int(checkbox_welcome),id)]
			data_checkbox_arabic = [(int(checkbox_arabic_filter),id)]
			print(data_checkbox_photo)
			print(data_checkbox_welcome)
			print(data_checkbox_arabic)
            #Update Database

			GroupsRepository().update_group_settings(record_welcome,data_welcome)
			GroupsRepository().update_group_settings(record_rules,data_rules)
			GroupsRepository().update_group_settings(record_tpnu,data_tpnu)
			GroupsRepository().update_group_settings(record_tpnu,data_tpnu)
			GroupsRepository().update_group_settings(record_checkbox_no_photo,data_checkbox_photo)
			GroupsRepository().update_group_settings(record_checkbox_welcome,data_checkbox_welcome)
			GroupsRepository().update_group_settings(record_checkbox_arabic,data_checkbox_arabic)
		row = GroupsRepository().get_groups_options(db_data)
		get_tpnu = GroupsRepository().get_type_no_username_cat()
		return render_template("edit.html",data=row,tpnu=get_tpnu)

@app.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
	print(id)
	return "delete"

@app.route('/logout')
def delete_session():
	session.clear()
	return redirect(url_for('login'))

@app.route('/login')
def login():
	if not request.args.get('hash',None):
		return render_template('index.html')
	tg_data = request.args
	data_check_string = string_generator(tg_data)
	secret_key = hashlib.sha256(app.config['BOT_TOKEN'].encode('utf-8')).digest()
	secret_key_bytes = secret_key
	data_check_string_bytes = bytes(data_check_string,'utf-8')
	hmac_string = hmac.new(secret_key_bytes, data_check_string_bytes, hashlib.sha256).hexdigest()
	if hmac_string == tg_data['hash']:
		# Control comes here if the data is authentic
		if time.time() - int(tg_data['auth_date']) > 3600:
			return redirect(url_for('login'))
		#Create Session
		session['logged_user'] = True
		session['tgid'] = tg_data['id']
		session['username'] = tg_data['username']
		session['photo_url'] = tg_data['photo_url']
		return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(port=4495,debug=False)
