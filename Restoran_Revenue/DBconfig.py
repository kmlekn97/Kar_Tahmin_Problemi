class DBconfig():
    __host=None
    __user=None
    __password=None
    __db=None
    def __init__(self):
        self.__host='localhost'
        self.__user='root'
        self.__password=''
        self.__db='restoran'
    def gethost(self):
        return self.__host
    def getuser(self):
        return self.__user
    def getpassword(self):
        return self.__password
    def getdb(self):
        return self.__db
