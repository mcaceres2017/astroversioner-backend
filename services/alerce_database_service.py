import pandas as pd
import psycopg2
from psycopg2 import pool
import requests


# this class connects to the postgresql database of ALeRCE for now.
class AlerceDatabaseService:
    connection_pool = None

    @staticmethod
    def initialize_connection_pool():
        """
        Initialize DatabaseClient object.
        Connects to the database using parameters from a JSON file.
        """

        url = "https://raw.githubusercontent.com/alercebroker/usecases/master/alercereaduser_v4.json"
        params = requests.get(url).json()["params"]
        pool_min_connections = 1
        pool_max_connections = 10
        print("[INFO] creating a pool connection to ALeRCE Postgresql")

        if AlerceDatabaseService.connection_pool is None:
            try:
                AlerceDatabaseService.connection_pool = (
                    psycopg2.pool.SimpleConnectionPool(
                        pool_min_connections,
                        pool_max_connections,
                        dbname=params["dbname"],
                        user=params["user"],
                        host=params["host"],
                        password=params["password"],
                    )
                )
            except BaseException as e:
                print(f"[ERROR] when creating a pool connection {e}")

            print("[INFO] Pool created!")
            print(type(AlerceDatabaseService.connection_pool))

    @staticmethod
    def execute_query(sql_query, params):
        """
        Executes a SQL query on the connected database.

        Args:
            sql_query (str): SQL query to be executed.

        Returns:
            pd.DataFrame: Dataframe containing the result of the query.
        """
        query_dataframe = pd.DataFrame()

        try:
            print("[INFO] get pool connection to ALeRCE")
            print(type(AlerceDatabaseService.connection_pool))
            conn = AlerceDatabaseService.connection_pool.getconn()

            print("[INFO] making query to ALeRCE")
            query_dataframe = pd.read_sql_query(sql_query, conn, params=params)
            query_dataframe = query_dataframe.loc[
                :, ~query_dataframe.columns.duplicated()
            ].copy()
            print("[INFO] query successful!")
        except BaseException as e:
            print(f"[ERROR] {e}")
        finally:
            print("[INFO] closing connection to ALeRCE")
            AlerceDatabaseService.connection_pool.putconn(conn)
            return query_dataframe

    @staticmethod
    def close_connection_pool():
        """
        Cierra el pool de conexiones a la base de datos.
        """
        if AlerceDatabaseService.connection_pool is not None:
            AlerceDatabaseService.connection_pool.closeall()
            AlerceDatabaseService.connection_pool = None
