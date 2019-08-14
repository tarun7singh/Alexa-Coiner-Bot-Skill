import requests, json
r = [{
    "id": "null",
    "name": {
        "value": "USD",
        "synonyms": ["US Dollar", "Dollar", "American Dollar"]
    }
},{
    "id": "null",
    "name": {
        "value": "AUD",
        "synonyms": ["Australian Dollar"]
    }
}, {
    "id": "null",
    "name": {
        "value": "BRL",
        "synonyms": ["Brazilian Real", "Real"]
    }
}, {
    "id": "null",
    "name": {
        "value": "CAD",
        "synonyms": ["Canadian Dollar"]
    }
}, {
    "id": "null",
    "name": {
        "value": "CHF",
        "synonyms": ["Swiss franc", "Fr", "CHf", "SFr"]
    }
}, {
    "id": "null",
    "name": {
        "value": "CLP",
        "synonyms": ["Chilean peso"]
    }
}, {
    "id": "null",
    "name": {
        "value": "CNY",
        "synonyms": ["Chinese Yuan", "Renminbi", "Yuan"]
    }
}, {
    "id": "null",
    "name": {
        "value": "CZK",
        "synonyms": ["Czech Koruna", "Koruna"]
    }
}, {
    "id": "null",
    "name": {
        "value": "DKK",
        "synonyms": ["Danish krone"]
    }
}, {
    "id": "null",
    "name": {
        "value": "EUR",
        "synonyms": ["Euro"]
    }
}, {
    "id": "null",
    "name": {
        "value": "GBP",
        "synonyms": ["British Pound", "Pound sterling"]
    }
}, {
    "id": "null",
    "name": {
        "value": "HKD",
        "synonyms": ["Hong Kong dollar"]
    }
}, {
    "id": "null",
    "name": {
        "value": "HUF",
        "synonyms": ["Hungarian forint"]
    }
}, {
    "id": "null",
    "name": {
        "value": "IDR",
        "synonyms": ["Indonesian Rupiah"]
    }
}, {
    "id": "null",
    "name": {
        "value": "ILS",
        "synonyms": ["Israeli shekel", "Israeli new shekel"]
    }
}, {
    "id": "null",
    "name": {
        "value": "INR",
        "synonyms": ["Indian Rupee", "Rupee"]
    }
}, {
    "id": "null",
    "name": {
        "value": "JPY",
        "synonyms": ["yen", "Japanese yen"]
    }
}, {
    "id": "null",
    "name": {
        "value": "KRW",
        "synonyms": ["Korean Won", "South Korean Won"]
    }
}, {
    "id": "null",
    "name": {
        "value": "MXN",
        "synonyms": ["Mexican Peso"]
    }
}, {
    "id": "null",
    "name": {
        "value": "MYR",
        "synonyms": ["Malaysian ringgit", "ringgit"]
    }
}, {
    "id": "null",
    "name": {
        "value": "NOK",
        "synonyms": ["Norwegian krone", "krone"]
    }
}, {
    "id": "null",
    "name": {
        "value": "NZD",
        "synonyms": ["New Zealand dollar"]
    }
}, {
    "id": "null",
    "name": {
        "value": "PHP",
        "synonyms": ["Philippine Peso", "Philippine Piso"]
    }
}, {
    "id": "null",
    "name": {
        "value": "PKR",
        "synonyms": ["Pakistani Rupee"]
    }
}, {
    "id": "null",
    "name": {
        "value": "PLN",
        "synonyms": ["Polish Zloty", "zloty"]
    }
}, {
    "id": "null",
    "name": {
        "value": "RUB",
        "synonyms": ["ruble", "Russian ruble"]
    }
}, {
    "id": "null",
    "name": {
        "value": "SEK",
        "synonyms": ["Swedish Krona"]
    }
}, {
    "id": "null",
    "name": {
        "value": "SGD",
        "synonyms": ["Singapore Dollar"]
    }
}, {
    "id": "null",
    "name": {
        "value": "THB",
        "synonyms": ["Thai baht", "baht"]
    }
}, {
    "id": "null",
    "name": {
        "value": "TRY",
        "synonyms": ["Turkish lira", "lira"]
    }
}, {
    "id": "null",
    "name": {
        "value": "TWD",
        "synonyms": ["Taiwan dollar", "New Taiwan dollar"]
    }
}, {
    "id": "null",
    "name": {
        "value": "ZAR",
        "synonyms": ["rand", "South African rand"]
    }
}]
result = {}
for coin in r:
    result[coin["name"]["value"]] = coin["name"]["synonyms"][0] + 's'
with open('fiat_list.json', 'w') as outfile:
    json.dump(result, outfile)