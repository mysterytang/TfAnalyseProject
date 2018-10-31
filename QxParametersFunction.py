
lev= 850
'define t=air.1'
'define rh=rhum.2'
'define prs=lev'
'define es=(6.112*exp(17.67*(t-273.15)/(t-29.65)))' 计算此温度下的饱和水汽压

'define q=rh*(0.62197*es/(prs-es))/100.' 混合比

'define e=prs*q/(0.62197+q)+1e-10'  水汽压

'define tlcl=55.0+2840.0/(3.5*log(t)-log(e)-4.805)'  对流抬升高度  Bolton(1980)公式

'define theta=t*pow((1000/prs),(0.2854*(1.0-0.28*q)))'    位温
'define eqt=theta*exp(((3376./tlcl)-2.54)*q*(1.0+0.81*q))'   假相当位温
