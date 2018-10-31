from ReadEC_netcdfData import  *
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from ReadNCSeaTemp import  DrawECParamOnMap

def DrawUVMap(lons,lats,uu,vv,title=""):
    m = Basemap(llcrnrlon=90, llcrnrlat=0, urcrnrlon=180, urcrnrlat=40, resolution='c', epsg=3415)
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    m.barbs(xi,yi,uu,vv,length=3,linewidth=0.6,pivot='middle')
    # cs = m.pcolor(xi, yi, np.squeeze(tlml))
    m.drawparallels(np.arange(0., 50., 5), labels=[1, 0, 0, 0], fontsize=10)
    m.drawmeridians(np.arange(90., 181., 5), labels=[0, 0, 0, 1], fontsize=10)
    m.drawcoastlines()
    m.drawcountries()
    # cbar = m.colorbar(cs, location='bottom', pad="10%")
    plt.title(title)
    plt.show()

#此函数计算批定时间的风切变，及显示风切变分布图
def CacuVshearAndMap(mTime):
    #读取资料的时间
    mTime=datetime.datetime(2016,8,17,12,0,0)
    mLevel=850
    #读取，此时间和高度层的，风的UV分量。
    lons,lats,uu850,vv850=ReadECMeteDataUV(mTime,mLevel)
    size=uu850.shape
    mLevel=200
    lons,lats,uu200,vv200=ReadECMeteDataUV(mTime,mLevel)
    #在此计算各位置点的风切变
    vshear=np.zeros(size)  #风切变存储变量
    dxy=8#单点计算范围是，此点位置的前后dxy个格点
    for i in np.arange(dxy,size[0]-dxy,1):
        for j in np.arange(dxy,size[1]-dxy,1):
            #开始每个点计算风切变值print(i,j)
            u850=uu850[i-dxy:i+dxy,j-dxy:j+dxy]
            v850 =vv850[i - dxy:i + dxy, j - dxy:j + dxy]
            u200 = uu200[i - dxy:i + dxy, j - dxy:j + dxy]
            v200 = vv200[i - dxy:i + dxy, j - dxy:j + dxy]
            vsh=np.mean(np.sqrt((u850-u200)*(u850-u200)+(v850-v200)*(v850-v200)))
            vshear[i,j]=vsh

    #完成计算风切变值
    print(np.max(vshear))
    print(np.mean(vshear))
    DrawECParamOnMap(lons, lats, vshear,mTime.strftime("%Y-%m-%d")+"风切变分布图")
    #DrawUVMap(lons,lats,uu850,vv850,mTime.strftime("%Y-%m-%d")+" 850hPa风场")
#此函数计算850hPa环流强度
def CacuCIRCAndMap(mTime):
    mLevel = 850
    # 读取，此时间和高度层的，风的UV分量。
    lons, lats, uu850, vv850 = ReadECMeteDataUV(mTime, mLevel)
    size = uu850.shape
    #print(lats.shape)
    # 在此计算各位置点的风切变
    circValue = np.zeros(size)
    dxy = 6  # 单点计算范围是，此点位置的前后6个格点
    for i in np.arange(dxy, size[0] - dxy, 1):  #纬度
        for j in np.arange(dxy, size[1] - dxy, 1): #经度
            #左边 西
            ua =np.squeeze(uu850[i + dxy:i + dxy+1, j - dxy:j + dxy]).sum()
            uc=np.squeeze(uu850[i - dxy:i - dxy+1, j - dxy:j + dxy]).sum()
            vb=np.squeeze(vv850[i-dxy:i+dxy,i+dxy:i+dxy+1]).sum()
            vd = np.squeeze(vv850[i - dxy:i + dxy, i - dxy:i - dxy + 1]).sum()
            circValue[i,j]=ua+vb-uc-vd

    #绘制环流强度分布图
    print(np.max(circValue))
    print(np.mean(circValue))
    DrawECParamOnMap(lons, lats, circValue, mTime.strftime("%Y-%m-%d") + "环流强度分布图")


def CacuDivergenceAndMap(mTime):
    mLevel=850
    lons, lats, diver = ReadECDivergenceData(mTime, mLevel)
    DrawECParamOnMap(lons, lats, diver, mTime.strftime("%Y-%m-%d") + " 850hPa散度分布图")

mTime=datetime.datetime(2016,8,17,12,0,0)
#CacuDivergenceAndMap(mTime)
CacuCIRCAndMap(mTime)
#DrawUVMap(lons,lats,uu200,vv200,mTime.strftime("%Y-%m-%d")+" 200hPa风场")
#print(vshear)
# print(lats.shape)
# print(uu)
# print(vv)


