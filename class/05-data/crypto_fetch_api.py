import requests

url = "https://pro-api.coinmarketcap.com/public-api/v3/cryptocurrency/listings/latest"
params = {"limit": 5, "convert": "USD"}
response = requests.get(url, params=params, timeout=10)
response.raise_for_status()

for coin in response.json()["data"]:
    quote = coin["quote"][0]
    print(f"{coin['name']}: ${quote['price']:.2f} ({quote['percent_change_24h']:.2f}%)")
