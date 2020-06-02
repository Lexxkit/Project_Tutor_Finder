"""This script is used for creating json files for project data:
 - teacher.json file from the mok data at data.py
 - booking.json and request.json - empty files to use in app.py for DB purposes
Run it once before start the app!!! Otherwise, all saved data will be deleted!"""
import json
import pprint   # this import is used for commented section

import data

with open('teachers_bd.json', 'w', encoding='utf-8') as f_w:
    json.dump(data.teachers, f_w, ensure_ascii=False)

with open('booking.json', 'w', encoding='utf-8') as f_w:
    info = []
    json.dump(info, f_w, ensure_ascii=False)

with open('request.json', 'w', encoding='utf-8') as f_w:
    info = []
    json.dump(info, f_w, ensure_ascii=False)


'''Uncomment the following section if you you want to check that json file is created properly
with open('teachers_bd.json', 'r') as f_t:
    teachers = json.load(f_t)

pprint.pprint(teachers)

with open('booking.json', 'r') as f_b:
    booking = json.load(f_b)
pprint(booking)
    
with open('request.json', 'r') as f_r:
    request = json.load(f_r)
pprint(request)
'''
