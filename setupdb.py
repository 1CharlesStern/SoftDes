import sqlite3
DATABASE="db.sqlite"

createdb="""CREATE TABLE IF NOT EXISTS routes (
		routeid integer PRIMARY KEY,
		driverid integer NOT NULL,
		date text,
		time text
		);"""
		
createuserstable="""CREATE TABLE IF NOT EXISTS users (
		username text PRIMARY KEY,
		password text NOT NULL,
		email text,
		);"""
		
createstopstable="""CREATE TABLE IF NOT EXISTS stops (
		route_ID text PRIMARY KEY,
		location text NOT NULL,
		rider_ID text NOT NULL,
		start bool,
		end bool,
		);"""
		
def dbSetup():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	c.execute(createdb)
	c.execute(createuserstable)
	c.execute(createstopstable)
	conn.commit()
	conn.close()

if __name__=="__main__":
	dbSetup()