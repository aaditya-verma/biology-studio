import numpy as np, itertools, sys, json
def s2l(c):
    c=np.array([int(c[i:i+2],16) for i in (1,3,5)])/255
    return np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4)
def l2s(l):
    l=np.clip(l,0,1); return np.where(l<=0.0031308,12.92*l,1.055*l**(1/2.4)-0.055)
M={'deut':[[0.367322,0.860646,-0.227968],[0.280085,0.672501,0.047413],[-0.011820,0.042940,0.968881]],
   'prot':[[0.152286,1.052583,-0.204868],[0.114503,0.786281,0.099216],[-0.003882,-0.048116,1.051998]],
   'trit':[[1.255528,-0.076749,-0.178779],[-0.078411,0.930809,0.147602],[0.004733,0.691367,0.303900]]}
def lab(lin):
    X=np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]])@lin
    X=X/np.array([0.95047,1,1.08883]); f=np.where(X>0.008856,np.cbrt(X),7.787*X+16/116)
    return np.array([116*f[1]-16,500*(f[0]-f[1]),200*(f[1]-f[2])])
def sim(c,v):
    l=s2l(c)
    if v=='norm': return lab(l)
    # Machado matrices operate in linear RGB
    return lab(np.clip(np.array(M[v])@l,0,1))
def de00(a,b):
    L1,a1,b1=a;L2,a2,b2=b;C1=np.hypot(a1,b1);C2=np.hypot(a2,b2);Cb=(C1+C2)/2
    G=0.5*(1-np.sqrt(Cb**7/(Cb**7+25**7)));a1p=(1+G)*a1;a2p=(1+G)*a2
    C1p=np.hypot(a1p,b1);C2p=np.hypot(a2p,b2);h1=np.degrees(np.arctan2(b1,a1p))%360;h2=np.degrees(np.arctan2(b2,a2p))%360
    dL=L2-L1;dC=C2p-C1p;dh=h2-h1
    if C1p*C2p==0: dh=0
    elif dh>180: dh-=360
    elif dh<-180: dh+=360
    dH=2*np.sqrt(C1p*C2p)*np.sin(np.radians(dh/2));Lb=(L1+L2)/2;Cbp=(C1p+C2p)/2
    hb=h1+h2
    if C1p*C2p!=0:
        hb=(h1+h2+360)/2 if abs(h1-h2)>180 else (h1+h2)/2
    T=1-0.17*np.cos(np.radians(hb-30))+0.24*np.cos(np.radians(2*hb))+0.32*np.cos(np.radians(3*hb+6))-0.2*np.cos(np.radians(4*hb-63))
    dth=30*np.exp(-((hb-275)/25)**2);Rc=2*np.sqrt(Cbp**7/(Cbp**7+25**7))
    Sl=1+0.015*(Lb-50)**2/np.sqrt(20+(Lb-50)**2);Sc=1+0.045*Cbp;Sh=1+0.015*Cbp*T;Rt=-np.sin(np.radians(2*dth))*Rc
    return float(np.sqrt((dL/Sl)**2+(dC/Sc)**2+(dH/Sh)**2+Rt*(dC/Sc)*(dH/Sh)))
TOK={'epi':'#56B4E9','epi-e':'#1986C4','hypo':'#BDD9B8','hypo-e':'#558C4B','ecto':'#0072B2','ecto-e':'#0082CA',
'meso':'#D55E00','meso-e':'#D05C00','endo':'#E6CF3A','endo-e':'#907F12','crest':'#009E73','crest-e':'#009069',
'ctx':'#828A99','ctx-e':'#767F8F','accent':'#994774','acc-dark':'#C77BA2'}
def check(c, only=None):
    worst=(999,None,None)
    for v in ['norm','deut','prot','trit']:
        for k,t in TOK.items():
            if only and k.split('-')[0] not in only and k not in only: continue
            d=de00(sim(c,v),sim(t,v))
            if d<worst[0]: worst=(d,k,v)
    return worst
if __name__=='__main__':
    for c in sys.argv[1:]:
        d,k,v=check(c); print(c, round(d,1), k, v, 'OK' if d>=15 else 'LOW')
