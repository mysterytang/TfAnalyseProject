#此文件读取风云系统AWX格式的卫星云图
import  os
import  cv2
import  struct
import  numpy as np
import codecs
def read_int16(stream):
    result = struct.unpack("h", stream.read(2))[0]
    return result
def read_int32(stream):
    result = struct.unpack("l", stream.read(4))[0]
    return result
def read_chars(reader, count):
    s=struct.unpack(str(count)+"s",reader.read(count))[0]
    return s

class AWX_FY_Manager(object):
    def __init__(self,pfile):
        if os.path.isfile(pfile):
            self.AwxFile=pfile
            self.awxF = open(pfile, 'rb')
            #self.awxF=codecs.open(pfile, "r", "utf8", "ignore")

        else :
            print("此文件不存在")
    #读取定位网格数据
    def readPosTable(self):
        pass
    #读取一级头文件 长度40个字节
    def readOneHeadSec(self):
        stream=self.awxF
        stream.seek(0,0)
        fName=read_chars(stream,12)   #1-12Sat96文件名
        print(fName)
        read_int16(stream)  #整型的字节顺序
        head1Len=read_int16(stream)  # 第一级文件头长度
        head2Len = read_int16(stream)  # 第二级文件头长度
        print(head1Len,head2Len)
        lenFillingData=read_int16(stream)  # 填充段长度
        self.lenRecord=read_int16(stream)  # 记录段长度
        self.numheadRecord=read_int16(stream)  #文件头占用记录数
        numDataRecord=read_int16(stream)  # 产品数据占用记录数
        #print(numheadRecord,numDataRecord)

        self.productType=read_int16(stream)  # 产品类别
        print("产品类别=",self.productType)
        read_int16(stream)  # 压缩方式
        formatStr=read_chars(stream, 8) #格式说明字符串
        read_int16(stream)  # 产品数据质量标记
        print(formatStr)
    # 读取二级头文件 及填充段
    #长度为64个字节
    def ReadTwoHeadSec(self):
        stream = self.awxF
        stream.seek(40, 0)

        fyType=read_chars(stream, 8) #卫星名称
        #根据产品类别，判断年索引开始日期
        yearIdx=58
        if self.productType==1:
            yearIdx=48
        elif self.productType==4:
            yearIdx=54

        stream.seek(yearIdx, 0)
        year= read_int16(stream)
        month = read_int16(stream)
        day = read_int16(stream)
        min = read_int16(stream)
        second = read_int16(stream)
        print(str(year),month,day,min,second)


        #根据产品类别，判断格点参数

        # read_int16(stream)  #通道号
        # tyC=read_int16(stream)  #投影方式
        # imgWidth=read_int16(stream)  #图像宽度
        # imgHeight=read_int16(stream) #图像高度
        #
        # print(str(int(imgWidth)),str(int(imgHeight)))
        # read_int16(stream)  #图像左上角扫描线号
        # read_int16(stream)  #图像左上角像元号
        # read_int16(stream) #抽样率

        stream.seek(yearIdx+20, 0)
        northLat=read_int16(stream)/100 #地理范围（北纬）
        westLon = read_int16(stream)/100  # 地理范围（西经）
        southLat = read_int16(stream) / 100  # 地理范围（南纬）
        eastLon = read_int16(stream)/100  # 地理范围（东经）
        print(northLat, southLat, westLon, eastLon)
        unitGrid=read_int16(stream)
        spaceLonGrid=read_int16(stream)  #投影中心纬度
        spaceLatGrid = read_int16(stream)  #投影中心经度
        print(spaceLonGrid, spaceLatGrid)
        self.numLonGrid = read_int16(stream)  # 投影中心纬度
        self.numLatGrid = read_int16(stream)  # 投影中心经度
        print("投影格点:")
        print(self.numLonGrid, self.numLatGrid)

        read_int16(stream)  # 投影标准纬度1
        read_int16(stream)  # 投影标准纬度2
        read_int16(stream)  # 投影水平分辨率
        read_int16(stream)  # 投影垂直分辨率
        read_int16(stream)  # 地理网格叠加标志
        read_int16(stream)  # 地理网格叠加值
        read_int16(stream)  # 调色表数据块长度
        table=read_int16(stream)  # 定标数据块长度
        gridTabe=read_int16(stream)  # 定位数据块长度
        read_int16(stream)  # 保留

        print(table,gridTabe)
    # 读调色表数据，调色表给出了对应灰度，表示的RGB色 R256，G256，B256
    def ReadColorTableSec(self):
        stream = self.awxF
        #f.seek(104, 0)
        r=[1]*256
        g = [1] * 256
        b = [1] * 256
        for i in range(256):
            r[i]=struct.unpack("b", stream.read(1))
        for i in range(256):
            g[i]=struct.unpack("b", stream.read(1))
        for i in range(256):
            b[i]=struct.unpack("b", stream.read(1))

        #输出下调色表
        # for i in range(256):
        #     print(i,r[i],g[i],b[i])
    #读取定标数据格式，1024个，2字节长度
    def ReadTableSec(self):
        f = self.awxF
        table = [1] * 1024
        # for i in range(1024):
        #     table[i] = struct.unpack("h", f.read(2))
        #     print(table[i])
    # 读取数据段文件
    def ReadTBBDataHeadSec(self):
        f=self.awxF
        f.seek(self.lenRecord*self.numheadRecord,0)
        ncount=self.numLatGrid*self.numLonGrid
        result=[0]*ncount
        for i in range(ncount):
            result[i] =struct.unpack("B", f.read(1))[0]
        arr=np.array(result)
        print(len(arr))
        arr=arr.reshape(self.numLonGrid,self.numLatGrid)
        print(arr)
        return arr



    def ReadHeadStruct(self):
        self.readOneHeadSec()
        self.ReadTwoHeadSec()
        self.ReadColorTableSec()
        self.ReadTableSec()
        img=self.ReadTBBDataHeadSec()
        cv2.imwrite('fy2c.png', img)
        cv2.imshow('FY2C', img)
        cv2.waitKey()
#开始读取测试文件
awxfile='C:\\TFProject\\项目梳理\\1-卫星资料读取\AWX格式\\FY2E_TBB_IR1_OTG_20120101_0000.AWX'
awx=AWX_FY_Manager(awxfile)
awx.ReadHeadStruct()


