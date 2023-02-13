import seaborn as sns
from matplotlib import pyplot as plt


class DataVisulation():
    def Barchart(self,X,Y,N):
        fig, ax = plt.subplots(figsize=(16, 12))
        barplot = sns.barplot(x=X, y=Y)
        for p in barplot.patches:
            barplot.text(p.get_width(), p.get_y() + 0.55 * p.get_height(),
                         ''.format(p.get_width()),
                         ha='center', va='center')
        barplot.set(xlabel="Number of Restaurants", ylabel="Revenue", title=f"Top {N} items Revenue")
        plt.show()
    def linePlot(self,avg_day_revenue):
        fig, ax = plt.subplots(figsize=(20, 10))
        lineplot = sns.lineplot(x=avg_day_revenue.index, y=avg_day_revenue)
        lineplot.set(xlabel="Date", ylabel="Total Revenue", title="Total day Revenue through time among all Revenue")
        plt.show()
    def SubLinePlot(self,y):
        date = []
        years = ['2022']
        for year in years:
            for month in range(1, 13):
                if month < 10:
                    date.append(year + '-0' + str(month))
                else:
                    date.append(year + '-' + str(month))

        fig, ax = plt.subplots(figsize=(20, 10))
        lineplot = sns.lineplot(x=date, y=y)
        lineplot.set(xlabel="Date", ylabel="Total Revenue", title="Total month Revenue through time among all Restaurant")
        lineplot.set_xticklabels(date, rotation=50)
        plt.show()