#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork

import requests
import urllib.request
from config import Config

MAIN_URL = "https://api.telegram.org/"
TOKEN = Config.BOT_TOKEN

def string_generator(data_incoming):
	data = data_incoming.copy()
	del data['hash']
	keys = sorted(data.keys())
	string_arr = []
	for key in keys:
		string_arr.append(key+'='+data[key])
	string_cat = '\n'.join(string_arr)
	return string_cat

def ApiMessage(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = MAIN_URL + "bot{}/sendmessage?chat_id={}&text={}&parse_mode=HTML".format(TOKEN, chat_id, text)
    send = requests.get(url)
    return send