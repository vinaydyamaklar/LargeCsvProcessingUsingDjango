# LargeCsvProcessingUsingDjango
csv_kjniuyn!kn
An admin dashboard can be opening by appending **/admin** at the end of the domain URL.

#### Structure
* **models.py:** Where all models live.
* **views.py:** Where all views for web pages live.
* **urls.py:** Router for web pages views.
* **templates.py:** Where all the base templates live.
* **admin.py:** All Django admin related settings.

#### Standards
* PEP8 compatible coding style.* Doc strings for all the modules and their members. These doc strings are read by Sphinx and Swagger to create documentations.

### Tech Stack
Following is the tech stack being used for main project:
* [Django 2.1.1] - The core Web Framework
* [Postgres 10.5] - As datastore
* [Celery 4.3.0] - As Job queue
* [Rabbit Mq] - As message broker

## Postgres DB Setup
```
sudo apt-get update
sudo apt-get install python-pip python-dev libpq-dev postgresql

# During the Postgres installation, an operating system user named postgres was created to correspond to the postgres PostgreSQL administrative user. We need to change to this user to perform administrative tasks
sudo su - postgres

# You should now be in a shell session for the postgres user. Log into a Postgres session by typing
psql

# Create database and user
CREATE DATABASE emproto_csv_db;
CREATE USER csv_user WITH PASSWORD 'your_pwd';

# Setting encodings to UTF-8, timezones and transaction isolations
ALTER ROLE csv_user SET client_encoding TO 'utf8';
ALTER ROLE csv_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE csv_user SET timezone TO 'UTC';

# Grant all permissions for the created user
GRANT ALL PRIVILEGES ON DATABASE emproto_csv_db TO csv_user;

# Exit
\q
exit

```
## Project **Setup**


### Installing RabbitMq
* sudo apt-get install -y erlang
* sudo apt-get install rabbitmq-server

##### RabbitMq Commands
* **Enable:** systemctl enable rabbitmq-server
* **Start:** systemctl start rabbitmq-server
* **Status check:** systemctl status rabbitmq-server
```
sudo apt-get update
sudo apt-get install python-pip python-dev python3.6-dev git
sudo apt-get install build-essential libssl-dev libffi-dev
sudo apt-get install libjpeg-dev libfreetype6-dev zlib1g-dev

sudo pip install virtualenv
sudo pip install --upgrade pip

virtualenv --python=python3 venv
source venv/bin/activate

mkdir flyer && cd flyer
git clone https://gitlab.com/zignite/clients/flyer/flyer-dashboard.git

cd dashboard
pip install -r requirements.txt


# MAKE MIGRATIONS ONLY IF YOU ARE MODIFYING THE MODELS
python manage.py makemigrations

python manage.py collectstatic
python manage.py migrate
python manage.py runserver

admin/flyeradmin34
```

### Server
```bash
157.175.50.39:8001
```