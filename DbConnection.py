#! -*- coding: utf-8 -*-

import logging
import psycopg2
import sys
import traceback

from settings import *


class DbConnection:
    """class containing methods to work with DB"""

    def __init__(self):
        """Initializing connection on class creation"""
        try:
            self.db_connection = psycopg2.connect(dbname=DB_NAME,
                                                  host=DB_HOSTNAME,
                                                  port=DB_PORT,
                                                  user=DB_USERNAME,
                                                  password=DB_PASSWORD)
        except psycopg2.OperationalError:
            logging.error("Couldn't connect to database '{db_name}' located on {hostname}:{port}".format(
                hostname=DB_HOSTNAME,
                port=DB_PORT,
                db_name=DB_NAME))
            exit(1)

    def execute_sql_statement(self, statement):
        """Executes SQL-statement and return results

        :param statement: sql-query statement
        :return: result of SQL-statement execution
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(statement)
            return cursor.fetchall()
        except Exception:
            logging.error("Something went wrong when tried to execute statement")
            logging.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
            logging.error("".join(traceback.format_tb(sys.exc_info()[2])))
            exit(1)
        finally:
            cursor.close()
            self.close_connection()

    def close_connection(self):
        """Closes active connection to DB"""
        try:
            self.db_connection.close()
        except Exception:
            logging.error("Something went wrong when tried to close connection")
            logging.error("{}: {}".format(sys.exc_info()[0], sys.exc_info()[1]))
            logging.error("".join(traceback.format_tb(sys.exc_info()[2])))
            exit(1)


if __name__ == "__main__":
    conn = DbConnection()
    res = conn.execute_sql_statement("select * from test")
    print(res)
    conn.close_connection()
