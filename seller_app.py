from flask import Flask, request
import json
import psycopg2
import jwt
from datetime import date
import mysql.connector
from mysql.connector import Error

from args import _define_args
from queries import SQL_QUERY, PSQL_QUERY
from field_to_table import field_to_table_map

app = Flask(__name__)

ARGS = _define_args()

# Connecting to mysql db
try:
    connection = mysql.connector.connect(host='localhost',
                                         database=ARGS.dbname,
                                         user=ARGS.username,
                                         password=ARGS.password)

    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("Your connected to database: ", record)

except Error as e:
    print("Error while connecting to MySQL", e)

# Connecting to postgressql db
CONN = psycopg2.connect("dbname = {0} user = {1} host=localhost password={2}"\
.format(ARGS.psqldbname, ARGS.psqlusername, ARGS.psqlpassword))

cur = CONN.cursor()

@app.route("/api/register", methods=["POST"])
def register():
    '''
    This api is used to register aswell as
    login users based on their request
    '''
    params = request.get_json()
    # Note email id should be unique for each user
    email_id = params.get("email_id", "")

    if "@" not in email_id or ".com" not in email_id:
        return (json.dumps({"message": "Please specify valid email_id"}))

    password = params.get("password", "")
    mode = params.get("mode", "")
    today = date.today()
    today = str(today)

    encoded_jwt = jwt.encode({'email': email_id}, password, algorithm='HS256')
    encoded_jwt = encoded_jwt.decode()

    sq_reg_query = SQL_QUERY.get("register_data", "")

    if mode=="register":
        sq_reg_query = sq_reg_query.format("access", encoded_jwt, email_id, today)
    else:
        result = authenticate(encoded_jwt, "access")
        if not result:
            return json.dumps("User {} doesn't exist please register first".format(email_id))
        sq_reg_query = sq_reg_query.format("auth", encoded_jwt, email_id, today)

    if mode=="register":
        resp = _validate_reg("access", sq_reg_query, encoded_jwt)
    else:
        resp = _validate_reg("auth", sq_reg_query, encoded_jwt)

    return resp


def _validate_reg(table, sq_reg_query, encoded_jwt):
    '''
    Validates if a user trying to register/login is
    already registered/loggedin
    '''
    try:
        cursor.execute(sq_reg_query)
    except mysql.connector.errors.IntegrityError:
        cursor.execute("ROLLBACK")
        connection.commit()
        if table =="auth":
            return (json.dumps({"message": "A user with the email id is already logged in"}))
        else:
            return (json.dumps({"message": \
                "A user with the email id already exists please generate its key"}))

    connection.commit()
    if table == "auth":
        return (json.dumps({"message": \
            "You are logged in Please use {} as key to access apis".format(encoded_jwt)}))
    else:
        return (json.dumps({"message": \
            "You are registered Please use {} as key to access apis".format(encoded_jwt)}))

def _get_sql_query(query, typ):
    '''
    Preapres both sql or psql queries
    '''
    if typ=="sql":
        sq_query = SQL_QUERY.get(query, "")
    elif typ=="psql":
        sq_query = PSQL_QUERY.get(query, "")

    return sq_query

