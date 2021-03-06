import configparser as cparser
import pymysql.cursors
import os

base_dir = str(os.path.dirname(os.path.dirname(__file__)))
base_dir = base_dir.replace('\\', '/')
file_path = base_dir + '/db_file.ini'

cf = cparser.ConfigParser()
cf.read(file_path)

host = cf.get('mysqlconf', 'host')
port = cf.get('mysqlconf', 'port')
db = cf.get('mysqlconf', 'db_name')
user = cf.get('mysqlconf', 'user')
password = cf.get('mysqlconf', 'password')


class DB:

    def __init__(self):
        try:
            # Connect to the database
            self.connection = pymysql.connect(host=host,
            port = int(port),
            user = user,
            password = password,
            db = db,
            charset = 'utf8mb4',
            cursorclass = pymysql.cursors.DictCursor)
        except pymysql.err.OperationalError as e:
            print("Mysql Error %d: %s" % (e.args[0], e.args[1]))

    def clear(self, table_name):
        real_sql = 'delete from' + table_name + ';'
        with self.connection.cursor() as cursor:
            cursor.execute('SET FOREIGN_KEY_CHECKS=0;')
            cursor.execute(real_sql)
        self.connection.commit()

    def insert(self, table_name, table_data):
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ",".join(table_data.keys())
        value = ",".join(table_data.values())
        real_sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ")"
        with self.connection.cursor() as cursor:
            cursor.execute(real_sql)
        self.connection.commit()

    def close(self):
        self.connection.close()

    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()


if __name__ == '__main__':

    db = DB()
    table_name = "aaa"
    data = {'id':1,'name':'aa','`limit`':2000,'status':1,'address':'北京会展中心','start_time':'2016-08-20 00:25:42'}
    table_name2 = "sign_guest"
    data2 = {'realname':'alen','phone':12312341234,'email':'xxx@mail.com','sign':0,'event_id':1}

    db.clear(table_name)
    db.insert(table_name, data)
    db.close()
