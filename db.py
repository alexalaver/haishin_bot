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
            self.cursor.execute("INSERT INTO orders(id, option, name, tel) VALUES(?, ?, ?, ?)", (id, option, name, tel,))
            self.connect.commit()

    def add_option(self, id, option):
        with self.connect:
            self.cursor.execute("INSERT INTO cashe(id, option) VALUES(?, ?)", (id, option))

    def add_name_cashe(self, id, us_text):
        with self.connect:
            self.cursor.execute("UPDATE cashe SET us_text = ? WHERE id = ?", (us_text, id,))
            self.connect.commit()

    def add_tel_cashe(self, id, tel):
        with self.connect:
            self.cursor.execute("UPDATE cashe SET tel = ? WHERE id = ?", (tel, id,))
            self.connect.commit()

    def set_cashe(self, id):
        with self.connect:
            return self.cursor.execute("SELECT us_text, option, tel FROM cashe WHERE id = ?", (id,)).fetchone()

    def delete_cashe(self, id):
        with self.connect:
            self.cursor.execute("DELETE FROM cashe WHERE id = ?", (id,))
            self.connect.commit()

    def delete_all_cashe(self):
        with self.connect:
            self.cursor.execute("DELETE FROM cashe")
            self.connect.commit()

    def delete_all_orders(self):
        with self.connect:
            self.cursor.execute("DELETE FROM orders")
            self.connect.commit()

    def check_adm(self, id):
        with self.connect:
            result = self.cursor.execute("SELECT lvl FROM users WHERE id=?", (id,)).fetchone()
            if result[0] == 0:
                return False
            elif result[0] == 1:
                return True

    def get_adm(self, id):
        with self.connect:
            result = self.cursor.execute("SELECT lvl FROM users WHERE id=?", (id,)).fetchone()[0]
            if result == 0:
                self.cursor.execute("UPDATE users SET lvl = 1 WHERE id=?", (id,))
                self.connect.commit()
            else:
                return False

    def del_adm(self, id):
        with self.connect:
            result = self.cursor.execute("SELECT lvl FROM users WHERE id=?", (id,)).fetchone()[0]
            if result == 1:
                self.cursor.execute("UPDATE users SET lvl = 0 WHERE id=?", (id,))
                self.connect.commit()
            else:
                return False




