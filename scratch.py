import os
from dotenv import load_dotenv
from AlteryxGallery import AlteryxGalleryAPI

load_dotenv()

base_url = "https://spider.theinformationlab.co.uk/webapi/"

# token_url = f"{base_url}oauth2/token"

# url = "https://spider.theinformationlab.co.uk/webapi/v3/workflows?view=Default"

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")


# payload = {"client_id": client_id, "client_secret": client_secret, "grant_type": "client_credentials"}

# response = httpx.post(token_url, data=payload)

# print(response.url)
# print(response.status_code)
# print(response.text)


with AlteryxGalleryAPI.GalleryClient(base_url=base_url) as client:
    client.authenticate(client_id, client_secret)
    response, content = client.get_all_workflows(name="00-Octopus Download Pipeline")
    print(f"workflow query status response: {response.status_code}")
    print(f"workflow query content: {content}")