#!/usr/bin/env python3

import json
import pandas as pd
from SWGOH_cPIT_Bot_VARs import *
from api_swgoh_help import api_swgoh_help, settings

MASTER_ExportGuildData = True
df_guildMasterFile = pd.DataFrame()
df_glsOnly = pd.DataFrame()
df_criticalToons = pd.DataFrame()

flag_all = 'all toons'
flag_gls = 'gls only'
flag_critical = 'important toon only'

dict_extraColumns = {
    "G11": " G11",
    "G12": " G12",
    "G13": " G13",
    "G13_R123": " G13_R123",
    "G13_R456": " G13_R456",
    "G13_R7": " G13_R7",
    "G13_R8": " G13_R8"
}

useAllGuildMates = False
useThisGuildMateOnly ="allowishus"

allycodes = [556142852]# 438248876 788459779
# allowishus 556142852
# Daroul 642881742
# Mish 836434711
# Guild of Light 788459779
# ALLiΔNCE KØTØR 637681396

minGearLevelForAnalysis = 1

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


# print(listAllToons)
# print(dict_cPIT_botTeams)
#
# print(dict_teamNames['dict_padme'])
#
# print(dict_cPIT_botTeams[0]['team'])
# print(dict_cPIT_botTeams[0]['teamMember'])
# print(dict_cPIT_botTeams[0]['teamMember'][0][teamMember_01])
# print(dict_cPIT_botTeams[0]['averageDamagePerPhase'][0][phase_01])
#
# print(dict_cPIT_botTeams[1]['team'])

flag_guildTeamDicts_playerName = "GuildMate"


# print(dict_cPIT_botTeams)

# for thisTeam in range(len(dict_cPIT_botTeams)):
#     print("cPIT TEAM: " + dict_cPIT_botTeams[thisTeam]['team'])
#     # dict_cPitTeamsPerGuildMate[cnt][flag_guildTeamDicts_playerName]['cpit'] = str(dict_cPIT_botTeams[thisTeam]['team'])
#
# exit()

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
        "UNIT: " + dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'] + " " +
        "Gear: " + str(dict_GuildMateDetails[0]['roster'][thisUnit]['gear']) + " " +
        # "GP: " + str(dict_GuildMateDetails[0]['roster'][thisUnit]['gp']) + " " +
        "RELIC: " + str(func_convertRelicLevel(int(dict_GuildMateDetails[0]['roster'][thisUnit]['relic']['currentTier'])))
    )

# ######################################################################################################################
def func_getGuildData(
):
    print("START func_getGuildData")
    payload = {}
    payload['allycodes'] = [allycodes]
    payload['language'] = "eng_us"
    payload['enums'] = True
    result = client.fetchGuilds(payload)


    guildName = result[0]['name']
    print(result)

    print("ENDE func_getGuildData")

    return result, guildName


# ######################################################################################################################
def func_prepareMasterTeamDictWithAllDataPerGuildMate(
    dict_guild
):
    print("############################")
    cnt = 0

    for guileMateKey in range(len(dict_guild[0]['roster'])):
        # print("### NEXT Guild Mate ###")
        # print(dict_guild[0]['roster'][guileMateKey]['name'] + " ID: " + str(dict_guild[0]['roster'][guileMateKey]['allyCode']))
        dict_cPitTeamsPerGuildMate[cnt][flag_guildTeamDicts_playerName] = str(dict_guild[0]['roster'][guileMateKey]['name'])

        # for thisTeam in range(len(dict_cPIT_botTeams)):
        #     # print("cPIT TEAM: " + dict_cPIT_botTeams[thisTeam]['team'])
        #     dict_cPitTeamsPerGuildMate[cnt][flag_guildTeamDicts_playerName]['cpit'] = str(dict_cPIT_botTeams[thisTeam]['team'])
        #
        cnt+=1

    print("dict_cPitTeamsPerGuildMate ############################")
    print(dict_cPitTeamsPerGuildMate)
    print("############################")

# ######################################################################################################################
def func_loopGuildRooster(
    dict_guild,
    df_guildRooster,
    df_glsOnly,
    df_criticalToons
):
    print(str(len(dict_guild[0]['roster'])))

    for guileMateKey in range(len(dict_guild[0]['roster'])):
        df_guildRooster, df_glsOnly, df_criticalToons = func_analyseThisGuildMateData(
            dict_guild, guileMateKey, df_guildRooster, df_glsOnly, df_criticalToons)

    return df_guildRooster, df_glsOnly


# ######################################################################################################################
def func_getGearLevelOrRelicLevel(
    dict_GuildMateDetails, thisUnit
):
    if dict_GuildMateDetails[0]['roster'][thisUnit]['gear'] <= 12:
        return "G" + str(dict_GuildMateDetails[0]['roster'][thisUnit]['gear'])
    else:
        return "R" + str(func_convertRelicLevel(int(dict_GuildMateDetails[0]['roster'][thisUnit]['relic']['currentTier'])))

