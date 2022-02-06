import mysql.connector 
from datetime import datetime
from datetime import date
from flask import Flask,request
import json
from flask import jsonify
from flask_cors import CORS
app=Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
"""
insert some code here
"""






def validate(datum):
	
	myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "",database = "datim")
	
	cur = myconn.cursor() 
	
	tup=[]
	tup.append(datum['hospitalName'])
	sql="SELECT datetimes FROM statisticalrecords WHERE hospitalName =%s ORDER BY datetimes DESC "
	cur.execute(sql,tup)
	result=cur.fetchone()
	
	
	

	
	sql = "insert into statisticalrecords(hospital_id,hospitalName,newBornNumber,deathNumber,numberOfpatientsServed,coronaCases) values (%s, %s, %s, %s, %s,%s)" 
	val = (datum['hospital_id'],datum['hospitalName'], datum['newBornNumber'],datum['deathNumber'], datum['numberOfpatientsServed'],datum['coronaCases']) 
	try:  
		cur.execute(sql,val)
		print(cur)
		myconn.commit()
	except:  
		myconn.rollback()

		
	
	
		


def datimRecords():
	myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "",database = "datim")
	
	cur = myconn.cursor() 
	cur.execute("SELECT * FROM statisticalrecords ")
	print(cur)
	data=cur.fetchall()
	print(cur)
	li=[]
	for x in data:
		sit = {}
		sit["hospital_id"] = x[0]
		sit["hospitalName"] =x[1]
		sit["newBornNumber"] =x[2]
		sit["deathNumber"] =x[3]
		sit["numberOfpatientsServed"] =x[4]
		sit["coronaCases"] =x[5]
		sit["date"] =datetime.strptime(str(x[7]),"%Y-%m-%d")
		li.append(sit)
	
	#records=json.load(data,default=str)
	#records=json.(records)
		
		


	return li

			
		
			





	


	
	


			
@app.route("/",methods=["POST","GET"])
def datim():
	print("recieved acall")
	if request.method=='POST':
		print(request.data)
		data=json.loads(request.data)
		print(data)
		if validate(data) :
			data['status']="success"
			data['statusReason']="insertion success"
			date=datetime.today().strftime('%Y-%m-%d')
			data['date']=date
			return data
		else:
			data['status']="Failed"
			data['statusReason']="data should be sent at a time interval of 24 hours"
			date=datetime.today().strftime('%Y-%m-%d')
			
			data['date']=date
			
			
			return data
	elif request.method=='GET':

		
		data=datimRecords()
		return jsonify({'records':data})





if __name__ == '__main__':
	app.run(debug=True,host="0.0.0.0") 
	



