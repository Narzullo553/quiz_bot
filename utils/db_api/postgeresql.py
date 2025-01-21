
import asyncpg
from typing import Union
from asyncpg import Connection
from asyncpg.pool import Pool
from data import config
class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None
    async def create(self):
        self.pool = await asyncpg.create_pool(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASS,
            database=config.DB_NAME
        )
    async def execute(self, sql_command, *args,
                      fetch: bool=False,
                      fetchrows: bool=False,
                      execute: bool=False,
                      fetchvall: bool=False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            if fetch:
                result = await connection.fetch(sql_command, *args)
            elif fetchrows:
                result = await connection.fetchrow(sql_command, *args)
            elif fetchvall:
                result = await connection.fetchval(sql_command, *args)
            elif execute:
                result = await connection.execute(sql_command, *args)
            return result

    @staticmethod
    def format_kwargs(sql_command, parameters: dict):
        sql_command += " AND ".join([f"{key}='{value}'" for key, value in parameters.items()])
        return sql_command

    async def create_table_users(self):
        sql = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                fullname VARCHAR(255) NOT NULL,
                telegram_id BIGINT NOT NULL UNIQUE
                )
        """
        return await self.execute(sql, execute=True)

    async def select_one_users(self, telegram_id):
        sql = """
            SELECT * FROM users WHERE telegram_id = $1
        """
        return await self.execute(sql, telegram_id, fetchrows=True)

    async def select_all_users(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, fetch=True)
    async def select_count_users(self):
        sql = "SELECT count(*) FROM users"
        return await self.execute(sql, fetchvall=True)

    async def add_users(self, fullname:str, telegram_id: int):
        sql = ("INSERT INTO users (fullname, telegram_id) VALUES ($1, $2)")
        return await self.execute(sql, fullname, telegram_id, execute=True)



    async def create_savollar(self):
        sql = """
            CREATE TABLE IF NOT EXISTS tests (
                id SERIAL PRIMARY KEY,
                telegram_id BIGINT NOT NULL,
                test_nomi VARCHAR(255) NOT NULL,
                test JSONB NOT NULL
                )
        """
        await self.execute(sql, execute=True)

    async def add_savollar(self, telegram_id: int, test_nomi, test):
        sql = """INSERT INTO tests (telegram_id,test_nomi,test) VALUES ($1, $2, $3)"""
        await self.execute(sql, telegram_id, test_nomi, test, execute=True)

    async def search_tests(self, telegram_id):
        sql = """SELECT test_nomi FROM tests WHERE telegram_id=$1"""
        return await self.execute(sql, telegram_id, fetch=True)

    async def select_tests(self,telegram_id, test_nomi):
        sql = """SELECT test FROM tests WHERE telegram_id=$1 and test_nomi=$2"""
        return await self.execute(sql, telegram_id, test_nomi, fetchrows=True)
    async def delete_tests(self,telegram_id, test_nomi):
        sql = """DELETE FROM tests WHERE telegram_id=$1 and test_nomi=$2"""
        return await self.execute(sql, telegram_id, test_nomi, execute=True)
    async def select_all_tests(self, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  telegram_id,test_nomi FROM tests
            LIMIT $1 OFFSET $2
        """
        return await self.execute(sql, page_size, offset, fetch=True)

    async def select_all_tests1(self, telegram_id, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size
        sql = """
            SELECT  telegram_id,test_nomi FROM tests
            where telegram_id=$3
            LIMIT $1 OFFSET $2
        """
        return await self.execute(sql, page_size, offset,telegram_id, fetch=True)
    async def test_count(self):
        sql = """SELECT count(*) FROM tests"""
        return await self.execute(sql, fetchvall=True)
    async def test_count1(self, db_id):
        sql = """SELECT count(*) FROM tests where telegram_id=$1"""
        return await self.execute(sql,db_id, fetchvall=True)
