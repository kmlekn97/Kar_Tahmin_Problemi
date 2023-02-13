import pandas as pd
import numpy as np
from lightgbm import LGBMRegressor
from sklearn.ensemble import  GradientBoostingRegressor
from sklearn.neural_network import MLPClassifier
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from GridSearchCVParametars import GridSearchCVParametars
from MySqlService import MySqlService
from DataBaseManager import DataBaseManager
from DataProcess import DataProcess
from DataVisulation import DataVisulation
from ModelTunning import ModelTunning
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

pd.options.display.float_format = '{:.1f}'.format  # 1 decimal only for float numbers display
np.set_printoptions(suppress=True)


service=MySqlService()
data=DataBaseManager(service)
cari=[]
tarih=[]
tarih=data.readdate(service)
cari=data.readcari(service)
print(cari)


df=pd.DataFrame()
df['kar']=pd.Series(cari)
df["tarih"]=pd.Series(tarih)
print(df)
dfkar=df.copy()

print(df.describe().T)

plt.scatter(df.index, cari)
plt.show()

prc=DataProcess()
prc.totalRevenue(df,99)
prc.outlinesData(df,99.9)

print(f"Min date from train set: {df['tarih'].min().date()}")
print(f"Max date from train set: {df['tarih'].max().date()}")

df['month'] = df['tarih'].dt.month
df['year'] = df['tarih'].dt.year

restoranlar=prc.findRestoran(data,service)
plotb=prc.Barplot(data,restoranlar,df,service)
dvision=DataVisulation()
dvision.Barchart(plotb[1],plotb[0],plotb[2])

avg_day_revenue=prc.daysAverageRevenue(df)
avg_day_revenue = df.groupby('tarih').agg({'kar': ['sum']})['kar']['sum']
dvision.linePlot(avg_day_revenue)

avg_mounth_revenue=prc.mounthAverageRevenue(df)

print(df)


dfselect=pd.DataFrame()
dfselect['c_kar']=pd.Series(cari)
dfselect['r_id']=pd.Series(data.readrestoran(service))
X=dfselect
y=dfkar['kar']

mlpc=MLPClassifier()
mTunning=ModelTunning()
mTunning.CraateDataset(X,y)
mTunning.CreateModel(mlpc)
gParamaters=GridSearchCVParametars()
classifacation=gParamaters.Paramaters(mTunning,mlpc,MLPClassifier)
mTunning.ModelSolve(mTunning.CreateModel(mlpc),classifacation[1],classifacation[0])
GBM=GradientBoostingRegressor()
XGB=XGBRegressor()
lightgbm=LGBMRegressor()
catb=CatBoostRegressor()
mTunning.RandomForest(gParamaters.RF())
mTunning.SolveGB(GBM,gParamaters.GB())
mTunning.SolveGB(XGB,gParamaters.GB())
mTunning.SolveGB(lightgbm,gParamaters.GB())
mTunning.SolveGB(catb,gParamaters.GB())
errors=mTunning.minerrors()
mTunning.SolveOptimalMethod(X,y,gParamaters)
mTunning.displayRevenue()
data.saveRevenue(service,mTunning.Revenue())