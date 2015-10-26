import os
import pandas as pd
import matplotlib.pyplot as plt
import time
import datetime

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
	path = "C:/Users/devans/bikeMileage"
else:
	path = "/home/devans/Documents/bikeMileage"

miscFiles = os.listdir(path)
bikes = ["fuji", "trek"]
# dat = pd.DataFrame()
for i, bike in enumerate(bikes):
#     print "Working on " + str(i) + " and the " + bike
    targ = [fl for fl in miscFiles if bike in fl][0]
    tmp = pd.read_table(path + "/" + targ, sep="\t")
    tmp["Bike"] = bike
    tmp["Date"].fillna("01.01.2014", None, 0, True)
    tmp["Date"] = [time.strftime("%Y-%m-%d", time.strptime(dte, "%d.%m.%Y")) for dte in tmp["Date"]]
#     print tmp.head()
    if (i == 0):
        dat = tmp
    else: 
        dat = dat.append(tmp)

dat.set_index("Date", True, False, True)

print("Total mileage: " + str(dat["Mileage"].sum()))

if os.name == "nt":
	dat.sort_index(0, None, True, True, "quicksort", "last")
dat.to_csv(path + "/bikeDat.csv")
# won't need this, but should create a date col in unix time
#for creating json:
# f = open("bikeDat.json", "wt")
# f.write("[")
# txt = "\n"
# for rw in range(len(dat)):
# 	print "Row:",rw
# 	for cl in dat:
#		print "Col: " + str(cl)
#		txt = txt + cl + ":[" + str(dat[cl][rw]) + "],"
#	txt = "{" + txt[:-1] + "},"
#	if rw == len(dat):
#		txt = txt[:-1]
#	f.write(txt)
#	txt = "\n"
#
#f.write("]\n")
#f.close()
#### temp df
rng = pd.date_range("2014-01-01", "2015-12-31")#dat.index.iloc
ts = pd.DataFrame(range(len(rng)),index=rng)

dat = pd.merge(ts, dat, how="outer",on=None, left_index=True, right_index=True)

#### Plotting ####
fuji = dat[dat["Bike"] == 'fuji']
trek = dat[dat["Bike"] == 'trek']
fuji = pd.merge(ts, fuji, how="outer",on=None, left_index=True, right_index=True)
trek = pd.merge(ts, trek, how="outer",on=None, left_index=True, right_index=True)

fuji["Mileage"].fillna(0, None, 0, True)
trek["Mileage"].fillna(0, None, 0, True)
# dat["Mileage"].fillna(0, None, 0, True)

f, axarr = plt.subplots(2, 1, sharey=True)
f.set_size_inches(11,7)
# raise
from2014 ="2014-03-01"
to2014 = "2014-12-01"
from2015 = "2015-03-01"
to2015 = "2015-11-01"

trek2014 = trek[from2014:to2014]["Mileage"].sum()
trek2015 = trek[from2015:to2015]["Mileage"].sum()
fuji2014 = fuji[from2014:to2014]["Mileage"].sum()
fuji2015 = fuji[from2015:to2015]["Mileage"].sum()
print "Trek mileage:\n" + "\t2014: " + str(trek2014) + "\t2015: " + str(trek2015) 
print  "Fuji mileage:\n" + "\t2014: " + str(fuji2014) + "\t2015: " + str(fuji2015)


axarr[1].bar(pd_to_plt(trek[from2014:to2014].index), trek[from2014:to2014]["Mileage"],width=1.5, label="Trek")
axarr[1].bar(pd_to_plt(fuji[from2014:to2014].index), fuji[from2014:to2014]["Mileage"],width=1.5, color='r', label="Fuji")
axarr[1].set_ylabel("Miles", alpha=0.5)
plt.text(0.1, 0.9, "Trek: " + str(trek2014), ha='center', va='center', color="blue", transform=axarr[1].transAxes)
plt.text(0.1, 0.8,"Fuji: " + str(fuji2014), ha='center', va='center', color='red', transform=axarr[1].transAxes)
# barTrek = mpatches.Patch(color='blue', label="Trek")
# barFuji = mpatches.Patch(color='red', label="Fuji")
# plt.legend(handles=[barTrek, barFuji])
axarr[0].bar(pd_to_plt(trek[from2015:to2015].index), trek[from2015:to2015]["Mileage"],width=1.5)
axarr[0].bar(pd_to_plt(fuji[from2015:to2015].index), fuji[from2015:to2015]["Mileage"],width=1.5, color='r')
axarr[0].set_ylabel("Miles", alpha=0.5)
plt.text(0.1, 0.9, "Trek: " + str(trek2015), ha='center', va='center', color="blue", transform=axarr[0].transAxes)
plt.text(0.1, 0.8,"Fuji: " + str(fuji2015), ha='center', va='center', color='red', transform=axarr[0].transAxes)

