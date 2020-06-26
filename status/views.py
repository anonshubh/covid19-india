from django.shortcuts import render,redirect
import json
import requests
from django.views.generic import View
from .forms import DarkTheme

class HomeView(View):
    form = DarkTheme
    def get(self,request,*args,**kwargs):
        data = fetch_data()
        context = {
            'combined':data,
            'form':self.form(),
        }
        return render(request,'index-light.html',context)
    
    def post(self,request,*args,**kwargs):
        switch = request.POST.get('night_theme')
        if switch == 'on':
            form = self.form(initial={'night_theme':True})
            data = fetch_data()
            context = {
                'combined':data,
                'form':form,
            }
            return render(request,'index-dark.html',context)
        else:
            return redirect('home')

def about(request):
    return render(request,'about-light.html')

def about_dark(request):
    return render(request,'about-dark.html')

def fetch_data():
    combined=[]
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
            cfr.append(float('0.0'))
        try:
            if rec[i]==0 and conf[i]!=0:
                rr.append('No Recoveries Yet')
            else:
                rr.append(round(100*rec[i]/conf[i],2))
        except:
            rr.append('No cases confirmed')
        try:
            rdr.append(round(rec[i]/dth[i], 2))
        except:
            rdr.append('No deaths occured')
    state[0] = 'INDIA'
    for i in range(38):
        join=[]
        join.extend([state[i],conf[i],delconf[i],act[i],delact[i],rec[i],delrec[i],dth[i],deldth[i],cfr[i],rr[i],rdr[i]])
        combined.append(join)
    combined=sorted(combined,key=lambda x: x[1],reverse=True)
    combi = []
    for i in range(38):
        data = zip([combined[i][0]],[combined[i][1]],[combined[i][2]],[combined[i][3]],[combined[i][4]],[combined[i][5]],[combined[i][6]],[combined[i][7]],[combined[i][8]],[combined[i][9]],[combined[i][10]],[combined[i][11]])
        combi.append(data)
    return combi