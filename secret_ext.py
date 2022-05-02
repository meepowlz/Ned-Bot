import requests
from bs4 import BeautifulSoup

# https://beautiful-soup-4.readthedocs.io/en/latest/#searching-the-tree

train_headcode = 800008

"""
- Raise error if no uid found?
Should work consistently; determine if the UID shifts places at any point depending on the responses
"""


def get_service_uid(train_headcode):
    """
    Looks up train by headcode
    Parses the returned html to extract the current service uid
    If no uid found, -1 returned
    :param train_headcode:
    :return:
    """
    # Get the html of resultant page after search
    r = requests.get(f"https://www.realtimetrains.co.uk/search/handler?qsearch={train_headcode}&type=detailed")
    r = r.text
    # Find service uid
    soup = BeautifulSoup(r, 'html.parser')
    li = soup.find_all("li")
    uid = -1
    for item in li:
        text = str(item)
        if "UID" in text:
            print(text)
            uid_index = text.find("UID")
            uid = text[uid_index + 4:].split(",", 1)[0]
            print(uid)
    return uid


print(get_service_uid(train_headcode))
