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
	
	#this is basicly sudocode at this point
	#this us not done and written by someone who knows nothing about sql
@app.route("/createAccount",methods=['POST'])
def createAccount():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	username = request.form['username']
	password = request.form['password']
	email = request.form['email']
	#query for duplicate usernames and emails
	invalidUser = c.execute("Select username From users Where username Like ?",username)
	invalidEmail = c.execute("Select username From users Where email Like ?",email)
	
	#if the new user is valid add them to the table
	if username and password and email:
		user = (username,password,email)
		c.execute("INSERT INTO users(username,password,email)VALUES(?,?,?)",user)
		conn.commit()
		#access in html side using the json response object and by accessing key 'result'   ex. data['result'] should give the below message
		return json.dumps({'result':'all fields correct, inserted into db'})
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()
	
		#this is basicly sudocode at this point
		#this us not done and written by someone who knows nothing about sql
@app.route("/addStop",methods=['POST'])	
def addStop():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	routeID = request.form['routeID']
	start = request.form['start']
	end = request.form['end']
	riderID = request['username']
	
	#add stops to table
	if routeID and start and end and riderID:
		startStop = (routeID,start,riderID)
		endStop = (routeID,end,riderID)
		c.execute("INSERT INTO stops(route_ID,location,rider_ID)VALUES(?,?,?)",startStop)
		c.execute("INSERT INTO stops(route_ID,location,rider_ID)VALUES(?,?,?)",endStop)
		conn.commit()
		return json.dumps({'result':'all fields correct, inserted into db'})
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()
	
		#this is basicly sudocode at this point
		#this us not done and written by someone who knows nothing about sql
@app.route("/addStop",methods=['POST'])	
def login():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	username = request.form['username']
	password = request.form['password']
	
	#query for if user exist
	invalidUser = c.execute("Select username From users Where username Like ?",username)
	
	#check password
	invalidPass = c.execute("Select password From users Where username Like ?",password)

	#if everything is good log them in 
	if invalidUser and invalidPass:
		return json.dumps({'result':'all fields correct, inserted into db'})
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()

	#this is basicly sudocode at this point
	#this us not done and written by someone who knows nothing about sql
@app.route("/hasRide",methods=['POST'])		
def hasRide():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	
	username = request.form['username']
	currentRide = c.execute("Select rider_ID From stops Where rider_ID Like ?",username)
	
	#need to return true if currentRide is not false 
	#if you couldnt tell I have no idea how to actuall code this stuff.
	if currentRide:
		return true
	else:
		return false;
	conn.close()



@app.route("/allDrives")
def allDrives():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	
	conn.close()
if __name__=="__main__":

	app.run()