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

def grabSnakePrice(driver):
    return

def morphToList(stringOfMorphs):
    if stringOfMorphs[0] == " ":
        stringOfMorphs = StringOfMorphs[1:]
    stringOfMorphs = stringOfMorphs.replace("['","").replace("']","").replace("100% ","").replace("', '"," ").replace(" Pos","").replace("Pos","").replace("Normal","").replace("'', ","")
    stringOfMorphsFixed = fixGeneString(stringOfMorphs)
    return stringOfMorphsFixed

def isItAfterAlphebetically(charOne,charTwo):
    if charOne <= charTwo:
        return True
    else:
        return False

def tfOfIfContainsThisMorph(sliceOfMorphs,morph):
    for x in sliceOfMorphs:
        if (morph in x):
            return True:
        else:
            return False:

def createNewColumns(snakeDataFrame):
    for x in snakeDataFrame["morphs"]:
        morphList = morphToList(x)
        for x in morphList:
            if x:
                snakeDataFrame["YN" + str(x)] = snakeDataFrame["morphs"].apply(tfOfIfContainsThisMorph(x))
                
    print(snakeDataFrame.columns)
    #grab list of all possible morphs
    #for each morph
        #create new column called yn<morphHere> and make them yes no based on if the morphs col contains that morph
    return snakeDataFrame

def getAllSnakesWithTheseTraits(childTraitList):
    #need to open csv and grab snakes
    #then compare with traitlist and return the snakes with those traits both male and female
    maleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportm', names = ["morphs","cost","link"])
    femaleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportf', names = ["morphs","cost","link"])
    #create new columns like ynAnaconda and ynArctic
    newMaleSnakeDataFrame = createNewColumns(maleSnakeDataFrame)
    newFemaleSnakeDataFrame = createNewColumns(femaleSnakeDataFrame)
    print("looking for snakes in male file of this morph " + str(childTraitList))
    foundSnakes = []
    fixedMorphs = []
    #print("morph--+ " + maleSnakeDataFrame["morphs"])
    maleSnakeMorphs = maleSnakeDataFrame["morphs"].tolist()
    femaleSnakeMorphs = femaleSnakeDataFrame["morphs"].tolist()
    #go thru all male snakes
    timeNow = time.time()
    print("starting to check the boys")
    for x in range(len(maleSnakeMorphs)):
        timeNow = time.time()
        
        #print(str(maleSnakeMorphs[x]+ "-----unfixed-------"))
        timeNow = time.time()
        #print(time.time())
        maleMorphList = morphToList(maleSnakeMorphs[x])
        maleMorphList.sort()
        #print("maleMorphList to list took: " + str(time.time() - timeNow) + " seconds.")
        #print("fixed --------- " + str(maleMorphList))
        
        
        
        count = 0
        #print("comparing ---- "+ str(maleMorphList) + " and ------ " + str(childTraitList))
        time.sleep(2)
        #print("childTrait list: " + str(childTraitList))
        
        #have to have all genes match. need to get to len of traitlist
        getToHere = len(childTraitList)
        count = 0
        #go thru all traits in the child
        for trait in childTraitList:
            #not getting right morph.getting entire list
            #print("checking trait: " + trait)
            afterTF = False
            for morph in maleMorphList:
                #print("morph " + str(morph))
                if morph == "":
                    #print("morph was empty. breaking now")
                    break
                #print("is this trait: " + str(trait) + " in this morph: " + str(morph))
                if trait == morph:
                    #print("found a matching trait: " + trait )
                    count +=1
                    break
                try:
                    afterTF = isItAfterAlphebetically(trait[0],morph[0])
                except IndexError:
                    print("cant tell if " + str(trait + " is after " + str(morph) ))
                if (afterTF):
                    afterTF = False
                    #print("breaking here")
                    break
        if count == getToHere:
            print("found a match ------------------------------------ this morph: " + str(fixedMorphs) + " and this morph are the same: "+ str(traitList))
            sys.exit()
            print(maleSnakeDataFrame[count])
            foundSnakes.append(maleSnakeDataFrame[count])
        #if count > 0 and count < len(childTraitList):
            #print("not all traits matched")
        print("going thru 1 kid vs 1 adult snake took: " + str(time.time() - timeNow) + " to finish")
    print("looking for snakes in female file of the same morph")
    #go thru female snakes the same way
    print("starting to check the girls ----------------------")
    for y in range(len(femaleSnakeDataFrame["morphs"])):
        
        femaleMorphList = morphToList(femaleSnakeMorphs[y])
        
        count = 0
        #print("comparing ---- "+ str(maleMorphList) + " and ------ " + str(childTraitList))
        time.sleep(2)
        #print("childTrait list: " + str(childTraitList))
        
        #have to have all genes match. need to get to len of traitlist
        getToHere = len(childTraitList)
        count = 0
        #go thru all traits in the child
        for trait in childTraitList:
            #not getting right morph.getting entire list
            #print("checking trait: " + trait)
            for morph in maleMorphList:
                #print("is this trait: " + str(trait) + " in this morph: " + str(morph))
                if trait == morph:
                    #print("found a matching trait: " + trait )
                    count +=1
        if count == getToHere:
            print("found a match ------------------------------------ this morph: " + str(fixedMorphs) + " and this morph are the same: "+ str(traitList))
            print(femaleSnakeDataFrame[count])
            foundSnakes.append(femaleSnakeDataFrame[count])
    if len(foundSnakes) == 0:
        print("no snakes of that morph type found")
        return []
    else:
        print("printing cost for all found snakes")
        print(foundSnakes[0][["cost"]])
        print(type(foundSnakes[0]["cost"]))
    
    