plt.setp(axarr[0].get_xticklabels(), rotation=20)
axarr[0].grid(True)
# axarr[0].set_title("2014")
plt.setp(axarr[1].get_xticklabels(), rotation=20)
axarr[1].grid(True)

handles, labels = axarr[1].get_legend_handles_labels()
axarr[0].legend(handles, labels)
axarr[0].set_title("Bicycle Mileage")
plt.savefig(path+"/BikePlot.pdf")
# plt.show()
### for writing json:

# axarr[0, 0].bar(pd_to_plt(trek[from2014:to2014].index), trek[from2014:to2014]["Mileage"],width=1.5)
# axarr[0, 0].set_title("Trek 2014")
# axarr[0, 1].bar(pd_to_plt(trek[from2015:to2015].index), trek[from2015:to2015]["Mileage"],width=1.5)
# axarr[0, 1].set_title("Trek 2015")
# axarr[1, 0].bar(pd_to_plt(fuji[from2014:to2014].index), fuji[from2014:to2014]["Mileage"],width=1.5, color='r')
# axarr[1, 0].set_title("Fuji 2014")
# axarr[1, 1].bar(pd_to_plt(fuji[from2015:to2015].index), fuji[from2015:to2015]["Mileage"],width=1.5, color='r')
# axarr[1, 1].set_title("Fuji 2015")
# 
# for i in [0,1]:
#     for j in [0,1]:
#         print str(i), str(j)
#         axarr[i,j].xaxis_date()
#         axarr[i,j].grid(True)
#         plt.setp(axarr[i,j].get_xticklabels(), rotation=20)
# #         for tick in axarr[i,j].get_xticklabels(): tick.set_rotation(45)
#         
# plt.show()        
# axarr[0, 0].xaxis_date()
# axarr[0, 1].xaxis_date()
# axarr[1, 0].xaxis_date()
# axarr[1, 1].xaxis_date()
# print(type(axarr[0,0]))
# 
# axarr[0,0].set_xticks()
# axarr[0,0].grid(True)
# axarr[0,1].grid(True)
# axarr[1,0].grid(True)
# axarr[1,1].grid(True)

# axarr[0].plot_date(pd_to_plt(trek.index), trek["Mileage"], ".")
# axarr[1].plot_date(pd_to_plt(fuji.index), fuji["Mileage"], ".", color='r')







# print "f is " + str(type(f))
# print "axarr is " + str(type(axarr))



# 
# axarr[0].plot(fuji.index, fuji["Mileage"])
# axarr[0].set_title("Bike Plots")
# axarr[1].plot(trek.index, trek["Mileage"])
# plt.show()
# #     
# file_trek = "E:/miscFiles/Bike Log for Red Trek - Sheet1.tsv"
# file_fuji = "E:/miscFiles/Bike Log for Red Fuji - Sheet1.tsv"
#  
# data_trek = pd.read_table(file_trek, sep= "\t")
# data_fuji = pd.read_table(file_fuji, sep= "\t")
# 
# print data_trek.head()
# print data_fuji.head()
# 
# 
# data_trek["Date"].fillna("01.01.2014", None, 0, True)
# data_fuji["Date"].fillna("01.01.2014", None, 0, True)
# 
# data_trek["Date"] = [time.strftime("%Y-%m-%d", time.strptime(dte, "%d.%m.%Y")) for dte in data_trek["Date"]]
# data_fuji["Date"] = [time.strftime("%Y-%m-%d", time.strptime(dte, "%d.%m.%Y")) for dte in data_fuji["Date"]] 
# 
# data_fuji.set_index("Date", False, False, True)
# data_trek.set_index("Date", False, False, True)
# 
# dat1 = pd.merge(data_fuji, data_trek, how="outer")
# # dat1.to_csv("E:/miscFiles/OuterJoinTest.csv")
# dat2 = data_fuji.append(data_trek)
# 
# # dat2.to_csv("E:/miscFiles/combineTest.csv")
# print "Outer join:\t" + str(dat1["Mileage"].sum())
# print "Combine:\t" + str(dat2["Mileage"].sum())
# 
# 
# # print dat.head()
