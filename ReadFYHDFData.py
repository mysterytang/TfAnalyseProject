##读取HDF格式的风云系统云图
##
import numpy as np
import  h5py
import  cv2
import struct, shutil
import os
import datetime
#以下为全局变量
ytHDFDir = "D:/Fy_HDF"  # 云图源文件夹目录
ytUserHDFDir="D:/TF_FY_HDF" #台风分析范围云图
ytUserJPGDir="D:/TF_FY_JPG"  #台风分析范围对应JPG云图

# 将以上数据进行指定区域和分辨率的插值
minLon, maxLon = 95, 165
minLat, maxLat = -5, 55
# 生成全圆盘，等经纬度投影图像
nx, ny = 2288, 2288  # 全圆盘的尺寸
res = 0.05  # 设置投影后图像分辨率

#此函数读取HDF格式原始云图2288X2288的定位网格
class FyStarsManager(object):
    def __init__(self,pfile,centerLon):
        self.PosFile=pfile
        self.centerLon=centerLon

    def ReadFYHDFLonLatPOS(self):
        # fyCenterLon=104.5 #卫星星下点经度
        # filename='NOM_ITG_2288_2288(0E0N)_LE.dat'

        fyCenterLon =self.centerLon  # 卫星星下点经度
        filename = self.PosFile

        f = open(filename, "rb")
        nx,ny=2288,2288
        datLon=np.zeros((nx,ny),dtype=float)
        datLat = np.zeros((nx, ny), dtype=float)
        #读取经度信息
        for i in range(nx):
            for j in range(ny):
                datLon[i,j]=struct.unpack('f',f.read(4))[0]
        #读取纬度信息
        for i in range(nx):
            for j in range(ny):
                datLat[i, j] = struct.unpack('f', f.read(4))[0]
        #风云2G星的星下点是104.5度。其定位网格的星下点为0,0,
        #将经度加上星下点经度，
        datLon=datLon+fyCenterLon
        f.close()
        return datLon,datLat
    #根据输入的经度和纬度，获取最临近的索引
    def GetLonLatFyXYIndex(self,lon,lat):
        xx,yy=0,0
        return  xx,yy

#将文件根据时间，存贮至指定保存目录下
def SaveHDFfile(filename,f):
    saveDir='D:/Fy_HDF'
    #分析文件名
    strValues=f.split('_')
    #获取时间
    idx=len(strValues)
    time=strValues[idx-2]
    hour=strValues[idx-1]
    mm=int(hour[2:4])
    #print(strValues)
    pass
    #print(mm)
    if mm==0 :#and strValues[7]=='FDI' :#只保存正点云图,k
        #根据时间保存文件 按 年/月/日  一天24个文件   /文件的方式保存
        year=time[0:4]
        month=time[4:6]
        dd=time[6:8]
        rdir=os.path.join(saveDir,str(year)+"/"+str(month)+"/"+str(dd))
        #目录不存在，则建立目录
        if not os.path.exists(rdir):
            os.makedirs(rdir)
        #将此文件保存至规范目录下
        nf=f[f.find('FY2F'):len(f)]
        #print(nf)
        rfile=os.path.join(rdir,nf)
        if not os.path.isfile(rfile) : #文件不存在则复制。
            shutil.move(filename, rfile)
            print("已复制 :"+rfile)
        else :
            print("文件已存在，跳过!")

#遍历所有文件夹，输出整点卫星云图，并按规范目录
def ReadAndReSaveHDFFile():
    ytSouceDir = "D:/fystars/fy2f"  # 文件夹目录
    list_dirs = os.walk(ytSouceDir)
    for root, dirs, files in list_dirs:
        for f in files:
            filename=os.path.join(root, f)
            SaveHDFfile(filename,f)
