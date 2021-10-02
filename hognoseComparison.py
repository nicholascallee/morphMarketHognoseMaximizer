import pandas as pd
from pandas import DataFrame as df
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import time
import numpy as np
import selenium.common.exceptions as sce
from selenium.common.exceptions import StaleElementReferenceException
import os.path
from os import path
import sys
import ast
import multiprocessing
from hognoseHelper import fixLikelienessElementList
from hognoseHelper import fixGenesElementList
from hognoseHelper import fixGeneString
from hognoseHelper import averageSnakePrices
from hognoseHelper import createNewColumns
from hognoseHelper import exportGenes
from hognoseHelper import getAllSnakesWithTheseTraits
from hognoseHelper import runMeFirst
from hognoseHelper import getListOfAllMorphs
from hognoseHelper import checkIfElementExistsByCssSelector
from hognoseHelper import turnIntoList
from hognoseHelper import exportResults
from hognoseHelper import logMe
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

def spawn(num, return_dict, maleSnakeDataFrame, femaleSnakeDataFrame, maleDataFrame, femaleDataFrame):
    print("starting process: " + str(num))

    driver = webdriver.Firefox()
    resultsDataFrame = df(columns=("id","maleMorphs","femaleMorphs","children","score","snakeLinks"))
    theId = 1
    # print(maleSnakeDataFrame.head(n=10))
    # print(femaleSnakeDataFrame.head(n=10))
    listOfAllMorphs = getListOfAllMorphs(maleSnakeDataFrame,femaleSnakeDataFrame)
    finalNumber = float(len(maleSnakeDataFrame) * float(len(femaleSnakeDataFrame)))
    count = 0
    dontGo = 0
    for x in range(len(maleSnakeDataFrame)):
        for y in range(len(femaleSnakeDataFrame)):
            #dataframe of males that are the same as male in question
            #     #get all the instances with that male
            if dontGo == 0:
                #print(maleSnakeDataFrame.iloc[x])
                resultDataFrame = compareSnakes(driver, maleSnakeDataFrame.iloc[x],femaleSnakeDataFrame.iloc[y],theId,maleDataFrame,femaleDataFrame,listOfAllMorphs,num)
                # if not resultDataFrame.empty:
                exportResults((resultDataFrame),num)
                resultsDataFrame = resultsDataFrame.append(resultDataFrame)
                resultsDataFrame.reset_index(inplace = True, drop = True)
                #print(resultsDataFrame.head(n=10))
                theId += 1
                logMe("snake combination number " + str(count) + " out of " + str(finalNumber) + " completed.",num)
                count += 1
            dontGo = 0
        resultsDataFrame = resultsDataFrame.sort_values(by = ["score"])
        logMe("printingReturndataframe",num)    
        logMe(resultsDataFrame.head(n=10),num)
        return_dict[num] = resultsDataFrame
     


def findAvgPriceOfSnake(driver,snake, maleDf, femaleDf, num):
    #instead of trying to load a fuck ton of pages, just look in the list of snakes we already made dumbass
    #print("in find avg price of snake" + str(type(snake)))
    snakesWithTheseParticularTraits = getAllSnakesWithTheseTraits(snake, maleDf, femaleDf,num)
    if isinstance(snakesWithTheseParticularTraits,int):
        if snakesWithTheseParticularTraits == 0:
            return 0
    else:
        pricesOfSpecificSnake = snakesWithTheseParticularTraits["cost"]
        #print("this is the cost of the snakes found in a list: " + str(pricesOfSpecificSnake))
        avg = averageSnakePrices(pricesOfSpecificSnake)
        return avg



