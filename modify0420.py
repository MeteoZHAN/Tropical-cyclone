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


ty_needen = np.array(wind[begin:end,:])    # 提取后的1989-2018 usa_wind
date_needen = np.array(date[begin:end,:])  # 提取后的1989-2018 date
lat = np.array(lat[begin:end,:])           # 提取后的1989-2018 lat
lon = np.array(lon[begin:end,:])           # 提取后的1989-2018 lon

ty_wp = []
date_wp = []
lat_wp = []
lon_wp = []
for i in range(3208):
    for j in range(360):
        if (100 < lon[i,j] < 180) and (0 < lat[i,j] < 50): #选定空间范围内的所有台风
            ty_wp.append(ty_needen[i,:])
            date_wp.append(date_needen[i,:])
            lat_wp.append(lat[i,:])
            lon_wp.append(lon[i,:])
            break

ty_wp = np.array(ty_wp)   # 西太1989-2018年 usa_wind数据
date_wp = np.array(date_wp)  # 西太1989-2018年 时间数据
lat_wp = np.array(lat_wp)  # 西太1989-2018年 纬度数据
lon_wp = np.array(lon_wp)  # 西太1989-2018年 经度数据

num_i = []
num_j = []
count_00 = 0
ri = si = nn = iw = 0
for i in range(0,len(ty_wp)):
    for j in range(0,360):
        try:
            if ty_wp[i,j] == -9999:
                continue
            else:
                if all(date_wp[i,j,11:13] == [b'0',b'0']) and \
                    all(date_wp[i,j+8,11:13] == [b'0',b'0']):
                    count_00 = count_00 + 1  # 记录总共有几个00-00时台风，其值与ri+si+nn+iw相等
                    q = ty_wp[i,j+8] - ty_wp[i,j]
                    if q >= 30:
                        ri = ri + 1
                        num_i.append(i)   # 记录RI型台风行位置 i
                        num_j.append(j)   # 记录RI型台风行位置 j
                    elif 5 < q < 30:
                        si = si + 1
                        num_i.append(i)   # 记录SI型台风行位置 i
                        num_j.append(j)   # 记录SI型台风行位置 j
                    elif -5 <= q <= 5:
                        nn = nn + 1                        
                    elif q < -5:
                        iw = iw + 1                        
        except:
            continue

# 每一类占比
r_ri = ri/(ri+si+nn+iw) * 100
print('RI型占比：',r_ri)
r_si = si/(ri+si+nn+iw)  * 100
print('SI型占比:',r_si)
r_n = nn/(ri+si+nn+iw) * 100
print('N型占比:',r_n)
r_iw = iw/(ri+si+nn+iw) * 100     
print('IW型占比:',r_iw) 

plt.figure(num=3) # 各类型台风比例图
name_list = ['RI','SI','N','IW']
num = [r_ri,r_si,r_n,r_iw]
plt.bar(range(4), num, color = ['r','g','b','y'], tick_label=name_list)
plt.ylabel('台风个数占比(%)')
plt.xlabel('台风类型')
plt.show()

num_i = np.array(num_i)
num_j = np.array(num_j)
lon_wp_i = lon_wp[num_i,num_j]  # 经度
lat_wp_j = lat_wp[num_i,num_j]  # 纬度

# 打1*1网格            
x = np.linspace(-180,180,361)   # lon: 1*1
y = np.linspace(90,-90,181)     # lat: 1*1
X,Y = np.meshgrid(x, y)         # 生成1*1网格

# 判断出台风路径所属格点位置
i_id = []
j_id = []
for i in range(len(lon_wp_i)):
    xi = yj = -1
    for xx in x:
        xi = xi + 1
        if xx - 0.5 < lon_wp_i[i] <= xx + 0.5:
            i_id.append(xi)   # 经度网格位置
            break
    for yy in y:
        yj = yj + 1
        if yy - 0.5 < lat_wp_j[i] <= yy + 0.5:
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

# plt.figure(num = 4) # 台风路径图
# ax = plt.axes(projection = ccrs.PlateCarree(central_longitude = 0))
# ax.coastlines(resolution = '110m')
# plt.ylabel('纬度')
# plt.xlabel('经度')
# for i in range(11):
#     plt.plot(lon[i,:],lat[i,:])
# ax.set_xticks([0, -60, -120, 60, 120, 180, -180], crs = ccrs.PlateCarree())
# ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs = ccrs.PlateCarree())
# # plt.plot(X, Y, 
# #           color='limegreen',  # 设置颜色为limegreen
# #           marker='.',         # 设置点类型为圆点
# #           linestyle='')       # 设置线型为空，也即没有线连接点
# plt.grid(True)
# plt.show()

plt.figure(num=5,figsize=(6, 4), dpi=100, clear=True)  # 台风次数图
ax = plt.axes(projection = ccrs.PlateCarree(central_longitude=0))
ax.coastlines(resolution = '110m')
fig = plt.contourf(X, Y, Z, 10, cmap='viridis_r') # 参数10为色阶密集程度，0为一分为二
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