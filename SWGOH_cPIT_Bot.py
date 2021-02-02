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
    "task_doThePitAnalysis": 1,
    "task_pit_exportHighRelicToonsNeededForPit": 0,
    "task_pit_exportPitTeamOverviewPerGuildMate": 0
}

useOnlyThisAmountOfGuildMates = 50
PitTeamCompositionTrys = 1500
minRelicLevel = 4
safetyDamageInPercentToCompensateFailedTrys = 10


allyCodes = [556142852] #836434711
# super STRONG GUild for PIT 967525461

# LoD Angry Anni 244315144 ... die schaffen wohl den Rancor nicht  https://swgoh.gg/g/37150/legends-of-doom/
# FrankElMas's Profile Rebel Assault ... die schaffen wohl den Rancor nicht 614731935
# allowishus 556142852
# Daroul 642881742
# Mish 836434711
# Guild of Light 788459779
# ALLiΔNCE KØTØR 637681396

guildNames = [None] * len(allyCodes)
playerNames =  [None] * len(allyCodes)


dict_guildMateNamesAndAllyCodes = {}
flag_allyCode = "allyCode"
flag_guildMateName = "name"

dict_teamCompostion = {}
dict_uniquePitTeamIDs = {}
# dict_uniquePitTeamsDamage = {{}}
dict_uniquePitTeamsDamage_p1 = {}
dict_uniquePitTeamsDamage_p2 = {}
dict_uniquePitTeamsDamage_p3 = {}
dict_uniquePitTeamsDamage_p4 = {}

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
flag_pitTrysDetail_uniqueIDBasedOnPitTeamIDs = "pit-team-id"
flag_pitTrysDetail_TeamsNeededThisPhase = "Teams needed"
flag_pitTrysDetail_AllyName = "AllyName"
flag_pitTrysDetail_AllyGuildCode = "AllyGuildCode"
flag_pitTrysDetail_PitTeam = "PitTeam"
flag_pitTrysDetail_PitTeam_tm1 = "Team-Member 1"
flag_pitTrysDetail_PitTeam_tm1_GearRelic = "Gear/Relic TM1"
flag_pitTrysDetail_PitTeam_tm2 = "Team-Member 2"
flag_pitTrysDetail_PitTeam_tm2_GearRelic = "Gear/Relic TM2"
flag_pitTrysDetail_PitTeam_tm3 = "Team-Member 3"
flag_pitTrysDetail_PitTeam_tm3_GearRelic = "Gear/Relic TM3"
flag_pitTrysDetail_PitTeam_tm4 = "Team-Member 4"
flag_pitTrysDetail_PitTeam_tm4_GearRelic = "Gear/Relic TM4"
flag_pitTrysDetail_PitTeam_tm5 = "Team-Member 5"
flag_pitTrysDetail_PitTeam_tm5_GearRelic = "Gear/Relic TM5"
flag_pitTrysDetail_PitPhase = "PitPhase"
flag_pitTrysDetail_expAvgDamage = "expAvgDamage"
flag_pitTrysDetail_totalDamageThisPhase = "totalDamageThisPhase"

flag_pitTrySummary_id = "ID"
flag_pitTrySummary_totalPitTeamsNeededThisTry = "Total Teams used"
flag_pitTrySummary_PhasesPassed = "TOTAL Phases FULLY Finished"
flag_pitTrySummary_LastPhase = "Last Phase Done"
flag_pitTrySummary_TotalDamageLastPhase = "Damage Achieved Last Phase"

flag_pitFinalInstruction_Instruction = "Beat The Beast"




const_noTeamThisPhaseFromThisGuildMate = "NO TEAM THIS PHASE"

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

    # print("ENDE func_getGuildData")

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
    guildMateNumber = 0
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
        guildMateNumber+=1
        print("### func_analyseThisGuildMateData >>> NEXT Guild Mate ###")
        print("#" + str(guildMateNumber) + " " + dict_guild[0]['roster'][guileMateKey]['name'] + " ID: " + str(
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
            , sep=";", index=False)

        df_glsOnly.to_csv(
            func_getFileNameAndPathForThisFile("GUILD_ROOSTER_GLs_"+guildName+".csv")
            , sep=";", index=False)

        df_criticalToons.to_csv(
            func_getFileNameAndPathForThisFile("GUILD_ROOSTER_ImportantToons_"+guildName+".csv")
            , sep=";", index=False)

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
        df_guildMasterFile, dict_guildRooster, thisAllyCode, flag_all, False)

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

    df_SUB_pitTeamOverviewPerGuildMate = pd.DataFrame()
    df_SUB_pit_HighGearToonsPerGuildMate = pd.DataFrame()

    return \
        df_guildMasterFile, df_glsOnly, df_criticalToons, \
        df_pitTeamOverviewPerGuildMate, df_pit_HighGearToonsPerGuildMate, \
        df_SUB_pitTeamOverviewPerGuildMate, df_SUB_pit_HighGearToonsPerGuildMate

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
def func_thisTeamMateRelicLevelIsSufficient(
    thisToonGearRelicLevel
):
    # print("this toon relic level " + thisToonGearRelicLevel[1:2])
    if \
        thisToonGearRelicLevel[:1] == 'R' and \
        int(thisToonGearRelicLevel[1:2]) >= minRelicLevel:
        # print("enough relicts @ level: " + thisToonGearRelicLevel[1:2])

        return True

    return False


