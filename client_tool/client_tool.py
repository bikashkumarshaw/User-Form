import json
import argparse
import requests
import jwt
import pprint

Allowed_Actions = [
    "login",
    "filter",
    "generate_key",
    "register",
    "fetch",
    "load"
]

class ClientTool(object):

    def run(self):
        self.define_args()
        if self.args.action.lower()=="generate_key":
            key = self.prepare_key()
            print ("\n"+key.decode("utf-8")+"\n")
        elif self.args.action.lower()=="register" or self.args.action.lower()=="login":
            self.register(self.args.action.lower())
        elif self.args.action.lower()=="filter":
            self.filter()
        elif self.args.action.lower()=="fetch":
            self.fetch()
        elif self.args.action.lower()=="load":
            self.load()
        else:
            raise Exception("Please chose action among the following:\n \t{}".format(Allowed_Actions))

    def prepare_key(self):
        encoded_jwt = jwt.encode({'email': self.args.email_id}, self.args.password.lower(), algorithm='HS256')
        return (encoded_jwt)

    def register(self, mode):
        data = dict(email_id=self.args.email_id, password=self.args.password, mode=mode)

        resp = self._req_service(data, "register")

        pprint.pprint(resp)

    def filter(self):
        data = dict(age=self.args.age, name=self.args.name, city=self.args.city, \
            state=self.args.state, pin=self.args.pin, key = self.args.key, filter_fields=self.args.filter_fields)

        resp = self._req_service(data, "filter")

        pprint.pprint(resp)

    def fetch(self):
        data = dict(age=self.args.age, name=self.args.name, city=self.args.city, \
            state=self.args.state, pin=self.args.pin, key = self.args.key, filter_fields=self.args.filter_fields)

        resp = self._req_service(data, "fetch")

        pprint.pprint(resp)

    def _req_service(self, data, api):
        r = requests.post("http://{0}:{1}/api/{2}".format(self.args.ip, self.args.port, api), \
        data=json.dumps(data), headers={'Content-Type': 'application/json'})

        return r.json()

    def load(self):
        data = dict(age=self.args.age, name=self.args.name, city=self.args.city, \
            state=self.args.state, pin=self.args.pin, key = self.args.key, \
            phone_number=self.args.number, address=self.args.address, misc=self.args.misc)

        resp = self._req_service(data, "load")

        pprint.pprint(resp)

    def define_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("--ip", help="specify bank insights service ip", type=str, required=True)
        parser.add_argument("--port", help="specify bank insights service port", type=str, required=True)
        parser.add_argument("--email-id", type=str, help="specify your email id", default="")
        parser.add_argument("--password", type=str, help= "specify password", default="")
        parser.add_argument("--action", type=str, help="specify the actions among: {}".format(Allowed_Actions), default="")
        parser.add_argument("--age", type=str, help= "specify age either in range or integer", default="")
        parser.add_argument("--city", type=str, help= "specify the city", default="")
        parser.add_argument("--state", type=str, help= "specify the state", default="")
        parser.add_argument("--pin", type=str, help= "specify the pin", default="")
        parser.add_argument("--address", type=str, help= "specify the address", default="")
        parser.add_argument("--name", type=str, help= "specify specify user's name", default="")
        parser.add_argument("--dob", type=str, help= "specify users dob eg. '1995-09-09'", default="")
        parser.add_argument("--misc", type=str, help= "specify misc in key value pairs \
                where each pair is separated by space and key value separated by ':' eg. k1:v1 k2:v2", default="")
        parser.add_argument("--number", type=str, help= "specify the phone number", default="")
        parser.add_argument("--key", type=str, help= "specify your key", default="")
        parser.add_argument("--filter-fields", type=str, help= "specify fields to be filtered", default="")
        self.args = parser.parse_args()

if __name__== "__main__":
    ClientTool().run()

