#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import request, Blueprint, session, render_template, redirect, url_for
from decorators import login_required
from database.repository.groups import GroupsRepository



route_staff = Blueprint('route_staff', __name__)

@route_staff.route('/staff/<id>', methods=['GET', 'POST'])
@login_required
def staff(id):
    row = GroupsRepository().getStafferById(id)
    if request.method == 'GET':
        if row is None:
                return '''
            		    <!doctype html>
            		    <h1>Id Non Valido!</code></h1>
            		    <a href="https://nebula.squirrel-network.online/crm">Return to previous page</a>
            			    '''
        return render_template("edit_staff.html",data=row)
    if request.method == 'POST':
        if row is None:
                return '''
            		    <!doctype html>
            		    <h1>Id Non Valido!</code></h1>
            		    <a href="https://nebula.squirrel-network.online/crm">Return to previous page</a>
            			    '''
        return redirect(url_for('route_staff.staff', id=id))