# ######################################################################################################################
def func_fillDataframeWithAvailablePitTeams(
    df_pitTeamOverviewPerGuildMate,
    df_pit_HighGearToonsPerGuildMate
):
    logDetailsIfSquadIsAvailable = False

    for thisGuildMate in df_pit_HighGearToonsPerGuildMate:
        if thisGuildMate in dict_extraColumns:
            continue

        # print("check if pit teams are available for " + thisGuildMate)
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

            # if \
            # df_pit_HighGearToonsPerGuildMate.loc[tm1, thisGuildMate][:1] == 'R' and \
            # df_pit_HighGearToonsPerGuildMate.loc[tm2, thisGuildMate][:1] == 'R' and \
            # df_pit_HighGearToonsPerGuildMate.loc[tm3, thisGuildMate][:1] == 'R' and \
            # df_pit_HighGearToonsPerGuildMate.loc[tm4, thisGuildMate][:1] == 'R' and \
            # df_pit_HighGearToonsPerGuildMate.loc[tm5, thisGuildMate][:1] == 'R':

            if \
                func_thisTeamMateRelicLevelIsSufficient(df_pit_HighGearToonsPerGuildMate.loc[tm1, thisGuildMate]) and \
                func_thisTeamMateRelicLevelIsSufficient(df_pit_HighGearToonsPerGuildMate.loc[tm2, thisGuildMate]) and \
                func_thisTeamMateRelicLevelIsSufficient(df_pit_HighGearToonsPerGuildMate.loc[tm3, thisGuildMate]) and \
                func_thisTeamMateRelicLevelIsSufficient(df_pit_HighGearToonsPerGuildMate.loc[tm4, thisGuildMate]) and \
                func_thisTeamMateRelicLevelIsSufficient(df_pit_HighGearToonsPerGuildMate.loc[tm5, thisGuildMate]):

                df_pitTeamOverviewPerGuildMate.loc[dict_cPIT_botTeams[thisTeam]['team'], thisGuildMate] = 1
                if logDetailsIfSquadIsAvailable:
                    print("YES @ " + dict_cPIT_botTeams[thisTeam]['team'])
            else:
                df_pitTeamOverviewPerGuildMate.loc[dict_cPIT_botTeams[thisTeam]['team'], thisGuildMate] = 0
                if logDetailsIfSquadIsAvailable:
                    print("NO @ " + dict_cPIT_botTeams[thisTeam]['team'])

    return df_pitTeamOverviewPerGuildMate

# ######################################################################################################################
def func_createListWithRandomAllyOrder(
    list_randomAllyOrder
):
    keys_list = list(dict_guildMateNamesAndAllyCodes)
    # print("keys_list before random mix in new list: " + str(keys_list))

    while len(list_randomAllyOrder) < useOnlyThisAmountOfGuildMates:
        nextRandomNumber = random.randrange(0, useOnlyThisAmountOfGuildMates)
        # print("nextRandomNumber: " + str(nextRandomNumber))
        nextRandomNumber = keys_list[nextRandomNumber]
        # print("nextRandomNumber: " + str(nextRandomNumber))
        if nextRandomNumber not in list_randomAllyOrder:
            # print("add this number in list")
            list_randomAllyOrder.append(nextRandomNumber)
        # else:
        #     print("nextRandomNumber already in list, next one")

        # print("len(list_randomAllyOrder) " + str(len(list_randomAllyOrder)))

    # print("using this guild mate order for the next pit try: " +str(list_randomAllyOrder))

    return list_randomAllyOrder

