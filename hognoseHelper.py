
import pandas as pd
from pandas import DataFrame as df
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException
import os.path
from os import path
import sys
import ast
import math

def createNewColumns(snakeDataFrame,sex):
    if (path.exists("/home/nick/Documents/morphMarketHognoseMaximizer/newSnakeDataFrame" + sex) != True):
        #for all morph combos in the dataframe
        print("creating new dataframe with new columns")
        
        #this gets list of all possible morphs
        listOfAllMorphs = []
        for x in snakeDataFrame["morphs"]:
            x = x.replace(" 66%","").replace("100% ","").replace("66%","").replace("100%","").replace("50%","").replace("100% ","").replace(" Pos","").replace("Pos","").replace("Normal","")
            x = ast.literal_eval(x)
            #print(x)
            
            #print(type(morphList))
            #for all the morphs in the combo list x
            for z in x:
                #print("if " + str(z) + " isnt already in the list of morphs then add it")
                if not z in listOfAllMorphs:
                    if z != '':
                        if z[0] == " ":
                            z = z[1:]
                        listOfAllMorphs.append(z)
                # else:
                    #print("list of all morphs " + str(listOfAllMorphs))
                    #print(str(z) + " was already in the list of morphs")
                #if the current morph has not already had a col created for it
                # if not "YN" + z in snakeDataFrame:
                #     # if the morph is noe empty
                #     if z:
                #         snakeDataFrame["YN" + str(z)] = snakeDataFrame["morphs"].apply(lambda y: containsMorph(z,y) )
        #print(listOfAllMorphs)
        for morph in listOfAllMorphs:
            snakeDataFrame["YN" + morph] = snakeDataFrame["morphs"].apply(lambda y: containsMorph(morph,y))
        
        snakeDataFrame.to_csv("/home/nick/Documents/morphMarketHognoseMaximizer/newSnakeDataFrame" + sex)   
        print("finished creating new DataFrame with new columns for " + sex)
    else:
        print("found datafiles for snakeDataFrame")
        snakeDataFrame = pd.read_csv("/home/nick/Documents/morphMarketHognoseMaximizer/newSnakeDataFrame" + sex)
    #print(snakeDataFrame.loc[snakeDataFrame["YNArctic"] == "True"].head(n=10))
    return snakeDataFrame