def grabSnakeComboData(driver, maleDf,femaleDf,calculateButtonElement, listOfAllMorphs,num):
    returner = []
    #snakeChildren = [likelieness morph avg price]
    snakeChildren = []
    #grab likelieness and traits/genes
    #print("check where webpage is at")
    
    likelienessElementList = driver.find_elements(By.CLASS_NAME, "prob")
    genesElementList = driver.find_elements(By.CLASS_NAME, "genes")
    try:
        likelienessElementList[0].text
    except:
        logMe("couldnt get likelieness list. trying again",num)
        for x in range(5):
            delay = 60 # seconds
            try:
                #if (checkIfElementExistsByCssSelector("body > h3:nth-child(1)")):
                time.sleep(2)
                driver.refresh()
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'prob')))
                logMe("Page is ready!",num)
            except TimeoutException:
                logMe("Loading took too much time!",num)
            likelienessElementList = driver.find_elements(By.CLASS_NAME, "prob")
            genesElementList = driver.find_elements(By.CLASS_NAME, "genes")
        try: 
            logMe("likelienessElementList[0]" + str(likelinessElementList[0].text),num)
        except:
            logMe("couldnt get likelieness list at all",num)
            sys.exit()
    #print(likelienessElementList)
    #fix elements to fit whats needed next
    fixedLikelienessList  = fixLikelienessElementList(likelienessElementList)
    #print(fixedLikelienessList)
    #print(len(fixedLikelienessList))
    fixedGenesList = fixGenesElementList(genesElementList)
    #print("fixedGenesList " + str(fixedGenesList))
    
    
    
    
    perfectGenesList = []
    for x in fixedGenesList:
        perfectGenesList.append(turnIntoList(x, listOfAllMorphs))
    #print(perfectGenesList)
    weightedTotalReturn = 0
    #print("looking through " + str(len(fixedLikelienessList))+ " snakes")
    logMe("the combo makes " + str(len(fixedLikelienessList)) + " children-------------------------------------------------------------------",num)
    logMe("",num)
    logMe("",num)
    if len(fixedLikelienessList) == 1:
        likelieness = fixedLikelienessList[0]
        genes = perfectGenesList[0]
        #print(type(maleDf))
        price = findAvgPriceOfSnake(driver, genes, maleDf, femaleDf,num)
        #if we found one
        if price != 0:
            logMe("found snakes with these genes: " + str(genes) + ". avg price: " + str(price),num)
            weightedTotalReturn += float(likelieness) * float(price)
        else:
            logMe("looked through snake with these genes: " + str(genes) + " and found no results",num)
    if len(fixedLikelienessList) != 1:
        #for x in range len of child list
        #print(len(fixedLikelienessList))
        #print("len ^^^")
        for x in range(len(fixedLikelienessList)):
            #print("going thru snakes with these genes: " + str(fixedGenesList[x]))
            if x != len(fixedLikelienessList):
                #print("got to here")
                #print(x)
                likelieness = fixedLikelienessList[x]
                genes = perfectGenesList[x]
                #print("checking for snake with these genes: " + str(genes))
                #print("calling findAvgPriceOfSnake")
                #print("type in grab snake combo data " + str(type(genes)))
                price = findAvgPriceOfSnake(driver, genes, maleDf, femaleDf,num)
                #if we found 
                if price != 0:
                    logMe("found snakes with these genes: "+str(genes) +". avg price: " + str(price),num)
                    weightedTotalReturn += float(likelieness) * float(price)
                else:
                    logMe("looked through snake with these genes: " +str(genes) + " and found no results",num)

    returner = [perfectGenesList,weightedTotalReturn] 
    return returner
    

