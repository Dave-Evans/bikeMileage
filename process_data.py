import os
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt
import time
import datetime
import numpy as np
import calendar
from pandas.core.common import isnull

### function for taking a pandas datatime index (%Y-%m%-%d) and making it a usable
###    form for matplotlib
def pd_to_plt(indx):
    pltDates = []
    for date in indx:
        strDate = str(date).split(" ")[0].split("-")
        pltDates.append(datetime.date(int(strDate[0]), int(strDate[1]), int(strDate[2])))
#     pltDates = [datetime.date(int(str(date).split("-")[0]),int(str(date).split("-")[1]),int(str(date).split("-")[2])) for date in indx]
    return pltDates

if os.name == "nt":
	path = "C:/workspace/projects/bikeMileage/bikeMileage"
else:
	path = "/home/devans/Documents/bikeMileage"

miscFiles = os.listdir(path)
bikes = ["schwinn","fuji", "redTrek", "blueTrek", "takara"]
colrs = ["slategray","darkred", 'red', "deepskyblue", "saddlebrown"]
# dat = pd.DataFrame()
for i, bike in enumerate(bikes):
#     print "Working on " + str(i) + " and the " + bike
    targ = [fl for fl in miscFiles if bike in fl][0]
    tmp = pd.read_table(path + "/" + targ, sep="\t")
    tmp["Bike"] = bike
    tmp["Date"].fillna("01.01.2014", None, 0, True)
    tmp["DateSec"] = [calendar.timegm(time.strptime(dte, "%d.%m.%Y")) for dte in tmp["Date"]]
    tmp["Date"] = [time.strftime("%Y-%m-%d", time.strptime(dte, "%d.%m.%Y")) for dte in tmp["Date"]]
#     print tmp.head()
    if (i == 0):
        dat = tmp
    else: 
        dat = dat.append(tmp)


# use this to put into seconds since epoch:
# http://stackoverflow.com/questions/17328655/pandas-set-datetimeindex
# datetime.datetime(int(str(dat.index).split("-")[0]), int(str(dat.index).split("-")[1]), int(str(dat.index).split("-")[2]))
print("Total mileage: " + str(dat["Mileage"].sum()))
f = lambda x : x.split("-")[0]
yrs = sorted(list(set(map(f, list(dat["Date"])))))

dat.set_index("Date", True, False, True)

for i in range(len(yrs)): yrs[i] = (yrs[i] + "-01-01", yrs[i] + "-12-31") 

rng = pd.date_range(min(yrs)[0], max(yrs)[1])
ts = pd.DataFrame(range(len(rng)), index=rng)
dat = pd.merge(ts, dat, how="outer",on=None, left_index=True, right_index=True)

dat["Mileage"].fillna(0, None, 0, True)