def findSnakeWithTheseTraitsInTheDataFrame(driver, traits, snakeMFrame, snakeFFrame):
    traits = traits[0]
    #print("traits " + str(traits))
    snakesWithTheseTraits = getAllSnakesWithTheseTraits(traits)
    return snakesWithTheseTraits
    

def findAvgPriceOfSnake(driver,snake, snakeMFrame, snakeFFrame):
    #instead of trying to load a fuck ton of pages, just look in the list of snakes we already made dumbass
    traits = snake[1]
    snakesWithTheseParticularTraits = findSnakeWithTheseTraitsInTheDataFrame(driver, snake[1], snakeMFrame, snakeFFrame)
    if snakesWithTheseParticularTraits == []:
        return 0
    else:
        pricesOfSpecificSnake = snakesWithTheseParticularTraits["cost"]
        print("this is the cost of the snakes found in a list: " + str(pricesOfSpecificSnake))
        avg = averageSnakePrices(pricesOfSpecificSnake)
        return avg
    #gotoSnakeWithTheseTraits(driver,traits)
    #pricesOfSpecificSnake = goThroughEachSnakeWithSpecificTraits(driver)
    #avg = averageSnakePrices(pricesOfSpecificSnake)
    #return avg

def fixLikelienessElementList(likelienessElementList):
    #print("fixing likelieness list")
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
                
    #print("new likelieness list: " + str(likelienessList))
    return likelienessList

def fixGeneString(geneString):
    geneString = geneString.replace(" 66%","").replace("100% ","").replace("66%","").replace("100%","").replace("50%","")
    print("geneString after replaces" + geneString)
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
    #print("geneList from fixGeneStringFN " + str(geneList))
    
    return geneList
    #if next 4 letters are spacehet then start new gene
    #if next 9 letters are spacelavender then start new gene


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
    #string manipulation needed here
    #return list of lists of genes
    #print("fixing genes list")
    #print(str(genesElementList) + " genes element list raw")
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
        
    #print("new genes list: " + str(fixedGenesList))
    exportGenes(fixedGenesList)
    return fixedGenesList

def grabSnakeComboData(driver, snakeMFrame, snakeFFrame):
    #print("starting grabsnakecomboData")
    returner = []
    snakeChildren = []
    #snakeChildren = [likelieness morph avg price]
    likelienessElementList = driver.find_elements(By.CLASS_NAME, "prob")
    genesElementList = driver.find_elements(By.CLASS_NAME, "genes")
    snakeComboUrl = driver.current_url
    weightedTotalReturn = 0
    #print("length of likelienesselementlist: " + str(len(likelienessElementList)))
    for x in range(1,len(likelienessElementList)):
        if x < len(likelienessElementList):
            #starts at the list of children made from parents
            likelienessElementList = driver.find_elements(By.CLASS_NAME, "prob")
            genesElementList = driver.find_elements(By.CLASS_NAME, "genes")
            fixedLikelienessList  = fixLikelienessElementList(likelienessElementList)
            fixedGenesList = fixGenesElementList(genesElementList)
            snakeChildren.append([fixedLikelienessList,fixedGenesList])
            #time.sleep(4)
            print("the parents would make these children: " + str(fixedGenesList) + " with these likelienesses: " + str(fixedLikelienessList))
            snakeChildPrice = findAvgPriceOfSnake(driver,snakeChildren[x-1], snakeMFrame, snakeFFrame)
            #print("what is showing when this pops up?")
            #time.sleep(3)
            snakeChildren[x-1].append(snakeChildPrice)
            #now we have snakes with avg prices. add themn all up weighted to get score
            #print("snake child likelieness " + str(snakeChildren[x-1][0]))
            if snakeChildren[x-1][0] == "":
                weightedTotalReturn = 0
            else:
                #print("adding together: "+ str(snakeChildren[x-1][0]) + "and " + str(snakeChildren[x-1][2]))
                if snakeChildren[x-1][2] != 0:    
                    weightedTotalReturn += float(snakeChildren[x-1][0]) * float(snakeChildren[x-1][2])
                else:
                    print("no snakes found for this morph combo so no prices. not adding to weightedTotalReturn")
    #print("snake children " + str(snakeChildren))
    traits = snakeChildren[0][1]
    traits = traits[0]
    snakeChildren[0][1] = traits
    returner = [snakeChildren,weightedTotalReturn]
    #print(traitList)    
    return returner
    

