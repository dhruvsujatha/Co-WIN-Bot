import requests
import json
from datetime import date
import time
from dotenv import load_dotenv, find_dotenv
import os

today = date.today()

dateNeeded = today.strftime("%d-%m-%Y")

urlss = 'https://discord.com/api/webhooks/843163876488118273/keN5f6orbIL23atTyHD9S50QPH24sXNbbJY1r1qnXJ7HRREX1rlZrhZyi8UD1OLUhJiM'

load_dotenv(find_dotenv())
auth = os.getenv('TOTALLYLEGALAUTHCODE')

headers = {
        'authority': 'scrapeme.live',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        "authorization" : auth,
    }

puburl = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='
proturl = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id='

statesmeta = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
distmeta = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/'

class metaAPI:
    def getstates(self):
        url = statesmeta
        print(url)
        resp = requests.get(url, headers = headers)
        return resp
    
    def getdist(self, state_id):
        url = distmeta+str(state_id)
        resp = requests.get(url, headers = headers)
        return resp

class CoWinAPI:
    def publicapi(self, district_id):
        url = puburl+str(district_id)+'&date='+str(dateNeeded)
        print(url)
        resp = requests.get(url, headers=headers)
        return resp
    
    def protectedapi(self, district_id):
        url = proturl+str(district_id)+'&date='+str(dateNeeded)
        print(url)
        resp = requests.get(url, headers=headers)
        return resp

class vacc(dict):
    def __init__(self, name, address, pincode, block_name, fee_type, available_capacity, vaccine, date, start, end, age):
        self.name = name
        self.address = address
        self.block_name = block_name
        self.fee_type = fee_type
        self.available_capacity = available_capacity
        self.vaccine = vaccine
        self.date = date
        self.age = age
        self.pincode = pincode
        self.start = start
        self.end = end

    def asdict(self):
        return {'name': self.name, 'address': self.address, 'pincode': self.pincode, 'block_name': self.block_name, 'fee_type': self.fee_type, 'available_capacity': self.available_capacity, 'vaccine': self.vaccine, 'date': self.date, 'from': self.start, 'to': self.end, 'age': self.age}

    def __getattr__(self, attr):
        return self[attr]


class dataSel:
    def __init__(self, resp, age = 18, min_avail = 5):
        self.resp = resp
        self.age = age
        self.min_avail = min_avail
        
    def dataSelection(self):
        filtered_centers = {'centers': []}
        available_centers = json.loads(self.resp.text)
        for center in available_centers['centers']:
            for slot in center['sessions']:
                if (slot['available_capacity'] > self.min_avail) & (slot['min_age_limit'] == self.age):
                    filtered_center = vacc(
                        center['name'], center['address'], center['pincode'], center['block_name'], center['fee_type'], slot['available_capacity'], slot['vaccine'], slot['date'], center['from'], center['to'], slot['min_age_limit'])
                    filtered_centers['centers'].append(
                        filtered_center.asdict())
        return filtered_centers

def currentresp(resp):
    currresplst = []
    for i in range(0, len(resp['centers'])):
        currresplst.append(resp['centers'][i])
    return currresplst