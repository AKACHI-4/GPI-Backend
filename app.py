from flask import Flask, request
from flask_cors import CORS
import yaml
from flask_pymongo import PyMongo 

app = Flask(__name__)
app.config['YAML_AS_TEXT'] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
mongo = PyMongo(app)
db = mongo.db

@app.route('/class-data', methods=['POST', 'GET'])
def classdata():
    data = yaml.safe_load(request.data)
    classdata = db.get_collection('class_data')
    classdata.insert_one(data)
    return { 'Output' : ' Data inserted successfully ' }

@app.route('/student-data', methods=['POST', 'GET'])    
def studentdata():
    data = yaml.safe_load(request.data)
    studentdata = db.get_collection('student_data')
    studentdata.insert_one(data)
    return { 'Output' : ' Data inserted successfully ' }

@app.route('/class-room', methods=['POST', 'GET'])
def classRoom():
    

    return {}

if __name__ == "__main__":
    app.run(debug=True)

    
