from django.shortcuts import render,reverse
from django.http import HttpResponseRedirect,JsonResponse
import json
import requests
from django.views.generic import View
from django.utils.timezone import datetime

from .models import StateData


class HomeView(View):
    def get(self,request,*args,**kwargs):
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
        testtemp=[]
        test=[]
        req1=requests.get('https://api.covid19india.org/state_test_data.json')
        z=json.loads(req1.text)

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
        for states in state:
            for i in range(0,len(z['states_tested_data'])):
                if z['states_tested_data'][i]['state']==states:
                    testtemp.append(z['states_tested_data'][i]['totaltested'])
            if(len(testtemp)!=0):
                test.append(testtemp[-1])
            else:
                test.append('0')
        sum_=0
        for i in range(0,len(test)):
            test[i]=int(test[i])
            sum_+=test[i]
        test[0]=sum_
        state[0] = 'INDIA'
        for i in range(38):
            join=[] 
            join.extend([state[i],conf[i],delconf[i],act[i],delact[i],rec[i],delrec[i],dth[i],deldth[i],cfr[i],rr[i],test[i]])
            combined.append(join)
        combined=sorted(combined,key=lambda x: x[1],reverse=True)
        comb = []
        for i in range(38):
            data = zip([combined[i][0]],[combined[i][1]],[combined[i][2]],[combined[i][3]],[combined[i][4]],[combined[i][5]],[combined[i][6]],[combined[i][7]],[combined[i][8]],[combined[i][9]],[combined[i][10]],[combined[i][11]])
            comb.append(data)
        
        context = {
            'combined':comb
        }
        return render(request,'index.html',context)

def about(request):
    return render(request,'about.html')


def yesterday_api(request):
    today = datetime.now()
    state_data = StateData.objects.filter(timestamp__day=today.day,timestamp__month=today.month,timestamp__year=today.year)
    if state_data.count() == 0:
        req = requests.get('https://api.covid19india.org/data.json')
        data = json.loads(req.text)
        for i in range(38):
            state_data = StateData()
            state = data['statewise'][i]['state']
            if(state == "State Unassigned"):
                continue
            active = int(data['statewise'][i]['active'])
            confirmed = int(data['statewise'][i]['confirmed'])
            confirmed_today = int(data['statewise'][i]['deltaconfirmed'])
            recovered = int(data['statewise'][i]['recovered'])
            recovered_today =  int(data['statewise'][i]['deltarecovered'])
            deaths = int(data['statewise'][i]['deaths'])
            deaths_today = int(data['statewise'][i]['deltadeaths'])
            active_today = confirmed_today - deaths_today - recovered_today
            if(state == "Total"):
                state = "India"
            state_data.location = state
            state_data.confirmed = confirmed
            state_data.confirmed_today = confirmed_today
            state_data.active = active
            state_data.active_today = active_today
            state_data.recovered = recovered
            state_data.recovered_today = recovered_today
            state_data.deaths = deaths
            state_data.deaths_today = deaths_today
            state_data.save()
        return HttpResponseRedirect(reverse('api-yesterday'))

    context = dict()
    for i in state_data:
        context[i.location]={
            'confirmed':i.confirmed,
            'confirmed_today':i.confirmed_today,
            'active':i.active,
            'active_today':i.active_today,
            'recovered':i.recovered,
            'recovered_today':i.recovered_today,
            'deaths':i.deaths,
            'deaths_today':i.deaths_today
        }
    return JsonResponse(context,status=200)


def yesterday_data(request):
    req3=requests.get('https://covid19slim.herokuapp.com/api/yesterday')
    x=json.loads(req3.text)
    location=[]
    conf_total=[]
    dth_total=[]
    rec_total=[]
    act_total=[]
    delact_yest=[]
    deldth_yest=[]
    delconf_yest=[]
    delrec_yest=[]
    for state in x: 
        if state!='India':   
            location.append(state)
        else:
            location.append('INDIA')
        conf_total.append(x[state]['confirmed'])
        dth_total.append(x[state]['deaths'])
        rec_total.append(x[state]['recovered'])
        act_total.append(x[state]['active'])
        delact_yest.append(x[state]['active_today'])
        delconf_yest.append(x[state]['confirmed_today'])
        deldth_yest.append(x[state]['deaths_today'])
        delrec_yest.append(x[state]['recovered_today'])
    combined=[]
    for i in range(37):
        join=[] 
        join.extend([location[i],conf_total[i],delconf_yest[i],act_total[i],delact_yest[i],rec_total[i],delrec_yest[i],dth_total[i],deldth_yest[i]])
        combined.append(join)
    combined=sorted(combined,key=lambda x: x[1],reverse=True)
    comb = []
    for i in range(37):
        data = zip([combined[i][0]],[combined[i][1]],[combined[i][2]],[combined[i][3]],[combined[i][4]],[combined[i][5]],[combined[i][6]],[combined[i][7]],[combined[i][8]])
        comb.append(data)

    context = {
        'combined':comb
    }

    return render(request,'yesterday.html',context)
