# NinjaSocial

NinjaSocial is a social media application built using Django and Bulma\
[Instance](https://social.ninjamar.dev)
## Running
### Install Dependencies
```bash
pip3 install -r requirements.txt
```
## Setup
NinjaSocial uses Auth0 as the backend. You need to create an Auth0 project.

Create a file called `.env`
```.env
SOCIAL_AUTH_AUTH0_DOMAIN = "DOMAIN"
SOCIAL_AUTH_AUTH0_KEY = "KEY"
SOCIAL_AUTH_AUTH0_SECRET = 'SECRET'

SECRET_KEY = 'DJANGO_SECRET_KEY'

```

## Testing/Running

### First Time
```bash
python3 manage.py createsuperuser
```

### Running
```bash
python3 manage.py runserver
```

## Deploying
I use [fly.io](https://fly.io) for deploying