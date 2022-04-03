#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

def string_generator(data_incoming):
	data = data_incoming.copy()
	del data['hash']
	keys = sorted(data.keys())
	string_arr = []
	for key in keys:
		string_arr.append(key+'='+data[key])
	string_cat = '\n'.join(string_arr)
	return string_cat