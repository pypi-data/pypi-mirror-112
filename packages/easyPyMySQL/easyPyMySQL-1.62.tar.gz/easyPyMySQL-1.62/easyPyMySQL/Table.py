from .TableField import TableField
from .TableLine import TableLine


class Table(object):
    def __init__(self, epm, tableName):
        self.tableName = tableName
        self.db = epm
        self.columns = [column["COLUMN_NAME"] for column in epm.do("select COLUMN_NAME from information_schema.columns where TABLE_SCHEMA = %s AND TABLE_NAME = %s;", (epm.db, self.tableName))]
        self.pk = [column["COLUMN_NAME"] for column in epm.do("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;", (epm.db, self.tableName))]
        self._columns_ignorecase = [column_name.upper() for column_name in self.columns]
        self._pk_ignorecase = [column_name.upper() for column_name in self.pk]
        # self.pk = self.pk[0][0]['COLUMN_NAME']

    # def logist(self, fields, s=""):
    #     # (["id","id"], "value");[22, 100, "helloworld"]
    #     # select * from {0} where (id = %s or id == %s) and value = %s
    #
    #     if type(fields) == type(()):
    #         for field in fields:
    #             if type(field) == type(""):
    #                 s += field + "=%s and "
    #             else:
    #                 s += self.logist(field) + " and "
    #                 # s = "id=%s or id=%s"
    #         else:
    #             s = s[:-5]
    #         return s
    #     elif type(fields) == type([]):
    #         for field in fields:
    #             if type(field) == type(""):
    #                 s += field + "=%s or "
    #             else:
    #                 s += self.logist(field) + " or "
    #         else:
    #             s = s[:-4]
    #         # s = "id=%s or id=%s"
    #         return "(" + s + ")"

    # def __call__(self, fields):
    #     self.SELECT_SQL = "select * from {0} where ".format(self.tableName)
    #     self.SELECT_SQL += self.logist(fields)
    #     # for field in fields:
    #     #     self.SELECT_SQL += " " + field
    #     #     #self.SELECT_SQL += " = %s " +
    #     # else:
    #     #     self.SELECT_SQL = self.SELECT_SQL[:-1]
    #     return self

    # def __getitem__(self, field_name):
    #     # 锁定位置
    #     return TableField(self.tableName, field_name)
        # self.SELECT_SQL = "select * from {0} where ".format(self.tableName)
        # self.SELECT_SQL += self.logist(fields)
        # return self
        # return self.db.do(self.SELECT_SQL, where)

    # def find(self, condition):
    #     """
    #     find函数用于查询，需要传进来一个__getitem__函数返回的查询条件condition
    #     :param condition:
    #     :return:
    #     """
    #     datas = self.db.do(condition.SQL()[0], condition.SQL()[1])
    #     if type(condition.table_name) != type([]):
    #         lines_data = []
    #         for data in datas:
    #             lines_data.append(TableLine(data, condition, self.pk, self.db))
    #
    #         return lines_data
    #     else:
    #         return datas


    def add(self, data):
        # 增
        """
        传入一个字典，字典的键对应数据库表的键，字典的值对应新增数据的值
        传入一个列表或元组，包含完整的、排好顺序的新增数据
        :param data:
        :return:
        """
        SQL = "insert into {0} ".format(self.tableName)
        if type(data) == type({}):
            key_SQL = "("
            deta_SQL = "("
            for key in data:
                if(key.upper() in self._columns_ignorecase):
                    key_SQL += self.columns[self._columns_ignorecase.index(key.upper())] + ","
                    deta_SQL += "%s,"
            else:
                key_SQL = key_SQL[:-1] + ")"
                deta_SQL = deta_SQL[:-1] + ")"
            SQL += key_SQL + " values " + deta_SQL
            values = list(data.values())
            result = self.db.do(SQL, values)

        elif(type(data) == type(())):
            deta_SQL = "("
            for i in range(len(data)):
                deta_SQL += "%s,"
            else:
                deta_SQL = deta_SQL[:-1]+")"
            SQL += " values " + deta_SQL
            result = self.db.do(SQL, data)
        return result




