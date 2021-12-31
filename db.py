import sqlite3


class DBConnector(object):
    db = 'db.sqlite3'

    def __init__(self):
        pass

    def execute(self, sql_string):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute(sql_string)
        data = cursor.fetchall()
        if 'INSERT' in sql_string or 'UPDATE' in sql_string:
            connection.commit()
        connection.close()
        return data

    def is_duplicated(self, client_id, user_id):
        query_string = f'SELECT * FROM search_history WHERE client_id={client_id} AND user_id={user_id};'
        data = self.execute(query_string)
        # print(data)
        if len(data):
            return True
        else:
            return False

    def write_user(self, client_id, user_id):
        query_string = f'INSERT INTO search_history (client_id, user_id) VALUES ({client_id}, {user_id});'
        data = self.execute(query_string)
        print(data)
