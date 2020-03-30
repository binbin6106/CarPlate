import sqlite3


class Tools:
    def __init__(self):
        self.conn = sqlite3.connect('CarPlane.db')
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def create_sql(self, sql_name, table_type):
        sql_user_info = "CREATE TABLE IF NOT EXISTS {}(" \
              "ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "NAME TEXT," \
              "PASSWORD TEXT" \
              ")".format(sql_name)
        sql_plate_info = ""
        if table_type == 'user':
            final_sql = sql_user_info
        else:
            final_sql = sql_plate_info

        self.c.execute(final_sql)
        self.conn.commit()

    def query_sql(self, info):
        pass

    def del_sql(self, info):
        pass

    def add_sql(self, info):
        pass

    def add_user(self, user_name, password):
        sql = 'INSERT INTO userinfo (NAME, PASSWORD) VALUES (%s, %s)' % (user_name, password)
        try:
            self.c.execute(sql)
            self.conn.commit()
            return '创建成功！'
        except Exception as e:
            return e

    def update_user(self):
        pass

    def del_user(self):
        pass

    def check_user(self, user_name, password):
        sql = "SELECT NAME, PASSWORD from userinfo where NAME is '{}'" .format(user_name)
        res = self.c.execute(sql)
        data = res.fetchone()
        if data:
            if user_name == data[0] and password == data[1]:
                return [1, '登陆成功']
            else:
                return [0, '用户名或密码错误！']
        else:
            return [0, '用户不存在！']

