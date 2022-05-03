import asyncio

import aiohttp
import requests
from bs4 import BeautifulSoup
import discord

# https://beautiful-soup-4.readthedocs.io/en/latest/#searching-the-tree

train_headcode = 800320

"""
- Raise error if no uid found?
Should work consistently; determine if the UID shifts places at any point depending on the responses
headcodes
800008 (gay train)
390119 (full wrap train)
800320 (random train for testing)
"""


async def get_service_uid(train_headcode):
    """
    Looks up train by headcode
    Parses the returned html to extract the current service uid
    If no uid found, -1 returned
    :param train_headcode:
    :return:
    """
    url = f"https://www.realtimetrains.co.uk/search/handler?qsearch={train_headcode}&type=detailed"
    # Get the html of resultant page after search
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            r = await response.text()
    print(r)
    # Find service uid
    soup = BeautifulSoup(r, 'html.parser')
    li = soup.find_all("li")
    uid = -1
    for item in li:
        text = str(item)
        if "UID" in text:
            #print(text)
            uid_index = text.find("UID")
            uid = text[uid_index + 4:].split(",", 1)[0]
            print(f"UID: {uid}")
    return uid

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(get_service_uid(train_headcode))
