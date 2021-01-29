#!/usr/bin/env python3

import os
import json
import pandas as pd
import random
from SWGOH_cPIT_Bot_VARs import *
from api_swgoh_help import api_swgoh_help, settings

subFolderForFileExport = 'file-exports'

swgoh_user = os.getenv('swgoh_user')
swgoh_secret = os.getenv('swgoh_secret')

exportDataframesInCSV = False

flag_all = 'all toons'
flag_gls = 'gls only'
flag_critical = 'important toon only'
flag_pitRaidOverview = 'df with pit teams per guild mate'

dict_extraColumns = {
    "G1-G11": " TOTAL G1 - G11",
    "G12": " TOTAL G12",
    "G13": " TOTAL G13",
    "G13_R123": " G13_R123",
    "G13_R456": " G13_R456",
    "G13_R7": " G13_R7",
    "G13_R8": " G13_R8"
}

#region COMPARISON ... turn ON / OFF player or guild comparison
dict_tasks = {
    "task_compare_guilds": 0,
    "task_compare_players": 0,
    "task_exportPlayersData": 0,
    "task_exportAllGuildData" : 1,
    "task_ignoreMissingGuildMates": 0,
    "task_doThePitAnalysis": 1
}
allyCodes = [836434711] #247174967
guildNames = [None] * len(allyCodes)
playerNames =  [None] * len(allyCodes)

useOnlyThisAmountOfGuildMates = 4

dict_guildMateNamesAndAllyCodes = {}
flag_allyCode = "allyCode"
flag_guildMateName = "name"

dict_teamCompostion = {}

# allowishus 556142852
# Daroul 642881742
# Mish 836434711
# Guild of Light 788459779
# ALLiΔNCE KØTØR 637681396
#endregion

minGearLevelForAnalysis = 1

teamMember_01 = "tm1"
teamMember_02 = "tm2"
teamMember_03 = "tm3"
teamMember_04 = "tm4"
teamMember_05 = "tm5"

phase_01 = 'p1'
phase_02 = 'p2'
phase_03 = 'p3'
phase_04 = 'p4'

# Initialize data structures
toons = {}
skills = {}
abilities = {}
gear = {}

creds = settings(swgoh_user, swgoh_secret)
client = api_swgoh_help(creds)

flag_pitTrysDetail_id = "ID"
flag_pitTrysDetail_AllyName = "AllyName"
flag_pitTrysDetail_AllyGuildCode = "AllyGuildCode"
flag_pitTrysDetail_PitTeam = "PitTeam"
flag_pitTrysDetail_PitPhase = "PitPhase"
flag_pitTrysDetail_expAvgDamage = "expAvgDamage"
flag_pitTrysDetail_totalDamageThisPhase = "totalDamageThisPhase"

flag_pitTrySummary_id = "ID"
flag_pitTrySummary_uniqueIDBasedOnPitTeamIDs = "pit-team-id"
flag_pitTrySummary_TotalDamage = "Total Damage"

PitTeamCompositionTrys = 5

# print(listAllToons)
# print(dict_cPIT_botTeams)
#
# print(dict_teamNames['dict_padme'])
#
# print(dict_cPIT_botTeams[0]['team'])
# print(dict_cPIT_botTeams[0]['teamMember'])
# print(dict_cPIT_botTeams[7]['teamMember'][0][teamMember_01])
# print(dict_cPIT_botTeams[0]['averageDamagePerPhase'][0][phase_01])
#
# print(dict_cPIT_botTeams[1]['team'])

# for thisTeam in range(len(dict_cPIT_botTeams)):
#     print("cPIT TEAM: " + dict_cPIT_botTeams[thisTeam]['team'])
#     print("cPIT TEAM: " + str(dict_cPIT_botTeams[thisTeam]['teamMember']))

flag_guildTeamDicts_playerName = "GuildMate"

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
    thisAllyCode
):
    print("\n#############################################\nSTART func_getGuildData for allycode " + str(thisAllyCode))
    payload = {}
    payload['allycodes'] = [thisAllyCode]
    payload['language'] = "eng_us"
    payload['enums'] = True
    result = client.fetchGuilds(payload)

    print(result)

    guildName = result[0]['name']

    func_createFreshGuildNameDict(guildName, result)

    print("guildName " + guildName)

    print("ENDE func_getGuildData")

    return result, guildName

