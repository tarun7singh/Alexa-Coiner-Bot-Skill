import requests, json
URL = 'https://api.coinmarketcap.com/v1/ticker/?limit=100'
r = requests.get(URL)
r = r.json()
result = []
for coin in r:
    single = {
        "id": 'null',
        "name": {
            "value": coin['id'],
            "synonyms": [
            coin['name'],
            coin['symbol'],
            coin['symbol'].lower()
            ]
        }
    }
    result.append(single)
with open('currency_slot.json', 'w') as outfile:
    json.dump(result, outfile)