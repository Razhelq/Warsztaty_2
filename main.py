"""
CREATE TABLE users (id serial,
email varchar(255) unique,
username varchar(255),
hashed_password varchar(80),
PRIMARY KEY(id)
);

CREATE TABLE messages (id serial,
from_id int,
to_id int,
text text,
creation_date timestamp,
PRIMARY KEY(id),
FOREIGN KEY(from_id) REFERENCES users(id)
FOREIGN KEY(to_id) REFERENCES users(id)
);

"""


from models import User, Message
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


    cnx.autocommit = True
    cursor = cnx.cursor()


    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username",
                        help="nazwa uzytkownika",
                        required=True)
    parser.add_argument("-p", "--password",
                        help="haslo uzytkownika",
                        required=True)
    parser.add_argument("-l", "--list",
                        help="żądanie wylistowania wszystkich użytkowników",
                        action="store_true")
    parser.add_argument("-ll", "--llist",
                        help="żądanie wylistowania wszystkich komunikatów",
                        action="store_true")
    parser.add_argument("-t", "--to",
                        help="odbiorca wiadomosci")
    parser.add_argument("-s", "--send",
                        help="wysyla komunikat",
                        action="store_true")
    parser.add_argument("-m", "--email",
                        help="email uzytkownika")
    parser.add_argument("-e", "--edit",
                        help="login	użytkownika	do	modyfikacji")
    parser.add_argument("-d", "--delete",
                        help="login	użytkownika	do	usunięcia")
    parser.add_argument("-n", "--new_pass",
                        help="nowe haslo uzytkownika")


    args = parser.parse_args()

    user = args.username
    password = args.password
    email = args.email
    edit = args.edit
    delete = args.delete
    listing_mode = args.list
    list = args.llist
    sending_mode = args.send
    recipient = args.to
    new_passwd = args.new_pass
    # print(User)
    # print("""
    #     uzytkownik: {}
    #     password: {}
    #     list mode: {}
    #     send mode: {}
    #     recipient: {}
    # """.format(user, password, listing_mode, sending_mode, recipient))


    if check_if_create_user(user, password, email, edit, delete):
        u = User.load_user_by_name(cursor, user)
        if u:
            print("Taki użytkownik już istnieje")
        else:
            if len(password) < 8:
                print("Hasło musi miec minimum 8 znaków")
            create_user(cursor, user, password, email)
            print("Uzytkownik stworzony")

    elif check_if_change_passwd(user, password, edit, new_passwd):
        u = User.load_user_by_name(cursor, edit)
        if u:
            if u.check_passwd(password):
                if len(password) < 8:
                    print("Hasło musi miec minimum 8 znaków")
                change_passwd(cursor, edit, new_passwd)
            else:
                print("Złe hasło")
        else:
            print("Taki uzytkownik nie istnieje")

    elif check_if_del_user(user, password, delete):
        u = User.load_user_by_name(cursor, delete)
        if u:
            if u.check_passwd(password):
                del_user(cursor, delete)
            else:
                print("Złę hasło")
        else:
            print("Taki uzytkownik nie istnieje")

    elif check_if_all_users(user, password, listing_mode):
        all_users(cursor)

    elif check_if_all_messages(user, password, list):
        u = User.load_user_by_name(cursor, user)
        if u:
            m = message()
            m.all_messages(cursor, list)
        else:
            print("Taki uzytkownik nie istnieje")

    elif check_if_message_by_id(user, password, msg_id):
        return user and password and mdg_id

    ### msgs



    else:
        parser.print_help()


def check_if_create_user(user, password, email, edit, delete):
    return user and password and email and not edit and not delete


def create_user(cursor, user, password, email):
    nu = User()
    nu.username = user
    nu.set_password(password)
    nu.email = email
    nu.save_to_db(cursor)


def check_if_change_passwd(user, password, edit, new_passwd):
    return user and password and edit and new_passwd


def change_passwd(cursor, edit, new_passwd):
    u = User.load_user_by_name(cursor, edit)
    u.set_password(new_passwd)
    u.save_to_db(cursor)


def check_if_del_user(user, password, delete):
    return user and password and delete


def del_user(cursor, delete):
    u = User.load_user_by_name(cursor, delete)
    u.delete(cursor)


def check_if_all_users(user, password, listing_mode):
    return user and password and listing_mode


def all_users(cursor):
    u = User()
    list_of_users = u.load_all_users(cursor)
    for x in list_of_users:
        print("ID - ", x.id, "Username - :", x.username, "Email - ", x.email)


def check_if_all_messages(user, password, list):
    return user and password and list


def all_messages(cursor, to_id):
    list_of_messages = u.load_all_messages(to_id):
    for x in list_of_messages:
        print("ID wiadomości - ", x.id, "Od usera - ", x.from_id, "Do usera ", x.to_id, "Treść wiadomości - ", x.text,
              "creation date - ", x.creation_date)





if __name__ == '__main__':
    main()
