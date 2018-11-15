#此文件读取所有NetCdf格式的欧洲数值产品数据
#资料按要素按年，每月存放
# dimensions(sizes): longitude(121), latitude(95), level(18), time(1464)
# variables(dimensions): float32
# longitude(longitude), float32
# latitude(latitude), int32
# level(level), int32
# time(time), int16
# u(time, level, latitude, longitude)
from netCDF4 import Dataset
import numpy as np
import datetime
import  os

ecDirfile="d:\\EcData"#UV\\2016\\U_201611.nc"
##--------------------------------
##定义函数，根据气象要素标识，时间，读取指定范围的变量数据
##获取指定时间，指定高度层的，UV风的分量
##---------------------------------
def ReadECMeteDataUV(mtime,level):
    #根据输入构造指定文件名
    ufile=ecDirfile+"\\GKU\\"+"U"+mtime.strftime('%Y')+".nc"
    vfile=ecDirfile+"\\GKV\\"+"V"+mtime.strftime('%Y')+".nc"
    fh = Dataset(ufile, mode='r')
    # u(time,level,latitude,longitude)
    times = np.asarray(fh.variables["time"][:])
    #print(times)
    lons=(fh.variables["longitude"][:])
    lats=(fh.variables["latitude"][:])
    levels=np.asarray(fh.variables['level'][:])
    #print(levels)
    mL=np.where(levels==level)[0] #找到当前高度层索引
    #print(mL)
    #计算距标准时间的小时数
    td=(mtime-datetime.datetime(1900,1,1,0,0,0)).total_seconds()/3600
    # print(td)
    # print(times)
    mH=np.where(times==td)[0]
    #print(mH)
    vFh = Dataset(vfile, mode='r')
    if mH>=0 and mL>=0:
        uu = np.asarray(fh.variables["u"][mH,mL, :, :], np.float).squeeze()
        vv = np.asarray(vFh.variables["v"][mH, mL, :, :], np.float).squeeze()
    return lons,lats, uu,vv
#
def ReadECDivergenceData(mtime,level):
    ufile = ecDirfile + "\\Divergence\\" + "Divergence_" + mtime.strftime('%Y') + ".nc"
    fh = Dataset(ufile, mode='r')
    #print(fh)
    lons = (fh.variables["longitude"][:])
    levels = np.asarray(fh.variables['level'][:])
    times = np.asarray(fh.variables["time"][:])
    lats = (fh.variables["latitude"][:])
    mL = np.where(levels == level)[0]  # 找到当前高度层索引
    # 计算距标准时间的小时数
    td = (mtime - datetime.datetime(1900, 1, 1, 0, 0, 0)).total_seconds() / 3600
    mH = np.where(times == td)[0]
    diver = np.asarray(fh.variables["d"][mH, mL, :, :], np.float).squeeze()
    return lons, lats, diver
#读取指定时间，批定高度层的温度
def ReadECTempData(mtime,level):
    ufile = ecDirfile + "\\T\\" + "T" + mtime.strftime('%Y') + ".nc"
    fh = Dataset(ufile, mode='r')
    #print(fh)
    lons = (fh.variables["longitude"][:])
    levels = np.asarray(fh.variables['level'][:])
    times = np.asarray(fh.variables["time"][:])
    lats = (fh.variables["latitude"][:])
    mL = np.where(levels == level)[0]  # 找到当前高度层索引
    # 计算距标准时间的小时数
    td = (mtime - datetime.datetime(1900, 1, 1, 0, 0, 0)).total_seconds() / 3600
    mH = np.where(times == td)[0]
    temp = np.asarray(fh.variables["t"][mH, mL, :, :], np.float).squeeze()
    return lons, lats, temp
#读取批定时间批定高度层的相对湿度
def ReadECRHData(mtime,level):
    ufile = ecDirfile + "\\RH\\" + "RH" + mtime.strftime('%Y') + ".nc"
    fh = Dataset(ufile, mode='r')
    #print(fh)
    lons = (fh.variables["longitude"][:])
    levels = np.asarray(fh.variables['level'][:])
    times = np.asarray(fh.variables["time"][:])
    lats = (fh.variables["latitude"][:])
    mL = np.where(levels == level)[0]  # 找到当前高度层索引
    # 计算距标准时间的小时数
    td = (mtime - datetime.datetime(1900, 1, 1, 0, 0, 0)).total_seconds() / 3600
    mH = np.where(times == td)[0]
    rh = np.asarray(fh.variables["r"][mH, mL, :, :], np.float).squeeze()
    rh[rh < 0] = 0
    rh[rh>100]=100
    #print(fh.variables["r"])
    return lons, lats, rh

#print(fh.variables["longitude"][:])
#print(fh.variables["latitude"][:])
# time=(fh.variables["time"][:])  #units: hours since 1900-01-01 00:00:00.0
# now = datetime.datetime(1900,1,1)
# print(time.shape)
# hh=int(time[0])
# last_time = now + datetime.timedelta(hours=hh)
# print(last_time.strftime("%Y%m%d"))
