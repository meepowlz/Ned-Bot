import requests

train_headcode = 800008

r = requests.get(f"https://www.realtimetrains.co.uk/search/handler?qsearch={train_headcode}&type=detailed")
print(r.text)