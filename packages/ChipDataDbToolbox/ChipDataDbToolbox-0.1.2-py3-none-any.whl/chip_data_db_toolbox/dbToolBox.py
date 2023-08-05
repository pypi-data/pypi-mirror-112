import sqlalchemy
import os
import re


class DBWrapper:
    def __init__(self, config, autocommit=True):
        """
        Expects a config with db connection strings. Use the self.connect() method to establish the connection.

        If autocommit is set to False then you need to
        begin a transaction and commit it at the end. Something like:
            transaction = DBWrapperObject.connection.begin()
            DBWrapperObject.execute("SomeSQLQuery")
            transaction.commit()

        If autocommit is set to True, just use DBWrapperObject.connection.execute("SomeSQL")

        If you use it in pandas just pass the DBWrapperObject.connection to pandas.
        """
        self.__autocommit = autocommit
        self.__config = config

        self.__db_connection_string = f"postgresql+psycopg2://{config['user_name']}:{config['password']}@{config['host_name']}:{config.get('port', 5432)}/{config['database_name']}"
        self.__engine = sqlalchemy.create_engine(self.__db_connection_string)

        self.__connection = None
        # self.__cursor = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        print(
            "Attempting to close connection after DBWrapper object is removed by the garbage collector."
        )
        self.close()

    @property
    def engine(self):
        return self.__engine

    @property
    def autocommit(self):
        return self.__autocommit

    @autocommit.setter
    def autocommit(self, flag):
        self.__autocommit = flag

    @property
    def config(self) -> dict:
        return self.__config

    @config.setter
    def config(self, config):
        self.__config = config

    @property
    def connection(self):
        return self.__connection

    def connect(self):
        self.__connection = self.__engine.connect().execution_options(
            autocommit=self.__autocommit
        )
        return self

    def close(self):
        try:
            self.__connection.close()
            print("Connection closed.")
        except Exception:
            print("Connection couldn't be closed on DBWrapper object cleanup.")
            pass

    def commit(self):
        self.__connection.commit()

    def rollback(self):
        self.__connection.rollback()


class SQLFilesHandler:
    def __init__(self, file_path):
        """
        Give the path to a sql file and read it in. Returns a
        file_string property where you can retrieve the full string
        or a queries_list property that you can retrieve the sql queries
        parsed. If you have 1 sql query inside the file, it returns a list of 1 element,
        otherwise it splits by semicolon (;).
        """
        self.__file_path = file_path
        self.__file_string = ""
        self.__queries_list = []

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, file_path):
        self.__file_path = file_path

    @property
    def file_string(self):
        return self.__file_string

    @property
    def queries_list(self):
        return self.__queries_list

    def read_file(self):
        with open(self.__file_path, "r", encoding="utf-8") as f:
            self.__file_string = f.read()
            self.__file_string = re.sub(" +", " ", self.__file_string)

            self.__queries_list = self.__file_string.split(";")
            for i in range(len(self.__queries_list)):
                self.__queries_list[i] = self.__queries_list[i].replace("\n", " ")
            self.__queries_list.pop()


def get_files_in_directory(files_path):
    """
    Just an utility function to get all files in the directory.
    """
    files = os.listdir(files_path)
    if len(files) > 0:
        return [f"{os.path.abspath(files_path)}/{file}" for file in files]
    else:
        print(f"No files have been found in directory {files_path}.")
        return []