def compareSnakes(driver,snakeMFrame, snakeFFrame, myId, maleDf, femaleDf, listOfAllMorphs,num):
    #gets all data out of frames and calculates a comparison of snakes then gets combo data with a fn
    for z in range(len(snakeMFrame)):
        maleMorphList = snakeMFrame[z+1]
        maleMorphList = maleMorphList.split(",")
        for x in range(len(maleMorphList)):
            maleMorphList[x] = maleMorphList[x].replace("[","").replace("]","").replace("'","").replace("100%","").replace("Pos ","")
        maleCost = snakeMFrame[z+2]
        maleLink = snakeMFrame[z+3]
        break
    for a in range(len(snakeFFrame)):
        femaleMorphList = snakeFFrame[a+1]
        femaleMorphList = femaleMorphList.split(",")
        for x in range(len(femaleMorphList)):
            femaleMorphList[x] = femaleMorphList[x].replace("[","").replace("]","").replace("'","").replace("100%","").replace("Pos ","")
        femaleCost = snakeFFrame[a+2]
        femaleLink = snakeFFrame[a+3]
        break
    
    
    delay = 60 # seconds
    for x in range(4):
        try:
            #goto calculator
            driver.get("https://www.morphmarket.com/c/reptiles/colubrids/western-hognose/genetic-calculator/")
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.trait-input-wrapper:nth-child(1) > input:nth-child(2)")))
            logMe("Page is ready!",num)
            break
        except TimeoutException:
            logMe("Loading took too much time!",num)
            if x == 3:
                driver.close()
                sys.exit()
    parentOneElement = driver.find_element(By.CSS_SELECTOR, "div.trait-input-wrapper:nth-child(1) > input:nth-child(2)")
    
    for x in range (len(maleMorphList)):
        maleMorphList[x] = maleMorphList[x].replace("66% ","").replace("100% ","").replace("50% ","")
        logMe("sending: " + str(maleMorphList[x]) + " into parent 1 text box",num)
        if maleMorphList[x][0] == " ":
            maleMorphList[x] = maleMorphList[x][1:]
        #print("parent 1 "  + "morph number :"+ str(x) + " " + str(maleMorphList[x]))
        try:
            parentOneElement.send_keys(maleMorphList[x])
            time.sleep(.1)
            parentOneElement.send_keys(Keys.TAB)
        except sce.ElementNotInteractableException:
            time.sleep(2)
            try:
                parentOneElement.send_keys(maleMorphList[x])
                time.sleep(.1)
                parentOneElement.send_keys(Keys.TAB)
            except sce.ElementNotInteractableException:
                logMe("couldnt input data into the calculator",num)
                sys.exit()
    parentTwoElement = driver.find_element(By.CSS_SELECTOR, "div.trait-input-wrapper:nth-child(3) > input:nth-child(2)")
    for y in range (len(femaleMorphList)):
        femaleMorphList[y]  = femaleMorphList[y].replace("66% ","").replace("100% ","").replace("50% ","")
        logMe("sending: " + str(femaleMorphList[y]) + " into parent 2 text box",num)
        try:
            if femaleMorphList[y][0] == " ":
                femaleMorphList[y] = femaleMorphList[y][1:]
        except IndexError:
            logMe("couldnt index into that femaleMorph List",num)
            logMe("female morph list" + str(),num)
        #print("parent 2 " + "morph number :"+ str(y) + " " + str(femaleMorphList[y]))
        try:
            parentTwoElement.send_keys(femaleMorphList[y])
            parentTwoElement.send_keys(Keys.TAB)
        except sce.ElementNotInteractableException:
            time.sleep(2)
            try:
                parentTwoElement.send_keys(femaleMorphList[y])
                parentTwoElement.send_keys(Keys.TAB)
            except sce.ElementNotInteractableException:
                logMe("couldnt input data into the calculator",num)
                sys.exit()
        
    calculateButtonCssSelector = ".tooltip-wrapper > button:nth-child(1)"
    calculateButtonElement = driver.find_element(By.CSS_SELECTOR,calculateButtonCssSelector)
    calculateButtonElement.click()
    time.sleep(1)
    #check for error page
    while (checkIfElementExistsByCssSelector(driver,"body > h3:nth-child(1)") == True):
        time.sleep(2)
        driver.refresh()
    
    dontGoFurther = 0
    while(checkIfElementExistsByCssSelector(driver,".tablesorter-headerRow") == False):
        logMe("couldnt find the element in the calulation page. trying again",num)
        dontGoFurther = 1
        results = grabSnakeComboData(driver, maleDf,femaleDf,calculateButtonElement, listOfAllMorphs,num)
        d = {'id': [myId], 'maleMorphs': [maleMorphList], 'femaleMorphs': [femaleMorphList], 'children': [results[0]], 'score': [results[1]], 'snakeLinks':[[maleLink, femaleLink]]}
        returningDataFrame = df(data = d)
       #print("printing children")
       #print(returningDataFrame["children"].head())
       #print("returning returningDataFrame from compare snakes")
        return returningDataFrame

    #print("calling grabSnakeComboData")
    #print(type(maleDf))
    if dontGoFurther == 0:
        results = grabSnakeComboData(driver,maleDf,femaleDf,calculateButtonElement, listOfAllMorphs,num)
        d = {'id': [myId], 'maleMorphs': [maleMorphList], 'femaleMorphs': [femaleMorphList], 'children': [results[0]], 'score': [results[1]], 'snakeLinks':[[maleLink, femaleLink]]}
        returningDataFrame = df(data = d)
        #print("printing children")
        #print(returningDataFrame["children"].head())
        #print("returning returningDataFrame from compare snakes")
        return returningDataFrame