def fixGeneString(geneString):
    print(geneString)
    geneString = geneString.replace(" 66%","").replace("100% ","").replace("66%","").replace("100%","").replace("50%","")
    #print("geneString after replaces" + geneString)
    if not geneString:
        #print("geneString Empty")
        return []
    geneList = []
    if geneString[0] ==" ":
        geneString = geneString[1:]
        
        
    
        
        
    geneHolder = ""
    noAddition = 0
    for x in range(len(geneString)):
        #print(x)
        #print(len(geneString))
        if geneHolder != "":
            if geneHolder[0] == " ":
                geneHolder = geneHolder[1:]
        #print(geneString[x])
        if geneString[x] == " ":
            if x == len(geneString)-1:
                geneList.append(geneHolder)
                break
            if geneString[x+1:x+x+4] == "Reve":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1] == "J":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1] == "M":
                if geneString[x+2] == "o":
                    geneList.append(geneHolder)
                    geneHolder = ""
                    noAddition = 1
            if geneString[x+1: x+3] == "Het":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1:x+2] =="RB":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1:x+2] == "Ti":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1:x+2] =="Su":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1] == "N":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1:x+2] == "Al":
                if geneString[x-1] != "d":
                    if geneString[x-2] != "e":
                        geneList.append(geneHolder)
                        geneHolder = ""
                        noAddition = 1
            if geneString[x+1:x+2] == "Pi":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1:x+4] == "Lave":
                if geneString[x-1] != "t":
                    if geneString[x-2] != "e":
                        if geneString[x-3] != "H":
                            geneList.append(geneHolder)
                            geneHolder = ""
                            noAddition = 1
                if geneString[x+2] == "e":
                    if geneString[x-1] != "r":
                        if geneString[x-2] != "e":
                            geneList.append(geneHolder)
                            geneHolder = ""
                            noAddition = 1
            if geneString[x+1:x+3] == "Pur":
                    geneList.append(geneHolder)
                    geneHolder = ""
                    noAddition = 1
            if geneString[x+2:x+3] == "em":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x-1] == "a":
                if geneString[x-2] == "d":
                    if geneString[x-3] == "n":
                        if geneString[x-4] =="o":
                            geneList.append(geneHolder)
                            geneHolder = ""
                            noAddition = 1
            if geneString[x+1:x+3] == "Ext":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1:x+3] == "Sab":
                if geneString[x-1] != "t":
                    if geneString[x-2] != "e":
                        if geneString[x-3] != "H":
                            geneList.append(geneHolder)
                            geneHolder = ""
                            noAddition = 1
            if geneString[x-1] == "c":
                if geneString[x-2] == "i":
                    if geneString[x-3] == "t":
                        if geneString[x-4] == "c":
                            geneList.append(geneHolder)
                            geneHolder = ""
                            noAddition = 1
            if geneString[x+1:x+2] == "Ar":
                if geneString[x-1] != "r":
                    if geneString[x-2] != "e":
                        if geneString[x-3] != "p":
                            geneList.append(geneHolder)
                            geneHolder = ""
                            noAddition = 1
                if geneString[x+2] == "n":
                    if geneString[x-1] != "r":
                        if geneString[x-2] != "e":
                            if geneString[x-3] != "p":
                                geneList.append(geneHolder)
                                geneHolder = ""
                                noAddition = 1
                if geneString[x-1] != "d":
                    if geneString[x-2] != "e":
                        geneList.append(geneHolder)
                        geneHolder = ""
                        noAddition = 1
            if noAddition == 0:
                geneHolder = geneHolder + geneString[x]        
        else:
            geneHolder = geneHolder + geneString[x]
        noAddition = 0
        if x == len(geneString) -1:
            geneList.append(geneHolder)
            break

    return geneList

