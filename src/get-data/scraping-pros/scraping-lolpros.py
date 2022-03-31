import requests
url = 'https://lolpros.gg/ladders'
r = requests.get(url)
# print(r.content)

from bs4 import BeautifulSoup
soup = BeautifulSoup(r.content, 'html.parser')
mydivs = soup.find_all("div", {"class": "row"})
for a in soup.find_all('a', href=True):
	if "player" in a:

		print(a)
# print(mydivs)

