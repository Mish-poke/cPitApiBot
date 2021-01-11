from api_swgoh_help import *
api_client = api_swgoh_help(settings('<Mishpoke>', '<Hainkman.#10sh>'))
allycodes = [123456789]

# Build local list of obtainable characters
payload = {}
payload['collection'] = "unitsList"
payload['language'] = "eng_us"
payload['enums'] = True
payload['match'] = {"rarity": 7,
                    "obtainable": True,
                    "obtainableTime": 0
                    }
payload['project'] = {"baseId": 1,
                      "nameKey": 1,
                      "descKey": 1,
                      "forceAlignment": 1,
                      "categoryIdList": 1,
                      "combatType": 1
                      }
units = client.fetchData(payload)

for unit in units:
    toons[unit['baseId']] = unit