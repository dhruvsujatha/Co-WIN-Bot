import requests
import json
from datetime import date
import time

today = date.today()

dateNeeded = today.strftime("%d-%m-%Y")

urlss = 'https://discord.com/api/webhooks/843163876488118273/keN5f6orbIL23atTyHD9S50QPH24sXNbbJY1r1qnXJ7HRREX1rlZrhZyi8UD1OLUhJiM'

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
        "authorization" : "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiI5NWEwNGEwZS03YmNjLTQxY2QtYTBhYS00ZDU2OWRmZGNmNDMiLCJ1c2VyX2lkIjoiOTVhMDRhMGUtN2JjYy00MWNkLWEwYWEtNGQ1NjlkZmRjZjQzIiwidXNlcl90eXBlIjoiQkVORUZJQ0lBUlkiLCJtb2JpbGVfbnVtYmVyIjo5OTg2MDUwNjUxLCJiZW5lZmljaWFyeV9yZWZlcmVuY2VfaWQiOjg0NDE0NTI4MjA3NzAwLCJzZWNyZXRfa2V5IjoiYjVjYWIxNjctNzk3Ny00ZGYxLTgwMjctYTYzYWExNDRmMDRlIiwidWEiOiJNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTAuMC40NDMwLjkzIFNhZmFyaS81MzcuMzYiLCJkYXRlX21vZGlmaWVkIjoiMjAyMS0wNS0xMFQxMDoxNzoyMy4yNTBaIiwiaWF0IjoxNjIwNjQxODQzLCJleHAiOjE2MjA2NDI3NDN9.Z-maZOH1iqv3RH_VMM8y0xfcm5waXN40S-dt_-Dp0bQ",
    }

puburl = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id='
proturl = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id='

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

class vaccine_center(dict):
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
    def __init__(self, resp, age):
        self.resp = resp
        self.age = age
        
    def dataSelection(self):
        filtered_centers = {'centers': []}
        available_centers = json.loads(self.resp.text)
        for center in available_centers['centers']:
            for slot in center['sessions']:
                if (slot['available_capacity'] > 5) & (slot['min_age_limit'] == self.age):
                    filtered_center = vaccine_center(
                        center['name'], center['address'], center['pincode'], center['block_name'], center['fee_type'], slot['available_capacity'], slot['vaccine'], slot['date'], center['from'], center['to'], slot['min_age_limit'])
                    filtered_centers['centers'].append(
                        filtered_center.asdict())
        return filtered_centers

def currentresp(resp):
    currresplst = []
    for i in range(0, len(resp['centers'])):
        currresplst.append(resp['centers'][i])
    return currresplst

def checkdupevals(data):
    for i in range(0, len(data)):
        oldname = data['centers'][i]["name"]
        oldarea = data['centers'][i]["block_name"]
        oldpin = data['centers'][i]["pincode"]
        oldvacc = data['centers'][i]["vaccine"]
        olddate = data['centers'][i]["date"]
        oldstart = data['centers'][i]["from"]
        oldend = data['centers'][i]["to"]
        oldfeetype = data['centers'][i]["fee_type"]
        oldavail = data['centers'][i]["available_capacity"]