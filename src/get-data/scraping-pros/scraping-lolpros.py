import numpy as np
from selenium import webdriver	
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm


def init():
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	driver = webdriver.Chrome(options=options)
	driver.get("https://www.trackingthepros.com/players/")
	time.sleep(1)
	return driver

def scrape_one_page(driver):
	one_page_players_url = []
	element = driver.find_elements(By.XPATH, "//tbody//tr")
	for x in element: 
		td = x.find_elements(By.XPATH, "td")
		a = td[0].text
		player_name = a[6:]
		player_link = f"https://www.trackingthepros.com/player/{player_name}/"
		one_page_players_url.append(player_link)
	# print("\n SCRAPED : ", len(one_page_players_url), "PRO PAGES")
	return one_page_players_url

def scrape_all_pages(driver):
	all_pages_players_url = []
	pagination = driver.find_element(By.CLASS_NAME, "pagination") # Gets the first occurence of .pagination
	last_page = int(pagination.text[-7:-4]) # Gets the last pages (the one before "next")
	last_page = 3 # For debug purpose
	# scrape_one_page(driver) # Scrapes first page
	for page_number in tqdm(range(2, last_page+1)):
		# print("SCRAPING PAGE NUMBER :", page_number)
		pagination = driver.find_element(By.CLASS_NAME, "pagination") # Refresh our pagination class
		lis = pagination.find_elements(By.TAG_NAME, "li") # Regresh our lists tag
		for x in lis:
			try: # Avoid debugging because the html of trackingthepros is kinda clunky
				links = x.find_elements(By.TAG_NAME, "a")
				for link in links:
					case_found = int(link.get_attribute("data-dt-idx")) # Gets the index of the case
					if case_found > 5: case_found = 5 # The index is the same than the page until page 5, where the next case index will always be 5
					if case_found == page_number or case_found == 5: # Check that we are going to click and scrape the right page
						# time.sleep(1)
						# print("CLICKED ON PAGE :", page_number)
						link.click() # Click to next page
						# time.sleep(1)
						all_pages_players_url.append(scrape_one_page(driver)) # Scrape the page
			except:
				pass
	driver.close() # Close the page since now we are going to go through all the player pages to get their informations
	return np.array(all_pages_players_url).flatten() # Flatten because we don't care about the pages number

def scrape_player_infos(driver, all_players_pages):
	pass

driver = init() # Init our driver
all_players_pages = scrape_all_pages(driver) # Scrapes all the url pages of the pro players
all_data = scrape_player_infos(driver, all_players_pages) # Gets all the data per pro player
print(all_players_pages.shape)



