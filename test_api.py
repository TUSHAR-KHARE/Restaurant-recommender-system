import requests

url = "http://127.0.0.1:5000/predict"
data = {
    "Locality": "Indiranagar",
    "Cuisines": "North Indian"
}

response = requests.post(url, json=data)
print("✅ API Response:", response.json())
