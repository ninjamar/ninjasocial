# NinjaSocial

NinjaSocial is a social media application built using Django and Bulma
## Running
### Install Dependencies
```bash
pip3 install -r requirements.txt
```
This project also uses `redis`. See [run.sh](run.sh) for more information.
## Setup
NinjaSocial uses Auth0 as the backend. You need to create an Auth0 project.

Create a file called `.env`
```.env
SOCIAL_AUTH_AUTH0_DOMAIN = "YOUR AUTH0 DOMAIN eg *.*.auth0.com"
SOCIAL_AUTH_AUTH0_KEY = "YOUR AUTH0 KEY"
SOCIAL_AUTH_AUTH0_SECRET = 'YOUR AUTH0 SECRET'

SECRET_KEY = 'DJANGO_SECRET_KEY'
AUTH0_TOKEN = 'AUTH0 API TOKEN'
AUTH0_ID = 'AUTH0 M2M APP ID'
AUTH0_SECRET = 'AUTH0 M2M APP SECRET'
```
<sub>[Auth0 Access Token docs](https://auth0.com/docs/secure/tokens/access-tokens/get-access-tokens)</sub>

## Testing/Running
The easiest way to run this is to run `python3 manage.py collectstatic` then run `uvicorn --host 0.0.0.0 --port 8080 --workers 2 social.asgi:application`. I suggest to disable the email verification middleware since that requires a cron job to review the api token.

## Deploying
I use [fly.io](https://fly.io) for deploying
