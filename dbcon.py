import sqlite3

class Database():
    def __init__(self):
        self.conn = sqlite3.connect('database')
        self.cursor = self.conn.cursor()

    def user_exist(self, user_id):
        ex = self.conn.execute(f'SELECT * FROM users WHERE user_id = {user_id}').fetchone()
        print(ex)
        return 1 if bool(ex) else 0

    def get_user(self, id):
        return self.cursor.execute(f'SELECT * FROM users WHERE user_id = {id}').fetchone()

    def get_connect_sections(self, page_id):
        return self.cursor.execute(f'SELECT * FROM sections WHERE connect_with_page == {page_id}').fetchall()

    def get_section(self, page_id):
        return self.cursor.execute(f'SELECT * FROM sections WHERE id == {page_id}').fetchone()