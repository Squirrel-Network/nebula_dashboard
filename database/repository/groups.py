from database.db_connect import Connection
from pypika import Query, Table

groups = Table("groups")

class GroupsRepository(Connection):
    def getById(self, args=None):
        query = Query.from_(groups).select("*").where(groups.id_group == '%s')
        q = query.get_sql(quote_char=None)
        return self._select(q, args)

    def get_badwords_group(self, args=None):
        q = "SELECT * FROM groups_badwords WHERE tg_group_id = %s"
        return self._selectAll(q, args)

    def get_groups(self, args=None):
        q = "SELECT * FROM groups gr INNER JOIN nebula_dashboard nu ON gr.id_group = nu.tg_group_id WHERE nu.tg_id = %s"
        return self._selectAll(q, args)