import requests
from decouple import config
from urllib.parse import quote
import traceback
import sys

def get_new_api_token():
    id = config("SOCIAL_AUTH_AUTH0_KEY")
    secret = config("SOCIAL_AUTH_AUTH0_SECRET")
    base_api_url = config("AUTH0_BASE_API_URL")
    data = f"grant_type=client_credentials&client_id={id}&client_secret={secret}&audience={quote(base_api_url + '/api/v2/')}"
    headers = {'content-type': "application/x-www-form-urlencoded"}
    r = requests.post(f"{base_api_url}/oauth/token",data=data, headers=headers)
    with open("cron_auth0_api_token", "w") as f:
        f.write(r.json()["access_token"])
if __name__ == "__main__":
    get_new_api_token()