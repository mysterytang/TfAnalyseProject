#输出台风生成预报有关的指标数据
#--------------------------------------------
#输出指标说明
#•	Lat  各点的纬度，直接根据坐标读取
#•	PLAND形成单独文件，与EC网格相同                完成
#•	DSTRM  与已存在TC的距离
#•	CSST  海表面温度，已有月平均值数据，直接读取      完成
#-------------------
#•	VSHEAR 风切变，，能过函数计算                  完成
#•	CIRC 850环流指数  通过函数计算                  完成
#•	HDIV（低层辐合辐散） 850hPa散度替换              完成
#---------------------------------
#•	BTWARM（无云水汽亮温）
#•	PCCOLD（冷云像素覆盖百分比）
#•	CPROB（24hTC形成气候概率）
import os
import datetime
import  h5py
import struct
from DrawDataOnMap import *
from calendar import monthrange
startYear=2000  #计算开始年
endYear=2001    #计算结束年

#通过EC场计算月平均风切变场
def saveTfparamstofile(mtime, vsh1, param):
    #将此变量保存至文件
    savedir="D:\\TF_ECOutput\\"+param+"\\"+str(mtime.year)+"\\"+str(mtime.month)
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    #保存至文件中
    file=savedir+"\\"+param+"_"+mtime.strftime('%Y-%m-%d-%H')+".hdf"
    hf = h5py.File(file, 'w')
    # 保存各通道数据
    hf.create_dataset('VAL', data=vsh1)
    hf.close()
    #以二进制形式存贮
    # with open(file, 'wb')as fp:
    #     for row in vsh1:
    #         for x in row:
    #             a = struct.pack('f', x)
    #             fp.write(a)

    #重新读取
#计算风切变指标
def run_ec_tf_all_vshear():
    #分别计算每个月的平均值
    #数据网格大小为95, 121
    for mon in range(1,13,1):
        saveHdfFile ='D:\\TF_ECOutput\\vshear\\vshear_men_'+str(mon)+".hdf"
        vshearSum=np.zeros((95,121),dtype=float)
        ncount=0
        for year in range(startYear, endYear, 1):
            print("开始计算" + str(year) + "年")
            mtime=datetime.datetime(year,mon,1)
            endtime=mtime+datetime.timedelta(days=monthrange(year,mon)[1])
            #print(endtime.strftime('%Y-%m-%d'))
            #读取当年此月的所有数据
            while mtime<endtime :
                print("开始读取"+mtime.strftime('%Y-%m-%d-%H'))
                lat,lon,vsh1 = GetvshearByTime(mtime)

                #此处也要保存每日，时次数据
                saveTfparamstofile(mtime,vsh1,"vshear")

                vshearSum=vshearSum+vsh1  #累加所有时次
                ncount=ncount+1           #共有多少个时次
                mtime=mtime+datetime.timedelta(hours=6)
        #将累年值，绘图，并保存至文件中
        vshearSum=vshearSum/ncount
        hf = h5py.File(saveHdfFile, 'w')
        # 保存各通道数据
        hf.create_dataset('VSHEAR', data=vshearSum)
        hf.create_dataset('Lat', data=lat)
        hf.create_dataset('Lon', data=lon)
        hf.close()
        #将数据绘制，并保存
        DrawECParamOnMap(lon,lat,vshearSum,str(mon)+"月VSHEAR分布图",saveHdfFile.replace(".hdf",".png"))
    print("完成VSHEAR计算！")
#计算circ指标
def run_ec_tf_all_circ():
    #分别计算每个月的平均值
    #数据网格大小为95, 121
    for mon in range(1,13,1):
        saveHdfFile ='D:\\TF_ECOutput\\CIRC\\circ_men_'+str(mon)+".hdf"
        circSum=np.zeros((95,121),dtype=float)
        ncount=0
        for year in range(startYear, endYear, 1):
            print("开始计算" + str(year) + "年")
            mtime=datetime.datetime(year,mon,1)
            endtime=mtime+datetime.timedelta(days=monthrange(year,mon)[1])
            #print(endtime.strftime('%Y-%m-%d'))
            #读取当年此月的所有数据
            while mtime<endtime :
                print("开始读取"+mtime.strftime('%Y-%m-%d-%H'))
                lon, lat, circValue = getCircbyTime(mtime)
                # 此处也要保存每日，时次数据
                saveTfparamstofile(mtime, circValue, "circ")
                circSum=circSum+circValue  #累加所有时次
                ncount=ncount+1           #共有多少个时次
                mtime=mtime+datetime.timedelta(hours=6)
        #将累年值，绘图，并保存至文件中
        circSum=circSum/ncount
        hf = h5py.File(saveHdfFile, 'w')
        # 保存各通道数据
        hf.create_dataset('CIRC', data=circSum)
        hf.create_dataset('Lat', data=lat)
        hf.create_dataset('Lon', data=lon)
        hf.close()
        #将数据绘制，并保存
        DrawECParamOnMap(lon,lat,circSum,str(mon)+"月CIRC分布图",saveHdfFile.replace(".hdf",".png"))
    print("完成CIRC计算！")
#计算HDIV（低层辐合辐散） 850hPa散度替换
def run_ec_tf_all_hdiv():
    #分别计算每个月的平均值
    #数据网格大小为95, 121
    for mon in range(1,13,1):
        saveHdfFile ='D:\\TF_ECOutput\\HDIV\\hdiv_men_'+str(mon)+".hdf"
        circSum=np.zeros((95,121),dtype=float)
        ncount=0
        for year in range(startYear, endYear, 1):
            print("开始计算" + str(year) + "年")
            mtime=datetime.datetime(year,mon,1)
            endtime=mtime+datetime.timedelta(days=monthrange(year,mon)[1])
            #print(endtime.strftime('%Y-%m-%d'))
            #读取当年此月的所有数据
            while mtime<endtime :
                print("开始读取"+mtime.strftime('%Y-%m-%d-%H'))
                lon, lat, circValue = get_divergenceBytime(mtime)
                # 此处也要保存每日，时次数据
                saveTfparamstofile(mtime, circValue, "hdiv")
                circSum=circSum+circValue  #累加所有时次
                ncount=ncount+1           #共有多少个时次
                mtime=mtime+datetime.timedelta(hours=6)
        #将累年值，绘图，并保存至文件中
        circSum=circSum/ncount
        hf = h5py.File(saveHdfFile, 'w')
        # 保存各通道数据
        hf.create_dataset('HDIV', data=circSum)
        hf.create_dataset('Lat', data=lat)
        hf.create_dataset('Lon', data=lon)
        hf.close()
        #将数据绘制，并保存
        DrawECParamOnMap(lon,lat,circSum,str(mon)+"月HDIV（850hPa散度）分布图",saveHdfFile.replace(".hdf",".png"))
    print("完成HDIV计算！")

if __name__ == '__main__':

    #run_ec_tf_all_hdiv()
    run_ec_tf_all_circ()
    run_ec_tf_all_vshear()
