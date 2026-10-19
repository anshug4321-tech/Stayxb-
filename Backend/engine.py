"""Room + price engine (Python port of the browser version: same hash, same prices)."""
import math
from datetime import date, timedelta
TAX=12; WEEKEND=1.08; SEED=7; BB=350; PICKUP=1200; LATE=1000
OCC={'skyline':.7,'palms':.62}; CATF={'Standard':1.05,'Comfort':1,'Deluxe':.95,'Suite':.85}
COUPONS={'STAYX5':5}
SOLD=('palms','Suite','2027-08-06','2027-08-08')  # forced sold-out test dates
# category: (rooms, price per night, max adults, max children)
HOTELS={'skyline':{'Standard':(40,3200,2,1),'Comfort':(30,4550,2,1),'Deluxe':(20,6100,2,2),'Suite':(10,7950,3,2)},
        'palms':{'Standard':(24,3800,2,1),'Comfort':(18,5700,2,2),'Deluxe':(12,8350,2,2),'Suite':(6,9500,3,2)}}
SEASON={'skyline':[.8,.85,.95,1.1,1.2,1,.95,.95,1,1.05,1,.95],'palms':[.6,.7,.85,1,1.2,1.6,2,2.2,1.5,1,.8,.9]}
ACC={'skyline':{101,102,103,104,501,502},'palms':{101,102,103,104,201,202}}
MAINT={'skyline':{305,706},'palms':{112,309}}
def _rooms():
    R=[]
    def add(h,no,cat,fl):
        R.append(dict(no=no,hotel=h,cat=cat,floor=fl,acc=no in ACC[h],status='maintenance' if no in MAINT[h] else 'active',
          quiet=(no%100 in (8,9,10)) if h=='skyline' else (117<=no<=124 or 215<=no<=218),high=h=='skyline' and fl>=8))
    for f in range(1,11):
        for i in range(1,11): add('skyline',f*100+i,'Standard' if f<=4 else 'Comfort' if f<=7 else 'Deluxe' if f<=9 else 'Suite',f)
    for rng,cat in ((range(101,125),'Standard'),(range(201,219),'Comfort'),(range(301,313),'Deluxe'),(range(401,407),'Suite')):
        for n in rng: add('palms',n,cat,cat)
    return R
ROOMS=_rooms()
def _h(s):  # FNV-1a, same as the browser code
    x=2166136261
    for c in s: x=((x^ord(c))*16777619)&0xFFFFFFFF
    return x/4294967296
def js_dow(d): return (d.weekday()+1)%7  # Sunday=0
def nights(f,t): return [f+timedelta(days=i) for i in range((t-f).days)]
def sim_busy(r,d):
    p=min(.95,OCC[r['hotel']]*(1.1 if js_dow(d) in (5,6) else 1)*CATF[r['cat']])
    return _h(f"{SEED}{r['hotel']}{r['no']}{d.isoformat()}")<p
def free_rooms(hotel,cat,f,t,blocked,prefs=None):
    p=prefs or {}; ns=nights(f,t); out=[]
    for r in ROOMS:
        if r['hotel']!=hotel or r['cat']!=cat or r['status']!='active' or (p.get('acc') and not r['acc']): continue
        bad=False
        for d in ns:
            iso=d.isoformat()
            if (hotel,cat)==SOLD[:2] and SOLD[2]<=iso<=SOLD[3] or (r['no'],iso) in blocked or sim_busy(r,d): bad=True; break
        if not bad: out.append(r)
    return sorted(out,key=lambda r:(-(2*bool(p.get('quiet') and r['quiet'])+bool(p.get('high') and r['high'])),r['no']))
def _r(x): return math.floor(x+.5)
def quote(hotel,cat,f,t,rooms,adults,children,plan='Flexible',meal='none',pickup=False,late=False,coupon=None):
    ns=nights(f,t); room=0
    for d in ns: room+=_r(HOTELS[hotel][cat][1]*SEASON[hotel][d.month-1]*(WEEKEND if js_dow(d) in (5,6) else 1)/50)*50
    room*=rooms; L=[[f'{len(ns)} nights x {rooms} room(s)',room]]; dc=0
    if len(ns)>=7: dc=room*.1; L.append(['Long-stay discount 10%',-dc])
    if plan=='Saver': s=(room-dc)*.1; L.append(['Saver plan 10% off',-s]); dc+=s
    if coupon in COUPONS: c=(room-dc)*COUPONS[coupon]/100; L.append([f'Coupon {coupon}',-c]); dc+=c
    ex=0
    if meal=='BB': m=BB*(adults+children*.5)*len(ns); ex+=m; L.append(['Breakfast',m])
    if pickup: ex+=PICKUP; L.append(['Airport pickup',PICKUP])
    if late: ex+=LATE; L.append(['Late check-out',LATE])
    sub=room-dc+ex; tax=sub*TAX/100; L.append([f'Tax {TAX}%',tax])
    return {'lines':[[a,_r(b)] for a,b in L],'total':_r(sub+tax)}