@app.route("/api/load", methods=["POST"])
def load_data():
    '''
    This api is used to load user data to mysql
    '''
    params = request.get_json()
    key = params.get("key", "")

    if not key:
        return json.dumps("key cannot be empty")
    else:
        result = authenticate(key, "access")
        if not result:
            return json.dumps("User with this key doesn't exist")
        key = "'"+key+"'"

    name = params.get("name", "")
    name = "'"+name+"'" if name else "NULL"

    address = params.get("address", "")
    address = "'"+address+"'" if address else "NULL"

    phone_number = params.get("phone_number", "")
    phone_number = "'"+phone_number+"'" if phone_number else "NULL"

    age = params.get("age", "")
    age = "'"+age+"'" if age else "NULL"

    dob = params.get("dob", "")
    dob = "'"+dob+"'" if dob else "NULL"

    misc = params.get("misc", "")

    state = params.get("state", "")
    state = "'"+state+"'" if state else "NULL"

    city = params.get("city", "")
    city = "'"+city+"'" if city else "NULL"

    pin = params.get("pin", "")
    pin = "'"+pin+"'" if pin else "NULL"

    _misc = ""
    if misc:
        _misc = ""
        misc = json.loads(misc)
        for k, val in misc.items():
            _misc = _misc+k.replace(" ", "_")+":"+val.replace(" ", "_")+" "

        _misc = "'"+_misc+"'" if _misc else "NULL"
        sq_misc_query = _get_sql_query("load_data", "sql")

        sq_misc_query = sq_misc_query.format("Misc", key+","+ _misc)

        try:
            cursor.execute(sq_misc_query)
        except mysql.connector.errors.IntegrityError:
            return json.dumps({"message": "failure! duplicate key"})

    sq_load_query = _get_sql_query("load_data", "sql")

    sq_load_query = sq_load_query.format("profile", key+","+name+","+phone_number+","+age+","+dob)

    try:
        cursor.execute(sq_load_query)
    except mysql.connector.errors.IntegrityError:
        return json.dumps({"message": "failure! duplicate key"})

    sq_load_query = _get_sql_query("load_data", "sql")

    sq_load_query = sq_load_query.format("address", key+","+address+","+state+","+city+","+pin)
    cursor.execute(sq_load_query)

    connection.commit()

    return (json.dumps({"message": "loaded profile info for {}".format(name)}))

def authenticate(key, table):
    '''
    This makes sure if the user is autherised for
    an action or not.
    '''
    sq_auth_query = _get_sql_query("auth_query", "sql")
    sq_auth_query = sq_auth_query.format(table, key)

    cursor.execute(sq_auth_query)

    return cursor.fetchall()

@app.route("/api/filter", methods=["POST"])
def filter_user_data():
    '''
    This api is used to filter fields from the data
    that has been loaded, once filtered these data
    is replicated into postgressql.
    '''
    params = request.get_json()

    key = params.get("key", "")
    results = authenticate(key, "auth")
    if not results:
        results = authenticate(key, "access")
        if not results:
            return json.dumps("User with this key doesn't exist")
        else:
            return json.dumps("User Session expired for this user please regenerate key")

    filter_fields = params.get("filter_fields", "")
    age = params.get("age", "")
    city = params.get("city", "")
    state = params.get("state", "")
    pin = params.get("pin", "")
    name = params.get("name", "")

    where_clause = []
    relation = []
    filter_table = []
    if age and ":" in age:
        age = age.split(":")
        if age[0].lower()=="all":
            where_clause.append("age<'{}'".format(age[1]))
        else:
            where_clause.append("age>'{}'".format(age[0]))

        relation.append("profile.id")
        filter_table.append("profile")
        filter_fields = filter_fields+",age"
    elif age:
        where_clause = where_clause.append("age='{}'".format(age))
        relation.append("profile.id")
        filter_table.append("profile")
        filter_fields = filter_fields+",age"

    if city:
        where_clause.append("address.city='{}'".format(city))
        relation.append("address.id")
        filter_table.append("address")
        filter_fields = filter_fields+",city"

    if state:
        where_clause.append("address.state='{}'".format(state))
        relation.append("address.id")
        filter_table.append("address")
        filter_fields = filter_fields+",state"

    if pin:
        where_clause.append("address.pin='{}'".format(pin))
        relation.append("address.id")
        filter_table.append("address")
        filter_fields = filter_fields+",pin"

    if name:
        where_clause.append("profile.name='{}'".format(name))
        relation.append("profile.id")
        filter_table.append("profile")
        filter_fields = filter_fields+",name"

    if "misc" in filter_fields:
        relation.append("Misc.id")
        filter_table.append("Misc")

    where_clause = list(set(where_clause))
    filter_fields = list(set(filter_fields.split(",")))
    _filter_fields = filter_fields
    relation.extend(list(map(lambda x: field_to_table_map.get(x, "")+".id", filter_fields)))
    relation = list(set(relation))

    if len(where_clause)>1:
        where_clause = " and ".join(where_clause)
    elif where_clause:
        where_clause = where_clause[0]

    _relation = relation
    relation = "=".join(relation)
    if len(_relation)>1:
        where_clause = where_clause+" and " +relation

    filter_table.extend(relation.replace(".id=", ",")\
                            .replace(".id", "").split(","))

    filter_fields = ",".join(list(map(lambda x: field_to_table_map.get(x, "")\
                                                    +"."+x, filter_fields)))

    filter_table = list(set(filter_table))
    filter_table = ",".join(filter_table)

    if where_clause:
        sq_filter_query = _get_sql_query("filter_where_query", "sql")
        sq_filter_query = sq_filter_query.format(filter_fields, filter_table, where_clause)
    else:
        sq_filter_query = _get_sql_query("filter_query", "sql")
        sq_filter_query = sq_filter_query.format(filter_fields, filter_table)

    cursor.execute(sq_filter_query)

    results = cursor.fetchall()

    for records in results:
        mongo_data = {}
        for index,fields in enumerate(_filter_fields):
            if fields=="dob":
                mongo_data[fields] = str(records[index])
            elif fields == "misc":
                MISC = {}
                misc = records[index].strip().split(" ")
                for data in misc:
                    key, val = data.split(":")
                    MISC[key] = val
                mongo_data[fields] = MISC
            else:
                mongo_data[fields] = records[index]

        psql_insert_query = _get_sql_query("insert_data", "psql")
        psql_insert_query = psql_insert_query.format(json.dumps(mongo_data))

        try:
            cur.execute(psql_insert_query)
        except:
            return json.dumps("error while filtering data")

        CONN.commit()

    return json.dumps("{} data were filtered".format(len(results)))

