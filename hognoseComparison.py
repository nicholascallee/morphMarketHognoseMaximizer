import pandas as pd
from pandas import DataFrame as df
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
from selenium.common.exceptions import StaleElementReferenceException



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



def getAllSnakesWithTheseTraits(traitList):
    #need to open csv and grab snakes
    #then compare with traitlist and return the snakes with those traits both male and female
    maleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportm', names = ["morphs","cost","link"])
    femaleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportf', names = ["morphs","cost","link"])
    #print(maleSnakeDataFrame["morphs"])
    print("looking for snakes in male file of this morph " + str(traitList))
    foundSnakes = []
    for morph in maleSnakeDataFrame["morphs"]:
        count = 0
        if morph == traitList:
            print("found a snake with this morph " +traitList + " adding to the pile")
            print(maleSnakeDataFrame[count])
            foundSnakes.append(maleSnakeDataFrame[count])
        count += 1
    print("looking for snakes in female file of the same morph")
    for morph in femaleSnakeDataFrame["morphs"]:
        count = 0
        if morph == traitList:
            print("found a snake with this morph " +traitList + " adding to the pile")
            print(femaleSnakeDataFrame[count])
            foundSnakes.append(femaleSnakeDataFrame[count])
        count += 1
    if len(foundSnakes) == 0:
        print("no snakes of that morph type found")
        return []
    else:
        print("printing cost for all found snakes")
        print(foundSnakes[0][["cost"]])
        print(type(foundSnakes[0]["cost"]))
    
    

def findSnakeWithTheseTraitsInTheDataFrame(driver, traits, snakeMFrame, snakeFFrame):
    #print(traits)
    morphHolder = ""
    traitList = []
    stopper = 0
    for w in range(len(traits)):
        # print(traits[w])
        # print("converting traits to list")
        if traits[w] != " ":
            # print("adding string to morphholder")
            morphHolder += traits[w]
            if w == len(traits)-1:
                # print("end of list. Adding last trait to traitlist.")
                traitList.append(morphHolder)
        if traits[w] == " ":
            if traits[w-1] == " ":
                # print("last two chars were spaces so adding morphHolder to the traitlist")
                traitList.append(morphHolder)
                morphHolder = ""
                stopper = 1
            if " " in morphHolder and stopper != 1:
                #print("was a space in morphholder and a space again so adding morphHolder to the traitlist")
                traitList.append(morphHolder)
                morphHolder = ""
                stopper = 0
            else:
                # print("adding string to morphholder")
                morphHolder += traits[w]
    if '' in traitList:
        traitList.remove('')
    returnedSnakes = getAllSnakesWithTheseTraits(traitList)
    if returnedSnakes == []:
        return []
    else:
        return returnedSnakes
    

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
    #gotoSnakeWithTheseTraits(driver,traits)
    #pricesOfSpecificSnake = goThroughEachSnakeWithSpecificTraits(driver)
    #avg = averageSnakePrices(pricesOfSpecificSnake)
    #return avg

def fixLikelienessElementList(likelienessElementList):
    print("fixing likelieness list")
    #return list of likelinesses
    likelienessList = []
    for x in range(len(likelienessElementList)):
        if x != 0:
            #print(likelienessElementList[x].text)
            likelienessList.append(float(likelienessElementList[x].text.replace("%","")))
    print("new likelieness list: " + str(likelienessList))
    return likelienessList
    
def fixGenesElementList(genesElementList):
    #return list of lists of genes
    print("fixing genes list")
    print(str(genesElementList) + " genes element list raw")
    fixedGenesList = []
    for x in range(len(genesElementList)):
        fixedGenesList.append(list(genesElementList[x].text))
    print("new genes list: " + str(fixedGenesList))
    return fixedGenesList

