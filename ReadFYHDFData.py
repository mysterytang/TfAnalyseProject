##读取HDF格式的风云系统云图
##
import numpy as np
import  h5py
import  cv2
import struct
#此函数读取HDF格式原始云图2288X2288的定位网格
class FyStarsManager(object):
    def __init__(self,pfile,centerLon):
        self.PosFile=pfile
        self.centerLon=centerLon
    def ReadFYHDFLonLatPOS(self):
        fyCenterLon=104.5 #卫星星下点经度
        filename='NOM_ITG_2288_2288(0E0N)_LE.dat'
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
        return datLon,datLat
    #根据输入的经度和纬度，获取最临近的索引
    def GetLonLatFyXYIndex(self,lon,lat):
        xx,yy=0,0

        return  xx,yy


#
file="C:\\fystars\\fy2g\\FY2G_FDI_ALL_NOM_20161016_0100.hdf"
f = h5py.File(file,'r')
dset=f['/']
#此数据为全圆盘数据
dataNom=np.array(dset["NOMChannelIR3"]) #红外1通道，灰度值
dataNom=dataNom/4

#生成全圆盘，等经纬度投影图像
nx,ny=2288,2288  #全圆盘的尺寸
minLon,maxLon=95,165
minLat,maxLat=-5,55
res = 0.05 #设置投影后图像分辨率
dstWidth =(int)((maxLon - minLon) / res)#//计算图像大小
dstHeight =(int)((maxLat - minLat) / res)
print(dstWidth,dstHeight)  #新生成像素的宽度

dataRet=np.zeros((dstHeight,dstWidth),dtype=float) #此为
startl = (minLon + 180) / res#;//投影
starth = (90 - maxLat) / res#;
print(dataRet.shape)
#获取定位网格
fyCenterLon = 104.5  # 卫星星下点经度
filename = 'NOM_ITG_2288_2288(0E0N)_LE.dat'
mFyPosManager=FyStarsManager(filename,fyCenterLon)
datLon,datLat=mFyPosManager.ReadFYHDFLonLatPOS()
#将全圆盘所有点投影到 遍历所有全圆盘点
for k in range(nx):
    for m in range(ny):
        #获取当前格点经纬度
        lat=datLat[k,m]
        lon=datLon[k,m]
        if lon>=minLon and lon<=maxLon and lat>=minLat and lat<=maxLat :
            y = (int)((maxLat - lat) / res) #当前经纬度对应新位置的索引
            x = (int)((lon - minLon) / res)
            if y<dstHeight and x<dstWidth :
                dataRet[y, x] = dataNom[k, m]  # dataCal[dataNom[k, m]];
            else :
                print(y,x)
cv2.imwrite("fyMap1.png",dataRet)
#对此图像进行双线性插值处理
for i in range(dstHeight):
    for j in range(dstWidth):
        if dataRet[i,j]==0:  #当前为需要插值的点
            #找到替代区域，默认6X6
            for dxy in range(2,10):#按2-10扩展搜索  以
                my=np.max([i,i-dxy])
                mx=np.max([j,j-dxy])
                if my+dxy*2>dstHeight :
                    my=dstHeight-dxy*2
                if mx+dxy*2>dstWidth:
                    mx=dstWidth-dxy*2
                mVal=dataRet[my:my+dxy*2,mx:mx+dxy*2]
                #print(mVal)
                idx=np.argwhere(mVal>1)
                if len(idx)>0:
                    #print(mVal[mVal>1])
                    v=np.mean(mVal[mVal>1])
                    #print(v)
                    dataRet[i,j]=v
                    break

            #print(mVal)
print("正在写入图像")
#cv2.imshow('Fy Image',dataRet)
cv2.imwrite("fyMap2.png",dataRet)


# print(dset["NOMChannelIR2"])
# print(dset["NOMChannelIR3"])
# print(dset["NOMChannelIR4"])
# print(dset["NOMChannelVIS"])
