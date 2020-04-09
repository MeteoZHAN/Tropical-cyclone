# -*- coding: utf-8 -*-

from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
# import numpy.ma as ma
from pylab import *
mpl.rcParams['font.sans-serif']=['SimHei']

nc_obj = Dataset('IBTrACS.ALL.v04r00.nc')
# print(nc_obj)
# print('------------------------------')
# 查看nc文件中的变量
# print(nc_obj.variables.keys())

lat = nc_obj.variables['usa_lat'][:]
lon = nc_obj.variables['usa_lon'][:]
date = nc_obj.variables['iso_time'][:]
wind = nc_obj.variables['usa_wind'][:]
print(nc_obj.variables['usa_wind'])

# 1989-2018 对应数据存储范围 begin end分别为开始结束行
for i in range(0, len(date)):
    try:
        if int(date[i,1,0]) == 1 and int(date[i,1,1]) == 9 \
            and int(date[i,1,2]) == 8 and int(date[i,1,3]) == 9:
                begin = i
                break
    except:
        continue

for i in range(0, len(date)):
    try:
        if int(date[i,1,0]) == 2 and int(date[i,1,1]) == 0 \
            and int(date[i,1,2]) == 1 and int(date[i,1,3]) == 9:
                end = i
                break
    except:
        continue

ty_needen = wind[begin:end,:] #提取后的1989-2018 usa_wind
date_needen = date[begin:end,:]
# print(date_needen[3207,1,:])

year = [0]
for i in range(1, len(date_needen)):
    try:
        if int(date_needen[i-1,1,3]) != int(date_needen[i,1,3]):
            year.append(i)            
    except:
        continue
year.append(len(date_needen)+1)

c4 = []
c5 = []
c = []
for k in range(0,30):    
    count4 = 0
    count5 = 0
    count = 0
    for i in range(year[k],year[k+1]-1):                
        for w in ty_needen[i,:]:
            if w >= 113 and w < 137:
                count4 = count4 + 1
                break               
        for w in ty_needen[i,:]:
            if w >= 137:
                count5 = count5 + 1
                break    
        for w in ty_needen[i,:]:
            if w > 0:
                count = count + 1
                break
    c5.append(count5)
    c4.append(count4)
    c.append(count)
    
x = range(1989,2019)


x1 = np.arange(1989,2019,1)

z1 = np.polyfit(x, c4, 1)
y1 = z1[0]*x1 + z1[1]

z2 = np.polyfit(x, c5, 1)
y2 = z2[0]*x1 + z2[1]

c4_np = np.array(c4)
c5_np = np.array(c5)
c4_and_c5 = c4_np + c5_np
z4_5 = np.polyfit(x, c4_and_c5, 1)
y4_5 = z4_5[0]*x1 + z4_5[1]


font1 = {'family':'SimHei','weight':'normal','size':10}
font2 = {'family':'Times New Roman','weight':'normal','size':10}

plt.figure(num=1)
plt.plot(x1,y1,'k--')
plt.plot(x,c4,'ko-',label='usa_wind TY-4')
plt.plot(x1,y2,'k--')
plt.plot(x,c5,'k*-',label='usa_wind TY-5')
plt.xlabel('Year',font2)
plt.ylabel('Typhoon frequency of 4-5 classes',font2)
plt.legend(prop = font2)
#设置坐标刻度值的大小以及刻度值的字体
ax = plt.gca()
plt.tick_params(labelsize = 12)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.show()

z3 = np.polyfit(x, np.array(c4)/np.array(c)*100, 1)
x1 = np.arange(1989,2019,1)
y3 = z3[0]*x1 + z3[1]
z4 = np.polyfit(x, np.array(c5)/np.array(c)*100, 1)
y4 = z4[0]*x1 + z4[1]

plt.figure(num=2)
plt.plot(x,y3,'k--')
plt.plot(x,np.array(c4)/np.array(c)*100,'ko-',label='usa_wind TY-4')
plt.plot(x,y4,'k--')
plt.plot(x,np.array(c5)/np.array(c)*100,'k*-',label='usa_wind TY-5')
plt.xlabel('Year',font2)
plt.ylabel('Proportion of 4-5 typhoons (%)',font2)
plt.legend(prop = font2)
#设置坐标刻度值的大小以及刻度值的字体
ax = plt.gca()
plt.tick_params(labelsize = 12)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.show()

plt.figure(num=3)
plt.plot(x1,y4_5,'k--')
plt.plot(x,c4_and_c5,'ko-',label = 'usa_wind TY-4 and TY-5')
plt.xlabel('Year',font2)
plt.ylabel('Typhoon total frequency of 4-5 classes',font2)
plt.legend(prop = font2)
#设置坐标刻度值的大小以及刻度值的字体
ax = plt.gca()
plt.tick_params(labelsize = 12)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.show()

plt.figure(num=4)
z444 = np.polyfit(x, c4_and_c5/np.array(c)*100, 1)
y444 = z444[0]*x1 + z444[1]
plt.plot(x,y444,'k--')
plt.plot(x,c4_and_c5/np.array(c)*100,'ko-',label='usa_wind TY-4 and TY-5')
plt.xlabel('Year',font2)
plt.ylabel('Proportion of 4-5 typhoons (%)',font2)
plt.legend(prop = font2)
#设置坐标刻度值的大小以及刻度值的字体
ax = plt.gca()
plt.tick_params(labelsize = 12)
labels = ax.get_xticklabels() + ax.get_yticklabels()
[label.set_fontname('Times New Roman') for label in labels]
plt.show()