def main():
    multiThread = 1
    maleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportm', names = ["morphs","cost","link"])
    femaleSnakeDataFrame = pd.read_csv('//home/nick/Documents/morphMarketHognoseMaximizer/snakeExportf', names = ["morphs","cost","link"])
    maleDataFrame, femaleDataFrame = runMeFirst(maleSnakeDataFrame,femaleSnakeDataFrame)
    splits = 2
    
    if multiThread == 1:
        #split male and female data frame into 6 different pieces
        #start a proces for each pair of pieces
            #in the process run everything below
        #when all processes are finished, grab all 6 returning dataframes and combine them
        #export
        slicesOfMaleDataFrame = np.array_split(maleDataFrame,splits)
        slicesOfFemaleDataFrame = np.array_split(femaleDataFrame,splits)
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        jobs =[]
        for n in range(splits):
            for o in range(splits):
                ret_value = multiprocessing.Value("d", 0.0, lock=False)
                p = multiprocessing.Process(target=spawn, args=[o+1*(n+1), return_dict, slicesOfMaleDataFrame[n], slicesOfFemaleDataFrame[o], maleSnakeDataFrame, femaleSnakeDataFrame])
                p.start()
                jobs.append(p)
            
            for proc in jobs:
               proc.join()
            print(return_dict.values())
    
    if multiThread == 0:
        driver = webdriver.Firefox()
        resultsDataFrame = df(columns=("id","maleMorphs","femaleMorphs","children","score","snakeLinks"))
        theId = 1
        # print(maleSnakeDataFrame.head(n=10))
        # print(femaleSnakeDataFrame.head(n=10))
        listOfAllMorphs = getListOfAllMorphs(maleSnakeDataFrame,femaleSnakeDataFrame)
        finalNumber = float(len(maleSnakeDataFrame) * float(len(femaleSnakeDataFrame)))
        count = 0
        dontGo = 0
        for x in range(len(maleSnakeDataFrame)):
            for y in range(len(femaleSnakeDataFrame)):
                #dataframe of males that are the same as male in question
                morphsInQuestion = maleSnakeDataFrame["morphs"].iloc[x]
                # print(morphsInQuestion)
                # print(resultsDataFrame["maleMorphs"])
                # # data frame where morphs are same as morph in question
                # checkerMaleDataFrame= resultsDataFrame[resultsDataFrame["maleMorphs"].str.contains(morphsInQuestion)]
                # print(checkerMaleDataFrame)
                # checkerMaleDataFrame = pd.DataFrame(checkerMaleDataFrame)
                # if not checkerMaleDataFrame.empty:
                #     # if frame of containing the dad also contains this mom then dont compare
                #     checkerFemaleDataFrame = checkerMaleDataFrame["femaleMorphs"].str.contains(femaleSnakeDataFrame.iloc[y])
                #     realDf2 = pd.DataFrame(checkerFemaleDataFrame)
                #     if not realDf2.empty():
                #         dontGo = 1
                #     #get all the instances with that male
                if dontGo == 0:
                    # if not resultDataFrame.empty:
                    #     print("found snakes for that set of parents: " + str(resultDataFrame.head()))
                    resultsDataFrame = resultsDataFrame.append(resultDataFrame)
                    resultsDataFrame.reset_index(inplace = True, drop = True)
                    #print(resultsDataFrame.head(n=10))
                    theId += 1
                    print("snake combination number " + str(count) + " out of " + str(finalNumber) + " completed.")
                    count += 1
                dontGo = 0
        resultsDataFrame = resultsDataFrame.sort_values(by = ["score"])
        print("printingReturndataframe")
        print(resultsDataFrame.head(n=10))
        resultsDataFrame.to_csv("//home/nick/Documents/morphMarketHognoseMaximizer/finalSnakeResults")
    
main()