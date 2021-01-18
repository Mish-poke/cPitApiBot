#!/usr/bin/env python3

import json

from api_swgoh_help import api_swgoh_help, settings


# Initialize data structures
toons = {}
skills = {}
abilities = {}
gear = {}

# ######################################################################################################################
def func_convertRelicLevel(
    thisRelicLevel
):

    relicLevel = thisRelicLevel - 2
    if relicLevel < 0:
        relicLevel = 0

    return relicLevel

# ######################################################################################################################
def func_getHighGearCount(
    gearLevelThisToon, cntR12, cntR13
):
    if players[0]['roster'][thisUnit]['gear'] == 12:
        cntR12 += 1
    if players[0]['roster'][thisUnit]['gear'] == 13:
        cntR13 += 1

    return cntR12, cntR13

# ######################################################################################################################
def func_showMainToonInfo(
    players,
    thisUnit
):
    print(
        "UNIT: " + players[0]['roster'][thisUnit]['defId'] + " " +
        "Gear: " + str(players[0]['roster'][thisUnit]['gear']) + " " +
        # "GP: " + str(players[0]['roster'][thisUnit]['gp']) + " " +
        "RELIC: " + str(func_convertRelicLevel(int(players[0]['roster'][thisUnit]['relic']['currentTier'])))
    )

# ######################################################################################################################
# ######################################################################################################################
# Change the settings below
creds = settings('Mishpoke', 'Hainkman.#10sh')
client = api_swgoh_help(creds)

print(client)

allycodes = [836434711]


# players = client.fetchPlayers(allycodes)

payload = {}
payload['allycodes'] = [allycodes]
payload['language'] = "eng_us"
payload['enums'] = True
result = client.fetchGuilds(payload)

print(result)

# print(result[5]['name'])

# print(result[0])
# print(result[0]['roster'][11]['name'])

# ######################################################################################################################

print(str(len(result[0]['roster'])))

for guileMateKey in range(len(result[0]['roster'])):
    print("### NEXT Guild Mate ###")
    print(result[0]['roster'][guileMateKey]['name'] + " ID: " + str(result[0]['roster'][guileMateKey]['allyCode']))

    ### limit analysis for one guild mate as of now ... remove line in case any guild mate should be used
    if result[0]['roster'][guileMateKey]['name'] == "Bon Rick": #Mishpoke
        players = client.fetchPlayers(int(result[0]['roster'][guileMateKey]['allyCode']))
        # print(players)
        # print(players[0]['roster'][0]['defId'])
        cntR12 = 0
        cntR13 = 0

        for thisUnit in range(len(players[0]['roster'])):
            if players[0]['roster'][thisUnit]['combatType'] == 'CHARACTER':
                if players[0]['roster'][thisUnit]['gear'] >= 12:
                    cntR12, cntR13 = func_getHighGearCount(
                        players[0]['roster'][thisUnit]['gear'],
                        cntR12, cntR13
                    )

                    func_showMainToonInfo(players, thisUnit)

        print(result[0]['roster'][guileMateKey]['name'] + " >>> R12 " + str(cntR12) + " // R13  " + str(cntR13) + " ")

exit()

# ######################################################################################################################
print("Build local list of obtainable characters")
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

print("###############################")
# print(units)

for thisUnit in units:
    toons[thisUnit['baseId']] = thisUnit
    print(toons[thisUnit['baseId']])

# ######################################################################################################################
print("Build local skills list")
payload = {}
payload['collection'] = "skillList"
payload['language'] = "eng_us"
payload['enums'] = True
payload['project'] = { "id": 1,
                       "abilityReference": 1,
                       "isZeta": 1
                       }
masterSkillData = client.fetchData(payload)

print("### masterSkillData ############################")
# print(masterSkillData)

for thisSkill in masterSkillData:
    skills[thisSkill['id']] = thisSkill
    print(thisSkill)

# ######################################################################################################################
print("Build local abilities list")
# skills[id]['abilityReference'] -> abilities[id]
payload = {}
payload['collection'] = "abilityList"
payload['language'] = "eng_us"
payload['enums'] = True
payload['project'] = { "id": 1,
                       "type": 1,
                       "nameKey": 1
                       }

userSkillData = client.fetchData(payload)
# print("### userSkillData ############################")
# print(userSkillData)

for ability in userSkillData:
    abilities[ability['id']] = ability['nameKey']
    print(ability['nameKey'])

# ######################################################################################################################
print("Build local gear list")
payload = {}
payload['collection'] = "equipmentList"
payload['language'] = "eng_us"
payload['enums'] = True
payload['project'] = {"id": 1,
                      "nameKey": 1
                      }
userGearList = client.fetchData(payload)

for item in userGearList:
    gear[item['id']] = item['nameKey']
    print(item['nameKey'])

payload = {}
payload['allycodes'] = allycodes
payload['language'] = "eng_us"
payload['enums'] = True
# Remove the project payload element to retrieve the player's entire roster
payload['project'] = { "name": 1 }

# Fetch player information (one or more allycodes in a list)
players = client.fetchPlayers(allycodes)

# Fetch a list of guild member allycodes
allycodes = [836434711, 647481613]
guild_allycodes = client.fetchGuilds(allycodes)

# Fetch a list of ranked zeta recommendations
zetas = client.fetchZetas()

print("done")