# ######################################################################################################################
def func_createFreshGuildNameDict(
    guildName,
    dict_guild
):
    if MASTER_createFreshGuildDict:
        print("dict_" + guildName + " = {")
        for guileMateKey in range(len(dict_guild[0]['roster'])):
            print(
                "'" + str(dict_guild[0]['roster'][guileMateKey]['name']) + "'" + ": " +
                "'" + "1" +"'" + ",")
            if guildName == 'Spartas 300':
                if dict_guild[0]['roster'][guileMateKey]['name'] not in dict_Spartas:
                    print(
                        "ATTENTION NEW GuildMate or changed name for: " +
                        str(dict_guild[0]['roster'][guileMateKey]['name'])
                    )
        print(" }")


# ######################################################################################################################
def func_fillGuildMateDictionary(
    guileMateKey,
    dict_guild
):
    guildMateName = str(dict_guild[0]['roster'][guileMateKey]['name'])
    guildMateAllyCode = str(dict_guild[0]['roster'][guileMateKey]['allyCode'])

    dict_guildMateNamesAndAllyCodes[guildMateAllyCode] = guildMateName
    # print(dict_guildMateNamesAndAllyCodes)

# ######################################################################################################################
def func_loopGuildRooster(
    dict_guild,
    df_guildRooster,
    df_glsOnly,
    df_criticalToons,
    df_pit_HighGearToonsPerGuildMate,
    thisAllyCode
):
    print(str(len(dict_guild[0]['roster'])))

    thisGuildMateNumber = 0
    for guileMateKey in range(len(dict_guild[0]['roster'])):
        thisGuildMateNumber += 1

        func_fillGuildMateDictionary(guileMateKey, dict_guild)

        if thisGuildMateNumber <= useOnlyThisAmountOfGuildMates:
            df_guildRooster, df_glsOnly, df_criticalToons, df_pit_HighGearToonsPerGuildMate = func_analyseThisGuildMateData(
                dict_guild,
                guileMateKey,
                df_guildRooster,
                df_glsOnly,
                df_criticalToons,
                df_pit_HighGearToonsPerGuildMate,
                thisAllyCode
            )

    return df_guildRooster, df_glsOnly, df_criticalToons, df_pit_HighGearToonsPerGuildMate

# ######################################################################################################################
def func_analyseThisGuildMateData(
    dict_guild,
    guileMateKey,
    df_guildRooster,
    df_glsOnly,
    df_criticalToons,
    df_pit_HighGearToonsPerGuildMate,
    thisAllyCode
):
    guildMateName = str(dict_guild[0]['roster'][guileMateKey]['name'])
    guildMateAllyCode = str(dict_guild[0]['roster'][guileMateKey]['allyCode'])

    fineToUseThisGuildMate = func_checkIfThisGuildMateShouldBeUsed(guildMateName)

    ### limit analysis for one guild mate as of now ... remove line in case any guild mate should be used
    if (
            fineToUseThisGuildMate and \
            (
                (dict_tasks["task_exportPlayersData"] and str(thisAllyCode) == str(guildMateAllyCode)) or \
                (dict_tasks["task_compare_players"] and str(thisAllyCode) == str(guildMateAllyCode)) or \
                dict_tasks["task_exportAllGuildData"] or \
                dict_tasks["task_compare_guilds"]
            )
    ):
        print("### func_analyseThisGuildMateData >>> NEXT Guild Mate ###")
        print(dict_guild[0]['roster'][guileMateKey]['name'] + " ID: " + str(
            dict_guild[0]['roster'][guileMateKey]['allyCode']))

        if str(thisAllyCode) == str(guildMateAllyCode):
            playerNames[allyCodes.index(thisAllyCode)] = dict_guild[0]['roster'][guileMateKey]['name']

        dict_GuildMateDetails = client.fetchPlayers(int(dict_guild[0]['roster'][guileMateKey]['allyCode']))

        # print(dict_GuildMateDetails)
        # print(dict_GuildMateDetails[0]['roster'][0]['nameKey'])
        cntR12 = 0
        cntR13 = 0

        for thisUnit in range(len(dict_GuildMateDetails[0]['roster'])):
            # if dict_GuildMateDetails[0]['roster'][thisUnit]['combatType'] == 'CHARACTER':
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
                    thisExtraColumn,
                    True)

                if thisGearOrRelicLevel[:1] == "R":
                    df_pit_HighGearToonsPerGuildMate = func_fillDetailsForThisDataframe(
                        df_pit_HighGearToonsPerGuildMate,
                        dict_GuildMateDetails,
                        guildMateName,
                        thisUnit,
                        thisGearOrRelicLevel,
                        thisExtraColumn,
                        False)

                if dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'] in list_gls:
                    df_glsOnly = func_fillDetailsForThisDataframe(
                        df_glsOnly,
                        dict_GuildMateDetails,
                        guildMateName,
                        thisUnit,
                        thisGearOrRelicLevel,
                        thisExtraColumn,
                        True)

                if dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'] in list_criticalToons:
                    df_criticalToons = func_fillDetailsForThisDataframe(
                        df_criticalToons,
                        dict_GuildMateDetails,
                        guildMateName,
                        thisUnit,
                        thisGearOrRelicLevel,
                        thisExtraColumn,
                        True)

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

    return df_guildRooster, df_glsOnly, df_criticalToons, df_pit_HighGearToonsPerGuildMate

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

    return dict_extraColumns["G1-G11"]

    return ""

