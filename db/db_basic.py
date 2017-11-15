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
            count = self.cursor.execute(sql)
        except:
            print(sql + ' execute failed.')
            return -1
        return count

    def fetchoneMysql(self):
        try:
            self.cursor.fetchone()
        except:
            print('fetchone failed.')
            return -1
        return 0

    def insertMysql(self, sql):
        #print("execute " + sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("insert failed.:", sql)
            return -1
        return 0

    def agency_begin(self):
        #print("execute " + sql)
        sql = "begin;"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("agency_begin failed.:", sql)
            return -1
        return 0

    def agency_commit(self):
        #print("execute " + sql)
        sql = "commit;"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("agency_commit failed.:", sql)
            return -1
        return 0

    def agency_rollback(self):
        #print("execute " + sql)
        sql = "rollback;"
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            print("agency_rollback failed.:", sql)
            return -1
        return 0

    def updateMysql(self, sql):
        #print("execute " + sql)
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except:
            self.conn.rollback()
            return -1
        return 0

    def closeMysql(self):
        self.cursor.close()
        self.conn.close()

