from Interface import Interface
class IDataBaseService(Interface):
    def connect(self):
        pass
    def Fullread(self,table,id=None,alan=None):
        pass
    def databasexecute(self,sql,data):
        pass
    def dataread(self, sql):
        pass
    def connectclose(self):
        pass