# ######################################################################################################################
def func_checkIfThisGuildMateShouldBeUsed(
    guildMateName
):
    if guildMateName in dict_Spartas:
        if (
                (dict_tasks["task_ignoreMissingGuildMates"] == 1 and str(dict_Spartas[guildMateName]) == "1") or
                (dict_tasks["task_ignoreMissingGuildMates"] == 0)
        ):
            return True
        else:
            return False
    else:
        return True

# ######################################################################################################################
def func_fillDetailsForThisDataframe(
    thisDF,
    dict_GuildMateDetails,
    guildMateName,
    thisUnit,
    thisGearOrRelicLevel,
    thisExtraColumn,
    addExtraColumn
):
    #region fill Main Rooster DF
    thisDF.loc[
        dict_GuildMateDetails[0]['roster'][thisUnit]['nameKey'],
        guildMateName] = thisGearOrRelicLevel

    if addExtraColumn:
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
    thisAllyCode,
    flag_whatDF,
    logGuildMateDetails
):
    if flag_whatDF == flag_all:
        thisDF = pd.DataFrame(index=listAllToons)

    if flag_whatDF == flag_gls:
        thisDF = pd.DataFrame(index=list_gls)

    if flag_whatDF == flag_critical:
        thisDF = pd.DataFrame(index=list_criticalToons)

    for guileMateKey in range(len(dict_guild[0]['roster'])):
        if \
            dict_tasks["task_compare_guilds"] or \
            dict_tasks["task_exportAllGuildData"] or \
            (
                    dict_tasks["task_exportPlayersData"] and
                    dict_guild[0]['roster'][guileMateKey]['allyCode'] == thisAllyCode
            ) or \
            (
                    dict_tasks["task_compare_players"] and
                    dict_guild[0]['roster'][guileMateKey]['allyCode'] == thisAllyCode
        ):
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
            # print("ups, this column is missing, no toon in such category: " + thisElement)
            thisDF[dict_extraColumns[thisElement]] = 0

    return thisDF

# ######################################################################################################################
def func_exportGuildDataIntoFiles(
    guildName,
    dict_guild,
    thisAllyCode,
    df_guildMasterFile,
    df_glsOnly,
    df_criticalToons
):
    if exportDataframesInCSV:
        df_guildMasterFile.to_csv(
            func_getFileNameAndPathForThisFile("GUILD_ROOSTER_"+guildName+".csv")
            , sep=";")

        df_glsOnly.to_csv(
            func_getFileNameAndPathForThisFile("GUILD_ROOSTER_GLs_"+guildName+".csv")
            , sep=";")

        df_criticalToons.to_csv(
            func_getFileNameAndPathForThisFile("GUILD_ROOSTER_ImportantToons_"+guildName+".csv")
            , sep=";")

    if dict_tasks["task_exportAllGuildData"]:
        fileName = func_getFileNameAndPathForThisFile("GUILD_ROOSTER_"+guildName+".xlsx")

    if dict_tasks["task_exportPlayersData"]:
        for guileMateKey in range(len(dict_guild[0]['roster'])):
            if dict_guild[0]['roster'][guileMateKey]['allyCode'] == thisAllyCode:
                fileName = func_getFileNameAndPathForThisFile(
                    "PLAYER_ROOSTER_"+str(dict_guild[0]['roster'][guileMateKey]['name'])+".xlsx")
    # writer = pd.ExcelWriter(fileName, engine='xlsxwriter')

    with pd.ExcelWriter(fileName) as writer:
        df_guildMasterFile.to_excel(writer, sheet_name='GUILD_ALL')
        df_glsOnly.to_excel(writer, sheet_name='GUILD_GLs')
        df_criticalToons.to_excel(writer, sheet_name='ImportantToons')