# ######################################################################################################################
def func_generateNextPitTry(
    thisPhase,
    phaseTag,
    damageDoneThisPhase,
    dict_teamDamageForThisPhase,
    df_pitTeamOverviewPerGuildMate
):
    dict_teamCompostion.clear()
    totalPitTeamsNeeded = 0

    list_randomAllyOrder = list()
    list_randomAllyOrder = func_createListWithRandomAllyOrder(list_randomAllyOrder)

    # for thisGuildMateID in dict_guildMateNamesAndAllyCodes:
    for thisGuildMateID in list_randomAllyOrder:
        # print("using this next thisGuildMateID: " + str(thisGuildMateID))
        # print(dict_guildMateNamesAndAllyCodes[thisGuildMateID])

        df_thisGuildMateToons = df_pitTeamOverviewPerGuildMate[
            df_pitTeamOverviewPerGuildMate[dict_guildMateNamesAndAllyCodes[thisGuildMateID]] == 1]

        # if dict_guildMateNamesAndAllyCodes[thisGuildMateID] == 'Leonidas':
        if len(df_thisGuildMateToons) > 0:
            # print(df_thisGuildMateToons)

            # print("len: " + str(len(df_thisGuildMateToons)))
            #TODO there will be cases when it does not make sense to use a certain team straight forward in phase 1!!!
            # maybe one should check estimated damage per phase and decide if team should be saved for later
            randomPitTeamThisGuildMate = random.randint(1, len(df_thisGuildMateToons))

            if randomPitTeamThisGuildMate > 0:
                totalPitTeamsNeeded+=1
                randomPitTeamThisGuildMate = randomPitTeamThisGuildMate - 1
                dict_teamCompostion[thisGuildMateID] = df_thisGuildMateToons.index[randomPitTeamThisGuildMate]

                damageDoneThisPhase+=dict_teamDamageForThisPhase[
                    df_thisGuildMateToons.index[randomPitTeamThisGuildMate]
                ]

                if damageDoneThisPhase >= 100 + safetyDamageInPercentToCompensateFailedTrys:
                    # print("no more teams needed, damage level " +str(thisPhase) + " reached")
                    break
                # print(dict_guildMateNamesAndAllyCodes[thisGuildMateID] + " will use " +
                #       df_thisGuildMateToons.index[randomPitTeamThisGuildMate] + " in Phase " + str(thisPhase) + " with an expected damage of " +
                #       str(dict_teamDamageForThisPhase[df_thisGuildMateToons.index[randomPitTeamThisGuildMate]])
                #       )
            else:
                # there will be cases that its better to not use a certain team from a guild mate in a phase to save
                # it for the next phase
                dict_teamCompostion[thisGuildMateID] = const_noTeamThisPhaseFromThisGuildMate

            # print(df_thisGuildMateToons.index[randomPitTeamThisGuildMate])

    # print("FINAL dict_teamCompostion: " + str(dict_teamCompostion))

    return dict_teamCompostion, damageDoneThisPhase, totalPitTeamsNeeded

# ######################################################################################################################
def func_createUniquePitTestID(
    dict_teamCompostion,
    thisTry,
    thisPhase
):
    uniqueIDSeperator = "-"

    # uniqueID = "#" + uniqueIDSeperator + str(thisTry) + uniqueIDSeperator + "P" + str(thisPhase)
    uniqueID = "P" + str(thisPhase)
    for thisTeam in dict_teamCompostion:
        if dict_teamCompostion[thisTeam] != const_noTeamThisPhaseFromThisGuildMate:
            # print("we need this teams unique id: " + dict_teamCompostion[thisTeam])
            # print("ID this team: " + dict_uniquePitTeamIDs[dict_teamCompostion[thisTeam]])
            uniqueID = uniqueID + uniqueIDSeperator + dict_uniquePitTeamIDs[dict_teamCompostion[thisTeam]]
        else:
            uniqueID = uniqueID + uniqueIDSeperator + "0"

    # print("### final unique ID: " + str(uniqueID) + "\n")
    return uniqueID

# ######################################################################################################################
def func_createDictWithUniquePitTeamIDs():
    for thisTeam in range(len(dict_cPIT_botTeams)):
        dict_uniquePitTeamIDs[
            dict_cPIT_botTeams[thisTeam]['team']] =  dict_cPIT_botTeams[thisTeam]['uniqueTeamID']

    print("\n### dict_uniquePitTeamIDs ###")
    print(dict_uniquePitTeamIDs)
    print("### dict_uniquePitTeamIDs ###\n")

    return dict_uniquePitTeamIDs

# ######################################################################################################################
def func_getPhaseTag(
    thisPhase
):
    if thisPhase == 1:
        return 'p1', dict_uniquePitTeamsDamage_p1

    if thisPhase == 2:
        return 'p2', dict_uniquePitTeamsDamage_p2

    if thisPhase == 3:
        return 'p3', dict_uniquePitTeamsDamage_p3

    return 'p4', dict_uniquePitTeamsDamage_p4

# ######################################################################################################################
def func_getVideoDictThisPhase(
    thisPhase
):
    if thisPhase == 1:
        return 'source_p1'

    if thisPhase == 2:
        return 'source_p2'

    if thisPhase == 3:
        return 'source_p3'

    return 'source_p4'


# ######################################################################################################################
def func_createDictWithAverageDamagePerPhasePerTeam():
    thisPhase = 1
    while thisPhase <= 4:
        phaseTag, dict_toBeUsed = func_getPhaseTag(thisPhase)
        for thisTeam in range(len(dict_cPIT_botTeams)):
            # print("DAMAGE FOR TEAM " + str(dict_cPIT_botTeams[thisTeam]['team']) +
            #       " in phase " + phaseTag + " = " +
            #       str(dict_cPIT_botTeams[thisTeam]['averageDamagePerPhase'][0][phaseTag])
            #     )
            dict_toBeUsed[
                dict_cPIT_botTeams[thisTeam]['team']] = dict_cPIT_botTeams[thisTeam]['averageDamagePerPhase'][0][phaseTag]

        thisPhase+=1

