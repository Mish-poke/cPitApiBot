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

    # ######################################################################################################################
    # def func_createListOfPossibleToons(
    # ):
    #
    #     print("Build local list of obtainable characters")
    #     payload = {}
    #     payload['collection'] = "unitsList"
    #     payload['language'] = "eng_us"
    #     payload['enums'] = True
    #     payload['match'] = {"rarity": 7,
    #                         "obtainable": True,
    #                         "obtainableTime": 0
    #                         }
    #     payload['project'] = {"baseId": 1,
    #                           "nameKey": 1,
    #                           "descKey": 1,
    #                           "forceAlignment": 1,
    #                           "categoryIdList": 1,
    #                           "combatType": 1
    #                           }
    #     units = client.fetchData(payload)
    #
    #     print(units)
    #
    #     return units

    #
    #
    # print("###############################")
    # # print(units)
    #
    # for thisUnit in units:
    #     toons[thisUnit['baseId']] = thisUnit
    #     print(toons[thisUnit['baseId']])
    #
    # # ######################################################################################################################
    # print("Build local skills list")
    # payload = {}
    # payload['collection'] = "skillList"
    # payload['language'] = "eng_us"
    # payload['enums'] = True
    # payload['project'] = { "id": 1,
    #                        "abilityReference": 1,
    #                        "isZeta": 1
    #                        }
    # masterSkillData = client.fetchData(payload)
    #
    # print("### masterSkillData ############################")
    # # print(masterSkillData)
    #
    # for thisSkill in masterSkillData:
    #     skills[thisSkill['id']] = thisSkill
    #     print(thisSkill)
    #
    # # ######################################################################################################################
    # print("Build local abilities list")
    # # skills[id]['abilityReference'] -> abilities[id]
    # payload = {}
    # payload['collection'] = "abilityList"
    # payload['language'] = "eng_us"
    # payload['enums'] = True
    # payload['project'] = { "id": 1,
    #                        "type": 1,
    #                        "nameKey": 1
    #                        }
    #
    # userSkillData = client.fetchData(payload)
    # # print("### userSkillData ############################")
    # # print(userSkillData)
    #
    # for ability in userSkillData:
    #     abilities[ability['id']] = ability['nameKey']
    #     print(ability['nameKey'])
    #
    # # ######################################################################################################################
    # print("Build local gear list")
    # payload = {}
    # payload['collection'] = "equipmentList"
    # payload['language'] = "eng_us"
    # payload['enums'] = True
    # payload['project'] = {"id": 1,
    #                       "nameKey": 1
    #                       }
    # userGearList = client.fetchData(payload)
    #
    # for item in userGearList:
    #     gear[item['id']] = item['nameKey']
    #     print(item['nameKey'])
    #
    # payload = {}
    # payload['allycodes'] = allycodes
    # payload['language'] = "eng_us"
    # payload['enums'] = True
    # # Remove the project payload element to retrieve the player's entire roster
    # payload['project'] = { "name": 1 }
    #
    # # Fetch player information (one or more allycodes in a list)
    # players = client.fetchPlayers(allycodes)
    #
    # # Fetch a list of guild member allycodes
    # allycodes = [836434711, 647481613]
    # guild_allycodes = client.fetchGuilds(allycodes)
    #
    # # Fetch a list of ranked zeta recommendations
    # zetas = client.fetchZetas()
    #
    # print("done")
