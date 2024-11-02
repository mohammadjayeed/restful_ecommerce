## Special Instruction
- .env file wthin restful_ecom is for local installation
- .env file in the root directory is for docker based deployment, remove it if you want to try local first
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
  pip install -r requirements.txt
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

## Step 6 - Run Redis With Docker
```bash
  docker run -d -p 6379:6379 redis
```

## Step 7 - Configure SMTP in .env
- You might have to create App password authentication for Google
- You can follow any other mailserver tutorial on youtube

## Step 8 - Start App
- Start the application by typing the following command
```bash
  python manage.py runserver
```

## Step 9 - Start Celery
```bash
celery -A restful_ecom worker --loglevel=info
```

## Step 10 - Start Celery Beat
```bash
celery -A restful_ecom beat
```
