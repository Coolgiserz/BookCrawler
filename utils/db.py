class DataBase():
    def __init__(self):
        self.handler = None

    def connect(self, host='localhost', port=27017):
        pass

    def insert(self, data):
        pass

    def query(self):
        pass

import pymongo
class MongoDB(DataBase):
    def __init__(self):
        super(MongoDB, self).__init__()

    def connect(self, host='localhost', port=27017):
        self.handler = pymongo.MongoClient('mongodb://{}:{}'.format(host, port))
        print("连接数据库成功")
        return self.handler

    def connectDB(self, db, collection):
        try:
            mydb = self.handler[db]
            self.collection = mydb[collection]
        except Exception as e:
            print("Connect fail: {}".format(e))


    def insert(self, data):
        try:
            self.collection.insert(data)
        except:
            print("插入数据异常")




