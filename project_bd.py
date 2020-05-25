"""This script is used for creating json files for project data:
 - teacher.json file from the mok data at data.py
Run it once before start the app!!! Otherwise, all saved data will be deleted!"""
import data
import json
import pprint

with open('teachers_bd.json', 'w', encoding='utf-8') as f_w:
    json.dump(data.teachers, f_w, ensure_ascii=False)


'''Uncomment the following section if you you want to check that json file is created properly
with open('teachers_bd.json', 'r') as f_t:
    teachers = json.load(f_t)

pprint.pprint(teachers)
'''
