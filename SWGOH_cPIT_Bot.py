#!/usr/bin/env python3

import json

from SWGOH_cPIT_Bot_VARs import *
from api_swgoh_help import api_swgoh_help, settings

dict_cPitTeamsPerGuildMate =  [{} for sub in range(50)]

dict_teamNames = {
    'dict_padme': 'PADME',
    'dict_gas': 'GENERALSKYWALKER'
}

teamMember_01 = "tm1"
teamMember_02 = "tm1"
teamMember_03 = "tm1"
teamMember_04 = "tm1"
teamMember_05 = "tm1"

phase_01 = 'p1'
phase_02 = 'p2'
phase_03 = 'p3'
phase_04 = 'p4'

# Initialize data structures
toons = {}
skills = {}
abilities = {}
gear = {}

creds = settings('Mishpoke', 'Hainkman.#10sh')
client = api_swgoh_help(creds)

allycodes = [836434711]

print(listAllToons)
print(dict_cPIT_botTeams)

print(dict_teamNames['dict_padme'])

print(dict_cPIT_botTeams[0]['team'])
print(dict_cPIT_botTeams[0]['teamMember'])
print(dict_cPIT_botTeams[0]['teamMember'][0][teamMember_01])
print(dict_cPIT_botTeams[0]['averageDamagePerPhase'][0][phase_01])

print(dict_cPIT_botTeams[1]['team'])

flag_guildTeamDicts_playerName = "GuildMate"
# dict_cPIT_botTeams = [
#     {
#         'team': 'PADME',
#         'teamMember':
#         [
#             {'tm1': 'PADMEAMIDALA', 'tm2': 'AHSOKATANO', 'tm3': 'ANAKINKNIGHT', 'tm4': 'GENERALKENOBI', 'tm5': 'C3POLEGENDARY'}
#         ],
#         'averageDamagePerPhase':
#         [
#             {'p1': 4.5, 'p2': 4.5, 'p3': 4.5, 'p4': 4.5}
#         ],
#     },
#     {
#         'team': 'GENERALSKYWALKER',
#         'teamMember': [
#             {'tm1': 'GENERALSKYWALKER', 'tm2': 'CT7567', 'tm3': 'ARCTROOPER501ST', 'tm4': 'CT210408', 'tm5': 'CT5555'}
#         ],
#         'averageDamagePerPhase':
#         [
#             {'p1': 4, 'p2': 4, 'p3': 4, 'p4': 4}
#         ],
#     }
# ]

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
    dict_GuildMateDetails, thisUnit, cntR12, cntR13
):
    if dict_GuildMateDetails[0]['roster'][thisUnit]['gear'] == 12:
        cntR12 += 1
    if dict_GuildMateDetails[0]['roster'][thisUnit]['gear'] == 13:
        cntR13 += 1

    return cntR12, cntR13

# ######################################################################################################################
def func_showMainToonInfo(
    dict_GuildMateDetails,
    thisUnit
):
    print(
        "UNIT: " + dict_GuildMateDetails[0]['roster'][thisUnit]['defId'] + " " +
        "Gear: " + str(dict_GuildMateDetails[0]['roster'][thisUnit]['gear']) + " " +
        # "GP: " + str(dict_GuildMateDetails[0]['roster'][thisUnit]['gp']) + " " +
        "RELIC: " + str(func_convertRelicLevel(int(dict_GuildMateDetails[0]['roster'][thisUnit]['relic']['currentTier'])))
    )

# ######################################################################################################################
def func_getGuildData(
):
    payload = {}
    payload['allycodes'] = [allycodes]
    payload['language'] = "eng_us"
    payload['enums'] = True
    result = client.fetchGuilds(payload)

    # print(result)

    return result


# ######################################################################################################################
def func_prepareMasterTeamDictWithAllDataPerGuildMate(
    dict_guild
):
    print("############################")
    cnt = 0

    for guileMateKey in range(len(dict_guild[0]['roster'])):
        # print("### NEXT Guild Mate ###")
        print(dict_guild[0]['roster'][guileMateKey]['name'] + " ID: " + str(dict_guild[0]['roster'][guileMateKey]['allyCode']))
        dict_cPitTeamsPerGuildMate[cnt][flag_guildTeamDicts_playerName] = str(dict_guild[0]['roster'][guileMateKey]['name'])

        # for thisTeam in range(len(dict_cPIT_botTeams)):
        #     # print("cPIT TEAM: " + dict_cPIT_botTeams[thisTeam]['team'])
        #     dict_cPitTeamsPerGuildMate[cnt][flag_guildTeamDicts_playerName]['cpit'] = str(dict_cPIT_botTeams[thisTeam]['team'])
        #
        cnt+=1

    print(dict_cPitTeamsPerGuildMate)
    print("############################")

# ######################################################################################################################
def func_loopGuildRooster(
    dict_guild
):
    print(str(len(dict_guild[0]['roster'])))

    for guileMateKey in range(len(dict_guild[0]['roster'])):
        print("### NEXT Guild Mate ###")
        print(dict_guild[0]['roster'][guileMateKey]['name'] + " ID: " + str(dict_guild[0]['roster'][guileMateKey]['allyCode']))

        func_analyseThisGuildMateData(dict_guild, guileMateKey)

# ######################################################################################################################
def func_analyseThisGuildMateData(
    dict_guild,
    guileMateKey
):
    ### limit analysis for one guild mate as of now ... remove line in case any guild mate should be used
    if dict_guild[0]['roster'][guileMateKey]['name'] == "Mishpoke":  # Mishpoke
        dict_GuildMateDetails = client.fetchPlayers(int(dict_guild[0]['roster'][guileMateKey]['allyCode']))

        # print(dict_GuildMateDetails)
        # print(dict_GuildMateDetails[0]['roster'][0]['defId'])
        cntR12 = 0
        cntR13 = 0

        for thisUnit in range(len(dict_GuildMateDetails[0]['roster'])):
            if dict_GuildMateDetails[0]['roster'][thisUnit]['combatType'] == 'CHARACTER':
                # print("'" + dict_GuildMateDetails[0]['roster'][thisUnit]['defId'] + "',")
                if dict_GuildMateDetails[0]['roster'][thisUnit]['gear'] >= 12:
                    cntR12, cntR13 = func_getHighGearCount(
                        dict_GuildMateDetails, thisUnit,
                        cntR12, cntR13
                    )

                    func_showMainToonInfo(dict_GuildMateDetails, thisUnit)

        print(
            dict_guild[0]['roster'][guileMateKey]['name'] + " >>> R12 " + str(cntR12) + " // R13  " + str(cntR13) + " ")

# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################
dict_guildRooster = func_getGuildData()
dict_cPitTeamsPerGuildMate = func_prepareMasterTeamDictWithAllDataPerGuildMate(dict_guildRooster)
func_loopGuildRooster(dict_guildRooster)

# dict_listOfAllToons = func_createListOfPossibleToons()

exit()

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
