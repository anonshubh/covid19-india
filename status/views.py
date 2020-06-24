from django.shortcuts import render
import json
import requests
from django.views.generic import View

class HomeView(View):
    def get(self,request,*args,**kwargs):
        state = [] 
        conf = [] 
        delconf = [] 
        act = [] 
        delact = [] 
        rec = [] 
        delrec = [] 
        dth = [] 
        deldth = [] 
        cfr = [] 
        rr = []
        rdr = []
        request1 = requests.get('https://api.covid19india.org/data.json')
        y = json.loads(request1.text)
        for i in range(38):
            act.append(int(y['statewise'][i]['active']))
            state.append(y['statewise'][i]['state'])
            conf.append(int(y['statewise'][i]['confirmed']))
            rec.append(int(y['statewise'][i]['recovered']))
            dth.append(int(y['statewise'][i]['deaths']))
            delconf.append(int(y['statewise'][i]['deltaconfirmed']))
            deldth.append(int(y['statewise'][i]['deltadeaths']))
            delrec.append(int(y['statewise'][i]['deltarecovered']))
            delact.append(delconf[i]-deldth[i]-delrec[i])
            try:
                cfr.append(round(100*dth[i]/conf[i], 2))
            except:
                cfr.append(int('0'))
            try:
                rr.append(round(100*rec[i]/conf[i], 2))
            except:
                rr.append('No cases confirmed')
            try:
                rdr.append(round(rec[i]/dth[i], 2))
            except:
                rdr.append('No deaths occured')
        state[0] = 'India'
        data = zip(state,conf,delconf,act,delact,rec,delrec,dth,deldth,cfr,rr,rdr)
        context = {
            'data':data
        }
        return render(request,'index.html',context)

