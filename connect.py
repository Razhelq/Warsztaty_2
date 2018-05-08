from psycopg2 import connect
import json

config_path = "db.json"

def connection(config_file):
    cfg_string = open(config_file).read()
    cfg_json = json.loads(cfg_string)
    return connect(user=cfg_json["username"],
                   password=cfg_json["passwd"],
                   host=cfg_json["hostname"],
                   database=cfg_json["db_name"])

try:
    cnx = connection(config_path)
    print("Połączono z bazą")
except Exception as e:
    print("Niepowodzenie połączenia:", e)
    exit()


cursor = cnx.cursor()