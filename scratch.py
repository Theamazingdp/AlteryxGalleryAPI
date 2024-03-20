import requests
import os
from dotenv import load_dotenv


load_dotenv()

base_url = "https://spider.theinformationlab.co.uk/webapi/"

token_url = f"{base_url}oauth2/token"

url = "https://spider.theinformationlab.co.uk/webapi/v3/workflows?view=Default"

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

payload = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}

response = requests.post(token_url, data=payload)

print(response.url)
print(response.status_code)
print(response.text)