# ######################################################################################################################
def func_checkIfAllAllyCodesAreNeeded(
):
    cnt = 0
    if dict_tasks["task_compare_guilds"] or dict_tasks["task_exportAllGuildData"]:
        for thisAllyCode in allyCodes:
            dict_guildRooster, thisGuildName = func_getGuildData(thisAllyCode)
            guildNames[cnt] = thisGuildName
            cnt+=1

        if guildNames[0] == guildNames[1]:
            print("\n###### both allycodes belong to the same guild. no double export needed")
            print(allyCodes)
            allyCodes.remove(allyCodes[1])
            print("remove the second ally code, its not needed")
            print(allyCodes)

        # allyCodes = func_clearAllyCodesToRemoveDoubleGuilds(guildnames)
        # TODO
        # one could make a function to filte through xzy guild names, just in case the script will be extended, so that
        # it will be possible to compare and or export many many different players or guilds. for now we remain with two


# ######################################################################################################################
def func_doAllAroundThisAllyCode(
    thisAllyCode,
    df_guildMasterFile,
    df_glsOnly,
    df_criticalToons,
    df_pitTeamOverviewPerGuildMate,
    df_pit_HighGearToonsPerGuildMate
):
    dict_guildRooster, guildName = func_getGuildData(thisAllyCode)

    #region PREPARE empty dfs
    df_guildMasterFile = func_prepareDataframeWithAllToons(
        df_guildMasterFile, dict_guildRooster, thisAllyCode, flag_all, True)

    # df_pitTeamOverviewPerGuildMate = df_guildMasterFile.copy()

    df_glsOnly = func_prepareDataframeWithAllToons(
        df_guildMasterFile, dict_guildRooster, thisAllyCode, flag_gls, False)

    df_criticalToons = func_prepareDataframeWithAllToons(
        df_guildMasterFile, dict_guildRooster, thisAllyCode, flag_critical, False)

    df_pitTeamOverviewPerGuildMate = func_prepareDataframeWithAllToons(
        df_pitTeamOverviewPerGuildMate, dict_guildRooster, thisAllyCode, flag_pitRaidOverview, False)

    df_pit_HighGearToonsPerGuildMate = func_prepareDataframeWithAllToons(
        df_pit_HighGearToonsPerGuildMate, dict_guildRooster, thisAllyCode, flag_all, False)

    #endregion

    # #region FILL dfs with needed data
    df_guildMasterFile, df_glsOnly, df_criticalToons, df_pit_HighGearToonsPerGuildMate = func_loopGuildRooster(
        dict_guildRooster, df_guildMasterFile, df_glsOnly, df_criticalToons, df_pit_HighGearToonsPerGuildMate, thisAllyCode)
    # #endregion

    df_guildMasterFile = func_fillMissingColumnsToHarmonizeLayout(df_guildMasterFile)
    df_glsOnly = func_fillMissingColumnsToHarmonizeLayout(df_glsOnly)
    df_criticalToons = func_fillMissingColumnsToHarmonizeLayout(df_criticalToons)

    if dict_tasks["task_exportPlayersData"] or dict_tasks["task_exportAllGuildData"]:
        func_exportGuildDataIntoFiles(
            guildName, dict_guildRooster, thisAllyCode,
            df_guildMasterFile, df_glsOnly, df_criticalToons
        )

    return \
        df_guildMasterFile, \
        df_glsOnly, \
        df_criticalToons, \
        df_pitTeamOverviewPerGuildMate, \
        df_pit_HighGearToonsPerGuildMate

# ######################################################################################################################
def func_fillMissingColumnsToHarmonizeLayout(
    thisDF
):
    thisDF = func_addMissingColumnsForGearCount(thisDF)

    thisDF = thisDF.sort_index(axis=1)

    return thisDF

