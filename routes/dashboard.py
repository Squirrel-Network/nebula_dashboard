#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import render_template, session, redirect, url_for, Blueprint
from database.repository.users import UsersRepository
from database.repository.groups import GroupsRepository
from decorators import login_required

route_dashboard = Blueprint('route_dashboard', __name__)

@route_dashboard.route('/dashboard')
@login_required
def dashboard():
	tg_id = int(session['tgid'])
	row = UsersRepository().getById(tg_id)
	if row:
		if row['enable'] == 1:
			groups = GroupsRepository().get_groups(tg_id)
			get_all_groups = GroupsRepository().getAll()
			get_owners = UsersRepository().getOwnerById(tg_id)
			return render_template('dashboard.html', data=groups, ownerdata=get_all_groups,owner=get_owners)
		else:
			return 'Non sei abilitato! Contatta un amministratore'
	else:
		return redirect(url_for('route_login.login'))