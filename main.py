import requests

url = "http://127.0.0.1:5000"
a = 1
b = 2
c = 3
d = 4
response = requests.get(f"{url}/user/{a}/{b}/{c}/{d}")

print(response.json())