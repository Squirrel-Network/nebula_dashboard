#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from flask import request, Blueprint, session, render_template, redirect, url_for
from utilities import ApiMessage, ApiTitle
from database.repository.groups import GroupsRepository
from database.repository.users import UsersRepository
from decorators import login_required

route_update = Blueprint('route_update', __name__)

@route_update.route('/update/<id>', methods=['GET', 'POST'])
@login_required
def update(id):
	get_badwords = GroupsRepository().get_badwords_group(id)
	if request.method == 'GET':
		tg_id = int(session['tgid'])
		db_data = (tg_id, id)
		row = GroupsRepository().get_groups_options(db_data)
		get_tpnu = GroupsRepository().get_type_no_username_cat()
		get_badwords = GroupsRepository().get_badwords_group(id)
		get_owners = UsersRepository().getOwnerById(tg_id)
		if get_owners:
			row = GroupsRepository().getById(id)
		return render_template("edit.html",data = row, tpnu = get_tpnu, badwords = get_badwords, owner = get_owners)

	if request.method == 'POST':
		tg_id = int(session['tgid'])
		db_data = (tg_id, id)
		rules_button = request.form.get('updateoptions')
		message_button = request.form.get('sendmessagebutton')
		title_button = request.form.get('updatetitle')
		bads = request.form.get('badword')
		ban_message_btn = request.form.get('sendbanmessage')
		group_filters_btn = request.form.get('sendgroupfilterbtn')

		if bads is not None:
			data = [(bads,id)]
			GroupsRepository().insert_badword(data)
			return redirect(url_for('route_update.update',id=id))

		if message_button is not None:
			send_message = request.form.get('sendbot')
			ApiMessage(send_message,id)
			return redirect(url_for('route_update.update',id=id))

		if title_button is not None:
			title = request.form.get('chattitle')
			record_title = 'group_name'
			ApiTitle(title,id)
			data = [(title,id)]
			GroupsRepository().update_group_settings(record_title,data)
			return redirect(url_for('route_update.update',id=id))

		if ban_message_btn is not None:
			ban_msg = request.form.get('banmessage')
			record_ban_message = 'ban_message'
			data_ban_message = [(ban_msg,id)]
			GroupsRepository().update_group_settings(record_ban_message,data_ban_message)
			return redirect(url_for('route_update.update',id=id))


		if group_filters_btn is not None:
			form = request.form
			#Record
			record_block_channel = 'sender_chat_block'
			record_spoiler = 'spoiler_block'
			record_vocal = 'set_no_vocal'
			record_antiflood = 'set_antiflood'
			#Get parameters via POST
			checkbox_block_ch = form.get('blockchannel') if form.get('blockchannel') is not None else 0
			checkbox_spoiler = form.get('setnospoiler') if form.get('setnospoiler') is not None else 0
			checkbox_vocal = form.get('setnovocal') if form.get('setnovocal') is not None else 0
			checkbox_antiflood = form.get('setantiflood') if form.get('setantiflood') is not None else 0
			#Prepare Data
			data_block_channel = [(int(checkbox_block_ch),id)]
			data_no_spoiler = [(int(checkbox_spoiler),id)]
			data_no_vocal = [(int(checkbox_vocal),id)]
			data_antiflood = [(int(checkbox_antiflood),id)]
			#Insert Data
			GroupsRepository().update_group_settings(record_block_channel,data_block_channel)
			GroupsRepository().update_group_settings(record_spoiler,data_no_spoiler)
			GroupsRepository().update_group_settings(record_vocal,data_no_vocal)
			GroupsRepository().update_group_settings(record_antiflood,data_antiflood)
			return redirect(url_for('route_update.update',id=id))


		if rules_button is not None:
			#Database Record
			record_welcome = 'welcome_text'
			record_rules = 'rules_text'
			record_tpnu = 'type_no_username'
			record_checkbox_no_photo = 'set_user_profile_picture'
			record_checkbox_welcome = 'set_welcome'
			record_checkbox_arabic = 'set_arabic_filter'
			record_checkbox_cirillic = 'set_cirillic_filter'
			record_checkbox_chinese = 'set_chinese_filter'
			record_checkbox_zoophile = 'zoophile_filter'
			#Data Arrived by <form>
			form = request.form

			checkbox_photo = form.get('userphoto') if form.get('userphoto') is not None else 0
			checkbox_welcome = form.get('welcomeswitch') if form.get('welcomeswitch') is not None else 0
			checkbox_arabic_filter = form.get('arabicfilter') if form.get('arabicfilter') is not None else 0
			checkbox_cirillic_filter = form.get('cirillicfilter') if form.get('cirillicfilter') is not None else 0
			checkbox_chinese_filter = form.get('chinesefilter') if form.get('chinesefilter') is not None else 0
			checkbox_zoophile_filter = form.get('zoophilefilter') if form.get('zoophilefilter') is not None else 0

			data_welcome = [(form['welcome'],id)]
			data_rules = [(form['rules'],id)]
			data_tpnu = [(int(form['tpnuselect']),id)]
			data_checkbox_photo = [(int(checkbox_photo),id)]
			data_checkbox_welcome = [(int(checkbox_welcome),id)]
			data_checkbox_arabic = [(int(checkbox_arabic_filter),id)]
			data_checkbox_cirillic = [(int(checkbox_cirillic_filter),id)]
			data_checkbox_chinese = [(int(checkbox_chinese_filter),id)]
			data_checkbox_zoophile = [(int(checkbox_zoophile_filter),id)]
            #Update Database

			GroupsRepository().update_group_settings(record_welcome,data_welcome)
			GroupsRepository().update_group_settings(record_rules,data_rules)
			GroupsRepository().update_group_settings(record_tpnu,data_tpnu)
			GroupsRepository().update_group_settings(record_tpnu,data_tpnu)
			GroupsRepository().update_group_settings(record_checkbox_no_photo,data_checkbox_photo)
			GroupsRepository().update_group_settings(record_checkbox_welcome,data_checkbox_welcome)
			GroupsRepository().update_group_settings(record_checkbox_arabic,data_checkbox_arabic)
			GroupsRepository().update_group_settings(record_checkbox_cirillic,data_checkbox_cirillic)
			GroupsRepository().update_group_settings(record_checkbox_chinese,data_checkbox_chinese)
			GroupsRepository().update_group_settings(record_checkbox_zoophile,data_checkbox_zoophile)
		row = GroupsRepository().get_groups_options(db_data)
		get_tpnu = GroupsRepository().get_type_no_username_cat()
		get_owner_data = UsersRepository().getOwnerById(tg_id)
		if get_owner_data:
			row = GroupsRepository().getById(id)
		return render_template("edit.html",data=row, tpnu=get_tpnu, badwords=get_badwords,owner = get_owner_data)