# ######################################################################################################################
def func_letsCompareTheFinalDatasets(
    listOf_guildMasterFile,
    listOf_glsOnly,
    listOf_criticalToons
):
    df_compared_guildMasterFile = func_createNewDataframeWithMainColumnsOnly(listOf_guildMasterFile, "guildMasterFile")
    df_compared_glsOnly = func_createNewDataframeWithMainColumnsOnly(listOf_glsOnly, "glsOnly")
    df_compared_criticalToons = func_createNewDataframeWithMainColumnsOnly(listOf_criticalToons, "criticalToons")

    # TODO >> check if both array places are in use
    if dict_tasks["task_compare_guilds"]:
        fileName = func_getFileNameAndPathForThisFile(
            "COMPARISON_" + guildNames[0] +" vs " + guildNames[1] + ".xlsx"
        )

    if dict_tasks["task_compare_players"]:
        fileName = func_getFileNameAndPathForThisFile(
            "COMPARISON_" + playerNames[0] +" vs " + playerNames[1] + ".xlsx"
        )

    with pd.ExcelWriter(fileName) as writer:
        df_compared_guildMasterFile.to_excel(writer, sheet_name='GUILD_ALL')
        df_compared_glsOnly.to_excel(writer, sheet_name='GUILD_GLs')
        df_compared_criticalToons.to_excel(writer, sheet_name='ImportantToons')

# ######################################################################################################################
def func_getFirstDataFrameColumnNameSuffix(
    flag_id
):
    if dict_tasks["task_exportPlayersData"] or dict_tasks["task_compare_players"]:
        suffix = playerNames[flag_id]
    else:
        suffix = guildNames[flag_id]

    return suffix

# ######################################################################################################################
def func_renameColumnsAndAddSuffix(
    thisDF,
    suffix
):
    thisDF = thisDF[[
        dict_extraColumns["G1-G11"],
        dict_extraColumns["G12"],
        dict_extraColumns["G13"],
        dict_extraColumns["G13_R123"],
        dict_extraColumns["G13_R456"],
        dict_extraColumns["G13_R7"],
        dict_extraColumns["G13_R8"],
    ]].copy()

    thisDF.rename(columns=
    {
        dict_extraColumns["G1-G11"]: dict_extraColumns["G1-G11"] + " " + suffix,
        dict_extraColumns["G12"]: dict_extraColumns["G12"] + " " + suffix,
        dict_extraColumns["G13"]: dict_extraColumns["G13"] + " " + suffix,
        dict_extraColumns["G13_R123"]: dict_extraColumns["G13_R123"] + " " + suffix,
        dict_extraColumns["G13_R456"]: dict_extraColumns["G13_R456"] + " " + suffix,
        dict_extraColumns["G13_R7"]: dict_extraColumns["G13_R7"] + " " + suffix,
        dict_extraColumns["G13_R8"]: dict_extraColumns["G13_R8"] + " " + suffix
    }, inplace=True)

    return thisDF

# ######################################################################################################################
def func_getFileNameAndPathForThisFile(
    fileName
):
    return os.path.join(file_dir, subFolderForFileExport, fileName)

# ######################################################################################################################
def func_createNewDataframeWithMainColumnsOnly(
    thisDF,
    fileName
):
    df_guild1 = thisDF[0]
    df_guild2 = thisDF[1]

    df_guild1.to_csv(func_getFileNameAndPathForThisFile("df_guild1_BEFORE" + ".csv"), sep=";")
    suffix_g1 = func_getFirstDataFrameColumnNameSuffix(0)
    df_guild1 = func_renameColumnsAndAddSuffix(df_guild1, suffix_g1)
    df_guild1.to_csv(func_getFileNameAndPathForThisFile("df_guild1" + ".csv"), sep=";")

    suffix_g2 = func_getFirstDataFrameColumnNameSuffix(1)
    df_guild2 = func_renameColumnsAndAddSuffix(df_guild2, suffix_g2)

    mergedDF = pd.concat([df_guild1, df_guild2], axis=1)
    mergedDF.to_csv(func_getFileNameAndPathForThisFile(fileName+".csv"), sep=";")
    if dict_tasks["task_compare_guilds"]:
        mergedDF["DELTA G13"] = \
            df_guild1[(dict_extraColumns["G13"] + " " + suffix_g1)] - \
            df_guild2[(dict_extraColumns["G13"] + " " + suffix_g2)]

    return mergedDF

