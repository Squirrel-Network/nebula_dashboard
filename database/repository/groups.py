#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright SquirrelNetwork
from database.db_connect import Connection
from pypika import Query, Table

groups = Table("groups")
tpnu = Table("nebula_type_no_username_cat")

class GroupsRepository(Connection):

    def getById(self, args=None):
        q = "SELECT * FROM groups WHERE id_group = %s"

        return self._select(q, args)

    def getAll(self):
        query = Query.from_(groups).select("*")
        q = query.get_sql(quote_char=None)

        return self._selectAll(q)

    def get_badwords_group(self, args=None):
        q = "SELECT * FROM groups_badwords WHERE tg_group_id = %s"
        return self._selectAll(q, args)

    def get_groups(self, args=None):
        q = "SELECT * FROM groups gr INNER JOIN nebula_dashboard nu ON gr.id_group = nu.tg_group_id WHERE nu.tg_id = %s"
        return self._selectAll(q, args)

    def get_groups_options(self, args=None):
        q = "SELECT * FROM groups gr INNER JOIN nebula_dashboard nu ON gr.id_group = nu.tg_group_id INNER JOIN nebula_type_no_username_cat ntnuc ON ntnuc.type_no_username_id = gr.type_no_username WHERE nu.tg_id = %s AND gr.id_group = %s"
        return self._select(q, args)

    def update_group_settings(self, record, args=None):
        q = "UPDATE groups SET @record = %s WHERE id_group = %s".replace('@record',record)
        return self._update(q, args)

    def get_type_no_username_cat(self, args=None):
        query = Query.from_(tpnu).select("*")
        q = query.get_sql(quote_char=None)
        return self._selectAll(q, args)

    def get_badwords_group(self, args=None):
        q = "SELECT * FROM groups_badwords WHERE tg_group_id = %s"
        return self._selectAll(q, args)

    def insert_badword(self, args=None):
        q = "INSERT IGNORE INTO groups_badwords (word, tg_group_id) VALUES (%s,%s)"

        return self._insert(q, args)

    def delete_badword(self, args=None):
        q = "DELETE FROM groups_badwords WHERE id = %s AND tg_group_id = %s"
        return self._delete(q, args)

    def delete_group_dashboard(self, args=None):
        print(args)
        q = "DELETE FROM nebula_dashboard WHERE tg_group_id = %s"

        return self._single_delete(q, args)

    def insert_article(self, args=None):
        q = "INSERT INTO nebula_dashboard_content (language, content) VALUES (%s, %s)"

        return self._insert(q, args)