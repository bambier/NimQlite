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
			More information in https://docs.python.org/3/library/sqlite3.html#module-sqlite3
		"""
		self.db = sqlite3.connect(database_name)
		self.cursor = self.db.cursor()


	def create_table(self, table_name, columns={}):
		"""
			Create table in database.
			Gets one string argument wich name is 'table_name' and sorted in table_name in self also one dictionary in 'columns' with format below :
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

			self.cursor.execute("""
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
					for first argument it receives a list of data according to the order of the columns
					created by '<create_table>' function for exapmle if colums order is "name" "age" "id"
					data shoud be "<some name>" "<some age>" "<some id>".
					
					Note that for each new data you sould call function if you have K data with N value
					function should calld for K series with N value.
			
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
		
			self.cursor.execute("""
				INSERT INTO {0} VALUES ({1});
			""".format(self.table_name, ' , '.join(data_sets)))
			return True
		except:
			return False



	def select_data(self, column=["*"]):
		"""
			SQLite SELECT statement is used to fetch the data from a SQLite database table which
			returns data in the form of a result table. These result tables are also called result sets.

			Gets columns name for argument.
			
			
			If operation was successful returns '<data>' else 'False'

			More information at https://www.tutorialspoint.com/sqlite/sqlite_select_query.htm
		"""
		try:
			data = list(self.cursor.execute("SELECT {0} FROM {1};".format(' , '.join(column), self.table_name)))
			return data
		except:
			return False


	def select_data_from_and(self, where, column=["*"]):
		try:
			data_sets = []
			for key , value in where.items():
				data_sets.append(f"{key} = '{value}'")
			data = list(
				self.cursor.execute("""
							SELECT {0} FROM {1} WHERE {2};
				""".format(' , '.join(column), self.table_name, ' AND '.join(data_sets)))
			)
			return data
		except:
			return False

	def select_data_from_or(self, where, column=["*"]):
		try:
			data_sets = []
			for key , value in where.items():
				data_sets.append(f"{key} = '{value}'")
			data = list(
				self.cursor.execute("""
							SELECT {0} FROM {1} WHERE {2};
				""".format(' , '.join(column), self.table_name, ' OR '.join(data_sets)))
			)
			return data
		except:
			return False



	# conn.execute("UPDATE COMPANY set SALARY = 25000.00 where ID = 1")
	def update_data(self, wich, where):
		try:
			pass
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
		
		
		

		
