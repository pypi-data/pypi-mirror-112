
import json
import numbers
import syslog

from time import sleep

from pyqldb.driver.qldb_driver import QldbDriver
from amazon.ion.json_encoder import IonToJSONEncoder

class QLDBDriver:
    def __init__(self, ledger):
        self.qldb_driver = QldbDriver(ledger_name = ledger)
        self.TABLE_CREATION_POLL_PERIOD_SEC = 2
    
    def to_collection(self, cursor):
        collection = []
        
        for row in cursor:
            json_string = json.dumps(row, cls=IonToJSONEncoder)
            collection.append(json.loads(json_string))

        return collection


    def execute(self, transaction_executor, statement):
        cursor = transaction_executor.execute_statement(statement)
        
        return cursor


    def create_table(self, table_name, primary_key = None):
        statement = f"CREATE TABLE {table_name}"
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))

        if primary_key is not None:
            sleep(self.TABLE_CREATION_POLL_PERIOD_SEC)
            statement = f"CREATE INDEX ON {table_name}({primary_key})"
            self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def drop_table(self, table_name):
        statement = f"DROP TABLE {table_name}"
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def table_exists(self, table_name):
        return table_name in self.list_tables()


    def add_attribute(self, table_name, identifier, attribute_name, value = None):
        if not self.table_exists(table_name):
            raise Exception("Table not found!")

        if isinstance(value, str):
            default_value = f"'{value}'"
        elif isinstance(value, numbers.Number):
            default_value = f"{value}"
        elif value is None:
            default_value = "null"

        statement = f"SELECT {identifier} FROM {table_name}"
        
        ids_tmp = self.query(statement)
        ids = []

        for id_tmp in ids_tmp:
            ids.append(id_tmp[identifier])

        step = 40
        
        while len(ids) > 0:
            statement = f"FROM {table_name} WHERE {identifier} IN {tuple(ids[:step])} SET {attribute_name} = {default_value}"
            syslog.syslog(statement)

            self.execute_statement(statement)
            del ids[:step]


    def remove_attribute(self, table_name, identifier, attribute_name):
        if not self.table_exists(table_name):
            raise Exception("Table not found!")

        statement = f"SELECT {identifier} FROM {table_name}"
        
        ids = self.query(statement)

        for id in ids:
            statement = f"FROM {table_name} WHERE {identifier} = {id[identifier]} REMOVE {attribute_name}"

            try:
                self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))
            except:
                pass


    def list_tables(self):
        collection = []

        for table in self.qldb_driver.list_tables():
            collection.append(table)

        return collection


    def insert_data(self, table_name, data):
        raw_data = json.dumps(data).replace("None", "null").replace('""', "null")
        statement = f"INSERT INTO {table_name} `{raw_data}`"
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def update_data(self, table_name, primary_key_field, primary_key_value, data):
        raw_data = str(data).replace("None", "null").replace('""', "null")

        statement = f"""
            UPDATE {table_name} AS x 
                SET x = {raw_data} 
            WHERE x.{primary_key_field} = {primary_key_value}"""
        
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def query(self, statement):
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))

        return self.to_collection(cursor)


    def query_single(self, statement):
        cursor = self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))
        collection = self.to_collection(cursor)

        if len(collection) > 1:
            raise Exception('more than 1 result recived')

        return collection[0]


    def execute_statement(self, statement):
        self.qldb_driver.execute_lambda(lambda x: self.execute(x, statement))


    def delete_many(self, table_name, primary_key_field, primary_key_values, step = 40):
        values = primary_key_values

        while len(values) > 0:
            statement = f"DELETE FROM {table_name} WHERE {primary_key_field} IN {values[:step]}"
            self.execute_statement(statement)
            del values[:step]


    def insert_many(self, table_name, data, step = 40):
        raw_data = data

        for i in range(len(data)):
            for key, value in data[i].items():
                try:
                    data[i][key] = data[i][key].replace("'", "")
                except:
                    pass

        while len(raw_data) > 0:
            data_tmp = str(raw_data[:step]).replace("None", "null")

            data_tmp = data_tmp[1:][:-1]

            statement = f"INSERT INTO {table_name} << {data_tmp} >>"

            syslog.syslog(statement + " \n")

            self.execute_statement(statement)

            del raw_data[:step]
