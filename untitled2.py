# -*- coding: utf-8 -*-

import cartopy.crs as ccrs
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']   #显示图像中文
matplotlib.rcParams['axes.unicode_minus'] =False #显示图像负号

nc_obj = Dataset('IBTrACS.ALL.v04r00.nc')
# for i in nc_obj.variables.keys():
#     print(i)
# print('-------------------------------')

lat = nc_obj.variables['usa_lat'][:]
lon = nc_obj.variables['usa_lon'][:]
date = nc_obj.variables['iso_time'][:]
wind = nc_obj.variables['usa_wind'][:]
# print(nc_obj.variables['usa_wind'])

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

ty_needen = np.array(wind[begin:end,:]) #提取后的1989-2018 usa_wind
date_needen = np.array(date[begin:end,:])
lat = np.array(lat[begin:end,:])
lon = np.array(lon[begin:end,:])

num_i = []
ri = si = n = iw = 0
for i in range(0,len(ty_needen)):
    for j in range(0,360):
        try:
            if ty_needen[i,j] == -9999:
                continue
            else:
                q = ty_needen[i,j+8] - ty_needen[i,j]
                if q >= 30:
                    ri = ri + 1
                    num_i.append(i)   # RI型台风行位置
                    break
                elif 5 < q < 30:
                    si = si + 1
                    break
                elif -5 <= q <= 5:
                    n = 1 + n
                    break
                elif q < -5:
                    iw = iw + 1
                    break
        except:
            continue

#每一类占比
r_ri = ri/(ri+si+n+iw) * 100
print(r_ri)
r_si = si/(ri+si+n+iw)  * 100
print(r_si)
r_n = n/(ri+si+n+iw) * 100
print(r_n)
r_iw = iw/(ri+si+n+iw) * 100     
print(r_iw) 

plt.figure(num=3) # 各类型台风比例图
name_list = ['RI','SI','N','IW']
num = [r_ri,r_si,r_n,r_iw]
plt.bar(range(4), num, color = ['r','g','b','y'], tick_label=name_list)
plt.ylabel('台风个数占比(%)')
plt.xlabel('台风类型')
plt.show()

lon = lon[num_i]
lat = lat[num_i]
# 打1*1网格            
x = np.linspace(-180,180,361)   # lon: 1*1
y = np.linspace(90,-90,181)     # lat: 1*1
X,Y = np.meshgrid(x, y)         # 生成1*1网格

# 判断出台风路径所属格点位置
i_id = []
j_id = []
for i in range(77):
    for j in range(360):       
        if lon[i,j] == -9999:   #将缺测值（-9999）转为nan
            lon[i,j] = np.nan
            lat[i,j] = np.nan
        else:
            xi = yj = -1
            for xx in x:
                xi = xi + 1
                if xx - 0.5 < lon[i,j] <= xx + 0.5:                    
                    i_id.append(xi)   # 经度网格位置
                    break
            for yy in y:
                yj = yj + 1
                if yy - 0.5 < lat[i,j] <= yy + 0.5:
                    j_id.append(yj)   # 纬度网格位置
                    break

arr = np.array([j_id,i_id])  # 出现台风的格点
n = [j_id,i_id]

m_grids = np.transpose(arr)   # 出现台风的格点转置
grids = np.array(list(set([tuple(t) for t in m_grids]))) # 去重
gc = []
for grid in grids:
    count = 1
    for g in m_grids:
        if g[0] == grid[0] and g[1] == grid[1]:
            count += 1
    gc.append(count)  # 各格点计数


Z = np.full([181,361], np.nan) # 设置nan数组
for i in range(181):
    for j in range(361):
        r = -1
        for k in grids:
            r = r + 1
            if k[0] == i and k[1] == j:
                Z[i,j] = gc[r]

plt.figure(num=4) # 台风路径图
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))
ax.coastlines(resolution='110m')
plt.ylabel('纬度')
plt.xlabel('经度')
for i in range(77):
    plt.plot(lon[i,:],lat[i,:])
ax.set_xticks([0, -60, -120, 60, 120, 180, -180], crs=ccrs.PlateCarree())
ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
# plt.plot(X, Y, 
#           color='limegreen',  # 设置颜色为limegreen
#           marker='.',         # 设置点类型为圆点
#           linestyle='')       # 设置线型为空，也即没有线连接点
plt.grid(True)
plt.show()

plt.figure(num=5,figsize=(6, 4), dpi=100,clear=True)  # 台风次数图
ax = plt.axes(projection = ccrs.PlateCarree(central_longitude=0))
ax.coastlines(resolution = '110m')
fig = plt.contourf(X, Y, Z, 10,levels = [1,3,5,7,9,12])
ax.set_xticks([0, -60, -120, 60, 100,120, 140,160,180, -180], 
              crs = ccrs.PlateCarree())
ax.set_yticks([-90, -60, -30, 0,10,20,30,40,50, 90], crs = ccrs.PlateCarree())
plt.grid(True)
plt.xlim(100, 180)
plt.ylim(0, 50)
cbar = plt.colorbar(fig, orientation = 'horizontal',
                    fraction = 0.06, pad = 0.15) # fraction cbar相对长度，pad表示距离图片相对位置
cbar.set_label('次数(个)', fontproperties = 'SimHei')
plt.ylabel('纬度(°)')
plt.xlabel('经度(°)')
plt.show()