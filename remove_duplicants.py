import json

# Opening JSON file
with open('spacex_dev/spacex.json') as d:
    dictData = json.load(d)
    print(dictData.first())