# ######################################################################################################################
def func_createListOfPitTeams(
    listOf_allPossiblePitTeams
):
    for thisTeam in range(len(dict_cPIT_botTeams)):
        # print("cPIT TEAM: " + dict_cPIT_botTeams[thisTeam]['team'])
        listOf_allPossiblePitTeams.append(dict_cPIT_botTeams[thisTeam]['team'])

    # print(listOf_allPossiblePitTeams)

    return listOf_allPossiblePitTeams

# ######################################################################################################################
def func_createMainDFs():
    df_guildMasterFile = pd.DataFrame()
    df_glsOnly = pd.DataFrame()
    df_criticalToons = pd.DataFrame()
    df_pitTeamOverviewPerGuildMate = pd.DataFrame()
    df_pit_HighGearToonsPerGuildMate = pd.DataFrame()

    return df_guildMasterFile, df_glsOnly, df_criticalToons, df_pitTeamOverviewPerGuildMate, df_pit_HighGearToonsPerGuildMate

# ######################################################################################################################
def func_getTeamMember(
    thisDictElement
):
    return \
        thisDictElement[0][teamMember_01],\
        thisDictElement[0][teamMember_02],\
        thisDictElement[0][teamMember_03],\
        thisDictElement[0][teamMember_04],\
        thisDictElement[0][teamMember_05]

# ######################################################################################################################
def func_fillDataframeWithAvailablePitTeams(
    df_pitTeamOverviewPerGuildMate,
    df_pit_HighGearToonsPerGuildMate
):
    logDetailsIfSquadIsAvailable = False

    for thisGuildMate in df_pit_HighGearToonsPerGuildMate:
        if thisGuildMate in dict_extraColumns:
            continue

        print("check if pit teams are available for " + thisGuildMate)
        for thisTeam in range(len(dict_cPIT_botTeams)):
            # print("cPIT TEAM: " + dict_cPIT_botTeams[thisTeam]['team'])
            # print(dict_cPIT_botTeams[thisTeam]['teamMember'])
            # print(dict_cPIT_botTeams[thisTeam]['teamMember'][0][teamMember_01])
            # print(dict_cPIT_botTeams[thisTeam]['teamMember'][0][teamMember_02])
            tm1, tm2, tm3, tm4, tm5 = func_getTeamMember(dict_cPIT_botTeams[thisTeam]['teamMember'])
            # print("tm1: " + tm1 + " R-Level " + thisGuildMate + ": " +
            #       df_pit_HighGearToonsPerGuildMate.loc[tm1, thisGuildMate])
            # print("tm2: " + tm2 + " R-Level " + thisGuildMate + ": " +
            #       df_pit_HighGearToonsPerGuildMate.loc[tm2, thisGuildMate])
            # print("tm3: " + tm3 + " R-Level " + thisGuildMate + ": " +
            #       df_pit_HighGearToonsPerGuildMate.loc[tm3, thisGuildMate])
            # print("tm4: " + tm4 + " R-Level " + thisGuildMate + ": " +
            #       df_pit_HighGearToonsPerGuildMate.loc[tm4, thisGuildMate])
            # print("tm5: " + tm5 + " R-Level " + thisGuildMate + ": " +
            #       df_pit_HighGearToonsPerGuildMate.loc[tm5, thisGuildMate])
            if \
                    df_pit_HighGearToonsPerGuildMate.loc[tm1, thisGuildMate][:1] == 'R' and \
                    df_pit_HighGearToonsPerGuildMate.loc[tm2, thisGuildMate][:1] == 'R' and \
                    df_pit_HighGearToonsPerGuildMate.loc[tm3, thisGuildMate][:1] == 'R' and \
                    df_pit_HighGearToonsPerGuildMate.loc[tm4, thisGuildMate][:1] == 'R' and \
                    df_pit_HighGearToonsPerGuildMate.loc[tm5, thisGuildMate][:1] == 'R':

                df_pitTeamOverviewPerGuildMate.loc[dict_cPIT_botTeams[thisTeam]['team'], thisGuildMate] = 1
                if logDetailsIfSquadIsAvailable:
                    print("YES @ " + dict_cPIT_botTeams[thisTeam]['team'])
            else:
                df_pitTeamOverviewPerGuildMate.loc[dict_cPIT_botTeams[thisTeam]['team'], thisGuildMate] = 0
                if logDetailsIfSquadIsAvailable:
                    print("NO @ " + dict_cPIT_botTeams[thisTeam]['team'])

    return df_pitTeamOverviewPerGuildMate

