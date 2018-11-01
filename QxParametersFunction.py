import math
#根据气压计算，此层的假相当位温
#prs,为气压，t为温度 单位为K   rh 为相对湿度
def CaculateSita(prs,t,rh) :
    es=(6.112*math.exp(17.67*(t-273.15)/(t-29.65)))# 计算此温度下的饱和水汽压
    q=rh*(0.62197*es/(prs-es))/100.  #' 混合比
    e=prs*q/(0.62197+q)+1e-10  #'  水汽压
    eqt = 0
    try:
        tlcl=55.0+2840.0/(3.5*math.log(t,e)-math.log(e,e)-4.805) #'  对流抬升高度  Bolton(1980)公式
        theta=t*math.pow((1000/prs),(0.2854*(1.0-0.28*q))) #'    位温
        eqt=theta*math.exp(((3376./tlcl)-2.54)*q*(1.0+0.81*q)) #'   假相当位温
    except:
        pass
    else :
        print("当前计算出错了",t,rh)
        print(tlcl)
        print(math.log(t,e))
    return  eqt
