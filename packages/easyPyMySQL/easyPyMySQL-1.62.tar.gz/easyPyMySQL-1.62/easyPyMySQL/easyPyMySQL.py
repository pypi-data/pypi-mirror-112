###################################################################
# 封装mysql的登录，封装sql语句的运行
# 提供ORM
###################################################################
import pymysql
from html.parser import HTMLParser
from .Table import Table
import sys,os, logging

class MyHTMLParser(HTMLParser):
    def init(self):
        self.handle_host = False
        self.handle_port = False
        self.handle_user = False
        self.handle_passWord = False
        self.handle_dbName = False
        self.host = ""
        self.port = ""
        self.user = ""
        self.passWord = ""
        self.dbName = ""

    def handle_starttag(self, tag, attrs):
        if(tag == "td" and attrs[0][1] == "dbConfig_Login_host"):
            self.handle_host = True
        if(tag == "td" and attrs[0][1] == "dbConfig_Login_port"):
            self.handle_port = True
        if(tag == "td" and attrs[0][1] == "dbConfig_Login_user"):self.handle_user = True
        if(tag == "td" and attrs[0][1] == "dbConfig_Login_db_passWord"):self.handle_passWord = True
        if(tag == "td" and attrs[0][1] == "dbConfig_Login_dbName"):self.handle_dbName = True

    def handle_data(self, data):
        if(self.handle_host):
            self.host = data
            self.handle_host = False
        if(self.handle_port):
            self.port = int(data)
            self.handle_port = False
        if(self.handle_user):
            self.user = data
            self.handle_user = False
        if(self.handle_passWord):
            self.passWord = data
            self.handle_passWord = False
        if(self.handle_dbName):
            self.dbName = data
            self.handle_dbName = False

class mysqlHelper(object):
    _subclasses = []
    def __init_subclass__(cls):
        super().__init__(cls)
        cls._subclasses.append(cls)

    def __init__(self, configFilePath):
        workpath = os.path.split(sys.argv[0])[0]
        configFilePath = os.path.join(workpath, configFilePath)
        parser = MyHTMLParser()
        parser.init()
        with open(configFilePath, "rb") as f:
            parser.feed(f.read().decode("utf-8"))

        self._SQLHelper__db = pymysql.connect(host=parser.host, port=parser.port, user=parser.user, password=parser.passWord, db=parser.dbName, cursorclass=pymysql.cursors.DictCursor, charset='utf8')    # 游标设置为字典类型
        self.cursor = self._SQLHelper__db.cursor()
        self.insert_id = None
        self.db = parser.dbName

    def __del__(self):
        self._SQLHelper__db.close()



    def do(self, SQL, values=None):
        _SQL = self.cursor.mogrify(SQL, values)
        try:
            self.cursor.execute(SQL, values)
            self.insert_id = self._SQLHelper__db.insert_id()
            self._SQLHelper__db.commit()
        except Exception as e:
            logging.error("SQL执行错误：\n" + SQL + "\n" + e)
        return self.cursor.fetchall()

    def table(self, tableName):
        return Table(self, tableName)



if __name__ == "__main__":
    import time
    t1 = time.time()

    # 使用配置文件创建数据库连接，析构时自动断开链接
    testdb = easyPyMySQL("dbConf.xhtml")

    # 选择数据库的某张表
    test_table1 = testdb.table("test")
    test_table2 = testdb.table("test_table2")

    # # 两表连接查询
    # select1 = (test_table1['id'] == test_table2 ['id']) & (test_table1['value'] >= 10) & (test_table1['value'] < 1000)
    # S = select1.SQL()[0]
    # print(testdb.do(S, select1.SQL()[1]))
    # # 单表查询
    # id = test_table1['id']
    # select2 = (id >= 1) & (id < 200) & ((id < 5) | (id > 100))
    # print(testdb.do(select2.SQL()[0],select2.SQL()[1]))


    # 更简便的查询接口，使用此接口进行单表查询后，可直接复制修改查到的数据
    # id = test_table1['id']
    # # select_condition3 = (id == 10) | (test_table2['id'] ==id)
    # select_condition3 = (id == 10)
    # datas = test_table1.find(select_condition3)
    # print(datas)
    # # 修改数据
    # one_line_of_data = datas[0]
    # one_line_of_data['value'] << 2
    # one_line_of_data['id'] << 10
    # # 提交修改
    # datas[0].flush()


    # 对某张表新增数据

    test_table1.add({'id':100,'value':255})
    # test_table1.add([100, 255])


    print("总耗时：", time.time()-t1)
