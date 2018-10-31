#下载所需要的Key 83db1486187c2146056ab562a2f3a1e
# {
#     "url": "https://api.ecmwf.int/v1",
#     "key": "29525ad53a00d3836be58b3dbbd68d6d",
#     "email": "wzhong_vivian@hotmail.com"
# }
from ecmwfapi import *
import datetime
import os
from calendar import monthrange
from datetime import timedelta
#以下主程序，根据时间循环下载所需要的数据
#资料数据直接，按单要素按月存贮。
#文件分开存贮
#根据项目计算要求，目前需要的资料主要有：
# 1.风，U，V
#------------------------------------------
#以下定义全局参数变量
time="00/06/12/18"   #资料的时次，EC资料共有四个时次
saveDir="C:\\EcData"
areaStr="60/90/-10.5/180"
gkLevelStr="100/200/300/400/500/550/600/650/700/750/800/850/875/900/925/950/975/1000"
#------------------------------------------
#
def main():
    begin = datetime.date(2016,1,1)  #资料开始时间
    end = datetime.date(2018,1,1)   #资料结束时间

    server = ECMWFDataServer()  #建立与EC服务器连接
    mMonth = begin               #当前下载资料的月份，按月份下载
    while mMonth <= end:
        print(str(mMonth))
        #------------------------------
        #以下开始下载数据
        print("开始下载"+mMonth.strftime('%Y-%m')+"EC气象要素资料")
        print(".................................")
        #----------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 风场U")
        param,savefile = DownECParamDm10U(mMonth)
        #print(param)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -----------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 风场V")
        param,savefile = DownECParamDm10V(month=mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # ----------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 地面SST")
        param,savefile = DownECParamDmSST(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -----------------------------------------
        # ----------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 地面气压")
        param,savefile = DownECParamDmSurfacePressure(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")

        # -------------------------------------------
        print("下载高空气象数据要素共9个")
        # ----------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 1")
        param,savefile= DownECParamGkDivergence(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 2")
        param,savefile = DownECParamGkGeopotential(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 3")
        param,savefile = DownECParamGkPV(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 4")
        param,savefile = DownECParamGkRH(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 5")
        param,savefile = DownECParamGkT(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 6")
        param,savefile = DownECParamGkU(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 7")
        param,savefile = DownECParamGkV(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 8")
        param,savefile = DownECParamGkVorticity(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        print("开始下载" + mMonth.strftime('%Y-%m-%d') + " 9")
        param,savefile = DownECParamGkW(mMonth)
        if not os.path.exists(savefile):
            server.retrieve(param)
        else:
            print(savefile+"文件已存在!")
        # -------------------------------------------
        #开始下一个月资料
        mMonth=datetime.date(mMonth.year+1,1,1)
        #mMonth = mMonth + timedelta(days=365)# days=monthrange(mMonth.year, mMonth.month)[1])
        print("开始下一个月资料"+mMonth.strftime("%Y-%m-%d"))
    print("已完成所有月份下载!" )

#下载地面10米 风U 分量指定月份的数据
def DownECParamDm10U(month):
    uDir=saveDir+"\\Dm10U"#+month.strftime('%Y%m') + ".nc"
    if not os.path.exists(uDir):
        os.makedirs(uDir)
    print(month.strftime('%Y%m'))
    endMonth=datetime.date(month.year+1,1,1)-timedelta(days=1)#days=monthrange(month.year,month.month)[1]-1)
    dateStr=month.strftime('%Y-%m-%d')+"/to/"+endMonth.strftime('%Y-%m-%d')
    params={
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levtype": "sfc",
        "param": "165.128",  #这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",#area:  N/W/S/E
        'format': "netcdf",
        "target": uDir+"\\U_"+month.strftime('%Y')+".nc"
    }
    #print(params)
    return params,uDir+"\\U_"+month.strftime('%Y')+".nc"
#下载地面10米 风 V分量指定月份的数据
def DownECParamDm10V(month):
    vDir = saveDir + "\\Dm10V"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levtype": "sfc",
        "param": "166.128",  # 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\V_" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\V_" + month.strftime('%Y') + ".nc"

#下载地面，SST
def DownECParamDmSST(month):
    vDir = saveDir + "\\SST"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levtype": "sfc",
         "param": "34.128",  # 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\SST_" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\SST_" + month.strftime('%Y') + ".nc"
#下载地面气压场数据
def DownECParamDmSurfacePressure(month):
    vDir = saveDir + "\\SurfacePressure"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levtype": "sfc",
        "param": "134.128", # 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\SurfacePressure_" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\SurfacePressure_" + month.strftime('%Y') + ".nc"

#---------------------以下高空的9个变量-----------------
def DownECParamGkDivergence(month):
    vDir = saveDir + "\\Divergence"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "155.128", # 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\Divergence_" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\Divergence_" + month.strftime('%Y') + ".nc"
def DownECParamGkGeopotential(month):
    vDir = saveDir + "\\Geopotential"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "129.128",# 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\Geopotential_" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\Geopotential_" + month.strftime('%Y') + ".nc"
def DownECParamGkPV(month):
    vDir = saveDir + "\\PV"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "60.128",# 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\PV_" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\PV_" + month.strftime('%Y') + ".nc"

def DownECParamGkRH(month):
    vDir = saveDir + "\\RH"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "157.128",# 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\RH" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params, vDir + "\\RH" + month.strftime('%Y') + ".nc"

def DownECParamGkT(month):
    vDir = saveDir + "\\T"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "130.128",# 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\T" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\T" + month.strftime('%Y') + ".nc"

def DownECParamGkU(month):
    vDir = saveDir + "\\GKU"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "131.128",# 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\U" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\U" + month.strftime('%Y') + ".nc"

def DownECParamGkV(month):
    vDir = saveDir + "\\GKV"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "132.128",# 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\V" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\V" + month.strftime('%Y') + ".nc"
def DownECParamGkVorticity(month):
    vDir = saveDir + "\\Vorticity"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "138.128",# 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\Vorticity" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\Vorticity" + month.strftime('%Y') + ".nc"
def DownECParamGkW(month):
    vDir = saveDir + "\\W"# + str(month.year)
    if not os.path.exists(vDir):
        os.makedirs(vDir)
    # print(month.strftime('%Y%m'))
    endMonth = datetime.date(month.year + 1,1,1) - timedelta(days=1)#endMonth = month + timedelta(days=365)#monthrange(month.year, month.month)[1] - 1)
    dateStr = month.strftime('%Y-%m-%d') + "/to/" + endMonth.strftime('%Y-%m-%d')
    params = {
        "class": "ei",
        "dataset": "interim",
        "date": dateStr,
        "expver": "1",
        "grid": "0.75/0.75",
        "levelist": gkLevelStr,
        "levtype": "pl",
        "param": "135.128",# 这是风向的，要素代号
        "step": "0",
        "stream": "oper",
        "time": "00:00:00/06:00:00/12:00:00/18:00:00",
        "type": "an",
        'area': areaStr,#"60/100/0/180",
        'format': "netcdf",
        "target": vDir + "\\W" + month.strftime('%Y') + ".nc"
    }
    # print(params)
    return params,vDir + "\\W" + month.strftime('%Y') + ".nc"
#--------------------------------------------------------
if __name__ == '__main__':
    main()