dat.sort_index(0, None, True, True, "quicksort", "last")
with PdfPages("./bikeMileage/plots.pdf") as pdf:
    for i, yr in enumerate(yrs):
        frm = yrs[i][0]
        to = yrs[i][1]
        yr = frm.split("-")[0]
        dat.loc[frm:to, "CumulativeMileage"] = dat.loc[frm:to,"Mileage"].cumsum()
        yearly = dat[frm:to]
        ax = plt.figure(figsize=(10,7)).add_subplot(111)
        axarr12 = ax.twinx()
        lab_pos = 0.9
        print yr + " Mileage"  
        for j, bike in enumerate(bikes):
            tmp = dat[dat["Bike"] == bike]
            tmp = tmp[frm:to]
            total_mileage = tmp["Mileage"].sum()
    #         print "is null? " + str(pd.isnull(total_mileage))
            if total_mileage == 0: continue 
            tmp = pd.merge(ts, tmp, how="outer",on=None, left_index=True, right_index=True)
            print "\t" + bike + ": " + str(total_mileage)
            ax.bar(pd_to_plt(tmp.index), tmp["Mileage"], width=1.5, label=bike, color=colrs[j], edgecolor=colrs[j])
            plt.text(0.05,
                     lab_pos,
                     bike + ": " + str(total_mileage),
                     ha='left',
                     va='center',
                     color=colrs[j],
                     transform=ax.transAxes,
                     size=10,
                     backgroundcolor="w")
            lab_pos = lab_pos-0.05
        plt.text(0.05,
                 lab_pos,
                 "Total: " + str(yearly["Mileage"].sum()),
                 ha='left',
                 va='center',
                 color='#551a8b',
                 transform=ax.transAxes,
                 fontsize=10,
                 backgroundcolor="w")
        axarr12.plot(pd_to_plt(yearly.index), yearly["CumulativeMileage"], color="#551a8b", label="Total", zorder=-30)  
        ax.set_ylabel("Miles", alpha=0.5, fontsize=10)
        ax.set_title("Bicycle Mileage for " + yr)
        plt.setp(ax.get_xticklabels(), rotation=20, fontsize=8)
        plt.setp(ax.get_yticklabels(), fontsize=8)
        plt.setp(axarr12.get_yticklabels(), fontsize=8)
        ax.grid(True)
        handles, labels = ax.get_legend_handles_labels()
        lgnd = ax.legend(handles, labels, fontsize=12)
        pdf.savefig()
        plt.close()
# plt.show()
# dat.loc[from2014:to2014, "CumulativeMileage"] = dat.loc[from2014:to2014,"Mileage"].cumsum()
# dat.loc[from2015:to2015,"CumulativeMileage"] = dat.loc[from2015:to2015, "Mileage"].cumsum()
dat.to_csv(path + "/bikeDat.csv")


