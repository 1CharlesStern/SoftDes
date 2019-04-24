from flask import Flask, render_template, json, request
import sqlite3
app= Flask(__name__)

DATABASE="db.sqlite"

@app.route("/")
def main():
	return render_template("index.html")

@app.route("/insertRoute",methods=['POST'])
def insertRoute():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	#get values from form by keyname
	routeid=request.form['routeID']
	driverid=request.form['driverID']
	date=request.form['date']
	time= request.form['time']
	if routeid and driverid and date and time:
		route=(routeid, driverid , date, time)
		c.execute("INSERT INTO routes(routeid,driverid,date,time)VALUES(?,?,?)",route)
		conn.commit()
		#access in html side using the json response object and by accessing key 'result'   ex. data['result'] should give the below message
		return json.dumps({'result':'all fields correct, inserted into db'})
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()
	
@app.route("/allDrives")
def allDrives():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor
	
	conn.close()
if __name__=="__main__":

	app.run()