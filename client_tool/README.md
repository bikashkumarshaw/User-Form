# Client tool:

### This tool is used to perform all actions as below:
    register
    login
    load
    filter
    fetch
    generate-key

# Install Virtual Environment:
```
pip install virtualenv

virtualenv -p python2 [environment name eg. env]

source env/bin/activate (env is the name of the environment here. please set according to your environment name)

Now install all the dependencies as listed below
```

## Dependencies:
- pip install -r requirements.txt

# Guide to use Client tool

## Arguments supported by tool

```
python clinet_tool.py -h
```
![](https://i.imgur.com/ts9thRn.png)

## Command:

The command below is used for new users to register to acces api's
```
python client_tool.py --email-id `specify your email id` --password `specify password here` --ip 159.69.60.242 --port 2233 --action register
```

The command below is used to get key for already existing user.
```
python client_tool.py --email-id `specify your email id` --password `specify password here` --ip 159.69.60.242 --port 2233 --action generate_key
```

The command below is used to login.
```
python client_tool.py --email-id `specify your email id` --password `specify password here` --ip 159.69.60.242 --port 2233 --action login
```

The command below is used to load data.
```
python client_tool.py --key 'specify your generated key here` --ip 159.69.60.242 --port 2233 --action load --age `specify the age` --city `specify city` --state `specify state` --pin `specify pin` --address `specify address` --name `specify user name here` --dob `specify users dob eg. '1995-09-09'` --misc specify misc in key value like dictionary eg. '{"name": "bikash"}'` --number `specify the phone number`
```

The command below is used to fetch data.
```
python client_tool.py --key 'specify you generated key here` --ip 159.69.60.242 --port 2233 --action fetch --filter-fields `This field is the colums you want to see these are comma separetd eg. name,age,city` --age `optional we can keep this as a number 10 or all:20 or 20:all` --city `optional this is the where clause filter` --state `optional this is the where clause filter` --name `optional this is the where clause filter` --key `specify your generated key here`


### Note Each users will be logged in for 5 days.
