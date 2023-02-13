import numpy as np
import pandas as pd
class DataProcess():
    def totalRevenue(self,df,p):
        percentile = np.percentile(df['kar'], p)
        print(f"The Revenue {p}th percentile is equal to {percentile}")
    def outlinesData(self,df,p):
        percentile = np.percentile(df['kar'], p)
        print(f"The Revenue {p}th percentile is equal to {percentile}")
        outliers_num = len(df[df['kar'] > percentile])
        sales_train = df[df['kar'] < percentile]
        print(f"We removed {outliers_num} outliers from the data")
        print(df['kar'].nunique())
    def findRestoran(self,data,service):
        id = data.readrestoran(service)
        restoranlar = []
        for i in id:
            if i not in restoranlar:
                restoranlar.append(i)
        return restoranlar

    def Barplot(self,data,restoranlar,df,service):
        df['kar'] = pd.Series(data.readcariidli(service))
        N = len(restoranlar)
        restoran = df.groupby('kar').sum()
        restoran.reset_index(inplace=True)
        idxs = restoran['kar'].values.argsort()[::-1][0:N]
        temp = restoran['kar'].to_numpy()
        max_sold = [temp[idx] for idx in idxs]
        res_ad = data.findRestoran(restoranlar, service)
        restoran['restoran_id'] = pd.Series(restoranlar)
        restoran_ids = restoran.loc[idxs, 'restoran_id'].values
        restoran['restoran_ad'] = pd.Series(res_ad)
        return max_sold,restoran['restoran_ad'],N
    def daysAverageRevenue(self,df):
        avg_total_revenues_day = df.groupby('tarih').agg({'kar': ['sum']}).mean().values[0]
        print(f"In average, total revenue per day is about {round(avg_total_revenues_day)} .")
    def mounthAverageRevenue(self,df):
        avg_total_revenues_month = df.groupby(['year', 'month']).agg({'kar': ['sum']}).mean().values[0]
        print(f"In average, total revenue per month is about {round(avg_total_revenues_month)} .")