def getAllSnakesWithTheseTraits(childTraitList, maleDf, femaleDf):
    maleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportm', names = ["morphs","cost","link"])
    femaleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportf', names = ["morphs","cost","link"])
    #create new columns like ynAnaconda and ynArctic
    #print(newMaleSnakeDataFrame["YNArctic"])
    # newMaleSnakeDataFrame = createNewColumns(maleSnakeDataFrame,"m")
    # newFemaleSnakeDataFrame = createNewColumns(femaleSnakeDataFrame,"f")
    #creating blank dataframe to put stuff into
    #print("in get all snakes with these traits" + str(type(childTraitList)))
    foundMaleSnakesDataFrame = pd.DataFrame(columns = maleDf.columns)
    if '' in childTraitList:
        childTraitList.remove('')
    #for all of the children
    #print(len(childTraitList))
    #print("len(childTraitList)^^")
    for x in range(len(childTraitList)):
        #print("x " + str(x))
        #print("trait not empty")
        if x == 0:
            if childTraitList[x] != 'Het':
                #print(type(childTraitList))
                trait = childTraitList[x]
                #print("YN" + trait)
                ynTrait = "YN" + trait
                if ynTrait != "YN":
                    #print(trait)
                    try:
                        concatThis = [foundMaleSnakesDataFrame,maleDf[maleDf[ynTrait] == True]]
                        foundMaleSnakesDataFrame = pd.concat(concatThis)
                    except KeyError:
                        print("Male directory contained no snakes with the morph " + str(trait) + ". Moving on...")
                        break
                    # if not foundMaleSnakesDataFrame.empty:
                    #     #print(foundMaleSnakeDataFrame.columns)
                    #     print("found the trait " + trait + " in some of the male snake instances")
                    if foundMaleSnakesDataFrame.empty:
                        print("didnt find the trait: " + str(trait) + " in the male snake instances")
                        break
            #if second or later
            if x > 0:
                if childTraitList[x] !='Het':
                    trait = childTraitList[x]
                    ynTrait = "YN" + trait
                    if ynTrait != "YN":
                        foundMaleSnakesDataFrame.drop(foundMaleSnakesDataFrame.loc[foundMaleSnakesDataFrame[ynTrait]==False].index, inplace=True)
                        # if not foundMaleSnakesDataFrame.empty:
                        #     print("still have snakes that match this morph combo " + str(childTraitList))
                        # else:
                        if foundMaleSnakesDataFrame.empty:
                            print("checking the trait " +trait+ " removed all the snakes from the subset. no snakes of that type found")
                            break
    # if not foundMaleSnakesDataFrame.empty:
    #     print("found matches against males for the snake with these traits: " + str(childTraitList ))
    # else:
    #     print("no mactches found in the male list")

    foundFemaleSnakesDataFrame = pd.DataFrame(columns = femaleDf.columns)
    for y in range(len(childTraitList)):
        #print("y " + str(y))
        if y == 0 :
            if childTraitList[y] != 'Het':
                trait = childTraitList[y]
                ynTrait = "YN" + trait
                if ynTrait != "YN":
                    #print("YN" + trait)
                    try:
                        concatThis2 = [foundFemaleSnakesDataFrame,femaleDf[femaleDf["YN"+str(trait)] == True]]
                        #print(concatThis2)
                        foundFemaleSnakesDataFrame = pd.concat(concatThis2)
                        #foundFemaleSnakesDataFrame.concat(newFemaleSnakeDataFrame.where(newFemaleSnakeDataFrame["YN"+ str(trait)] == True))
                    except KeyError:
                        print("Female directory contained no snakes with the morph" + str(trait) + ". Moving on...")
                        break
                    # if not foundFemaleSnakesDataFrame.empty:
                    #     print("found the trait " + trait + " in some of the female snake instances")
        #if second or later
        if y >0:
            if childTraitList[y] != 'Het':
                trait = childTraitList[y]
                ynTrait = "YN" + trait
                if ynTrait != "YN":
                    foundFemaleSnakesDataFrame.drop(foundFemaleSnakesDataFrame.loc[foundFemaleSnakesDataFrame[ynTrait]==False].index, inplace=True)
                    # if not foundFemaleSnakesDataFrame.empty:
                    #     print("still have snakes that match this morph combo " + str(childTraitList))
    # if not foundFemaleSnakesDataFrame.empty:
    #     print("found matches against females for the snake with these traits: " + str(childTraitList ))
    # if foundFemaleSnakesDataFrame.empty: 
    #     print("found no matches in the female list")

    if not foundMaleSnakesDataFrame.empty:
        if not foundFemaleSnakesDataFrame.empty:
                foundSnakesDataFrame = foundMaleSnakesDataFrame.append(foundFemaleSnakesDataFrame, ignore_index = True)
                count = 0
                for value in foundSnakesDataFrame["morphs"]:
                    if (isinstance(value,float)):
                        if math.isnan(value):
                            foundSnakesDataFrame.drop([count], inplace = True)
                    else:
                        count += 1
                foundSnakesDataFrame.reset_index(inplace = True, drop = True)
                count = 0
                for x in foundSnakesDataFrame["morphs"]:
                    x = ast.literal_eval(x)
                    if len(x) > len(childTraitList):
                        foundSnakesDataFrame.drop([count], inplace = True)
                        foundSnakesDataFrame.reset_index(inplace = True, drop = True)
                    else:
                        count += 1
                    
                #foundSnakesDataFrame = foundSnakesDataFrame[]
                return(foundSnakesDataFrame)
        else:
            return foundMaleSnakesDataFrame
    if not foundFemaleSnakesDataFrame.empty:
        return foundFemaleSnakesDataFrame
    else:
        return 0

def fixLikelienessElementList(likelienessElementList):
    #return list of likelinesses
    likelienessList = []
    for x in range(len(likelienessElementList)):
        if likelienessElementList[x].text != '':
            if x != 0:
                #print(likelienessElementList[x].text)
                #time.sleep(.5)
                try:
                    likelienessList.append(float(likelienessElementList[x].text.replace("%","")))
                except StaleElementReferenceException:
                    time.sleep(3)
                    try:
                        likelienessList.append(float(likelienessElementList[x].text.replace("%","")))
                    except StaleElementReferenceException:
                        print("couldnt find the likelieness elements")
                        sys.exit()
                
    return likelienessList

