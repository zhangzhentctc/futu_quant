import pymysql
import logging


class MySQLCommand(object):
    def __init__(self,host,port,user,passwd,db):
        self.host = host
        self.port = port
        self.user = user
        self.password = passwd
        self.db = db

    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host,port=self.port,user=self.user,passwd=self.password,db=self.db,charset='utf8')
            self.cursor = self.conn.cursor()
        except:
            print('connect mysql error.')

    def queryMysql(self, sql):
        print("execute " + sql)
        try:
            self.cursor.execute(sql)
            row = self.cursor.fetchone()
            print(row)
        except:
            print(sql + ' execute failed.')

    def insertMysql(self, sql):
        print("execute " + sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("insert failed.")

    def updateMysql(self, sql):
        print("execute " + sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()
