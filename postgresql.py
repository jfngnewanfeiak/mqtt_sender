import psycopg2
import os
class POSTGRESQL:
    def __init__(self) -> None:
        self._host = ''
        self._user = ''
        self._password = os.environ.get('MYPASSWORD')
        self._database = ''
        self._db_connection = None
    

    def setting_connection(self,host:str,user:str,database:str):
        self._host = host
        self._user = user
        self._database = database
    
    def connect_DB(self):
        self._db_connection = psycopg2.connect(
            host=self._host,
            user=self._user,
            password=self._password,
            database=self._database 
        )
        print("connect DB {}".format(self._database))