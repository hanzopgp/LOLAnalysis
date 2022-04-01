from re import A
import requests
from bs4 import BeautifulSoup

from selenium import webdriver	
from selenium.webdriver.common.keys import Keys
import time







# use chrome
driver = webdriver.Chrome()
driver.get("https://www.trackingthepros.com/players/")
time.sleep(1)
# get all tr from table
element = driver.find_elements_by_xpath("//tbody//tr")


# iterate over elements of table
for x in element: 

	# extract player then playe's link
	td = x.find_elements_by_xpath("td")
	a = td[0].text
	player_name = a[6:]
	player_link = f"https://www.trackingthepros.com/player/{player_name}/"
	print(player_link)
	