# ######################################################################################################################
def func_createEmpyDataframeForAllResults():
    df_resultAllDetails = pd.DataFrame(
        columns=[
            flag_pitTrysDetail_id,
            flag_pitTrysDetail_uniqueIDBasedOnPitTeamIDs,
            flag_pitTrysDetail_TeamsNeededThisPhase,
            flag_pitTrysDetail_AllyName,
            flag_pitTrysDetail_AllyGuildCode,
            flag_pitTrysDetail_PitTeam,
            flag_pitTrysDetail_PitTeam_tm1,
            flag_pitTrysDetail_PitTeam_tm1_GearRelic,
            flag_pitTrysDetail_PitTeam_tm2,
            flag_pitTrysDetail_PitTeam_tm2_GearRelic,
            flag_pitTrysDetail_PitTeam_tm3,
            flag_pitTrysDetail_PitTeam_tm3_GearRelic,
            flag_pitTrysDetail_PitTeam_tm4,
            flag_pitTrysDetail_PitTeam_tm4_GearRelic,
            flag_pitTrysDetail_PitTeam_tm5,
            flag_pitTrysDetail_PitTeam_tm5_GearRelic,
            flag_pitTrysDetail_PitPhase,
            flag_pitTrysDetail_expAvgDamage,
            flag_pitTrysDetail_totalDamageThisPhase
        ]
    )

    df_resultSummary = pd.DataFrame(
        columns=[
            flag_pitTrySummary_id,
            flag_pitTrySummary_totalPitTeamsNeededThisTry,
            flag_pitTrySummary_PhasesPassed,
            flag_pitTrySummary_LastPhase,
            flag_pitTrySummary_TotalDamageLastPhase
        ]
    )

    df_bestResult = pd.DataFrame()

    df_finalInstruction = pd.DataFrame(
        columns=[
            flag_pitFinalInstruction_Instruction
        ]
    )

    return df_resultAllDetails, df_resultSummary, df_bestResult, df_finalInstruction

# ######################################################################################################################
def func_fillResultDataframe(
    thisTry,
    thisPhase,
    uniqueID,
    dict_teamCompostion,
    totalPitTeamsNeeded,
    df_resultAllDetails
):
    totalDamageThisPhase = 0
    for thisTeam in dict_teamCompostion:
        if dict_teamCompostion[thisTeam] != const_noTeamThisPhaseFromThisGuildMate:
            for thisTeamPitTeam in range(len(dict_cPIT_botTeams)):
                if dict_teamCompostion[thisTeam] == dict_cPIT_botTeams[thisTeamPitTeam]['team']:
                    tm1, tm2, tm3, tm4, tm5 = func_getTeamMember(
                        dict_cPIT_botTeams[thisTeamPitTeam]['teamMember']
                    )
            # print("thisTeam: " + dict_teamCompostion[thisTeam])
            # print("dmg: " + str(dict_teamDamageForThisPhase[dict_teamCompostion[thisTeam]]))
            totalDamageThisPhase+=dict_teamDamageForThisPhase[dict_teamCompostion[thisTeam]]
            df_resultAllDetails = df_resultAllDetails.append(
                {
                    flag_pitTrysDetail_id: thisTry,
                    flag_pitTrysDetail_PitPhase: thisPhase,
                    flag_pitTrysDetail_uniqueIDBasedOnPitTeamIDs: uniqueID,
                    flag_pitTrysDetail_TeamsNeededThisPhase: str(totalPitTeamsNeeded),
                    flag_pitTrysDetail_AllyName: dict_guildMateNamesAndAllyCodes[thisTeam],
                    flag_pitTrysDetail_AllyGuildCode: thisTeam,

                    flag_pitTrysDetail_PitTeam_tm1: tm1,
                    flag_pitTrysDetail_PitTeam_tm1_GearRelic:
                        df_guildMasterFile.loc[tm1,
                                               dict_guildMateNamesAndAllyCodes[thisTeam]],

                    flag_pitTrysDetail_PitTeam_tm2: tm2,
                    flag_pitTrysDetail_PitTeam_tm2_GearRelic:
                        df_guildMasterFile.loc[tm2,
                                               dict_guildMateNamesAndAllyCodes[thisTeam]],

                    flag_pitTrysDetail_PitTeam_tm3: tm3,
                    flag_pitTrysDetail_PitTeam_tm3_GearRelic:
                        df_guildMasterFile.loc[tm3,
                                               dict_guildMateNamesAndAllyCodes[thisTeam]],

                    flag_pitTrysDetail_PitTeam_tm4: tm4,
                    flag_pitTrysDetail_PitTeam_tm4_GearRelic:
                        df_guildMasterFile.loc[tm4,
                                               dict_guildMateNamesAndAllyCodes[thisTeam]],

                    flag_pitTrysDetail_PitTeam_tm5: tm5,
                    flag_pitTrysDetail_PitTeam_tm5_GearRelic:
                        df_guildMasterFile.loc[tm5,
                                               dict_guildMateNamesAndAllyCodes[thisTeam]],

                    flag_pitTrysDetail_PitTeam: dict_teamCompostion[thisTeam],
                    flag_pitTrysDetail_expAvgDamage: dict_teamDamageForThisPhase[dict_teamCompostion[thisTeam]],
                    flag_pitTrysDetail_totalDamageThisPhase: str(totalDamageThisPhase)
                },
                ignore_index=True
            )

    return df_resultAllDetails