def SaveHDFToImageAndByte(file):
    #file="C:\\fystars\\fy2g\\FY2G_FDI_ALL_NOM_20161016_0100.hdf"
    # 将数据保存至新的HDF文件中
    # 直接用原文件名
    saveHdfDir = os.path.dirname(file).replace(ytHDFDir, ytUserHDFDir)
    if not os.path.exists(saveHdfDir):
        os.makedirs(saveHdfDir)
    saveHdfFile = os.path.join(saveHdfDir, os.path.basename(file))
    # print(saveHdfFile)
    if not os.path.isfile(saveHdfFile):   #文件不存在则，重新读取插值
        print("读取"+saveHdfFile+"  .....")
        tf_ir1, tf_ir2, tf_ir3, tf_ir4 = ReadorgHDF(file)
        # 读取定标对应的定标数据
        f = h5py.File(file, 'r')
        dset = f['/']
        cal1 = np.array(dset["CALChannelIR1"])
        cal2 = np.array(dset["CALChannelIR2"])
        cal3 = np.array(dset["CALChannelIR3"])
        cal4 = np.array(dset["CALChannelIR4"])
        #calvis = np.array(dset["CALChannelVIS"])
        f.close()

        print("保存数据至"+saveHdfFile)
        hf = h5py.File(saveHdfFile, 'w')
        # 保存各通道数据
        hf.create_dataset('NOMChannelIR1', data=tf_ir1)
        hf.create_dataset('NOMChannelIR2', data=tf_ir2)
        hf.create_dataset('NOMChannelIR3', data=tf_ir3)
        hf.create_dataset('NOMChannelIR4', data=tf_ir4)
        #hf.create_dataset('NOMChannelVIS', data=tf_vis)
        # 保存定标数据
        hf.create_dataset('CALChannelIR1', data=cal1)
        hf.create_dataset('CALChannelIR2', data=cal2)
        hf.create_dataset('CALChannelIR3', data=cal3)
        hf.create_dataset('CALChannelIR4', data=cal4)
        #hf.create_dataset('CALChannelVIS', data=calvis)
        hf.close()
    else: #直接从生成后的文件读取数据
        f = h5py.File(saveHdfFile, 'r')
        dset = f['/']
        # 此数据为全圆盘数据
        # 读取各通道的数据，以及经纬网格数据 ，定标数据
        tf_ir1 = np.array(dset["NOMChannelIR1"])/4  # 红外1通道，灰度值
        tf_ir2 = np.array(dset["NOMChannelIR2"])/4  # 红外1通道，灰度值
        tf_ir3 = np.array(dset["NOMChannelIR3"])/4  # 红外1通道，灰度值
        tf_ir4 = np.array(dset["NOMChannelIR4"])/4  # 红外1通道，灰度值
        #tf_vis = np.array(dset["NOMChannelVIS"])/4  # 红外1通道，灰度值


    #将图像加入经纬网格数据

    #SaveHdfToJPG(file, tf_ir1, tf_ir2, tf_ir3, tf_ir4)#, tf_vis)
    print("完成当前时次处理"+file)


def SaveHdfToJPG(file, tf_ir1, tf_ir2, tf_ir3, tf_ir4):#, tf_vis):
    print("输出图像")
    # 将新区域图生成卫星云图，保存图像格式
    saveJPGDir = os.path.dirname(file).replace(ytHDFDir, ytUserJPGDir)
    if not os.path.exists(saveJPGDir):
        os.makedirs(saveJPGDir)
    ir1jpg = os.path.join(saveJPGDir, "IR1_" + os.path.basename(file).replace(".hdf", ".jpg"))
    cv2.imwrite(ir1jpg, tf_ir1)
    DrawLonLatGrid(ir1jpg)
    ir2jpg = os.path.join(saveJPGDir, "IR2_" + os.path.basename(file).replace(".hdf", ".jpg"))
    cv2.imwrite(ir2jpg, tf_ir2)
    DrawLonLatGrid(ir2jpg)
    ir3jpg = os.path.join(saveJPGDir, "IR3_" + os.path.basename(file).replace(".hdf", ".jpg"))
    cv2.imwrite(ir3jpg, tf_ir3)
    DrawLonLatGrid(ir3jpg)
    ir4jpg = os.path.join(saveJPGDir, "IR4_" + os.path.basename(file).replace(".hdf", ".jpg"))
    cv2.imwrite(ir4jpg, tf_ir4)
    DrawLonLatGrid(ir4jpg)
    # visjpg = os.path.join(saveJPGDir, "VIS_" + os.path.basename(file).replace(".hdf", ".jpg"))
    # cv2.imwrite(visjpg, tf_vis)
    # DrawLonLatGrid(visjpg)


