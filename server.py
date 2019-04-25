from flask import Flask, render_template, json, request, make_response
import sqlite3

app= Flask(__name__,static_url_path='/static')

DATABASE="db.sqlite"

@app.route("/")
def main():
	resp = make_response(render_template("mainPage.html"))
	resp.set_cookie('username', 'I am cookie')
	return resp
	
@app.route("/createRide")
def createRideP():
	return render_template("createRide.html")
	
@app.route("/addStopP")
def addStopP():
	return render_template("addStop.html")
	
@app.route("/login")
def addStP():
	return render_template("login.html")

@app.route("/createUser")	
def createUser():
	return render_template("createUser.html")
	

@app.route("/insertRoute",methods=['POST'])
def insertRoute():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	#get values from form by keyname
	driverid=request.form['driverID']
	date=request.form['date']
	time= request.form['time']
	start = request.form['start']
	end = request.form['end']
	
	routeStops(routeid driverID, start, end)
	
	if routeid and driverid and date and time:
		route=(routeid, driverid , date, time)
		c.execute("INSERT INTO routes(routeid,driverid,date,time)VALUES(?,?,?)",route)
		conn.commit()
		#access in html side using the json response object and by accessing key 'result'   ex. data['result'] should give the below message
		return json.dumps({'result':'all fields correct, inserted into db'})
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()

def routeStops(routeid, username, start , end):
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	
	#add stops to table
	if routeid and start and end and username:
		startStop = (routeid,start,username,true)
		endStop = (routeid,end,username,true)
		c.execute("INSERT INTO stops(routeid,location,riderid,start)VALUES(?,?,?)",startStop)
		c.execute("INSERT INTO stops(routeid,location,riderid,end)VALUES(?,?,?)",endStop)
		conn.commit()
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
	c.execute("SELECT username,password FROM users WHERE username = ?",username)
	userExist =  c.fetchone()
	if userExist
		resp = make_response(render_template("createUser.html"))
		return resp	
	
	#if the new user is valid add them to the table
	if username and password and email:
		user = (username,password,email)
		c.execute("INSERT INTO users(username,password,email)VALUES(?,?,?)",user)
		conn.commit()
		resp = make_response(render_template("mainPage.html"))
		resp = resp.set_cookie(username)
		return resp	
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()
	
		#this is basicly sudocode at this point
		#this us not done and written by someone who knows nothing about sql
@app.route("/insertStop",methods=['POST'])	
def insertStop():
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
		c.execute("INSERT INTO stops(routeid,location,riderid)VALUES(?,?,?)",startStop)
		c.execute("INSERT INTO stops(routeid,location,riderid)VALUES(?,?,?)",endStop)
		conn.commit()
		return json.dumps({'result':'all fields correct, inserted into db'})
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()
	
		#this is basicly sudocode at this point
		#this us not done and written by someone who knows nothing about sql
@app.route("/login",methods=['POST'])
def login():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	username = request.form['username']
	password = request.form['password']
	
	#query for if user exist
	c.execute("SELECT username,password FROM users WHERE username = ?",username)
	userQ = c.fetchone()

	#if everything is good log them in 
	if userQ[1] == password:
		resp = make_response(render_template("mainPage.html"))
		resp.set_cookie(username)
		return resp
	else:
		resp = make_response(render_template("login.html"))
		return resp	
	conn.close()

	#this is basicly sudocode at this point
	#this us not done and written by someone who knows nothing about sql
@app.route("/hasRide",methods=['POST','GET'])		
def hasRide():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	
	username = request.form['username']
	c.execute("SELECT riderid FROM stops WHERE riderid=?",username)
	currentRide = c.fetchone()
	#need to return true if currentRide is not false 
	#if you couldnt tell I have no idea how to actuall code this stuff.
	if currentRide:
		return True
	else:
		return False;
	conn.close()



@app.route("/allDrives", methods=['POST','GET'])
def allDrives():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	c.execute("SELECT routeid AND time AND date FROM routes")
	rows=c.fetchall()
	list = ()
	for row in rows:
		c.execute("SELECT location FROM stops WHERE start=true AND routeid=?",row[0])
		start = c.fetchone()
		c.execute("SELECT location FROM stops WHERE end=true AND routeid=?",row[0])
		end = c.fetchone()
		dict = {"routeID":row[0],"start""StartingPoint": start,"Destination": end,"DepartureTime": row[1]+row[2]}
		list.append(dict)
		
	#pretty sure this data is accessed by the column names so data[index_of_row][column_name] column names are routeid,driverid,date,time case sensitive
	return json.dumps(list)
	conn.close()
	
if __name__=="__main__":

	app.run()