# ######################################################################################################################
def func_fillSummaryDataframe(
    thisTry,
    thisPhase,
    damageDoneThisPhase,
    totalPitTeamsNeededThisTry,
    df_resultSummary
):
    if thisPhase == 4 and damageDoneThisPhase >= 100:
        phasesPassed = 4
    else:
        phasesPassed = thisPhase -1

    df_resultSummary = df_resultSummary.append(
        {
            flag_pitTrySummary_id: thisTry,
            flag_pitTrySummary_totalPitTeamsNeededThisTry: str(totalPitTeamsNeededThisTry),
            flag_pitTrySummary_LastPhase: thisPhase,
            flag_pitTrySummary_PhasesPassed: phasesPassed,
            flag_pitTrySummary_TotalDamageLastPhase: damageDoneThisPhase
        },
        ignore_index=True
    )

    return df_resultSummary

# ######################################################################################################################
def func_restoreInitialValuesForNextTry(
    df_SUB_pit_HighGearToonsPerGuildMate,
    df_SUB_pitTeamOverviewPerGuildMate
):

    df_pit_HighGearToonsPerGuildMate = df_SUB_pit_HighGearToonsPerGuildMate.copy()
    df_pitTeamOverviewPerGuildMate = df_SUB_pitTeamOverviewPerGuildMate.copy()

    return df_pit_HighGearToonsPerGuildMate, df_pitTeamOverviewPerGuildMate

# ######################################################################################################################
def func_updateHighGearToonsPerGuildMate(
    dict_teamCompostion,
    df_pit_HighGearToonsPerGuildMate
):
    for thisAllycode in dict_teamCompostion:
        thisGuildMate = dict_guildMateNamesAndAllyCodes[thisAllycode]
        # print("Deactivate all Toons in the HighGearRelicTable for the used team of " +
        #       dict_teamCompostion[thisAllycode] + " for guild mate " + thisGuildMate)

        for thisTeam in range(len(dict_cPIT_botTeams)):
            if dict_teamCompostion[thisAllycode] == dict_cPIT_botTeams[thisTeam]['team']:
                tm1, tm2, tm3, tm4, tm5 = func_getTeamMember(
                    dict_cPIT_botTeams[thisTeam]['teamMember']
                )

                # print("tm1: " + tm1)
                # print("tm2: " + tm2)
                # print("tm3: " + tm3)
                # print("tm4: " + tm4)
                # print("tm5: " + tm5)

                df_pit_HighGearToonsPerGuildMate.loc[tm1, thisGuildMate] = "USED"
                df_pit_HighGearToonsPerGuildMate.loc[tm2, thisGuildMate] = "USED"
                df_pit_HighGearToonsPerGuildMate.loc[tm3, thisGuildMate] = "USED"
                df_pit_HighGearToonsPerGuildMate.loc[tm4, thisGuildMate] = "USED"
                df_pit_HighGearToonsPerGuildMate.loc[tm5, thisGuildMate] = "USED"


    return df_pit_HighGearToonsPerGuildMate

# ######################################################################################################################
def func_exportUpdatedDataframes(
    exportSubDataframesToCheckAlgo,
    thisTry, thisPhase,
    df_pit_HighGearToonsPerGuildMate, df_pitTeamOverviewPerGuildMate
):
    if exportSubDataframesToCheckAlgo:
        df_pit_HighGearToonsPerGuildMate.to_csv(
            func_getFileNameAndPathForThisFile(
                str(thisTry) + "_" + str(thisPhase) + "_df_pit_HighGearToonsPerGuildMate" + ".csv"),
            sep=";", index=False)

        df_pitTeamOverviewPerGuildMate.to_csv(
            func_getFileNameAndPathForThisFile(
                str(thisTry) + "_" + str(thisPhase) + "_df_pitTeamOverviewPerGuildMate" + ".csv"),
            sep=";", index=False)

# ######################################################################################################################
def func_exportThisFileIntoCSV(
    thisDF,
    flagWhat
):
    if flagWhat == "df_resultSummary":
        thisDF.to_csv(
            func_getFileNameAndPathForThisFile("_1_PIT_RESULT_Overview" + ".csv"),
            sep=";", index=False)

    if flagWhat == "df_resultAllDetails":
        thisDF.to_csv(
            func_getFileNameAndPathForThisFile("_2_PIT_RESULT_DETAILs" + ".csv"),
            sep=";", index=False)

    if flagWhat == "df_bestResult":
        thisDF.to_csv(
            func_getFileNameAndPathForThisFile("_3_PIT_BEST_RESULT_Details" + ".csv"),
            sep=";", index=False)

    if flagWhat == "df_finalInstruction":
        thisDF.to_csv(
            func_getFileNameAndPathForThisFile("_4_PIT_FinalInstruction" + ".csv"),
            sep=";", index=False)

