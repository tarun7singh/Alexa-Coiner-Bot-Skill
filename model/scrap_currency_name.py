import requests, json
URL = 'https://api.coinmarketcap.com/v1/ticker/?limit=100'
r = requests.get(URL)
r = r.json()
result = []
for coin in r:
    single = coin['name'].title()
    result.append(single)
with open('currency_name.json', 'w') as outfile:
    json.dump(result, outfile)