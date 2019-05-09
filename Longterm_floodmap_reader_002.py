# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 13:29:28 2019

@author: simon.desmet
"""

#script for getting flood map data off EA flood maps

from selenium import webdriver
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import os # a module that allows os commands
import time
import sys


#open selenium chrome driver
#chromedir = 'B:\\Chrome\\'
chromedir = r'\\Cslooafs01v\ztwe\Sheffield_Library\Software\Miscellaneous Software\ChromeDriver'

os.chdir(chromedir)
browser = webdriver.Chrome() #needs updating to give location of chromedriver


# get input file



#inputfilepath  = raw_input("list of NGR coodinates or post codes (CSV):")
inputfilepath  = 'B:\\D\\LNW Tunnel list.csv'

#outputpath = raw_input("output / save folder please:")
outputpath = 'B:\\D\\TEST_results'

os.chdir(outputpath)#sets the path for working folder to current directory

os.getcwd()#prints current directory to see if the above has worked.

inputcsv = pd.read_csv(inputfilepath, header=0)

#see if there is postcode data.
Postcodecolumnheader = 'none'
for column in inputcsv: # iterate through input csv columns
    item = inputcsv.at[0, column]# for each column look at 1st data entry
    if isinstance(item,str):# if the item in the 1st row is a string then...
        if len(item) == 5 or 6 or 7 and item[-2:].isalpha() and item[-3].isnumeric():# is the item 12 characters long, and are characters 1 & 2 both letters?
            print column#if they are print the column header
            print item
            Postcodecolumnheader = column#and then set the column header to the NGRcolumnheader
        else:
            continue
    else:
        continue
NGRcolumnheader = 'none' 
#if there are no postcodes, get NGRs instead if they are there
if Postcodecolumnheader == 'none':
    print 'find NGRs in dataset'
    #workout which column contains NGRs if present by checking 1, if the data is a string, 2 data is 12 elements long, 3 first two characters are letters.
    NGRcolumnheader = 'none' # defaults to no NGR data present
    for column in inputcsv: # iterate through input csv columns
        item = inputcsv.at[1, column]# for each column look at 1st data entry
        if isinstance(item,str):# if the item in the 1st row is a string then...
            if len(item) == 12 and item[0:1].isalpha():# is the item 12 characters long, and are characters 1 & 2 both letters?
                print column#if they are print the column header
                NGRcolumnheader = column#and then set the column header to the NGRcolumnheader
            else:
                continue
        else:
            continue
        if NGRcolumnheader == 'none': # if there are no NGRs or postcodes in the inputfile, close the script
            print 'no postcodes or NGR in file'
            time.sleep(3)
            sys.exit()
        else:
            continue
        
# convert NGRs to postcodes
updatedcsv = inputcsv

if NGRcolumnheader != 'none':#if NGR not none, then we take NGRs and find postcodes using webpage.
    postcodelist = []
    browser.get(('https://www.freemaptools.com/convert-ngr-to-postcode.htm'))
    NGRinput = browser.find_element_by_id('postcode')
    convertbutton = browser.find_element_by_xpath('//*[@id="content"]/center/p')
    for NGR in inputcsv[NGRcolumnheader]:
        NGRinput.send_keys(NGR)
        convertbutton.click()
        time.sleep(2)
        outputtext = browser.find_element_by_id('message').text
        outputtextstripped = outputtext.replace(" ","")
        postcodetext = outputtextstripped.split(':')[1]
        postcodelist.append(postcodetext)
        NGRinput.clear() # clears input box
    # add postcodes to csvimport table.

    
    updatedcsv['postcode'] = postcodelist
    # then close the browser
    browser.close
    

#then pass postcodes to next process.

            

#locationslist = open(inputfilepath).readlines() # reads list out of txt file and saves as a list
#locationslist = locationslist[:-1] # !!!!trim the final blank line off the list. !!! note if there is no blank line at bottom of the list, this will drop last file in list!
#print locationslist

#for l in loactionslist;
#   inputlocation = l
browser.get(('https://flood-warning-information.service.gov.uk/long-term-flood-risk/map'))
locationfinder = browser.find_element_by_id('txtSearch') # finds the txtsearch object on the Longterm flood risk webpage - the postcode box
searchbutton = browser.find_element_by_id('mapSearch')


for pcode in updatedcsv['Postcode']:
    inputlocation = pcode

    locationfinder.send_keys(inputlocation)
    searchbutton.click()


    element = browser.find_element_by_id("map") # finds item based on

    actions = ActionChains(browser)
    actions.move_to_element(element).perform()

#browser.implicitly_wait(355)
    time.sleep(3)
# get rivers and sea flood map screenshot
    browser.save_screenshot(inputlocation+'_'+'Rivers&Sea'+'_'+"pageshot.png");

    location = element.location;
    print location
    size = element.size;
    print size

    x = location['x'];
    print x
    y = location['y'];
    print y
    y = 140
    width = location['x']+size['width'];
    print width
    height = location['y']+size['height'];
    print height

    im = Image.open(inputlocation+'_'+'Rivers&Sea'+'_'+"pageshot.png")
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(inputlocation+'_'+'Rivers&Sea'+'_'+'finalshot.png')  

#get surface water flood map

    surfacewaterbutton = browser.find_element_by_id('SurfaceWater_6-SW-Extent')
    surfacewaterbutton.click()

    time.sleep(3)
    browser.save_screenshot(inputlocation+'_'+'SurfaceWater'+'_'+"pageshot.png");
    im = Image.open(inputlocation+'_'+'SurfaceWater'+'_'+"pageshot.png")
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(inputlocation+'_'+'SurfaceWater'+'_'+'finalshot.png')  

# get reservoirs flood map
    reservoirROFRbutton = browser.find_element_by_id('Reservoirs_3-ROFR')
    reservoirROFRbutton.click()

    time.sleep(3)
    browser.save_screenshot(inputlocation+'_'+'Reservoirs'+'_'+"pageshot.png");
    im = Image.open(inputlocation+'_'+'Reservoirs'+'_'+"pageshot.png")
    im = im.crop((int(x), int(y), int(width), int(height)))
    im.save(inputlocation+'_'+'Reservoirs'+'_'+'finalshot.png')  

updatedcsv.to_csv(path_or_buf=outputpath+'NGRs_and_postcodes'+'.csv', sep=',')
#close browser

browser.close()