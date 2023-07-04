import sqlite3

class Data:
    def __init__(self, dataname):
        self.connect = sqlite3.connect(dataname)
        self.cursor = self.connect.cursor()


    def add_user(self, id, first_name, username):
        with self.connect:
            self.cursor.execute("INSERT INTO users(id, first_name, username) VALUES(?, ?, ?)", (id, first_name, username,))
            self.connect.commit()

    def check_user(self, id):
        with self.connect:
            result = self.cursor.execute("SELECT id FROM users WHERE id = ?", (id,)).fetchall()
            return bool(len(result))

    def add_message(self, id, option, name, tel):
        with self.connect:
            self.connect.execute("INSERT INTO orders(id, option, name, tel) VALUES(?, ?, ?, ?)", (id, option, name, tel,))
            self.connect.commit()

    def add_option(self, id, option):
        with self.connect:
            self.connect.execute("INSERT INTO cashe(id, option) VALUES(?, ?)", (id, option))

    def add_name_cashe(self, id, us_text):
        with self.connect:
            self.connect.execute("UPDATE cashe SET us_text = ? WHERE id = ?", (us_text, id,))
            self.connect.commit()

    def set_cashe(self, id):
        with self.connect:
            return self.connect.execute("SELECT us_text, option FROM cashe WHERE id = ?", (id,)).fetchone()

    def delete_cashe(self, id):
        with self.connect:
            self.connect.execute("DELETE FROM cashe WHERE id = ?", (id,))
            self.connect.commit()