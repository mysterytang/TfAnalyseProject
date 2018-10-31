#-*- coding: utf-8 -*-
#此程序读取数值预报各要素场数据
#
import numpy as np
import matplotlib.pyplot as plt
import os
import struct
import  matplotlib.font_manager as fm
from mpl_toolkits.basemap import Basemap
#导入字体管理
myfont=fm.FontProperties(fname="C:\Windows\Fonts\STFANGSO.TTF")  #Matplotlib的字体管理   将字体路径复制到这里

#读取文件网格内，55X108网格点的浮点数，台风相关气象要素值
def ReadDatFile(file="",latCount=55,lonCount=108):
    if not os.path.exists(file):
        print("The path %s does not exist!" % file)
        return
    f = open(file, "rb+")
    paramCount=lonCount*latCount
    data_raw = struct.unpack('f' * paramCount, f.read(4 * paramCount))
    f.close()
    verify_data = np.asarray(data_raw).reshape(-1, lonCount)
    #print(np.shape(verify_data))
    return verify_data

#读取台风点概率分布图
#读取TXT格式的数据
def ReadTxtFile(file=""):
    data=np.loadtxt(file,dtype=np.float ,delimiter=',')
    #print(data.shape)
    return data


#利用wgrib.exe读取grib文件，但因数据文件太大，此方法取消
def ReadEcGribFile(file="",idx=0):
    file="D:\\ECWMF\\GK\\2016_full_pressure_levels.grib"
    outfilename="C:\\2016\\"+idx+".txt"
    #time='16102606'
    #cmdstr="C:\\TFProject\\wgrib\\wgrib.exe " + file + " | find \":d="+time+" :\"| "
    #msg=os.popen(cmdstr).readlines()
    os.system('C:\TFProject\wgrib\wgrib.exe ' + file + ' -s '+idx+' -text -nh -o ' + outfilename)
    f = open(outfilename, 'r')
    grds = f.read().strip()
    grds = grds.split('\n')
    data = np.array(grds)
    data.resize(55, 108)
    data = data.astype(float)
    return  data
#输入由C#生成的所有气象要素场的DAT文件#
#所有DAT文件为二进制数据，55X108个格点，
#将气象要素在地图场中绘制出来
def DrawDatFile(tfEcValues=[],u=[],v=[]):
    #此网格数据由C#输出程序设定
    lats = np.arange(0, 41, 0.75)  # 纬度间隔
    lons = np.arange(99.75, 180.5, 0.75) #经度间隔

    # lats = np.arange(0, 62, 2)  # 纬度间隔
    # lons = np.arange(90, 162, 2)
    m = Basemap(llcrnrlon=90, llcrnrlat=0, urcrnrlon=180, urcrnrlat=40, resolution='c', epsg=3415)
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    #print(np.squeeze(tfEcValues))
    cs = m.contour(xi, yi, np.squeeze(tfEcValues))
    cs = m.contourf(xi, yi, np.squeeze(tfEcValues))
    #b = m.barbs(xi, yi, u * 2.5, v * 2.5)

    # 绘制经纬线
    m.drawparallels(np.arange(0., 50., 5), labels=[1, 0, 0, 0], fontsize=10)
    m.drawmeridians(np.arange(90., 181., 5), labels=[0, 0, 0, 1], fontsize=10)

    # Add Coastlines, States, and Country
    m.drawcoastlines(color='tan')
    m.drawcountries()
    # Add Colorbar
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    # Add Title
    plt.title('气象要素场分布',fontsize=20, fontname='华文仿宋', fontproperties=myfont)
    plt.show()
def DrawTFStartPoint(tfEcValues=[]):
    #此网格数据由C#输出程序设定
    lats = np.arange(0, 62, 2)  # 纬度间隔
    lons = np.arange(90, 162, 2)
    m = Basemap(llcrnrlon=90, llcrnrlat=0, urcrnrlon=180, urcrnrlat=40, resolution='c', epsg=3415)
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    #print(np.squeeze(tfEcValues))
    #cs = m.contour(xi, yi, np.squeeze(tfEcValues))
    cs = m.contourf(xi, yi, np.squeeze(tfEcValues))
    # 绘制经纬线
    m.drawparallels(np.arange(0., 50., 5), labels=[1, 0, 0, 0], fontsize=10)
    m.drawmeridians(np.arange(90., 181., 5), labels=[0, 0, 0, 1], fontsize=10)

    # Add Coastlines, States, and Country
    m.drawcoastlines(color='tan')
    m.drawcountries()
    # Add Colorbar
    cbar = m.colorbar(cs, location='bottom', pad="10%")
    # Add Title
    plt.title('台风（TS）生成点位置分布',fontsize=20, fontname='华文仿宋', fontproperties=myfont)
    plt.show()
#绘制风场
def DrawEcUV(uu=[],vv=[]):
    lats = np.arange(0, 41, 0.75)  # 纬度间隔
    lons = np.arange(99.75, 180.5, 0.75)
    m = Basemap(llcrnrlon=90, llcrnrlat=0, urcrnrlon=180, urcrnrlat=40, resolution='c', epsg=3415)
    lon, lat = np.meshgrid(lons, lats)
    xi, yi = m(lon, lat)
    m.drawcoastlines(color='tan')
    # print(xi.shape())
    # print(yi.shape())
    b = m.barbs(xi, yi, uu , vv)
    plt.show()
# tfEcValues=ReadEcGribFile()
# print(np.shape(tfEcValues))
#------------------------------------------------------
# 读取自己输出的二进制测试文件
mfile = "C:\\TFProject\\20161026\\Geopotential_2016102600_200.dat"
txtfile="C:\TFProject\输出要素\TfClimate(TD1).txt"
txtfile2="C:\TFProject\输出要素\TfClimate(TS).txt"
# 读取了此文件的数据
#tfEcValues = ReadDatFile(mfile)
tfEcValues = ReadTxtFile(txtfile)
tfEcValues_ts = ReadTxtFile(txtfile2)
#DrawTFStartPoint(tfEcValues)
DrawTFStartPoint(tfEcValues)
# a=np.max(tfEcValues)
# b=np.max(tfEcValues_ts)
# print(a)
# print(b)


#----------------------------------------------------------
# ufile = "C:\\TFProject\\20161026\\U velocity_2016102606_500.dat"
# uuValues = ReadDatFile(ufile)
# vfile = "C:\\TFProject\\20161 6\\V velocity_2016102606_500.dat"
# vvValues = ReadDatFile(vfile)

#
# uuValues=np.ones(108*55)
# uuValues.reshape(55,108)
# vvValues=np.ones(108*55)
# vvValues.reshape(55,108)
# DrawEcUV(uu=uuValues,vv=vvValues)

# uu=ReadEcGribFile()
# vv=ReadEcGribFile()
#
# print(uuValues[10,:])
# print(vvValues[10,:])
# #DrawDatFile(tfEcValues)