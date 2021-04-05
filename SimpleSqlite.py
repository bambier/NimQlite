#!/usr/bin/env python

import sqlite3
import sys


class DataBase:

	def __init__(self, database_name="db.sqlite3"):
		"""
			Initialize database for connecting.
			Gets one string argument wich name is 'database_name'.
			If there is no argument default is 'db.sqlite3'.

			Database named as 'db' in 'self' and cursor named as 'cursor' in 'self'.
			Also you can use 'execute' for execute costum commands.

			More information in https://docs.python.org/3/library/sqlite3.html#module-sqlite3
		"""
		self.db = sqlite3.connect(database_name)
		self.cursor = self.db.cursor()
		self.execute = self.cursor.execute


	def create_table(self, table_name, columns={}):
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

			self.execute("""
					CREATE TABLE {0} 
								({1});
					""".format(table_name, ' , '.join(data_set)))
			self.table_name = table_name
			return True
		except:
			return False


	def insert_data(self, values):
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
		
			self.execute("""
				INSERT INTO {0} VALUES ({1});
			""".format(self.table_name, ' , '.join(data_sets)))
			return True
		except:
			return False



	def select_data(self, column=["*"]):
		"""
			SQLite SELECT statement is used to fetch the data from a SQLite database table which
			returns data in the form of a result table. These result tables are also called result sets.


			If operation was successful returns '<data>' else 'False'

			More information at https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
		"""
		try:
			data = list(self.execute("SELECT {0} FROM {1};".format(' , '.join(column), self.table_name)))
			return data
		except:
			return False


	def select_data_from_and(self, where, column=["*"]):
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
			data = list(
				self.execute("""
							SELECT {0} FROM {1} WHERE {2};
				""".format(' , '.join(column), self.table_name, ' AND '.join(data_sets)))
			)
			return data
		except:
			return False

	def select_data_from_or(self, where, column=["*"]):
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
			data = list(
				self.execute("""
							SELECT {0} FROM {1} WHERE {2};
				""".format(' , '.join(column), self.table_name, ' OR '.join(data_sets)))
			)
			return data
		except:
			return False



	# conn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID = 1")
	def update_data(self, wich, where):
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
			
			self.execute(f"""
				UPDATE {self.table_name} SET {' '.join(data_sets_wich)} WHERE {' '.join(data_sets_where)};
			""")
			return True
		except:
			return False


	def delete(self, where):
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

			self.execute(f"""
				DELETE FROM {self.table_name} WHERE {' '.join(data_sets)};
			""")
		except:
			return False


	def execute_command(self, command):
		try:
			return self.execute(command)
		except:
			return False


	def commit(self):
		"""
			Save (commit) the changes.

			If operation was successful returns 'True' else 'False'
		"""
		self.db.commit()
		return True
	
	def close(self):
		"""
			We can also close the connection if we are done with it.
			Just be sure any changes have been committed or they will be lost.

			If operation was successful returns 'True' else 'False'
		"""
		self.db.close()
		return True


