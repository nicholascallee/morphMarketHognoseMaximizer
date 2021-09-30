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
from hognoseHelper import fixLikelienessElementList
from hognoseHelper import fixGenesElementList
from hognoseHelper import fixGeneString
from hognoseHelper import averageSnakePrices
from hognoseHelper import createNewColumns
from hognoseHelper import exportGenes
from hognoseHelper import getAllSnakesWithTheseTraits
from hognoseHelper import runMeFirst



def findAvgPriceOfSnake(driver,snake):
    #instead of trying to load a fuck ton of pages, just look in the list of snakes we already made dumbass
    snakesWithTheseParticularTraits = getAllSnakesWithTheseTraits(snake)
    if snakesWithTheseParticularTraits == 0:
        return 0
    else:
        pricesOfSpecificSnake = snakesWithTheseParticularTraits["cost"]
        print("this is the cost of the snakes found in a list: " + str(pricesOfSpecificSnake))
        avg = averageSnakePrices(pricesOfSpecificSnake)
        return avg



def grabSnakeComboData(driver):
    returner = []
    #snakeChildren = [likelieness morph avg price]
    snakeChildren = []
    #grab likelieness and traits/genes
    likelienessElementList = driver.find_elements(By.CLASS_NAME, "prob")
    genesElementList = driver.find_elements(By.CLASS_NAME, "genes")
    
    #fix elements to fit whats needed next
    fixedLikelienessList  = fixLikelienessElementList(likelienessElementList)
    fixedGenesList = fixGenesElementList(genesElementList)
    
    weightedTotalReturn = 0
    #for x in range len of child list
    for x in range(1,len(likelienessElementList)-1):
        likelieness = fixedLikelienessList[x]
        genes = fixedGenesList[x]
        print("calling findAvgPriceOfSnake")
        price = findAvgPriceOfSnake(driver, genes)
        #if we found one
        if price != 0:
            print("found snakes with that morph. avg price: " + str(price))
            weightedTotalReturn += float(likelieness) * float(price)

    returner = [fixedGenesList,weightedTotalReturn] 
    return returner
    

def compareSnakes(driver,snakeMFrame, snakeFFrame, myId):
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
        #print("parent 1 "  + "morph number :"+ str(x) + " " + str(maleMorphList[x]))
        parentOneElement.send_keys(maleMorphList[x])
        parentOneElement.send_keys(Keys.TAB)
    parentTwoElement = driver.find_element(By.CSS_SELECTOR, "div.trait-input-wrapper:nth-child(3) > input:nth-child(2)")
    for y in range (len(femaleMorphList)):
        femaleMorphList[y]  = femaleMorphList[y].replace("66% ","").replace("100% ","")
        try:
            if femaleMorphList[y][0] == " ":
                femaleMorphList[y] = femaleMorphList[y][1:]
        except IndexError:
            print("couldnt index into that femaleMorph List")
            print("female morph list" + str())
        #print("parent 2 " + "morph number :"+ str(y) + " " + str(femaleMorphList[y]))
        parentTwoElement.send_keys(femaleMorphList[y])
        parentTwoElement.send_keys(Keys.TAB)
    calculateButtonCssSelector = ".tooltip-wrapper > button:nth-child(1)"
    calculateButtonElement = driver.find_element(By.CSS_SELECTOR,calculateButtonCssSelector)
    calculateButtonElement.click()
    time.sleep(2)
    results = grabSnakeComboData(driver)
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
            resultDataFrame = compareSnakes(driver, maleSnakeDataFrame.iloc[x],femaleSnakeDataFrame.iloc[y],theId)
            resultsDataFrame = resultsDataFrame.append(resultDataFrame)
            theId += 1
            print("finished comparing "+ str(y) +" y " + str(x) + " x " + " combination of snakes out of " + str(len(maleSnakeDataFrame) ) +" x "+ str(len(femaleSnakeDataFrame)) + " y")
        
    resultsDataFrame = resultsDataFrame.sort_values(by = ["score"])
    print("printingReturndataframe")
    print(resultsDataFrame.head(n=10))
    resultsDataFrame.to_csv("//home/nick/Documents/morphMarketHognoseMaximizer/finalSnakeResults")

maleDataFrame, femaleDataFrame = runMeFirst()
main()