from clcrypto import password_hash, check_password


class User(object):
    __id = None
    username = None
    __hashed_password = None
    email = None

    def __init__(self):
        self.__id = -1
        self.username = ""
        self.email = ""
        self.__hashed_password = ""

    @property
    def id(self):
        return self.__id

    @property
    def hashed_password(self):
        return self.__hashed_password

    def check_passwd(self, password):
        return check_password(password, self.hashed_password)

    def set_password(self, password, salt=None):
        self.__hashed_password = password_hash(password, salt)

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO users(username, email, hashed_password)
            VALUES(%s, %s, %s) RETURNING id"""
            values = (self.username, self.email, self.hashed_password)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE users SET username=%s, email=%s, hashed_password=%s
            WHERE id=%s"""
            values = (self.username, self.email, self.hashed_password, self.id)
            cursor.execute(sql, values)
            return True

    @staticmethod
    def load_user_by_name(cursor, user_name):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE username=%s"
        cursor.execute(sql, (user_name, ))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_user_by_id(cursor, user_id):
        sql = "SELECT id, username, email, hashed_password FROM users WHERE id=%s"
        cursor.execute(sql, (user_id, ))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_user = User()
            loaded_user.__id = data[0]
            loaded_user.username = data[1]
            loaded_user.email = data[2]
            loaded_user.__hashed_password = data[3]
            return loaded_user
        else:
            return None

    @staticmethod
    def load_all_users(cursor):
        sql = "SELECT id, username, email, hashed_password FROM Users"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_user = User()
            loaded_user.__id = row[0]
            loaded_user.username = row[1]
            loaded_user.email = row[2]
            loaded_user.__hashed_password = row[3]
            ret.append(loaded_user)
        return ret

    def delete(self, cursor):
        sql = "DELETE FROM users WHERE id=%s"
        cursor.execute(sql, (self.__id, ))
        self.__id = -1
        return True


class Message(object):
    __id = None
    from_id = None
    to_id = None
    text = None
    creation_date = None

    def __init__(self):
        self.__id = -1
        self.from_id = -1
        self.to_id = -1
        self.text = ''
        self.creation_date = 0

    @property
    def id(self):
        return self.__id

    @staticmethod
    def load_message_by_id(cursor, id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM users WHERE id=%s"
        cursor.execute(sql, (id,))  # (user_id, ) - bo tworzymy krotkę
        data = cursor.fetchone()
        if data:
            loaded_message = Message()
            loaded_message.__id = data[0]
            loaded_message.from_id = data[1]
            loaded_message.to_id = data[2]
            loaded_message.text = data[3]
            loaded_message.creation_date = data[4]
            return loaded_message
        else:
            return None

    @staticmethod
    def load_all_messages_for_user(cursor, to_id):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM messages WHERE to_id=%s"
        cursor.execute(sql, (to_id, ))
        ret = []
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.creation_date = row[4]
            ret.append(loaded_user)
        return ret

    @staticmethod
    def load_all_messages(cursor):
        sql = "SELECT id, from_id, to_id, text, creation_date FROM Users"
        ret = []
        cursor.execute(sql)
        for row in cursor.fetchall():
            loaded_message = Message()
            loaded_message.__id = row[0]
            loaded_message.from_id = row[1]
            loaded_message.to_id = row[2]
            loaded_message.text = row[3]
            loaded_message.creation_date = row[4]
            ret.append(loaded_user)
        return ret

    def save_to_db(self, cursor):
        if self.__id == -1:
            # saving new instance using prepared statements
            sql = """INSERT INTO messages(from_id, to_id, text, creation_date)
            VALUES(%s, %s, %s, %s) RETURNING id"""
            values = (self.from_id, self.to_id, self.text, self.creation_date)
            cursor.execute(sql, values)
            self.__id = cursor.fetchone()[0]  # albo cursor.fetchone()['id']
            return True
        else:
            sql = """UPDATE messages SET from_id=%s, to_id=%s, text=%s, creation_date=%s
            WHERE id=%s"""
            values = (self.from_id, self.to_id, self.text, self.creation_date)
            cursor.execute(sql, values)
            return True
