
from selenium import webdriver
from selenium.common import exceptions  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time
import csv

def openAndGotoCorrectFilteredList(sex):
    dontGoFurther = False
    driver= webdriver.Firefox()
    driver.get("https://www.morphmarket.com/us/c/reptiles/colubrids/western-hognose?sort=nfs&has_id=1")
    filtersXpath = "/html/body/div[3]/div[2]/div/div[1]/div[2]/span/a[1]"
    filterElement = driver.find_element_by_xpath(filtersXpath)
    filterElement.click()
    sexDropDownXPath = "//*[@id='id_sex']"
    sexDropDownElement = driver.find_element_by_xpath(sexDropDownXPath)
    sexDropDownElement.click()
    femaleSelectionXPath = "/html/body/header/form/div/div[4]/div/div[4]/div[2]/select/option[3]"
    maleSelectionXPath = "/html/body/header/form/div/div[4]/div/div[4]/div[2]/select/option[2]"
    if sex == "m":
        maleSelectionElement = driver.find_element_by_xpath(maleSelectionXPath)
    if sex == "f":
        selectionElement = driver.find_element_by_xpath(femaleSelectionXPath)
    else:
        print("didnt pick m or f, try again.")
        dontGoFurther = True
    if dontGoFurther == True:
        maleSelectionElement.click()
        goFilterButtonXPath = "//*[@id='adv-search-btn']"
        goFilterButtonElement = driver.find_element_by_xpath(goFilterButtonXPath)
        goFilterButtonElement.click()
        sortByButtonXPath = "/html/body/div[3]/div[2]/div/div[1]/div[1]/div[1]/button"
        sortByButtonElement = driver.find_element_by_xpath(sortByButtonXPath)
        sortByButtonElement.click()
        newestPostedSelectionXPath = "/html/body/div[3]/div[2]/div/div[1]/div[1]/div[1]/ul/a[7]"
        newestPostedSelectionElement = driver.find_element_by_xpath(newestPostedSelectionXPath)
        newestPostedSelectionElement.click()
    return driver

def grabSnakeListingDataOnSinglePage(driver):
    time.sleep(1)
    morphList =[]
    ##grabbing vis-rec morphs
    try:
        morphListElement = driver.find_elements_by_xpath('.//span[@class = "badge trait vis-rec"]')
        for morph in morphListElement:
             morphList.append(morph.text)
    except exceptions.StaleElementReferenceException:
        print("no vis-rec traits")
    #grabbing het-rec morphs
    try:
        morphListElement = driver.find_elements_by_xpath('.//span[@class = "badge trait het-rec"]')
        for morph in morphListElement:
             morphList.append(morph.text)
    except exceptions.StaleElementReferenceException:
        print("no het-rec traits")
     #grabbing dom-codom morphs
    try:
        morphListElement = driver.find_elements_by_xpath('.//span[@class = "badge trait dom-codom"]')
        for morph in morphListElement:
             morphList.append(morph.text)
    except exceptions.StaleElementReferenceException:
        print("no dom-codom traits")
     #grabbing super-dom-codom morphs
    try:
        morphListElement = driver.find_elements_by_xpath('.//span[@class = "badge trait super-dom-codom"]')
        for morph in morphListElement:
             morphList.append(morph.text)
    except exceptions.StaleElementReferenceException:
        print("no super-dom-codom traits")
    #grabbing badge trait pos-rec morphs
    try:
        morphListElement = driver.find_elements_by_xpath('.//span[@class = "badge trait pos-rec"]')
        for morph in morphListElement:
             morphList.append(morph.text)
    except exceptions.StaleElementReferenceException:
        print("no pos-rec traits")
     #grabbing badge trait other morphs
    try:
        morphListElement = driver.find_elements_by_xpath('.//span[@class = "badge trait other"]')
        for morph in morphListElement:
             morphList.append(morph.text)
    except exceptions.StaleElementReferenceException:
        print("no other traits")
    #grabbing price
    priceElement = driver.find_element(By.CSS_SELECTOR,"dd.price")
    price  = priceElement.text[3:]
    #grabbing link
    link = driver.current_url
    returnList = [morphList,price,link]
    return returnList
    
def gotoNextPageOfListings(driver):
    try:
        nextPageElement = driver.find_element(By.CSS_SELECTOR,"li.page-item:nth-child(8) > a:nth-child(1)")
        nextPageElement.click();
    except exceptions.StaleElementReferenceException:
        print("no next page button found")


def itterateThroughSnakesOnePage(driver):
    snakes = []
    for x in range(len(driver.find_elements(By.CLASS_NAME,"snake-thumb"))):
        snakeDriverElements = driver.find_elements(By.CLASS_NAME,"snake-thumb")
        snakeDriverElements[x].click()
        snake = grabSnakeListingDataOnSinglePage(driver)
        snakes.append(snake)
        print(snakes[x])
        driver.back()
    return snakes

def nextButtonStillValid(driver):
    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "li.page-item:nth-child(8)")))
    if element.text != "":
        return True
def exportSnakes(snakes,sex):
    # open the file in the write mode
    f = open('/home/nick/Documents/snakeExport' + sex, 'w')
    # create the csv writer
    writer = csv.writer(f)
    # write a row to the csv file
    for x in snakes:
        writer.writerow(x)
    # close the file
    f.close()
    return True
    
def grabSnakeData(sex):
    #checkThatCheckerWorks();
    driver= openAndGotoCorrectFilteredList(sex)
    ## for listing in list
    snakes = itterateThroughSnakesOnePage(driver)
    try:
        checkerValue = driver.find_element(By.CSS_SELECTOR,"li.page-item:nth-child(8) > a:nth-child(1)").get_attribute("value")
    except exceptions.NoSuchElementException:
        print("couild not find the next button")
        checkerValue = ''
    while(checkerValue != ''):
        gotoNextPageOfListings(driver)
        for snake in itterateThroughSnakesOnePage(driver):
            snakes.append(snake)
        try:
            checkerValue = driver.find_element(By.CSS_SELECTOR,"li.page-item:nth-child(8) > a:nth-child(1)").get_attribute("value")
        except exceptions.NoSuchElementException:
            print("couild not find the next button")
            checkerValue = ''
    goodBad = exportSnakes(snakes,sex)
    if goodBad == True :
        print("sucessfully documented all " + sex + " snakes.")
        return [driver,True]
    else:
        return [driver,False]

def main():
    returnList = grabSnakeData("m")
    if returnList[1] == True:
        femaleReturnTuple = grabSnakeData("f")
        if femaleReList[1] == True:
            print("finished grabbing the data for all male and female hognose snakes on morph market.")
        else:
            print("second grabbing of the snake data failed. Try again.")
    else:
        print("first grabbing of snake data failed. Try again.")

main();

