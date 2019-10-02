# User-Form
This form lets user register, login, load data, filter them and fetch them.

#### Note you would need postgresql and mysql installed in your system for this.

## Install postgresql
```
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
```

## Create username and db for postgresql
```
sudo -u postgres createuser <username>
sudo -u postgres createdb <dbname>
sudo -u postgres psql
alter user <username> with encrypted password '<password>';
grant all privileges on database <dbname> to <username> ;
```

## Clone:
```
git clone https://github.com/bikashkumarshaw/Bank_insights.git
```

## Install Virtual Environment:
```
pip install virtualenv

cd User-Form

virtualenv -p python3 [environment name eg. env]

source env/bin/activate (env is the name of the environment here. please set according to your environment name)

Now install all the dependencies as listed below
```

## Dependencies:
- pip install -r requirements.txt

## Run command:
```
python seller_app.py --port `specify the port to host the service` --dbname `provide your mysql db name` --ip `specify the ip of the machine where this service will be hosted` --user `provide your mysql username` --password `specify the password of mysql user` --psqldbname `provide your postgressql db name` --psqluser `provide your postgressql username` --psqlpassword `specify the password of postgressql user`
```

## API'S supported:

```
fetch (Used to fetch data of users)
load (Used to load data of users)
filter (Used to filter data based on users choice
register (Used to register users)
login (Used by users to login)
```