# ######################################################################################################################
def func_appendThisString(
    df_finalInstruction,
    str_thisInstruction
):
    df_finalInstruction = df_finalInstruction.append(
        {
            flag_pitFinalInstruction_Instruction: str_thisInstruction
        },
        ignore_index=True
    )

    return df_finalInstruction

# ######################################################################################################################
def func_checkIfRelicLevelAreMissing(
    thisGuildMate,
    pitTeamMember,
    putSomeRelicsOn
):
    if \
        df_guildMasterFile.loc[pitTeamMember, thisGuildMate] != "R5" and \
        df_guildMasterFile.loc[pitTeamMember, thisGuildMate] != "R6" and \
        df_guildMasterFile.loc[pitTeamMember, thisGuildMate] != "R7" and \
        df_guildMasterFile.loc[pitTeamMember, thisGuildMate] != "R8":
        putSomeRelicsOn = putSomeRelicsOn + "(" + pitTeamMember + " only " +  df_guildMasterFile.loc[pitTeamMember, thisGuildMate] + ") "

    return putSomeRelicsOn

# ######################################################################################################################
def func_getNamesOfAllGuildMatesUsingThisTeam(
    subDF_guildMatesWithThatTeamInThatPhase,
    tm1, tm2, tm3, tm4, tm5
):
    guildMateString = ""
    for thisGuildMate in subDF_guildMatesWithThatTeamInThatPhase[flag_pitTrysDetail_AllyName].unique():
        print("team was used by: " + thisGuildMate)

        putSomeRelicsOn = " ... Relicts missing for: "
        putSomeRelicsOn = func_checkIfRelicLevelAreMissing(thisGuildMate, tm1, putSomeRelicsOn)
        putSomeRelicsOn = func_checkIfRelicLevelAreMissing(thisGuildMate, tm2, putSomeRelicsOn)
        putSomeRelicsOn = func_checkIfRelicLevelAreMissing(thisGuildMate, tm3, putSomeRelicsOn)
        putSomeRelicsOn = func_checkIfRelicLevelAreMissing(thisGuildMate, tm4, putSomeRelicsOn)
        putSomeRelicsOn = func_checkIfRelicLevelAreMissing(thisGuildMate, tm5, putSomeRelicsOn)

        if len(putSomeRelicsOn) == len(" ... Relicts missing for: "):
            putSomeRelicsOn = " ... all toons at perfect relic level"

        if len(guildMateString) == 0:
            guildMateString = guildMateString + "@" + thisGuildMate + putSomeRelicsOn + "\n"
        else:
            guildMateString = guildMateString + "@" + thisGuildMate + putSomeRelicsOn + "\n"

    return guildMateString

# ######################################################################################################################
def func_createFinalResult(
    df_resultSummary,
    df_resultAllDetails,
    df_bestResult,
    df_finalInstruction
):
    thisPhase = 1
    str_thisInstruction = ""

    totalPhaseAccomplished = df_resultSummary.iloc[0, df_resultSummary.columns.get_loc(flag_pitTrySummary_LastPhase)]
    print("Lets create the final instruction for all " + str(totalPhaseAccomplished) + " phases.")
    while thisPhase <= totalPhaseAccomplished:
        print("\n### PHASE " + str(thisPhase) + " ###########################")

        str_thisInstruction = "### INSTRUCTION for PIT PHASE " + str(thisPhase) + " ###########################"

        df_finalInstruction = func_appendThisString(df_finalInstruction, str_thisInstruction)

        for thisPitTeam in df_bestResult[flag_pitTrysDetail_PitTeam].unique():
            print("\n### START with that team: " + thisPitTeam)

            videoDictElementThisPhase = func_getVideoDictThisPhase(thisPhase)

            for thisTeamPitTeam in range(len(dict_cPIT_botTeams)):
                if thisPitTeam == dict_cPIT_botTeams[thisTeamPitTeam]['team']:
                    tm1, tm2, tm3, tm4, tm5 = func_getTeamMember(
                        dict_cPIT_botTeams[thisTeamPitTeam]['teamMember']
                    )

                    videoPath = dict_cPIT_botTeams[thisTeamPitTeam][videoDictElementThisPhase]

            subDF_guildMatesWithThatTeamInThatPhase = df_bestResult[
                (df_bestResult[flag_pitTrysDetail_PitTeam] == thisPitTeam) &
                (df_bestResult[flag_pitTrysDetail_PitPhase] == thisPhase)
                ]

            guildMateString = func_getNamesOfAllGuildMatesUsingThisTeam(
                subDF_guildMatesWithThatTeamInThatPhase, tm1, tm2, tm3, tm4, tm5
            )

            # there are cases where teams are used in other phases and should therefore not show up as empty string
            if len(guildMateString) == 0:
                continue

            str_thisInstruction = ("###############################\n# PIT TEAM: " + \
                "1. " + str(tm1) + " / " + \
                "2. " + str(tm2) + " / " + \
                "3. " + str(tm3) + " / " + \
                "4. " + str(tm4) + " / " + \
                "5. " + str(tm5) + " / "
            )
            df_finalInstruction = func_appendThisString(df_finalInstruction, str_thisInstruction)

            str_thisInstruction = (">>> TARGET DAMAGE: " + str(dict_teamDamageForThisPhase[thisPitTeam]) + "% <<<")
            df_finalInstruction = func_appendThisString(df_finalInstruction, str_thisInstruction)



            guildMateString = "# Please use this team \n" + guildMateString
            df_finalInstruction = func_appendThisString(df_finalInstruction, guildMateString)

            str_education = ""
            if len(videoPath) > 0:
                str_education = "sample video for this team & phase: " + videoPath

            df_finalInstruction = func_appendThisString(df_finalInstruction, str_education)

        thisPhase+=1

    return df_finalInstruction

