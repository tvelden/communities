# this script is to check the countries and their continents
# the printed output need to be added into codata dictionaries
# make sure all the countries are covered in both dictionaries in codata

import json, codata
f = open('all_records.json', 'rU')
records = json.loads(f.read())
f.close()

countries = []
for key, val in records.iteritems():
    countries += val[6]
countries = set(countries)

findCo = []
for co in countries:
    if co.title() not in codata.cn_to_ccn.keys():
        findCo.append(co)
print findCo
