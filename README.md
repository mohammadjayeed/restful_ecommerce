## Endpoint Documentation
- [API Endpoints Collection](https://documenter.getpostman.com/view/20444054/2sAY4x9MRh)

## Special Instruction
- .env file wthin restful_ecom is for local installation
- .env file in the root directory is for docker based deployment
-  please note that postgres has been used as database



# Local Installation


## Step 1 - Repository
- Clone the following [repository](https://github.com/mohammadjayeed/restful_ecommerce.git),
```bash
  git clone  https://github.com/mohammadjayeed/restful_ecommerce.git
```
## Step 2 - Virtual Environment
- Make a virtual environment with the following command
```bash
  python -m venv venv
```
-  Activate the virtual environment with the command
```bash
  venv/scripts/activate  or  source venv/bin/activate (for linux)
```
## Step 3 - Dependencies
- Install dependencies
```bash
  pip install -r requirement.txt
```
## Step 4 - Migrations
- Run the following command to apply it to the database
```bash
  python manage.py migrate
```
## Step 5 - Superuser
- Run the following command to create a superuser to access admin panel by adding the required information. We will require username and password to login to the admin panel
```bash
  python manage.py createsuperuser
```
## Step 6 - Start App
- Start the application by typing the following command
```bash
  python manage.py runserver
```

# Docker Installation
- Make sure you have docker installed on your machine

- From the terminal, input these commands:
```bash
  docker compose up --build
```
- Finally create a superuser (if you would like to) with the following commands:
```bash
  docker exec -it <container_id_or_name> /bin/bash
```
A prompt will show up. Type:
```bash
  python manage.py createsuperuser
```
- Provide user credentials as necessary 