# ######################################################################################################################
# ######################################################################################################################
# ######################################################################################################################

file_dir = os.path.dirname(os.path.abspath(__file__))

listOf_guildMasterFile = list()
listOf_glsOnly = list()
listOf_criticalToons = list()
listOf_allPossiblePitTeams = list()

df_guildMasterFile, df_glsOnly, df_criticalToons, \
df_pitTeamOverviewPerGuildMate, df_pit_HighGearToonsPerGuildMate, \
df_SUB_pitTeamOverviewPerGuildMate, df_SUB_pit_HighGearToonsPerGuildMate = func_createMainDFs()

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

    # print("### dict_guildMateNamesAndAllyCodes ###")
    # print(dict_guildMateNamesAndAllyCodes)


#region CORE ALGO ... create random pit team compositions to finish that beast
if dict_tasks["task_doThePitAnalysis"]:
    exportSubDataframesToCheckAlgo = False

    df_resultAllDetails, df_resultSummary, df_bestResult, df_finalInstruction = func_createEmpyDataframeForAllResults()
    dict_uniquePitTeamIDs = func_createDictWithUniquePitTeamIDs()
    func_createDictWithAverageDamagePerPhasePerTeam()
    # print("dict_uniquePitTeamsDamage_p1: " + str(dict_uniquePitTeamsDamage_p1))
    # print("dict_uniquePitTeamsDamage_p2: " + str(dict_uniquePitTeamsDamage_p2))
    # print("dict_uniquePitTeamsDamage_p3: " + str(dict_uniquePitTeamsDamage_p3))
    # print("dict_uniquePitTeamsDamage_p4: " + str(dict_uniquePitTeamsDamage_p4))

    # print(df_pitTeamOverviewPerGuildMate.head(3)

    if dict_tasks["task_pit_exportHighRelicToonsNeededForPit"]:
        df_pit_HighGearToonsPerGuildMate.to_csv(
            func_getFileNameAndPathForThisFile("df_pit_HighGearToonsPerGuildMate" + ".csv"),
            sep=";", index=False)

    df_pitTeamOverviewPerGuildMate = func_fillDataframeWithAvailablePitTeams(
        df_pitTeamOverviewPerGuildMate,
        df_pit_HighGearToonsPerGuildMate
    )

    if dict_tasks["task_pit_exportPitTeamOverviewPerGuildMate"]:
        df_pitTeamOverviewPerGuildMate.to_csv(
            func_getFileNameAndPathForThisFile("df_pitTeamOverviewPerGuildMate" + ".csv"),
            sep=";", index=False)

    df_SUB_pit_HighGearToonsPerGuildMate = df_pit_HighGearToonsPerGuildMate.copy()
    df_SUB_pitTeamOverviewPerGuildMate = df_pitTeamOverviewPerGuildMate.copy()

    thisTry = 1
    while thisTry <= PitTeamCompositionTrys:
        df_pit_HighGearToonsPerGuildMate, df_pitTeamOverviewPerGuildMate = func_restoreInitialValuesForNextTry(
            df_SUB_pit_HighGearToonsPerGuildMate, df_SUB_pitTeamOverviewPerGuildMate
        )

        if exportSubDataframesToCheckAlgo:
            df_pitTeamOverviewPerGuildMate.to_csv(
                func_getFileNameAndPathForThisFile(
                    str(thisTry) + "_INITAL_" + "_df_pitTeamOverviewPerGuildMate" + ".csv"),
                sep=";", index=False)

        thisPhase = 1
        totalDamageDoneThisTry = 0
        setupsCreatedThisPhase = 0
        totalPitTeamsNeededThisTry = 0
        print("\n##################################################################### "
              "### NEXT TRY #" +str(thisTry) + " to beat the beast ######################################")
        while thisPhase <= 4:
            setupsCreatedThisPhase+= 1
            damageDoneThisPhase = 0
            totalPitTeamsNeededThisPhase = 0
            # comments should not be used, code should be self explanatory, but there is quite some complexity involved

            # STEP1: loop through all available PIT Teams per guild mate and create unique pit team composition
            # ... stop as soon as enough teams are available to finish the phase
            phaseTag, dict_teamDamageForThisPhase = func_getPhaseTag(thisPhase)

            dict_teamCompostion, damageDoneThisPhase, totalPitTeamsNeededThisPhase = \
                func_generateNextPitTry(
                    thisPhase, phaseTag,
                    damageDoneThisPhase, dict_teamDamageForThisPhase, df_pitTeamOverviewPerGuildMate
                )

            totalPitTeamsNeededThisTry+= totalPitTeamsNeededThisPhase

            if damageDoneThisPhase >= 100 + safetyDamageInPercentToCompensateFailedTrys:
                totalDamageDoneThisTry+= 100
            else:
                totalDamageDoneThisTry+= damageDoneThisPhase

            uniqueID = func_createUniquePitTestID(dict_teamCompostion, thisTry, thisPhase)

            if uniqueID in df_resultAllDetails.values:
                if totalDamageDoneThisTry < 100 + safetyDamageInPercentToCompensateFailedTrys:
                    print("Unique ID ("+str(uniqueID)+") available >> this setup was tested before with only "+str(totalDamageDoneThisTry)+"% damage >> create new one")

                    if setupsCreatedThisPhase < 10:
                        print("RETRY to create a unique setup ... same setup was created again. this was the " + str(
                            setupsCreatedThisPhase) + ".")
                        continue
                    else:
                        print("STOP to create a unique setup ... same setup was created again. this was the " + str(setupsCreatedThisPhase) + ".")
                        break

            df_resultAllDetails = func_fillResultDataframe(
                thisTry, thisPhase, uniqueID, dict_teamCompostion, totalPitTeamsNeededThisPhase, df_resultAllDetails)

            # print("totalDamagePossibleThisSetup: " + str(df_resultAllDetails.loc[uniqueID, totalDamageThisPhase]));

            if damageDoneThisPhase < 100:
                # print("Damage done in Phase " + str(thisPhase) + " is only " + str(damageDoneThisPhase) + " no need to further test, restart with new setup")
                print("UPS. " + str(thisPhase) + " damage only: " + str(damageDoneThisPhase) + "% ... next try")

                df_resultSummary = func_fillSummaryDataframe(
                    thisTry, thisPhase, damageDoneThisPhase, totalPitTeamsNeededThisTry, df_resultSummary)

                break
            else:
                print("OH YES! Phase " + str(thisPhase) + " is doable")

                if thisPhase == 4:
                    df_resultSummary = func_fillSummaryDataframe(
                        thisTry, thisPhase, damageDoneThisPhase, totalPitTeamsNeededThisTry, df_resultSummary)

                #region IMPORATANT >> UPDATE GUILD MATE ROOSTER with available toons!
                df_pit_HighGearToonsPerGuildMate = \
                    func_updateHighGearToonsPerGuildMate(
                        dict_teamCompostion, df_pit_HighGearToonsPerGuildMate
                    )

                # after updating the guild rooster >> rebuild of PIT TEAM overview
                df_pitTeamOverviewPerGuildMate = func_fillDataframeWithAvailablePitTeams(
                    df_pitTeamOverviewPerGuildMate,
                    df_pit_HighGearToonsPerGuildMate
                )
                #endregion

                #region export updated dataframes after this pit phase
                func_exportUpdatedDataframes(exportSubDataframesToCheckAlgo, thisTry, thisPhase,
                                             df_pit_HighGearToonsPerGuildMate, df_pitTeamOverviewPerGuildMate)
                #endregion

            thisPhase+=1

        thisTry+=1

    df_resultSummary = df_resultSummary.sort_values(
        by=[
            flag_pitTrySummary_LastPhase,
            flag_pitTrySummary_TotalDamageLastPhase
        ], ascending=False
    )

    func_exportThisFileIntoCSV(df_resultSummary, "df_resultSummary")

    func_exportThisFileIntoCSV(df_resultAllDetails, "df_resultAllDetails")

    df_bestResult = df_resultAllDetails[
        df_resultAllDetails[flag_pitTrysDetail_id] ==
        df_resultSummary.iloc[0, df_resultSummary.columns.get_loc(flag_pitTrySummary_id)]
    ]

    func_exportThisFileIntoCSV(df_bestResult, "df_bestResult")

    df_finalInstruction = func_createFinalResult(
        df_resultSummary, df_resultAllDetails, df_bestResult, df_finalInstruction)

    func_exportThisFileIntoCSV(df_finalInstruction, "df_finalInstruction")

#print(df_guildMasterFile.loc['General Kenobi', 'Daeshara'])

print("dict_guildMateNamesAndAllyCodes")
print(dict_guildMateNamesAndAllyCodes)

if len(allyCodes) > 1:
    if dict_tasks["task_compare_guilds"] or dict_tasks["task_compare_players"]:
        func_letsCompareTheFinalDatasets(
            listOf_guildMasterFile, listOf_glsOnly, listOf_criticalToons)