# ######################################################################################################################
def func_getExtraColumnForThisToon(
    thisGearOrRelicLevel
):
    if thisGearOrRelicLevel == "G11":
        return dict_extraColumns["G11"]

    if thisGearOrRelicLevel == "G12":
        return dict_extraColumns["G12"]

    if thisGearOrRelicLevel == "R1" or thisGearOrRelicLevel == "R2" or thisGearOrRelicLevel == "R3":
        return dict_extraColumns["G13_R123"]

    if thisGearOrRelicLevel == "R4" or thisGearOrRelicLevel == "R5" or thisGearOrRelicLevel == "R6":
        return dict_extraColumns["G13_R456"]

    if thisGearOrRelicLevel == "R7":
        return dict_extraColumns["G13_R7"]

    if thisGearOrRelicLevel == "R8":
        return dict_extraColumns["G13_R8"]

    return ""

# ######################################################################################################################
def func_analyseThisGuildMateData(
    dict_guild,
    guileMateKey,
    df_guildRooster,
    df_glsOnly,
    df_criticalToons
):
    guildMateName = str(dict_guild[0]['roster'][guileMateKey]['name'])

    ### limit analysis for one guild mate as of now ... remove line in case any guild mate should be used
    if useAllGuildMates or guildMateName == useThisGuildMateOnly:  # Mishpoke
        print("### NEXT Guild Mate ###")
        print(dict_guild[0]['roster'][guileMateKey]['name'] + " ID: " + str(
            dict_guild[0]['roster'][guileMateKey]['allyCode']))

        dict_GuildMateDetails = client.fetchPlayers(int(dict_guild[0]['roster'][guileMateKey]['allyCode']))

        # print(dict_GuildMateDetails)
        # print(dict_GuildMateDetails[0]['roster'][0]['nameKey'])
        cntR12 = 0
        cntR13 = 0

        for thisUnit in range(len(dict_GuildMateDetails[0]['roster'])):
            if dict_GuildMateDetails[0]['roster'][thisUnit]['combatType'] == 'CHARACTER':
                # print("'" + dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'] + "',")
                if dict_GuildMateDetails[0]['roster'][thisUnit]['gear'] >= minGearLevelForAnalysis:
                    thisGearOrRelicLevel = func_getGearLevelOrRelicLevel(dict_GuildMateDetails, thisUnit)
                    thisExtraColumn = func_getExtraColumnForThisToon(thisGearOrRelicLevel)

                    # print('### ' + str( dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey']))
                    # print("thisGearOrRelicLevel: " + str(thisGearOrRelicLevel))
                    # print("thisExtraColumn: " + str(thisExtraColumn))

                    df_guildRooster = func_fillDetailsForThisDataframe(
                        df_guildRooster,
                        dict_GuildMateDetails,
                        guildMateName,
                        thisUnit,
                        thisGearOrRelicLevel,
                        thisExtraColumn)

                    if dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'] in list_gls:
                        df_glsOnly = func_fillDetailsForThisDataframe(
                            df_glsOnly,
                            dict_GuildMateDetails,
                            guildMateName,
                            thisUnit,
                            thisGearOrRelicLevel,
                            thisExtraColumn)

                    if dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'] in list_criticalToons:
                        df_criticalToons = func_fillDetailsForThisDataframe(
                            df_criticalToons,
                            dict_GuildMateDetails,
                            guildMateName,
                            thisUnit,
                            thisGearOrRelicLevel,
                            thisExtraColumn)

                    cntR12, cntR13 = func_getHighGearCount(
                        dict_GuildMateDetails, thisUnit,
                        cntR12, cntR13
                    )
                else:
                    if exportGuildDataAsCSV:
                        df_guildRooster.loc[
                            dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
                            guildMateName] = 'na'
                    # func_showMainToonInfo(dict_GuildMateDetails, thisUnit)

        print(
            dict_guild[0]['roster'][guileMateKey]['name'] + " >>> R12 " + str(cntR12) + " // R13  " + str(cntR13) + " ")

    return df_guildRooster, df_glsOnly, df_criticalToons

# ######################################################################################################################
def func_fillDetailsForThisDataframe(
    thisDF,
    dict_GuildMateDetails,
    guildMateName,
    thisUnit,
    thisGearOrRelicLevel,
    thisExtraColumn
):
    #region fill Main Rooster DF
    thisDF.loc[
        dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
        guildMateName] = thisGearOrRelicLevel

    if thisGearOrRelicLevel[:1] == "R":
        if dict_extraColumns["G13"] in thisDF.columns:
            thisDF.loc[
                dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'], dict_extraColumns["G13"]] = \
                thisDF.loc[dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
                dict_extraColumns["G13"]] + 1
        else:
            thisDF[dict_extraColumns["G13"]] = 0
            thisDF.loc[
                dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
                dict_extraColumns["G13"]] = 1

    if thisExtraColumn != "":
        # print("count this toon in this extra column: " + str(thisExtraColumn) )
        if thisExtraColumn in thisDF.columns:
            # print("Column is there already")
            # print("Current value: " + str( thisDF.loc[
            #     dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
            #     thisExtraColumn] ))
            thisDF.loc[
                dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
                thisExtraColumn] = thisDF.loc[
                dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
                thisExtraColumn] + 1
        else:
            # print("NEW column")
            thisDF[thisExtraColumn] = 0
            thisDF.loc[
                dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
                thisExtraColumn] = 1
    #endregion

    return thisDF

