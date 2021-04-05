# SimpleSqlite
Simple Python3 sqlite3 controler

This package uses **python SQLITE3** pip.

This code just makes it easy for you to execute squat code with its functions. So you no longer need to write long codes to paste a data into your database
 
 
How to use it is as follows:

` from SimpleSqlite import DataBase `

` db = DataBase(database_name='mydb.sqlite3') `

`db.create_table(table_name="users", columns={"username":['text', True], "password":['text', False], "age":['integer', False]}) `

` db.insert_data(table_name="users", values=['nima', '1234', '20']) `

`  db.select_data(table_name='users', column=['username', 'age']) `

You can find more function in source code.


