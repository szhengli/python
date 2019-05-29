import pymysql
import re

class DBHelper:
    # 构造函数
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.conn = None
        self.cur = None
        self.table_name = None

    # 连接数据库
    def conn_db(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user
                                        , password=self.password
                                        , port=self.port, db=self.db, charset='utf8')
        except Exception as e:
            raise e
        self.cur = self.conn.cursor()
        return self.cur

    # 关闭数据库
    def close(self):
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()

    # 判断表是否存在
    def table_exists(self, table_name):
        check_sql = "show tables;"
        self.cur.execute(check_sql)
        tables = self.cur.fetchall()
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        if table_name in table_list:
            return 1
        else:
            return 0

    # 执行语句
    def exec(self, sql):
        if sql:
            try:
                self.cur.execute(sql)
                self.conn.commit()
            except Exception as e:
                self.conn.rollback()
                raise e
        else:
            exit('退出:传入的执行语句不能为空')

    # 查询汇总行数的可以调用
    def get_total(self):
        try:
            total = self.cur.fetchone()
            if total:
                total = total[0]
                total = int(total)
            else:
                total = 0
            return total
        except Exception as e:
            raise e
