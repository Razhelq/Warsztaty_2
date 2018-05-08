"""
CREATE TABLE "Users" (id serial,
email varchar(255) unique,
username varchar(255),
hashed_password varchar(80),
PRIMARY KEY(id));
"""


from models import User
from psycopg2 import connect
import json
import argparse


def main():
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

    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        help="nazwa uzytkownika",
                        required=True)
    parser.add_argument("-p", "--password",
                        help="haslo uzytkownika",
                        required=True)
    parser.add_argument("-l", "--list",
                        help="wypisuje komunikaty dla uzytkownika",
                        action="store_true")
    parser.add_argument("-t", "--to", help="odbiorca wiadomosci")
    parser.add_argument("-s", "--send",
                        help="wysyla komunikat",
                        action="store_true")
    parser.add_argument("-m", "--email",
                        help="email uzytkownika")
    parser.add_argument("-e", "--edit",
                        help="login	użytkownika	do	modyfikacji")
    parser.add_argument("-d", "--delete",
                        help="login	użytkownika	do	usunięcia")


    args = parser.parse_args()

    user = args.username
    password = args.password
    email = args.email
    edit = args.edit
    delete = args.delete
    listing_mode = args.list
    sending_mode = args.send
    recipient = args.to
    print(User)
    print("""
        uzytkownik: {}
        password: {}
        list mode: {}
        send mode: {}
        recipient: {}
    """.format(user, password, listing_mode, sending_mode, recipient))


    if nalezy_stworzyc(user, password, email, edit, delete):
        u = User.load_user_by_name(cursor, user)
        if u:
            print("Taki użytkownik już istnieje")
        else:
            stworz_uzytkownika(cursor, user, password, email)


def nalezy_stworzyc(user, password, email, edit, delete):
    return user and password and email and not edit and not delete


def stworz_uzytkownika(cursor, user, password, email):
    nu = User()
    nu.username = user
    nu.username = password
    nu.username = email
    nu.save_to_db(cursor)


if __name__ == '__main__':
    main()