def averageSnakePrices(snakePrices):
    if len(snakePrices) > 0:
        adder = 0
        length = 0
        for x in snakePrices:
            x = x.replace(",","")
            adder  += float(x)
            length += 1
        avg = adder/length
        return avg
    else:
        return 0

def fixLookingAt(this):
    this = this.replace("100% ","").replace("50% ","").replace("66% ","").replace("Pos ","")
    this = ast.literal_eval(this)
    #print(this)
    #print(type(this))
    return this

def containsMorph(morph,lookingAt):
    #print(morph)
    #print("morph ^^^")
    #print("starting to look at new instance ")
    lookingAt = fixLookingAt(lookingAt)
    for z in range(len(lookingAt)):
        #print("is " + str(morph) + " equal to " + str(lookingAt[z]))
        if str(morph) == str(lookingAt[z]):
            #print("Yes, " + str(morph) + " is equal to " + str(lookingAt[z]))
            return True
    #print("none of the morphs in this instances morph combination containted: " + morph)
    return False

def exportGenes(geneList):
    if path.exists('/home/nick/Documents/geneExportForTesting'):
        f = open('/home/nick/Documents/geneExportForTesting', 'a')
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(geneList)
        # close the file
        f.close()
        return True
    else:
        # open the file in the write mode
        f = open('/home/nick/Documents/geneExportForTesting', 'w')
        # create the csv writer
        writer = csv.writer(f)
        # write a row to the csv file
        writer.writerow(geneList)
        # close the file
        f.close()
        return True

def getListOfAllMorphs(maleSnakeDataFrame,femaleSnakeDataFrame):
    listOfAllMorphs = []
    for x in maleSnakeDataFrame["morphs"]:
        x = x.replace(" 66%","").replace("100% ","").replace("66%","").replace("100%","").replace("50%","").replace("100% ","").replace(" Pos","").replace("Pos","").replace("Normal","")
        x = ast.literal_eval(x)
        #print(x)
        
        #print(type(morphList))
        #for all the morphs in the combo list x
        for z in x:
            #print("if " + str(z) + " isnt already in the list of morphs then add it")
            if not z in listOfAllMorphs:
                if z != '':
                    if z[0] == " ":
                        z = z[1:]
                    listOfAllMorphs.append(z)
    for x in femaleSnakeDataFrame["morphs"]:
        x = x.replace(" 66%","").replace("100% ","").replace("66%","").replace("100%","").replace("50%","").replace("100% ","").replace(" Pos","").replace("Pos","").replace("Normal","")
        x = ast.literal_eval(x)
        #print(x)
        
        #print(type(morphList))
        #for all the morphs in the combo list x
        for z in x:
            #print("if " + str(z) + " isnt already in the list of morphs then add it")
            if not z in listOfAllMorphs:
                if z != '':
                    if z[0] == " ":
                        z = z[1:]
                    listOfAllMorphs.append(z)
    return listOfAllMorphs

def turnIntoList(x,listOfAllGenes):
    geneList = []
    geneHolder = ""
    #print(x)
    for y in x:
        if not geneHolder in listOfAllGenes:
            #print("not in list of all genes")
            geneHolder  = geneHolder + y
        else:
            #print("was in list of all genes")
            geneList.append(geneHolder)
            geneHolder = ""
    if geneHolder in listOfAllGenes:
        geneList.append(geneHolder)
    time.sleep(1)
    return geneList
            

def fixGenesElementList(genesElementList):
    #print("genesElementList[0].text" + str(genesElementList[1].text))
    fixedGenesList = []
    partiallyFixedGenesList = []
    for x in range(len(genesElementList)):
        if x != 0:    
            #print(genesElementList[x].text)
            partiallyFixedGenesList.append(genesElementList[x].text.replace(" 100%","").replace(" 50%","").replace(" Pos","").replace("50% " , "").replace("100% ",""))
    #print(type(partiallyFixedGenesList))
    return partiallyFixedGenesList

def runMeFirst(maleSnakeDataFrame, femaleSnakeDataFrame):
    male = createNewColumns(maleSnakeDataFrame,"m")
    female = createNewColumns(femaleSnakeDataFrame,"f")
    return [male, female]