# ######################################################################################################################
def func_generateNextPitTry():
    dict_teamCompostion.clear()

    for thisGuildMateID in dict_guildMateNamesAndAllyCodes:
        # print(dict_guildMateNamesAndAllyCodes[thisGuildMateID])

        df_thisGuildMateToons = df_pitTeamOverviewPerGuildMate[
            df_pitTeamOverviewPerGuildMate[dict_guildMateNamesAndAllyCodes[thisGuildMateID]] == 1]

        # if dict_guildMateNamesAndAllyCodes[thisGuildMateID] == 'Leonidas':
        if len(df_thisGuildMateToons) > 0:
            print("df_thisGuildMateToons")
            print(df_thisGuildMateToons)

            print("len: " + str(len(df_thisGuildMateToons)))

            useThisTeam = random.randint(1, len(df_thisGuildMateToons))-1
            print(useThisTeam)

            print(df_thisGuildMateToons.index[useThisTeam])

            dict_teamCompostion[thisGuildMateID] = df_thisGuildMateToons.index[useThisTeam]



# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################

file_dir = os.path.dirname(os.path.abspath(__file__))

listOf_guildMasterFile = list()
listOf_glsOnly = list()
listOf_criticalToons = list()
listOf_allPossiblePitTeams = list()

df_guildMasterFile, df_glsOnly, df_criticalToons, df_pitTeamOverviewPerGuildMate, df_pit_HighGearToonsPerGuildMate = func_createMainDFs()

listOf_allPossiblePitTeams = func_createListOfPitTeams(listOf_allPossiblePitTeams)
df_pitTeamOverviewPerGuildMate = pd.DataFrame(index=listOf_allPossiblePitTeams)
print(df_pitTeamOverviewPerGuildMate.head(3))

if len(allyCodes) > 1:
    func_checkIfAllAllyCodesAreNeeded()

for thisAllyCode in allyCodes:
    print("### NEXT ALLY CODE: " + str(thisAllyCode))
    df_guildMasterFile, df_glsOnly, df_criticalToons, df_pitTeamOverviewPerGuildMate, df_pit_HighGearToonsPerGuildMate = \
        func_doAllAroundThisAllyCode(
            thisAllyCode,
            df_guildMasterFile,
            df_glsOnly,
            df_criticalToons,
            df_pitTeamOverviewPerGuildMate,
            df_pit_HighGearToonsPerGuildMate)

    listOf_guildMasterFile.append(df_guildMasterFile)
    listOf_glsOnly.append(df_glsOnly)
    listOf_criticalToons.append(df_criticalToons)

if dict_tasks["task_doThePitAnalysis"]:
    # print(df_pitTeamOverviewPerGuildMate.head(3)
    df_pit_HighGearToonsPerGuildMate.to_csv(
        func_getFileNameAndPathForThisFile("df_pit_HighGearToonsPerGuildMate" + ".csv"),
        sep=";")

    df_pitTeamOverviewPerGuildMate = func_fillDataframeWithAvailablePitTeams(
        df_pitTeamOverviewPerGuildMate,
        df_pit_HighGearToonsPerGuildMate
    )

    df_pitTeamOverviewPerGuildMate.to_csv(
        func_getFileNameAndPathForThisFile("df_pitTeamOverviewPerGuildMate" + ".csv"),
        sep=";")

    thisTry = 1
    while thisTry <= PitTeamCompositionTrys:
        thisUniqueID, dict_teamCompostion = func_generateNextPitTry()

print(df_guildMasterFile.loc['General Kenobi', 'Daeshara'])

print("dict_guildMateNamesAndAllyCodes")
print(dict_guildMateNamesAndAllyCodes)

if len(allyCodes) > 1:
    if dict_tasks["task_compare_guilds"] or dict_tasks["task_compare_players"]:
        func_letsCompareTheFinalDatasets(
            listOf_guildMasterFile, listOf_glsOnly, listOf_criticalToons)

