from flask import Flask, render_template, json, request, redirect, make_response, url_for
from functools import wraps
import sqlite3
import uuid

app= Flask(__name__,static_url_path='/static')

DATABASE="db.sqlite"

def login_required(f):
	@wraps(f)
	def wrap():
		print("in the wrapper")
		if 'username' in request.cookies:
			user = request.cookies['username']
			return f(user)
		else:
			return redirect(url_for('login'))
	return wrap

@app.route("/mainPage",methods=['GET'])
@login_required
def mainPage(username):
	if request.method == 'GET':
		resp = make_response(render_template("mainPage.html"))
		return resp

def loginInternal(username, password):
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	c.execute("SELECT username,password FROM users WHERE username = ?",(username,))
	userQ = c.fetchone()
	if userQ and userQ[1] == password:
		resp = make_response(redirect(url_for('mainPage')))
		resp.set_cookie("username", username)
		conn.close()
		return (resp);
	else:
		resp = make_response(render_template("login.html"))
		conn.close()
		return resp


@app.route("/login",methods=['GET','POST'])
def login():
	if request.method == 'GET':
		if 'username' in request.cookies:
			return redirect(url_for('mainPage'))
		resp = make_response(render_template("login.html"))
		return resp
	elif request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		return loginInternal(username, password)



@app.route("/addStop",methods=['GET', 'POST'])
@login_required
def addStop(username):
	if request.method == 'GET':
		resp = make_response(render_template("addStop.html"))
		return resp
	elif request.method == 'POST':
		conn=sqlite3.connect(DATABASE)
		c=conn.cursor()
		routeid = request.cookies['routeid']
		start = request.form['start']
		end = request.form['end']
		riderID = username
			#add stops to table
		if routeid and start and end and riderID:
			stopid = generateUniqueStopId(c)
			startStop = (stopid, routeid,start,riderID)
			c.execute("INSERT INTO stops(stopid, routeid,location,riderid)VALUES(?,?,?,?)",startStop)
			stopid = generateUniqueStopId(c)
			endStop = (stopid,routeid,end,riderID)
			c.execute("INSERT INTO stops(stopid, routeid,location,riderid)VALUES(?,?,?,?)",endStop)
			conn.commit()
			return redirect(url_for('riderWaiting'))
		else:
			return redirect(url_for('addStop'))


@app.route("/createRide",methods=['GET', 'POST'])
@login_required
def createRide(username):
	if request.method == 'GET':
		resp = make_response(render_template("createRide.html"))
		return resp
	elif request.method == 'POST':
		conn=sqlite3.connect(DATABASE)
		c=conn.cursor()
		#get values from form by keyname
		driverid=username
		date=request.form['date']
		time= request.form['time']
		start = request.form['start']
		end = request.form['end']
		loop = True
		routeid = 0

		while(loop):
			routeid = uuid.uuid1().int>>120
			c.execute("SELECT routeid FROM routes WHERE routeid = ?",(routeid,))
			idExistsAlready = c.fetchone()
			if not idExistsAlready:
				loop = False
		print(routeid);
		if routeid and driverid and date and time:
			routeStops(routeid, driverid, start, end)
			route=(routeid, driverid , date, time)
			c.execute("INSERT INTO routes(routeid,driverid,date,time)VALUES(?,?,?,?)",route)
			conn.commit()
			#access in html side using the json response object and by accessing key 'result'   ex. data['result'] should give the below message
			return redirect(url_for('mainPage'))
		else:
			return redirect(url_for('createRide'))
		conn.close()

@app.route("/createUser",methods=['GET', 'POST'])
def createUser():
	if request.method == 'GET':
		resp = make_response(render_template("createUser.html"))
		return resp
	elif request.method == 'POST':
		conn=sqlite3.connect(DATABASE)
		c=conn.cursor()
		username = request.form['username']
		password = request.form['password']
		confirmPassword = request.form['confirmPassword']
		email = request.form['email']
		if(password != confirmPassword):
			resp = make_response(render_template("createUser.html"))
			return resp
		#query for duplicate usernames and emails
		c.execute("SELECT username,password FROM users WHERE username = ?",(username,))
		userExist = c.fetchone()
		if not userExist and username and password and email:
			user = (username,password,email)
			c.execute("INSERT INTO users(username,password,email)VALUES(?,?,?)",user)
			conn.commit()
			conn.close()
			print("calling internal login")
			return loginInternal(username, password)
		else:
				resp = make_response(render_template("createUser.html"))
				conn.close()
				return resp

@app.route("/riderWaiting",methods=['GET', 'POST'])
@login_required
def riderWaiting(username):
	if request.method == 'GET':
		resp = make_response(render_template("riderWaiting.html"))
		return resp
	elif request.method == 'POST':
		resp = make_response(render_template("riderWaiting.html"))
		return resp

