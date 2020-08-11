from django.utils.timezone import datetime
from django.shortcuts import reverse
import json
import requests
from status.models import StateData

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()


@sched.scheduled_job('cron',hour=20,minute=51)
def yesterday_api():
    print("Hello000000000000000000000000000000")
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
        # state_data.save()

sched.start()