@app.route("/api/fetch", methods=["POST"])
def fetch_user_data():
    '''
    This api is used to fetch the filtered data
    from postgressql db.
    '''
    params = request.get_json()

    key = params.get("key", "")
    results = authenticate(key, "auth")
    if not results:
        results = authenticate(key, "access")
        if not results:
            return json.dumps("User with this key doesn't exist")
        else:
            return json.dumps("User Session expired for this user please regenerate key")

    filter_fields = params.get("filter_fields", "")
    age = params.get("age", "")
    city = params.get("city", "")
    state = params.get("state", "")
    pin = params.get("pin", "")
    name = params.get("name", "")

    where_clause = []
    if age and ":" in age:
        age = age.split(":")
        if age[0].lower()=="all":
            where_clause.append("(data->>'age')::int < {}".format(age[1]))
        else:
            where_clause.append("(data->>'age')::int > {}".format(age[0]))

    elif age:
        where_clause = where_clause.append("(data->>'age')::int = {}".format(age))

    if city:
        where_clause.append("data->>'city' = '{}'".format(city))

    if state:
        where_clause.append("data->>'state' = '{}'".format(state))

    if pin:
        where_clause.append("data->>'pin' = '{}'".format(pin))

    if name:
        where_clause.append("data->>'name' = '{}'".format(name))

    if len(where_clause)>1:
        where_clause = " and ".join(where_clause)
    elif where_clause:
        where_clause = where_clause[0]

    filter_fields = filter_fields.strip().split(",")
    _filter_fields = filter_fields

    filter_fields = list(map(lambda x: "data->>'{0}' as {1}".format(x, x), filter_fields))

    filter_fields = ",".join(filter_fields)

    if where_clause:
        psql_filter_query = _get_sql_query("filter_where_query", "psql")
        psql_filter_query = psql_filter_query.format(filter_fields, where_clause)
    else:
        psql_filter_query = _get_sql_query("filter_query", "psql")
        psql_filter_query = psql_filter_query.format(filter_fields)

    try:
        cur.execute(psql_filter_query)
    except:
        return json.dumps("error while filtering data")

    result = cur.fetchall()

    final_resp = []
    for records in result:
        mongo_data = {}
        for index,fields in enumerate(_filter_fields):
            if fields == "misc":
                MISC = json.loads(records[index])
                mongo_data[fields] = MISC
            else:
                mongo_data[fields] = records[index]

        final_resp.append(mongo_data)

    return json.dumps({"result": final_resp})

if __name__=="__main__":
    app.run(debug=True, host=ARGS.ip, port=ARGS.port)