@app.route("/insertRoute",methods=['GET','POST'])
def insertRoute(user):
	if request.method == 'GET':
		resp = make_response(render_template("insertRoute.html"))
		return resp
	elif request.method == 'POST':
		conn=sqlite3.connect(DATABASE)
		c=conn.cursor()
		#get values from form by keyname
		driverid=request.form['driverid']
		date=request.form['date']
		time= request.form['time']
		start = request.form['start']
		end = request.form['end']

		routeStops(routeid, driverid, start, end)
		if routeid and driverid and date and time:
			route=(routeid, driverid , date, time)
			c.execute("INSERT INTO routes(routeid,driverid,date,time)VALUES(?,?,?)",route)
			conn.commit()
			#access in html side using the json response object and by accessing key 'result'   ex. data['result'] should give the below message
			return json.dumps({'result':'all fields correct, inserted into db'})
		else:
			return json.dumps({'result':'there was an issue with your request'})
		conn.close()
def generateUniqueStopId(c):
	loop = True
	stopid = 0
	while(loop):
		stopid = uuid.uuid1().int>>120
		c.execute("SELECT stopid FROM stops WHERE stopid = ?",(stopid,))
		idExistsAlready = c.fetchone()
		if not idExistsAlready:
			loop = False

	return stopid

def routeStops(routeid, username, start , end):
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()

	#add stops to table
	if routeid and start and end and username:
		stopid = generateUniqueStopId(c)
		startStop = (stopid, routeid,start,username,"True")
		c.execute("INSERT INTO stops(stopid, routeid,location,riderid,start)VALUES(?,?,?,?,?)",startStop)
		stopid = generateUniqueStopId(c)
		endStop = (stopid, routeid,end,username,"True")
		c.execute("INSERT INTO stops(stopid, routeid,location,riderid,end)VALUES(?,?,?,?,?)",endStop)
		conn.commit()
		return json.dumps({'result':'all fields correct, inserted into db'})
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()

@app.route("/createAccount",methods=['GET','POST'])
def createAccount():
	if request.method == 'GET':
		resp = make_response(render_template("createAccount.html"))
		return resp
	elif request.method == 'POST':
		conn=sqlite3.connect(DATABASE)
		c=conn.cursor()
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		#query for duplicate usernames and emails
		c.execute("SELECT username,password FROM users WHERE username = ?",username)
		userExist =  c.fetchone()
		if userExist:
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
	routeid = request.form['routeid']
	start = request.form['start']
	end = request.form['end']
	riderID = request['username']
		#add stops to table
	if routeid and start and end and riderID:
		stopid = generateUniqueStopId(c)
		startStop = (stopid, routeid,start,riderID)
		c.execute("INSERT INTO stops(stopid, routeid,location,riderid)VALUES(?,?,?,?)",startStop)
		stopid = generateUniqueStopId(c)
		endStop = (stopid,routeid,end,riderID)
		c.execute("INSERT INTO stops(stopid, routeid,location,riderid)VALUES(?,?,?,?)",endStop)
		conn.commit()
		return json.dumps({'result':'all fields correct, inserted into db'})
	else:
		return json.dumps({'result':'there was an issue with your request'})
	conn.close()

@app.route("/hasRide",methods=['POST'])
def hasRide():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()

	username = request.form['username']
	c.execute("SELECT riderid FROM stops WHERE riderid=?",(username,))
	currentRide = c.fetchone()
	if currentRide:
		return json.dumps({'result':'true'})
	else:
		return json.dumps({'result':'false'})
	conn.close()

@app.route("/cancelRide",methods=['POST'])
def cancelRide():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()

	username = request.form['username']
	c.execute("DELETE FROM stops WHERE riderid=?",(username,))
	currentRide = c.fetchone()
	return json.dumps({'result':'success'})
	conn.close()

@app.route("/allDrives", methods=['POST','GET'])
def allDrives():
	conn=sqlite3.connect(DATABASE)
	c=conn.cursor()
	c.execute("SELECT routeid,time,date FROM routes")
	rows=c.fetchall()
	print(rows)
	list = []
	for row in rows:
		c.execute("SELECT location FROM stops WHERE start='True' AND routeid=?",(row[0],))
		start = c.fetchone()
		c.execute("SELECT location FROM stops WHERE end='True' AND routeid=?",(row[0],))
		end = c.fetchone()
		print(row)
		dict = {"routeid":row[0],"StartingPoint": start[0],"Destination": end[0],"DepartureTime": row[1]+" " +row[2]}
		list.append(dict)

	#pretty sure this data is accessed by the column names so data[index_of_row][column_name] column names are routeid,driverid,date,time case sensitive
	jsonList = json.dumps(list)
	finalJson = '{"data":' + jsonList + "}"
	return finalJson
	conn.close()

if __name__=="__main__":
	app.run()
