#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
import os
from config import Config
from flask import Flask, render_template,redirect, session, url_for
from decorators import login_required
from routes.login import route_login
from routes.dashboard import route_dashboard
from routes.test import route_test
from routes.update import route_update
from routes.delete_group import route_delete_group
from routes.commands import commands_route
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


@app.route('/deletebadword/<id>/<groupid>', methods=['GET', 'POST'])
@login_required
def deletebadword(id,groupid):
	data = [(id,groupid)]
	GroupsRepository().delete_badword(data)
	return redirect(url_for('route_update.update',id=groupid))

@app.route('/logout')
def delete_session():
	session.clear()
	return redirect(url_for('route_login.login'))

################
#### ROUTES ####
################
app.register_blueprint(route_login)
app.register_blueprint(route_update)
app.register_blueprint(route_dashboard)
app.register_blueprint(route_delete_group)
app.register_blueprint(route_test)
app.register_blueprint(commands_route)

if __name__ == '__main__':
	app.run(port=Config.APP_PORT,debug=Config.DEBUG)
