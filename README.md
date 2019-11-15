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
* PEP8 compatible coding style.*

### Tech Stack
Following is the tech stack being used for main project:
* [Django 2.1.1] - The core Web Framework
* [Postgres 10.5] - As datastore
* [Celery 4.3.0] - As Job queue
* [Rabbit Mq] - As message broker

## Mongo DB Setup
```
# Install mongo DB by going through below link
https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/

# You can also install MongoDB as specified below

# 1. Install mongodb:
sudo apt-get install mongodb

# 2. Unlock the mongodb
sudo rm /var/lib/mongodb/mongod.lock
sudo mongod --repair

# 3. Enable and start the service
sudo systemctl enable mongodb
sudo service mongodb start

# 4. Quick lookups:
sudo systemctl start mongodb # start mongodb server
sudo systemctl status mongodb # get the status of mongodb server
sudo systemctl enable mongodb # enable for auto restart on boot
sudo systemctl restart mongodb # restart mongodb server
sudo systemctl stop mongodb # stop mongodb server
sudo systemctl disable mongodb # disable auto start on boot for mongodb server


# After installation, enter to shell of mongoDB with below command
mongo

# In mongo shell create database
use large_csv

# Create User
db.createUser({user:"csv_user",pwd:"your_pwd",roles:[{role:"dbOwner",db:"large_csv"}]})

# Exit mongo shell
quit() or Ctrl+C
exit

# In the environment file(local.py/prod.py)
update the Database details
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