#在云图上绘制经纬网格
def DrawLonLatGrid(ir1jpg):
    tf_ir1 = cv2.imread(ir1jpg, 0)
    tf_ir1 = cv2.cvtColor(tf_ir1, cv2.COLOR_GRAY2BGR)
    #Lon 100-160 Lat 0-50
    font = cv2.FONT_HERSHEY_SIMPLEX  # 使用默认字体
    #  添加文字，1.2表示字体大小，（0,40）是初始的位置，(255,255,255)表示颜色，2表示粗细
    for lat in range(0,55,5):
        py=int((maxLat-lat)/res)
        cv2.line(tf_ir1, (0, py), (1400, py), (255, 0, 0))
        cv2.putText(tf_ir1, str(lat), (700, py), font, 0.6, (0, 255, 255),1)
    for lon in range(100,165,5):
        px = int((lon - minLon) / res)
        cv2.line(tf_ir1, (px, 0), (px, 1200), (255, 0, 0))
        cv2.putText(tf_ir1, str(lon), (px-16, 600), font, 0.6, (0, 255, 255),1)
    #添加文本
    cv2.imwrite(ir1jpg, tf_ir1)
def ReadorgHDF(file):
    f = h5py.File(file, 'r')
    dset = f['/']
    # 此数据为全圆盘数据
    # 读取各通道的数据，以及经纬网格数据 ，定标数据
    ir1 = np.array(dset["NOMChannelIR1"])  # 红外1通道，灰度值
    ir2 = np.array(dset["NOMChannelIR2"])  # 红外1通道，灰度值
    ir3 = np.array(dset["NOMChannelIR3"])  # 红外1通道，灰度值
    ir4 = np.array(dset["NOMChannelIR4"])  # 红外1通道，灰度值
    #vis = np.array(dset["NOMChannelVIS"])  # 红外1通道，灰度值
    # 以下对应的定标数据
    cal1 = np.array(dset["CALChannelIR1"])
    cal2 = np.array(dset["CALChannelIR2"])
    cal3 = np.array(dset["CALChannelIR3"])
    cal4 = np.array(dset["CALChannelIR4"])
    #calvis = np.array(dset["CALChannelVIS"])

    fyCenterLon = float(dset["NomFileInfo"]['NOMCenterLon'])

    f.close()
    # 获取定位网格
    # fyCenterLon = 104.5  # 读取此卫星 的星下点经度
    filename = 'NOM_ITG_2288_2288(0E0N)_LE.dat'
    mFyPosManager = FyStarsManager(filename, fyCenterLon)
    datLon, datLat = mFyPosManager.ReadFYHDFLonLatPOS()
    # 将全圆盘插值到指定台风区域
    print("处理IR1")
    tf_ir1 = InterToUserGridarray(datLat, datLon, ir1)
    print("处理IR2")
    tf_ir2 = InterToUserGridarray(datLat, datLon, ir2)
    print("处理IR3")
    tf_ir3 = InterToUserGridarray(datLat, datLon, ir3)
    print("处理IR4")
    tf_ir4 = InterToUserGridarray(datLat, datLon, ir4)
    #print("处理VIS")
    #tf_vis = InterToUserGridarray(datLat, datLon, vis)
    return tf_ir1, tf_ir2, tf_ir3, tf_ir4#, tf_vis


#对全圆盘网格进行等经纬度投影变幻，并插值
def InterToUserGridarray(datLat, datLon, dataNom):
    dstWidth = (int)((maxLon - minLon) / res)  # //计算图像大小
    dstHeight = (int)((maxLat - minLat) / res)
    # print(dstWidth,dstHeight)  #新生成像素的宽度
    # startl = (minLon + 180) / res  # ;//投影
    # starth = (90 - maxLat) / res  # ;

    dataRet = np.zeros((dstHeight, dstWidth), dtype=float)  # 此为
    # 将全圆盘所有点投影到 遍历所有全圆盘点
    print("开始变幻投影")
    for k in range(nx):
        for m in range(ny):
            # 获取当前格点经纬度
            lat = datLat[k, m]
            lon = datLon[k, m]
            if lon >= minLon and lon <= maxLon and lat >= minLat and lat <= maxLat:
                y = (int)((maxLat - lat) / res)  # 当前经纬度对应新位置的索引
                x = (int)((lon - minLon) / res)
                if y < dstHeight and x < dstWidth:
                    dataRet[y, x] = dataNom[k, m]  # dataCal[dataNom[k, m]];
                # else:
                    # print(y, x)
    print("开始插值")
    # 对此图像进行双线性插值处理
    # for i in range(dstHeight):
    #     for j in range(dstWidth):
    #         if dataRet[i, j] == 0:  # 当前为需要插值的点
                # 找到替代区域，默认6X6
        #print(i,j,dataRet[i,j])
    idx0val = np.argwhere(dataRet == 0)
    for i, j in idx0val:
        for dxy in range(2, 10):  # 按2-10扩展搜索  以
            my = np.max([i, i - dxy])
            mx = np.max([j, j - dxy])
            if my + dxy * 2 > dstHeight:
                my = dstHeight - dxy * 2
            if mx + dxy * 2 > dstWidth:
                mx = dstWidth - dxy * 2
            mVal = dataRet[my:my + dxy * 2, mx:mx + dxy * 2]
            # print(mVal)
            idx = np.argwhere(mVal > 1)
            if len(idx) > 0:
                # print(mVal[mVal>1])
                v = np.mean(mVal[mVal > 1])
                # print(v)
                dataRet[i, j] = v
                break
    return  dataRet

