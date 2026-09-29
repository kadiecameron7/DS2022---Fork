import requests

url = "https://api.coingecko.com/api/v3/coins/markets"
params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 5,
    "page": 1,
}
response = requests.get(url, params=params, timeout=10).json()
response.raise_for_status()

for coin in response.json():
    print(f"{coin['name']}: ${coin['current_price']} ({coin['price_change_percentage_24h']:.2f}%)")
