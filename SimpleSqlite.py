#!/usr/bin/env python

import sqlite3
import logging
from uuid import uuid4


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



class DataBase:

	def __init__(self, database_name:str=f"{uuid4()}.sqlite3")-> None:
		"""
			Initialize database for connecting.
			Gets one string argument wich name is 'database_name'.
			If there is no argument default is 'db.sqlite3'.

			Database named as 'db' in 'self'.
			Also you can use 'execute' for execute costum commands.

			More information in https://docs.python.org/3/library/sqlite3.html#module-sqlite3
		"""
		logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Creating databse")
		db = sqlite3.connect(database_name)
		self.db = db
		self.execute = db.execute



	def create_table(self, table_name:str, columns:dict)-> bool:
		"""
			Create table in database.
			Gets one string argument wich name is 'table_name' and one dictionary in 'columns' with format below :
							{"<column_name>":{"<data_type>":<UNIQUE : True/False>}}
					'column_name' must be string and 'data_type' one of options bellow in string format:
							1.null :
								The value is a NULL value.
							2.integer :
								The value is a signed integer, stored in 1, 2, 3, 4, 6, or 8 bytes depending on the magnitude of the value.
							3.real :
								The value is a floating point value, stored as an 8-byte IEEE floating point number.
							4.text :
								The value is a text string, stored using the database encoding (UTF-8, UTF-16BE or UTF-16LE)
							5.blob :
								The value is a blob of data, stored exactly as it was input.

						for example :
							{"username":"text", "id":"integer", "number":"null"}

						for more information visit https://www.tutorialspoint.com/sqlite/sqlite_data_types.htm

			If operation was successful returns 'True' else 'False'

			More info at https://www.tutorialspoint.com/sqlite/sqlite_create_table.htm
		"""
		try:
			data_set = []
			for column_name, data_type in columns.items():
				if data_type[1] is True:
					data_set.append(f'{column_name} {data_type[0]} UNIQUE')
				else:
					data_set.append(f'{column_name} {data_type[0]}')

			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Creating table")
			self.execute("""
					CREATE TABLE {0} 
								({1});
					""".format(table_name, ' , '.join(data_set)))
			return True
		except Exception as e:
			return False

	def insert_data(self, table_name: str, values:list) ->bool:
		"""
			Insert a row of data to column in Database.
					for first argument gets table name and for the second argument, it receives a list of
					data according to the order of the columns created by '<create_table>' function for
					exapmle if colums order is "name" "age" "id" data shoud be "<some name>" "<some age>" "<some id>".
					
					Note that for each new data you sould call function if you have K data with N value function should
					calld for K series with N value.
			
			If operation was successful returns 'True' else 'False'

			More information at https://www.tutorialspoint.com/sqlite/sqlite_insert_query.htm
		"""
		try:
			data_sets = []
			for data in values:
				if type(data) == type(str()):
					data_sets.append(f"'{data}'")
				elif type(data) == type(None):
					data_sets.append("null")
				elif type(data) in (type(int()), type(float())):
					data_sets.append(str(data))
				else:
					raise Exception('Invalid data.')
		
			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Inserting data in to database")
			self.execute("""
				INSERT INTO {0} VALUES ({1});
			""".format(table_name, ' , '.join(data_sets)))
			return True
		except Exception as e:
			logging.error(f"{bcolors.FAIL}{bcolors.BOLD}[ERROR]{bcolors.ENDC} {e}")
			return False


	def select_data(self, table_name: str, column:list=["*"]):
		"""
			SQLite SELECT statement is used to fetch the data from a SQLite database table which
			returns data in the form of a result table. These result tables are also called result sets.


			If operation was successful returns '<data>' else 'False'

			More information at https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
		"""
		try:
			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Selecting data")
			data = list(self.execute("SELECT {0} FROM {1};".format(' , '.join(column), table_name)))
			return data
		except Exception as E:
			print(E)
			return False

	def select_data_from_and(self, table_name, where:str, column:list=["*"]):
		"""
			SQLite SELECT statement is used to fetch the data from a SQLite database table which
			returns data in the form of a result table. These result tables are also called result sets.

			Like select_data but with AND operator

			If operation was successful returns '<data>' else 'False'

			More information at https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
		"""
		try:
			data_sets = []
			for key , value in where.items():
				data_sets.append(f"{key} = '{value}'")
			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Selecting data from and")
			data = list(
				self.execute("""
							SELECT {0} FROM {1} WHERE {2};
				""".format(' , '.join(column), table_name, ' AND '.join(data_sets)))
			)
			return data
		except Exception as e:
			logging.error(f"{bcolors.FAIL}{bcolors.BOLD}[ERROR]{bcolors.ENDC} {e}")
			return False

	def select_data_from_or(self, table_name, where:str, column=["*"]):
		"""
			SQLite SELECT statement is used to fetch the data from a SQLite database table which
			returns data in the form of a result table. These result tables are also called result sets.

			Like select_data but with OR operator

			If operation was successful returns '<data>' else 'False'

			More information at https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
		"""
		try:
			data_sets = []
			for key , value in where.items():
				data_sets.append(f"{key} = '{value}'")
			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Selecting from or")
			data = list(
				self.execute("""
							SELECT {0} FROM {1} WHERE {2};
				""".format(' , '.join(column), table_name, ' OR '.join(data_sets)))
			)
			return data
		except Exception as e:
			logging.error(f"{bcolors.FAIL}{bcolors.BOLD}[ERROR]{bcolors.ENDC} {e}")
			return False



	# conn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID = 1")
	def update_data(self, table_name, wich:str, where:str) -> bool:
		"""
			SQLite UPDATE Query is used to modify the existing records in a table.
			You can use WHERE clause with UPDATE query to update selected rows, otherwise
			all the rows would be updated.

			this methd recives 2 argument first one is 'wich' that means wich property must be update,
			second one is 'where' property that means where shuld be chabge.
			example usage :
				wich = {"<column name>" : "<new value>", }
				where = {"<filterd column name>" : "<value>",}

			If operation was successful returns 'True' else 'False'
		"""
		try:
			data_sets_where = []
			for key , value in where.items():
				data_sets_where.append(f'{key} = {value}')
			
			data_sets_wich = []
			for key, value in wich.items():
				data_sets_wich.append(f'{key} = {value}')
			
			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Updating data")
			self.execute(f"""
				UPDATE {table_name} SET {' '.join(data_sets_wich)} WHERE {' '.join(data_sets_where)};
			""")
			return True
		except Exception as e:
			logging.error(f"{bcolors.FAIL}{bcolors.BOLD}[ERROR]{bcolors.ENDC} {e}")
			return False


	def delete(self, table_name, where:str)-> bool:
		"""
			SQLite DELETE Query is used to delete the existing records from a table.
			You can use WHERE clause with DELETE query to delete the selected rows,
			otherwise all the records would be deleted.

			If operation was successful returns 'True' else 'False'

		"""
		try:
			data_sets = []
			for key , value in where.items():
				data_sets.append(f'{key} = {value}')

			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Deleting data")
			self.execute(f"""
				DELETE FROM {table_name} WHERE {' '.join(data_sets)};
			""")
			return True
		except Exception as e:
			logging.error(f"{bcolors.FAIL}{bcolors.BOLD}[ERROR]{bcolors.ENDC} {e}")
			return False

	def execute_command(self, table_name, command:str):
		try:
			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Executing data")
			return self.execute(command)
		except Exception as e:
			logging.error(f"{bcolors.FAIL}{bcolors.BOLD}[ERROR]{bcolors.ENDC} {e}")
			return False

	def commit(self)->bool:
		"""
			Save (commit) the changes.

			If operation was successful returns 'True' else 'False'
		"""
		try:
			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} Commiting data")
			self.db.commit()
			return True
		except Exception as e:
			logging.error(f"{bcolors.FAIL}{bcolors.BOLD}[ERROR]{bcolors.ENDC} {e}")
			return False
	def close(self) -> bool:
		"""
			We can also close the connection if we are done with it.
			Just be sure any changes have been committed or they will be lost.

			If operation was successful returns 'True' else 'False'
		"""
		try:
			logging.info(f"{bcolors.OKCYAN}{bcolors.BOLD}[INFO]{bcolors.ENDC} CLosing database")
			self.db.close()
			return True
		except Exception as e:
			logging.error(f"{bcolors.FAIL}{bcolors.BOLD}[ERROR]{bcolors.ENDC} {e}")
			return False

