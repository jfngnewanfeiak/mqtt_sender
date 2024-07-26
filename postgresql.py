import psycopg2
import os
class POSTGRESQL:
    def __init__(self) -> None:
        self._host = ''
        self._user = ''
        self._password = 'password'
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
    
    def exec_update(self,query:str):
        with self._db_connection:
            with self._db_connection.cursor() as cursor:
                cursor.execute(query=query)
            self._db_connection.commit()
        cursor.close()
    
    def exec_select(self,query:str):
        retV = None
        with self._db_connection:
            with self._db_connection.cursor() as cursor:
                cursor.execute(query=query)
                retV = cursor.fetchall()
            self._db_connection.commit()
        cursor.close()
        return retV
    

if __name__ == "__main__":
    # インスタンス作成
    DB = POSTGRESQL()
    # DBに接続するための設定
    DB.setting_connection(host='10.77.114.51',user='postgres',database='mytable')
    # DBに接続
    DB.connect_DB()
    # select実行(以下はdata_bridgeというテーブルから全ての情報を引き出す)
    a=DB.exec_select('select * from data_bridge')
    print(a)
    # update実行 (data_bridgeテーブルのvalueというデータがTrueならFalseに書き換える)
    DB.exec_update("UPDATE data_bridge SET value = 'False' where value='True'")
    a=DB.exec_select('select * from data_bridge')
    print(a)

