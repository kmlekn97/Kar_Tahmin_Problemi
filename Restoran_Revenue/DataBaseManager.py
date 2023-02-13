class DataBaseManager():
    __IDataBaseManager=None
    def __init__(self, IDataBaseManager):
        self.__IDataBaseManager = IDataBaseManager

    def readcari(self,database):
        kar=[]
        database.connect()
        data = database.Fullread("cari")
        for i in range(len(data)):
            kar.append(data[i][1]-data[i][2])
        database.connectclose()
        return kar
    def readcariidli(self,database):
        kar=[]
        database.connect()
        sql = "Select SUM(cari_gelir-cari_gider) as kar FROM cari Group by restoran_id"
        data=database.dataread(sql)
        for i in range(len(data)):
            kar.append(data[i][0])
        database.connectclose()
        return kar
    def readdate(self,database):
        tarih = []
        database.connect()
        data = database.Fullread("cari")
        for i in range(len(data)):
            tarih.append(data[i][4])
        database.connectclose()
        return tarih
    def readrestoran(self,database):
        restoran_id=[]
        database.connect()
        data = database.Fullread("cari")
        for i in range(len(data)):
            restoran_id.append(data[i][3])
        database.connectclose()
        return restoran_id
    def findRestoran(self,restoran_id=[],database=None):
        restoran_ad = []
        database.connect()
        for i in range(len(restoran_id)):
            data = database.Fullread("restoranlar","Restoran_id",restoran_id[i])
            for i in range(len(data)):
                restoran_ad.append(data[i][1])
        database.connectclose()
        return restoran_ad
    def saveRevenue(self,database,karmiktari):
        database.connect()
        sql = "INSERT INTO kartahmin (karTahmin_miktari) VALUES ('%s')"
        data = (float(karmiktari))
        database.databasexecute(sql, data)
        database.connectclose()
