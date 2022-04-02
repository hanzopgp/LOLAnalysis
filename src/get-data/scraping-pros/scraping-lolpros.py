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
	last_page = 2 # For debug purpose
	all_pages_players_url.append(scrape_one_page(driver)) # Scrapes first page
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

def get_driver_one_player(player_url):
	options = webdriver.ChromeOptions()
	options.add_experimental_option('excludeSwitches', ['enable-logging'])
	player_driver = webdriver.Chrome(options=options)
	player_driver.get(player_url)
	time.sleep(1)
	return player_driver

def scrape_one_player_infos(player_driver):
	player_infos = []
	url_str = str(player_driver.current_url)
	name = url_str.split("/")[-2]
	if name == "player": # Sometimes there is a player in table but url doesn't work
		return []
	player_infos.append(name)
	trs = player_driver.find_elements(By.XPATH, "//tbody//tr")
	for tr in trs: 
		tds = tr.find_elements(By.XPATH, "td") 
		country = ""
		age = ""
		for i, td in enumerate(tds):
			if td.text == "Birthplace":
				country = tds[i+1].text
			elif td.text == "Birthday":
				age_string = tds[i+1].text
				age = int(age_string[age_string.find('(')+1:age_string.find(')')])
		player_infos.append(country)
		player_infos.append(age)
			
	return player_infos

def scrape_players_infos(all_players_pages):
	all_data = []
	for player_url in tqdm(all_players_pages[:10]):
		player_driver = get_driver_one_player(player_url)
		all_data.append(scrape_one_player_infos(player_driver))
		player_driver.close()
	return np.array(all_data)

driver = init() # Init our driver
all_players_pages = scrape_all_pages(driver) # Scrapes all the url pages of the pro players
all_data = scrape_players_infos(all_players_pages) # Gets all the data per pro player
print(all_data)



