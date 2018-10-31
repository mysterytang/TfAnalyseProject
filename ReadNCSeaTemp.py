#
#此文件读取NC数据中，全球各月的海面平均温度值
## lons,lats,temp=ReadNcSeaData(month=7)
# DrawSeaTempOnMap(lons,lats,temp)
#
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
#
#提取批定月份的海平面温度场数据
#此处人为设定了区域为，经度100-160 纬度0-50度
def ReadNcSeaData(file="",month=1):
    file="C:/Users/Administrator/PycharmProjects/ReadNCProject/data/data.nc"
    fh = Dataset(file,mode='r')
    # locTemp=tempData[11,1,90:130,280:340]
    #print(fh.variables['Z'])
    # np.savetxt("C:\\12月海面平均温度.txt",locTemp,fmt='%.1f')
    # 获取每个变量的值
    lons = fh.variables['X'][100:160]  #从东经100度开始 100度至160
    lats = fh.variables['Y'][90:140]  #北纬0.5度至39.5
    tlml = fh.variables['temp'][month-1,1,90:140,100:160]

    # lons = fh.variables['X'][:]  #从东经100度开始 100度至140
    # lats = fh.variables['Y'][:]  # 北纬0.5度至39.5
    # tlml = fh.variables['temp'][month - 1, 1, :,:]
    print(tlml.shape)
    fh.close()
    return  lons,lats,tlml

    # Plot Data
    # 这里我的tlml数据是24小时的，我这里只绘制第1小时的（tlml_0）
    #tlml_0 = tlml[1,1,:,:]
def DrawECParamOnMap(lons, lats, tlml,title="EC Data Map"):
    #m=Basemap(llcrnrlon = 90, llcrnrlat = 0, urcrnrlon = 180, urcrnrlat =40,resolution = 'c', epsg = 3415)
    m = Basemap(llcrnrlon=90, llcrnrlat=0, urcrnrlon=180, urcrnrlat=40, resolution='c', epsg=3415)
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    cs = m.pcolor(xi, yi,np.squeeze(tlml))
    m.drawparallels(np.arange(0., 50., 5), labels=[1,0,0,0], fontsize=10)
    m.drawmeridians(np.arange(90., 181., 5), labels=[0,0,0,1], fontsize=10)
    m.drawcoastlines()
    m.drawcountries()
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    plt.title(title)
    plt.show()

# lons,lats,temp=ReadNcSeaData(month=7)
# #print(lons)
# print(temp.shape)
# DrawSeaTempOnMap(lons,lats,temp)

