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
        sql_plate_info = "CREATE TABLE IF NOT EXISTS {}(" \
              "ID INTEGER PRIMARY KEY AUTOINCREMENT, " \
              "plate TEXT," \
              "intime TEXT," \
              "outime TEXT," \
              "isin TEXT" \
              ")".format(sql_name)
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

    def input_plate(self, info):
        sql = "INSERT INTO plateinfo (plate, isin) VALUES ('{}', '{}')".format(info, '0')
        try:
            self.c.execute(sql)
            self.conn.commit()
            return [1, '录入成功!']
        except Exception as e:
            return [0, '录入失败!原因{}'.format(e)]

    def check_plate(self, plate_num):
        sql = "SELECT * from plateinfo where plate is '{}'".format(plate_num)
        res = self.c.execute(sql)
        data = res.fetchone()
        if data:
            return [1, data]
        else:
            return [0]

    def update_intime_plate_info(self, time, plate_id):
        sql = "UPDATE plateinfo SET intime = '{}', isin = '1' WHERE ID = '{}'".format(time, plate_id)
        try:
            self.c.execute(sql)
            self.conn.commit()
            return [1, '进入登记成功!']
        except Exception as e:
            return [0, '进入登记失败!原因{}'.format(e)]

    def update_outime_plate_info(self, time, plate_id):
        sql = "UPDATE plateinfo SET outime = '{}', isin = '0' WHERE ID = '{}'".format(time, plate_id)
        try:
            self.c.execute(sql)
            self.conn.commit()
            return [1, '驶出登记成功!']
        except Exception as e:
            return [0, '驶出登记失败!原因{}'.format(e)]