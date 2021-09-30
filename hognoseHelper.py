
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

def averageSnakePrices(snakePrices):
    if len(snakePrices) > 0:
        adder = 0
        length = 0
        for x in snakePrices:
            adder  += int(x)
            length += 1
        avg = adder/length
        return avg
    else:
        return 0


def morphToList(stringOfMorphs):
    if stringOfMorphs[0] == " ":
        stringOfMorphs = StringOfMorphs[1:]
    stringOfMorphs = stringOfMorphs.replace("['","").replace("']","").replace("100% ","").replace("', '"," ").replace(" Pos","").replace("Pos","").replace("Normal","").replace("'', ","")
    stringOfMorphsFixed = fixGeneString(stringOfMorphs)
    return stringOfMorphsFixed


def containsMorph(morph,lookingAt):
    for x in lookingAt:
        if x == morph:
            return True
        else:
            return False

def createNewColumns(snakeDataFrame,sex):
    if (path.exists("/home/nick/Documents/morphMarketHognoseMaximizer/newSnakeDataFrame" + sex) != True):
        for x in snakeDataFrame["morphs"]:
            morphList = morphToList(x)
            for x in morphList:
                if x:
                    snakeDataFrame["YN" + str(x)] = snakeDataFrame["morphs"].apply(lambda y: containsMorph(x,y) )
        snakeDataFrame.to_csv("/home/nick/Documents/morphMarketHognoseMaximizer/newSnakeDataFrame" + sex)   
    else:
        snakeDataFrame = pd.read_csv("/home/nick/Documents/morphMarketHognoseMaximizer/newSnakeDataFrame" + sex)
    return snakeDataFrame

def getAllSnakesWithTheseTraits(childTraitList):
    maleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportm', names = ["morphs","cost","link"])
    femaleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportf', names = ["morphs","cost","link"])
    #create new columns like ynAnaconda and ynArctic
    newMaleSnakeDataFrame = createNewColumns(maleSnakeDataFrame,"m")
    newFemaleSnakeDataFrame = createNewColumns(femaleSnakeDataFrame,"f")
    foundMaleSnakesDataFrame = pd.DataFrame(columns = newMaleSnakeDataFrame.columns)
    #for all of the children
    for x in range(len(childTraitList)):
        if x == 0:
            #print(type(childTraitList))
            trait = childTraitList[x]
            #print(trait)
            try:
                foundMaleSnakesDataFrame.append(newMaleSnakeDataFrame.where(newMaleSnakeDataFrame["YN"+str(trait)] == True))
            except KeyError:
               # print("Male directory contained no snakes with the morph " + str(trait) + ". Moving on...")
                break
        #if second or later
        if x >0:
            foundMaleSnakesDataFrame.drop(foundMaleSnakesDataFrame.loc[foundMaleSnakesDataFrame['YN' + str(trait) ]==False].index, inplace=True)
    if not foundMaleSnakesDataFrame.empty:
        print("found matches against males for the snake with these traits: " + str(childTraitList ))

    foundFemaleSnakesDataFrame = pd.DataFrame(columns = newFemaleSnakeDataFrame.columns)
    for y in range(len(childTraitList)):
        if y == 0 :
            trait = childTraitList[y]
            try:
                foundFemaleSnakesDataFrame.append(newFemaleSnakeDataFrame.where(newFemaleSnakeDataFrame["YN"+ str(trait)] == True))
            except KeyError:
                #print("Female directory contained no snakes with the morph" + str(trait) + ". Moving on...")
                break
        #if second or later
        if y >0:
            foundFemaleSnakesDataFrame.drop(foundFemaleSnakesDataFrame.loc[foundFemaleSnakesDataFrame['YN' + str(trait) ]==False].index, inplace=True)
    if not foundFemaleSnakesDataFrame.empty:
        print("found matches against females for the snake with these traits: " + str(childTraitList ))

    if not foundMaleSnakesDataFrame.empty:
        if not foundFemaleSnakesDataFrame.empty:
                foundSnakesDataFrame = foundMaleSnakesDataFrame.append(foundFemaleSnakesDataFrame)
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
        if x != 0:
            #print(likelienessElementList[x].text)
            time.sleep(.5)
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

def fixGeneString(geneString):
    geneString = geneString.replace(" 66%","").replace("100% ","").replace("66%","").replace("100%","").replace("50%","")
    #print("geneString after replaces" + geneString)
    if not geneString:
        print("geneString Empty")
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
            if geneString[x+1] == "H":
                if geneString[x+2] =="e":
                    if geneString[x+3] =="t":
                        geneList.append(geneHolder)
                        geneHolder = ""
                        noAddition = 1
            if geneString[x+1] == "T":
                if geneString[x+2] == "i":
                    geneList.append(geneHolder)
                    geneHolder = ""
                    noAddition = 1
            if geneString[x+1] =="S":
                if geneString[x+2] == "u":
                    geneList.append(geneHolder)
                    geneHolder = ""
                    noAddition = 1
            if geneString[x+1] == "N":
                geneList.append(geneHolder)
                geneHolder = ""
                noAddition = 1
            if geneString[x+1] == "L":
                if geneString[x+2] == "a":
                    if geneString[x+3] == "v":
                        if geneString[x+4] == "e":
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
            if geneString[x+1] == "P":
                if geneString[x+2] == "u":
                    if geneString[x+3] == "r":
                        geneList.append(geneHolder)
                        geneHolder = ""
                        noAddition = 1
                if geneString[x+2] == "e":
                    if geneString[x+3] == "m":
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
            if geneString[x+1] == "E":
                if geneString[x+2] == "x":
                    if geneString[x+3] == "t":
                        geneList.append(geneHolder)
                        geneHolder = ""
                        noAddition = 1
            if geneString[x+1] == "S":
                if geneString[x+2] == "a":
                    if geneString[x+3] == "b":
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
            if geneString[x+1] == "A":
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

def fixGenesElementList(genesElementList):
    fixedGenesList = []
    partiallyFixedGenesList = []
    for x in range(len(genesElementList)):
        if x != 0:    
            #print(genesElementList[x].text)
            partiallyFixedGenesList.append(genesElementList[x].text)
    for y in range(len(partiallyFixedGenesList)):
        fixedGenesList.append(partiallyFixedGenesList[y].replace(" 100%","").replace(" 50%","").replace(" Pos",""))
    for z in range(len(fixedGenesList)):
        fixedGenesList[z] = fixGeneString(fixedGenesList[z])

    exportGenes(fixedGenesList)
    return fixedGenesList