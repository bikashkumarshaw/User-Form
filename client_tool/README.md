# Client tool:

## This tool is used to generate jwt key for users.

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

### Note Each users key will be active for 5 days.
