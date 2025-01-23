import sqlite3
from venv import logger

class Database:
    def __init__(self, path_to_db='main.db'):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None,
                fetch_one=False, fetch_all=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetch_one:
            data = cursor.fetchone()
        if fetch_all:
            data = cursor.fetchall()
        connection.close()
        return data

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])

    def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                telegram_id BIGINT NOT NULL UNIQUE
                )
        """
        self.execute(sql, commit=True)

    def select_one_users(self, telegram_id):
        sql = """
            SELECT * FROM users WHERE telegram_id = ?
        """
        return self.execute(sql, (telegram_id,), fetch_one=True)

    def select_all_users(self):
        sql = "SELECT * FROM users"
        return  self.execute(sql, fetch_all=True)
    def select_count_users(self):
        sql = "SELECT count(*) FROM users"
        return self.execute(sql, fetch_one=True)

    def add_users(self, fullname:str, telegram_id: int):
        sql = "INSERT INTO users (fullname, telegram_id) VALUES (?, ?)"
        return self.execute(sql, (fullname, telegram_id), commit=True)

    def updete_users(self, old_tg_id, new_tg_id):
        sql = """UPDATE users SET telegram_id = ? WHERE telegram_id = ?"""
        return self.execute(sql, (new_tg_id, old_tg_id), commit=True)



    def create_savollar(self):
        sql = """
            CREATE TABLE IF NOT EXISTS tests (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                test_nomi VARCHAR(255) NOT NULL,
                test JSONB NOT NULL
                )
        """
        self.execute(sql, commit=True)

    def add_savollar(self, telegram_id: int, test_nomi, test):
        sql = """INSERT INTO tests (telegram_id,test_nomi,test) VALUES (?, ?, ?)"""
        self.execute(sql, (telegram_id, test_nomi, test), commit=True)

    def search_tests(self, telegram_id):
        sql = """SELECT test_nomi FROM tests WHERE telegram_id=?"""
        return self.execute(sql, (telegram_id,), fetch_all=True)

    def select_tests(self,telegram_id, test_nomi):
        sql = """SELECT test FROM tests WHERE telegram_id=? and test_nomi=?"""
        return self.execute(sql, (telegram_id, test_nomi), fetch_one=True)
    def delete_tests(self,telegram_id, test_nomi):
        sql = """DELETE FROM tests WHERE telegram_id=? and test_nomi=?"""
        return self.execute(sql, (telegram_id, test_nomi), commit=True)
    def select_all_tests(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  telegram_id,test_nomi FROM tests
            LIMIT ? OFFSET ?
        """
        return self.execute(sql, (page_size, offset), fetch_all=True)
    def test_count(self):
        sql = """SELECT count(*) FROM tests"""
        return self.execute(sql, fetch_one=True)
    def test_count1(self, db_id):
        sql = """SELECT count(*) FROM tests where telegram_id = ?"""
        return self.execute(sql,(db_id,), fetch_one=True)
    def select_all_tests1(self, telegram_id, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  telegram_id, test_nomi FROM tests
            where telegram_id=?
            LIMIT ? OFFSET ?
        """
        return self.execute(sql, (telegram_id, page_size,offset), fetch_all=True)