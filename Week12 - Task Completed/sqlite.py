import sqlite3


con=sqlite3.connect("project.db")
cursor=con.cursor()

cursor.execute()  # add create table query

con.commit()
con.close()