def compareSnakes(driver, snakeMFrame, snakeFFrame, myId):
    #gets all data out of frames and calculates a comparison of snakes then gets combo data with a fn
    for z in range(len(snakeMFrame)):
        maleMorphList = snakeMFrame[z]
        maleMorphList = maleMorphList.split(",")
        for x in range(len(maleMorphList)):
            maleMorphList[x] = maleMorphList[x].replace("[","").replace("]","").replace("'","").replace("100%","").replace("Pos ","")
        maleCost = snakeMFrame[z+1]
        maleLink = snakeMFrame[z+2]
        break
    for a in range(len(snakeFFrame)):
        femaleMorphList = snakeFFrame[z]
        femaleMorphList = femaleMorphList.split(",")
        for x in range(len(femaleMorphList)):
            femaleMorphList[x] = femaleMorphList[x].replace("[","").replace("]","").replace("'","").replace("100%","").replace("Pos ","")
        femaleCost = snakeFFrame[z+1]
        femaleLink = snakeFFrame[z+2]
        break
    driver.get("https://www.morphmarket.com/c/reptiles/colubrids/western-hognose/genetic-calculator/")
    parentOneElement = driver.find_element(By.CSS_SELECTOR, "div.trait-input-wrapper:nth-child(1) > input:nth-child(2)")
    
    for x in range (len(maleMorphList)):
        maleMorphList[x] = maleMorphList[x].replace("66% ","").replace("100% ","")
        if maleMorphList[x][0] == " ":
            maleMorphList[x] = maleMorphList[x][1:]
        print("parent 1 "  + "morph number :"+ str(x) + " " + str(maleMorphList[x]))
        parentOneElement.send_keys(maleMorphList[x])
        parentOneElement.send_keys(Keys.TAB)
    parentTwoElement = driver.find_element(By.CSS_SELECTOR, "div.trait-input-wrapper:nth-child(3) > input:nth-child(2)")
    for y in range (len(femaleMorphList)):
        femaleMorphList[y]  = femaleMorphList[y].replace("66% ","").replace("100% ","")
        if femaleMorphList[y][0] == " ":
            femaleMorphList[y] = femaleMorphList[y][1:]
        print("parent 2 " + "morph number :"+ str(y) + " " + str(femaleMorphList[y]))
        parentTwoElement.send_keys(femaleMorphList[y])
        parentTwoElement.send_keys(Keys.TAB)
    calculateButtonCssSelector = ".tooltip-wrapper > button:nth-child(1)"
    calculateButtonElement = driver.find_element(By.CSS_SELECTOR,calculateButtonCssSelector)
    calculateButtonElement.click()
    time.sleep(2)
    results = grabSnakeComboData(driver, snakeMFrame, snakeFFrame)
    d = {'id': [myId], 'maleMorphs': [maleMorphList], 'femaleMorphs': [femaleMorphList], 'children': [results[0]], 'score': [results[1]], 'snakeLinks':[[maleLink, femaleLink]]}
    returningDataFrame = df(data = d)
    #print("printing children")
    #print(returningDataFrame["children"].head())
    #print("returning returningDataFrame from compare snakes")
    return returningDataFrame


def main():
    maleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportm')
    femaleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportf')
    driver = webdriver.Firefox()
    resultsDataFrame = df(columns=("id","maleMorphs","femaleMorphs","children","score","snakeLinks"))
    theId = 1
    # print(maleSnakeDataFrame.head(n=10))
    # print(femaleSnakeDataFrame.head(n=10))
    for x in range(len(maleSnakeDataFrame)):
        for y in range(len(femaleSnakeDataFrame)):
            # print("x =  "+str(x))
            # print("y =  "+str(y))
            resultDataFrame = compareSnakes(driver, maleSnakeDataFrame.iloc[x],femaleSnakeDataFrame.iloc[y],theId)
            #print("appending the result of compare snakes to the results dataframe. here is the result: " + str(resultDataFrame.head()) )
            resultsDataFrame = resultsDataFrame.append(resultDataFrame)
            theId += 1
    resultsDataFrame = resultsDataFrame.sort_values(by = ["score"])
    print("printingReturndataframe")
    print(resultsDataFrame.head(n=10))
main()