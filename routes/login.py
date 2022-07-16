#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import hashlib
import hmac
import time
from flask import render_template, request,redirect, session, url_for, Blueprint
from utilities import string_generator

route_login = Blueprint('route_login', __name__)

#@app.route('/login')
@route_login.route('/login', methods=['GET'])
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