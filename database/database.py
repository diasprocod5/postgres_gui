import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('db_name')

class Database:

    __instance = None
    __connection = None
    __cursor = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def connect(self, user, password):
        try:
            self.__connection = psycopg2.connect(
                user=user,
                password=password,
                host=db_host,
                port=db_port,
                dbname=db_name
            )
            return True
        except OperationalError as e:
            print(f'Ошибка подключения к БД: {e}')
            return False

    def disconnect(self):
        self.__connection.close()

    def _open_cursor(self):
        if self.__connection:
            self.__cursor = self.__connection.cursor()
    def _close_cursor(self):
        self.__cursor.close()

    def execute_query(self, query, params=None, commit_on_success=False):
        try:
            self._open_cursor()
            self.__cursor.execute(query, params or ())
            if self.__cursor.description:
                data = self.__cursor.fetchall()
                headers = [desc[0] for desc in self.__cursor.description]
                if commit_on_success:
                    self.__connection.commit()
                return data, headers
            else:
                self.__connection.commit()
                return True
        except Exception as e:
            self.__connection.rollback()
            return False
        finally:
            self._close_cursor()




