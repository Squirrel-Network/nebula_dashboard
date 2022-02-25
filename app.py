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
		return redirect(url_for('dashboard'))
	else:
		return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(port=4495,debug=False)
