import requests
from bs4 import BeautifulSoup

# https://beautiful-soup-4.readthedocs.io/en/latest/#searching-the-tree

train_headcode = 800008

r = requests.get(f"https://www.realtimetrains.co.uk/search/handler?qsearch={train_headcode}&type=detailed")
r = r.text
soup = BeautifulSoup(r, 'html.parser')
print(soup.find_all("li", string="UID" in))