# raise BaseException
# # datetime.datetime(int(str(dat.index).split("-")[0]), int(str(dat.index).split("-")[1]), int(str(dat.index).split("-")[2]))
# 
# 
# from2014 ="2014-03-01"
# to2014 = "2014-12-01"
# from2015 = "2015-03-01"
# to2015 = "2015-12-01"
# 
# 
# # won't need this, but should create a date col in unix time
# 
# #### temp df
# rng = pd.date_range("2014-01-01", "2015-12-31")#dat.index.iloc
# ts = pd.DataFrame(range(len(rng)),index=rng)
# 
# dat = pd.merge(ts, dat, how="outer",on=None, left_index=True, right_index=True)
# dat["Mileage"].fillna(0, None, 0, True)
# if os.name == "nt":
#     dat.sort_index(0, None, True, True, "quicksort", "last")
#     dat.loc[from2014:to2014, "CumulativeMileage"] = dat.loc[from2014:to2014,"Mileage"].cumsum()
#     dat.loc[from2015:to2015,"CumulativeMileage"] = dat.loc[from2015:to2015, "Mileage"].cumsum()
#     dat.to_csv(path + "/bikeDat.csv")
# 
# #### Plotting ####
# fuji = dat[dat["Bike"] == 'fuji']
# trek = dat[dat["Bike"] == 'trek']
# fuji = pd.merge(ts, fuji, how="outer",on=None, left_index=True, right_index=True)
# trek = pd.merge(ts, trek, how="outer",on=None, left_index=True, right_index=True)
# 
# fuji["Mileage"].fillna(0, None, 0, True)
# trek["Mileage"].fillna(0, None, 0, True)
# # dat["Mileage"].fillna(0, None, 0, True)
# 
# f, axarr = plt.subplots(2, 1, sharey=True)
# f.set_size_inches(11,7)
# 
# trek2014 = trek[from2014:to2014]["Mileage"].sum()
# trek2015 = trek[from2015:to2015]["Mileage"].sum()
# fuji2014 = fuji[from2014:to2014]["Mileage"].sum()
# fuji2015 = fuji[from2015:to2015]["Mileage"].sum()
# print "Trek mileage:\n" + "\t2014: " + str(trek2014) + "\t2015: " + str(trek2015) 
# print  "Fuji mileage:\n" + "\t2014: " + str(fuji2014) + "\t2015: " + str(fuji2015)
# 
# ## Top graph
# axarr[1].bar(pd_to_plt(trek[from2014:to2014].index), trek[from2014:to2014]["Mileage"],width=1.5, label="Trek")
# axarr[1].bar(pd_to_plt(fuji[from2014:to2014].index), fuji[from2014:to2014]["Mileage"],width=1.5, color='r', label="Fuji")
# axarr12 = axarr[1].twinx()
# 
# axarr12.plot(pd_to_plt(dat[from2014:to2014].index), dat["CumulativeMileage"][from2014:to2014], color="#551a8b", label="Total", zorder=-30)  
# axarr[1].set_ylabel("Miles", alpha=0.5, fontsize=10)
# plt.text(0.05, 0.9, "Trek: " + str(trek2014), ha='left', va='center', color="blue", transform=axarr[1].transAxes, size=10,backgroundcolor="w")
# plt.text(0.05, 0.8,"Fuji: " + str(fuji2014), ha='left', va='center', color='red', transform=axarr[1].transAxes, size=10,backgroundcolor="w")
# plt.text(0.05, 0.7,"Total: " + str(fuji2014 + trek2014), ha='left', va='center', color='#551a8b', transform=axarr[1].transAxes, size=10,backgroundcolor="w")
# # axarr[1].plot(pd_to_plt(dat[from2014:to2014].index),dat[from2014:to2014]["CumulativeMileage"])
# # barTrek = mpatches.Patch(color='blue', label="Trek")
# # barFuji = mpatches.Patch(color='red', label="Fuji")
# # plt.legend(handles=[barTrek, barFuji])
# axarr[0].bar(pd_to_plt(trek[from2015:to2015].index), trek[from2015:to2015]["Mileage"],width=1.5, zorder=3)
# axarr[0].bar(pd_to_plt(fuji[from2015:to2015].index), fuji[from2015:to2015]["Mileage"],width=1.5, color='r', zorder=3)
# axarr02 = axarr[0].twinx()
# 
# axarr02.plot(pd_to_plt(dat[from2015:to2015].index), dat["CumulativeMileage"][from2015:to2015], "#551a8b", zorder=-30)  
# axarr[0].set_ylabel("Miles", alpha=0.5, fontsize=10)
# plt.text(0.05, 0.9, "Trek: " + str(trek2015), ha='left', va='center', color="blue", transform=axarr[0].transAxes, fontsize=10,backgroundcolor="w")
# plt.text(0.05, 0.8,"Fuji: " + str(fuji2015), ha='left', va='center', color='red', transform=axarr[0].transAxes, fontsize=10,backgroundcolor="w")
# plt.text(0.05, 0.7,"Total: " + str(fuji2015 + trek2015), ha='left', va='center', color='#551a8b', transform=axarr[0].transAxes, fontsize=10,backgroundcolor="w")
# 
# plt.setp(axarr[0].get_xticklabels(), rotation=20, fontsize=8)
# plt.setp(axarr[0].get_yticklabels(), fontsize=8)
# plt.setp(axarr02.get_yticklabels(), fontsize=8)
# axarr[0].grid(True)
# # axarr[0].set_title("2014")
# plt.setp(axarr[1].get_xticklabels(), rotation=20, fontsize=8)
# plt.setp(axarr12.get_yticklabels(), fontsize=8)
# axarr[1].grid(True)
# 
# handles, labels = axarr[1].get_legend_handles_labels()
# lgnd = axarr[0].legend(handles, labels, fontsize=12)
# # lgnd.get_frame().set_facecolor('w')
# axarr[0].set_title("Bicycle Mileage")
# plt.savefig(path+"/BikePlot.pdf")
# # plt.show()
# ### for writing json:
# 
# # axarr[0, 0].bar(pd_to_plt(trek[from2014:to2014].index), trek[from2014:to2014]["Mileage"],width=1.5)
# # axarr[0, 0].set_title("Trek 2014")
# # axarr[0, 1].bar(pd_to_plt(trek[from2015:to2015].index), trek[from2015:to2015]["Mileage"],width=1.5)
# # axarr[0, 1].set_title("Trek 2015")
# # axarr[1, 0].bar(pd_to_plt(fuji[from2014:to2014].index), fuji[from2014:to2014]["Mileage"],width=1.5, color='r')
# # axarr[1, 0].set_title("Fuji 2014")
# # axarr[1, 1].bar(pd_to_plt(fuji[from2015:to2015].index), fuji[from2015:to2015]["Mileage"],width=1.5, color='r')
# # axarr[1, 1].set_title("Fuji 2015")
# # 
# # for i in [0,1]:
# #     for j in [0,1]:
# #         print str(i), str(j)
# #         axarr[i,j].xaxis_date()
# #         axarr[i,j].grid(True)
# #         plt.setp(axarr[i,j].get_xticklabels(), rotation=20)
# # #         for tick in axarr[i,j].get_xticklabels(): tick.set_rotation(45)
# #         
# # plt.show()        
# # axarr[0, 0].xaxis_date()
# # axarr[0, 1].xaxis_date()
# # axarr[1, 0].xaxis_date()
# # axarr[1, 1].xaxis_date()
# # print(type(axarr[0,0]))
# # 
# # axarr[0,0].set_xticks()
# # axarr[0,0].grid(True)
# # axarr[0,1].grid(True)
# # axarr[1,0].grid(True)
# # axarr[1,1].grid(True)
# 
# # axarr[0].plot_date(pd_to_plt(trek.index), trek["Mileage"], ".")
# # axarr[1].plot_date(pd_to_plt(fuji.index), fuji["Mileage"], ".", color='r')
# 
# 
# 
# 
# 
# 
# 
# # print "f is " + str(type(f))
# # print "axarr is " + str(type(axarr))
# 
# 
# 
# # 
# # axarr[0].plot(fuji.index, fuji["Mileage"])
# # axarr[0].set_title("Bike Plots")
# # axarr[1].plot(trek.index, trek["Mileage"])
# # plt.show()
# # #     
# # file_trek = "E:/miscFiles/Bike Log for Red Trek - Sheet1.tsv"
# # file_fuji = "E:/miscFiles/Bike Log for Red Fuji - Sheet1.tsv"
# #  
# # data_trek = pd.read_table(file_trek, sep= "\t")
# # data_fuji = pd.read_table(file_fuji, sep= "\t")
# # 
# # print data_trek.head()
# # print data_fuji.head()
# # 
# # 
# # data_trek["Date"].fillna("01.01.2014", None, 0, True)
# # data_fuji["Date"].fillna("01.01.2014", None, 0, True)
# # 
# # data_trek["Date"] = [time.strftime("%Y-%m-%d", time.strptime(dte, "%d.%m.%Y")) for dte in data_trek["Date"]]
# # data_fuji["Date"] = [time.strftime("%Y-%m-%d", time.strptime(dte, "%d.%m.%Y")) for dte in data_fuji["Date"]] 
# # 
# # data_fuji.set_index("Date", False, False, True)
# # data_trek.set_index("Date", False, False, True)
# # 
# # dat1 = pd.merge(data_fuji, data_trek, how="outer")
# # # dat1.to_csv("E:/miscFiles/OuterJoinTest.csv")
# # dat2 = data_fuji.append(data_trek)
# # 
# # # dat2.to_csv("E:/miscFiles/combineTest.csv")
# # print "Outer join:\t" + str(dat1["Mileage"].sum())
# # print "Combine:\t" + str(dat2["Mileage"].sum())
# # 
# # 
# # # print dat.head()
