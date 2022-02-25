from database.db_connect import Connection
from pypika import Query, Table

users = Table("nebula_dashboard")

class UsersRepository(Connection):
  def getById(self, args=None):
    query = Query.from_(users).select("*").where(users.tg_id == "%s")
    q = query.get_sql(quote_char=None)
    
    return self._select(q, args)