def TestOpencvFun():
    img=cv2.imread('fyMapIR2.png',0)
    ret,thresh=cv2.threshold(img,200,300,0)
    image,contours,hierarchy=cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    color = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    img = cv2.drawContours(color, contours, -1, (0, 0, 255), 1)
    #对找到的边界进行处理
    for c in contours:
        if len(c)>100:
            #外接多边形
            #x,y,w,h=cv2.boundingRect(c)
            #cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
            #最小区域多边形
            rect=cv2.minAreaRect(c)
            box=cv2.boxPoints(rect)
            box=np.int0(box)
            cv2.drawContours(img,[box],0,(0,255,0),2)

            #计算中心区域
            (x,y),radius=cv2.minEnclosingCircle(c)
            center=(int(x),int(y))
            radius=int(radius)
            img=cv2.circle(img,center,radius,(255,0,0),2)
    cv2.imwrite('contour.png',color)
    cv2.imshow('Canny',color)
    cv2.waitKey()
    cv2.destroyAllWindows()
    #img=cv2.pyrDown(cv2.imread('fyMapIR2.png',cv2.IMREAD_UNCHANGED))

    pass

#-------------------------------2018年11月12日-------------------------------
#读取HDF，整理后的云图，提取研究区域内的云图图像，对各通道的数据，重新保存至新HDF文件中
#并把各通道图像，生成PNG图像，
def ReSaveUserHDFAndImage():

    #根据时间遍历处理云图
    begin = datetime.date(2016, 1, 1)  # 资料开始时间
    end = datetime.date(2018, 1, 1)  # 资料结束时间
    nday = begin  # 当前下载资料的月份，按月份下载
    while nday <= end:
        #处理一天的云图数据
        mHdfDirs=ytHDFDir+"/{:0>2d}/{:0>2d}/{:0>2d}".format(nday.year,nday.month,nday.day)
        #根据时间生成文件名
        ytFlags=['FY2F','FY2G']
        for hour in range(24):  #根据24小时生成
            name2f = GetExtHDFileName(mHdfDirs,hour, nday, ytFlags)
            SaveHDFToImageAndByte(name2f) #开始处理此数据
            print(name2f)
        nday =nday+datetime.timedelta(days=1)
        break
    print("完成所有云图处理")

#找到此时次的，任意风云系列卫星云图
def GetExtHDFileName(mHdfDirs,hour, nday, ytFlags):
    for flag in ytFlags:
        name2f =mHdfDirs+"/"+flag + "_FDI_ALL_NOM_" + nday.strftime("%Y%m%d") + "_{:0>2d}".format(hour) + "00.hdf"
        #print(name2f)
        if os.path.isfile(name2f):
            return name2f
    print("未找到此时次云图文件"+str(nday)+str(hour))
    return ""

#
# file="C:\\fystars\\fy2g\\FY2G_FDI_ALL_NOM_20161016_0100.hdf"
# f = h5py.File(file,'r')
# dset=f['/']
# fInfo=float(dset["NomFileInfo"]['NOMCenterLon']) #红外1通道，灰度值
# print(fInfo)

# filename = 'NOM_ITG_2288_2288(0E0N)_LE.dat'
# mFyPosManager=FyStarsManager(filename,104.5)
# datLonf,datLatf=mFyPosManager.ReadFYHDFLonLatPOS()
#
# filename = 'C:/NOM_ITG_2288_2288(0E0N)_LE.dat'
# mFyPosManager=FyStarsManager(filename,105.5)
# datLong,datLatg=mFyPosManager.ReadFYHDFLonLatPOS()
#
# print(datLonf[1000,200:500]-datLong[1000,200:500])
# print(datLatg[1000,200:500]-datLatg[1000,200:500])


ReSaveUserHDFAndImage()



#TestOpencvFun()
#ReadAndReSaveHDFFile()  已处理完成
# print(dset["NOMChannelIR2"])
# print(dset["NOMChannelIR3"])
# print(dset["NOMChannelIR4"])
# print(dset["NOMChannelVIS"])
