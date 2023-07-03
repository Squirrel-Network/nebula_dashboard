#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

from flask import Blueprint, render_template

commands_route = Blueprint('commands_route', __name__)

@commands_route.route('/commands', methods=['GET', 'POST'])
def commands():
	return render_template("commands.html")
