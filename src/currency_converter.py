import requests

url = "https://hajana1-free-currency-converter-by-hajana-one-v1.p.rapidapi.com/currency-api.php"

querystring = {
    "amount": "500",
    "from": "EUR",
    "to": "USD"
}

headers = {
    'x-rapidapi-key': "5f68165e2emshf9462f5483ad7bap17785ajsna20dfc08cf3a",
    'x-rapidapi-host': "hajana1-free-currency-converter-by-hajana-one-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
