import sqlite3
DATABASE="db.sqlite"

createdb="""CREATE TABLE IF NOT EXISTS routes (
		routeid integer PRIMARY KEY,
		driverid integer NOT NULL,
		date text,
		time text
		);"""
		
createdb="""CREATE TABLE IF NOT EXISTS Users (
		username text PRIMARY KEY,
		password text NOT NULL,
		email text,
		);"""
		
def dbSetup():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	c.execute(createdb)
	conn.commit()
	conn.close()

if __name__=="__main__":
	dbSetup()