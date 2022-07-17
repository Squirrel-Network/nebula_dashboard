#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, url_for, redirect
from decorators import login_required
from database.repository.groups import GroupsRepository

route_delete_group = Blueprint('route_delete_group', __name__)

@route_delete_group.route('/delete/<id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    GroupsRepository().delete_group_dashboard(id)
    return redirect(url_for('route_dashboard.dashboard'))