# ######################################################################################################################
def func_prepareDataframeWithAllToons(
    thisDF,
    dict_guild,
    flag_whatDF,
    logGuildMateDetails
):
    if flag_whatDF ==  flag_all:
        thisDF = pd.DataFrame(index=listAllToons)

    if flag_whatDF == flag_gls:
        thisDF = pd.DataFrame(index=list_gls)

    if flag_whatDF == flag_critical:
        thisDF = pd.DataFrame(index=list_criticalToons)

    for guileMateKey in range(len(dict_guild[0]['roster'])):
        if useAllGuildMates or dict_guild[0]['roster'][guileMateKey]['name'] == useThisGuildMateOnly:
            if logGuildMateDetails:
                print("### ADD NEXT Guild Mate ###")
                print(
                    dict_guild[0]['roster'][guileMateKey]['name'] +
                    " ID: " + str(dict_guild[0]['roster'][guileMateKey]['allyCode'])
                )

            newColumnName = str(dict_guild[0]['roster'][guileMateKey]['name'])

            if logGuildMateDetails:
                print("nextColumnName " + newColumnName)

            thisDF[newColumnName] = ""
            # thisDF = thisDF.assign(newColumnName = newColumnName)

    return thisDF

# ######################################################################################################################
def func_resortColumns(
        df_guildMasterFile,
        dict_guildRooster
):
    df_guildMasterFile.columns = df_guildMasterFile.columns.sort_values()

    return df_guildMasterFile

# ######################################################################################################################
def func_addMissingColumnsForGearCount(
    thisDF
):
    for thisElement in dict_extraColumns:
        if dict_extraColumns[thisElement] not in thisDF.columns:
            print("up, this column is missing, no toon in such category: " + thisElement)
            thisDF[ dict_extraColumns[thisElement]] = 0

    return thisDF

# ######################################################################################################################
def func_exportGuildDataIntoFiles(
    guildName,
    dict_guildRooster,
    df_guildMasterFile,
    df_glsOnly,
    df_criticalToons
):
    df_guildMasterFile = func_addMissingColumnsForGearCount(df_guildMasterFile)
    df_glsOnly = func_addMissingColumnsForGearCount(df_glsOnly)
    df_criticalToons = func_addMissingColumnsForGearCount(df_criticalToons)

    df_guildMasterFile = df_guildMasterFile.sort_index(axis=1)
    df_glsOnly = df_glsOnly.sort_index(axis=1)
    df_criticalToons = df_criticalToons.sort_index(axis=1)

    df_guildMasterFile.to_csv("GUILD_ROOSTER_"+guildName+".csv", sep=";")
    df_glsOnly.to_csv("GUILD_ROOSTER_GLs_"+guildName+".csv", sep=";")
    df_criticalToons.to_csv("GUILD_ROOSTER_ImportantToons_"+guildName+".csv", sep=";")

    fileName = "GUILD_ROOSTER_"+guildName+".xlsx"
    # writer = pd.ExcelWriter(fileName, engine='xlsxwriter')

    with pd.ExcelWriter(fileName) as writer:
        df_guildMasterFile.to_excel(writer, sheet_name='GUILD_ALL')
        df_glsOnly.to_excel(writer, sheet_name='GUILD_GLs')
        df_criticalToons.to_excel(writer, sheet_name='ImportantToons')

# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################

dict_guildRooster, guildName = func_getGuildData()

if MASTER_ExportGuildData:
    df_guildMasterFile = func_prepareDataframeWithAllToons(df_guildMasterFile, dict_guildRooster, flag_all, True)
    df_glsOnly = func_prepareDataframeWithAllToons(df_guildMasterFile, dict_guildRooster, flag_gls, False)
    df_criticalToons = func_prepareDataframeWithAllToons(df_guildMasterFile, dict_guildRooster, flag_critical, False)

dict_cPitTeamsPerGuildMate = func_prepareMasterTeamDictWithAllDataPerGuildMate(dict_guildRooster)
df_guildMasterFile, df_glsOnly = func_loopGuildRooster(dict_guildRooster, df_guildMasterFile, df_glsOnly, df_criticalToons)

if MASTER_ExportGuildData:
    func_exportGuildDataIntoFiles(guildName, dict_guildRooster, df_guildMasterFile, df_glsOnly, df_criticalToons)


# dict_listOfAllToons = func_createListOfPossibleToons()