def grabSnakeComboData(driver, snakeMFrame, snakeFFrame):
    print("starting grabsnakecomboData")
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
            if x != 1:
                print("wasnt at the snake combo page so going there now")
                driver.get(snakeComboUrl)
            likelienessElementList = driver.find_elements(By.CLASS_NAME, "prob")
            genesElementList = driver.find_elements(By.CLASS_NAME, "genes")
            fixedLikelienessList  = fixLikelienessElementList(likelienessElementList)
            fixedGenesList = fixGenesElementList(genesElementList)
            snakeChildren.append([fixedLikelienessList,fixedGenesList])
            time.sleep(4)
            snakeChildPrice = findAvgPriceOfSnake(driver,snakeChildren[x-1], snakeMFrame, snakeFFrame)
            #print("what is showing when this pops up?")
            time.sleep(3)
            snakeChildren[x-1].append(snakeChildPrice)
            #now we have snakes with avg prices. add themn all up weighted to get score
            #print("snake child likelieness " + str(snakeChildren[x-1][0]))
            if snakeChildren[x-1][0] == "":
                weightedTotalReturn = 0
            else:
                weightedTotalReturn += float(snakeChildren[x-1][0]) * float(snakeChildren[x-1][2])
    #print("snake children " + str(snakeChildren))
    traits = snakeChildren[0][1]
    #print(traits)
    morphHolder = ""
    traitList = []
    for w in range(len(traits)):
        # print(traits[w])
        # print("converting traits to list")
        if traits[w] != " ":
            # print("adding string to morphholder")
            morphHolder += traits[w]
            if w == len(traits)-1:
                # print("end of list. Adding last trait to traitlist.")
                traitList.append(morphHolder)
        if traits[w] == " ":
            if traits[w-1] == " ":
                print("last two chars were spaces so adding morphHolder to the traitlist")
                traitList.append(morphHolder)
                morphHolder = ""
            else:
                # print("adding string to morphholder")
                morphHolder += traits[w]
    snakeChildren[0][1] = traitList
    returner = [snakeChildren,weightedTotalReturn]
    #print(traitList)    
    return returner
    

def compareSnakes(driver, snakeMFrame, snakeFFrame, myId):
    #gets all data out of frames and calculates a comparison of snakes then gets combo data with a fn
    for z in range(len(snakeMFrame)):
        maleMorphList = snakeMFrame[z]
        maleMorphList = maleMorphList.split(",")
        for x in range(len(maleMorphList)):
            maleMorphList[x] = maleMorphList[x].replace("[","").replace("]","").replace("'","").replace("100%","")
        maleCost = snakeMFrame[z+1]
        maleLink = snakeMFrame[z+2]
        break
    for a in range(len(snakeFFrame)):
        femaleMorphList = snakeFFrame[z]
        femaleMorphList = femaleMorphList.split(",")
        for x in range(len(femaleMorphList)):
            femaleMorphList[x] = femaleMorphList[x].replace("[","").replace("]","").replace("'","").replace("100%","")
        femaleCost = snakeFFrame[z+1]
        femaleLink = snakeFFrame[z+2]
        break
    driver.get("https://www.morphmarket.com/c/reptiles/colubrids/western-hognose/genetic-calculator/")
    parentOneElement = driver.find_element(By.CSS_SELECTOR, "div.trait-input-wrapper:nth-child(1) > input:nth-child(2)")
    for x in range (len(maleMorphList)):
        parentOneElement.send_keys(maleMorphList[x])
        parentOneElement.send_keys(Keys.TAB)
    parentTwoElement = driver.find_element(By.CSS_SELECTOR, "div.trait-input-wrapper:nth-child(3) > input:nth-child(2)")
    for y in range (len(femaleMorphList)):
        parentTwoElement.send_keys(femaleMorphList[y])
        parentTwoElement.send_keys(Keys.TAB)
    calculateButtonCssSelector = ".tooltip-wrapper > button:nth-child(1)"
    calculateButtonElement = driver.find_element(By.CSS_SELECTOR,calculateButtonCssSelector)
    calculateButtonElement.click()
    time.sleep(4)
    results = grabSnakeComboData(driver, snakeMFrame, snakeFFrame)
    d = {'id': [myId], 'maleMorphs': [maleMorphList], 'femaleMorphs': [femaleMorphList], 'children': [results[0]], 'score': [results[1]], 'snakeLinks':[[maleLink, femaleLink]]}
    returningDataFrame = df(data = d)
    #print("printing children")
    #print(returningDataFrame["children"].head())
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
            resultsDataFrame = resultsDataFrame.append(resultDataFrame)
            theId += 1
    resultsDataFrame = resultsDataFrame.sort_values(by = ["score"])
    print("printingReturndataframe")
    print(resultsDataFrame.head(n=10))
main()