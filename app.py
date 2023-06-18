from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import yaml
from flask_pymongo import PyMongo 
from bson import json_util
from haversine import haversine, Unit
import uuid

app = Flask(__name__)
app.config['YAML_AS_TEXT'] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
mongo = PyMongo(app)
db = mongo.db

@app.route('/generate-link/<string:admin_id>', methods=['GET'])
def generate_link(admin_id):
    unique = str(uuid.uuid4())
    unique_link = f"localhost:3000/student-form/{admin_id}/{unique}"
    return { 'link' : unique_link }

@app.route('/class-data', methods=['POST', 'GET'])
def classdata():
    if request.data:
        data = yaml.safe_load(request.data)

        classdata = db.get_collection('class_data')
        classdata.insert_one(data)

        return { 'Output' : 'Data inserted successfully' }
    else:
        return { 'Error' : 'No data provided' }, 400

@app.route('/student-data/<string:admin_id>/<string:uuid>', methods=['POST', 'GET'])    
def studentdata(admin_id, uuid):
    if request.data:
        data = yaml.safe_load(request.data)

        classdata = db.get_collection('class_data')
        class_info = classdata.find_one({})

        radius = float(class_info['radius'])

        admin_coord = (class_info['latitude'], class_info['longitude'])
        user_coord = (data['latitude'], data['longitude'])        

        distance = float(haversine(admin_coord, user_coord, unit=Unit.METERS))

        data['present'] = distance < radius

        studentdata = db.get_collection('student_data')
        studentdata.insert_one(data)
        return { 'Output' : 'Data inserted successfully' }
    else:
        return { 'Error' : 'No data provided' }, 400

@app.route('/GetClassData', methods=['GET'])
def GetClassData():
    class_data = db.get_collection('class_data')

    result = class_data.find_one()
    data = list(result)

    for item in data :
        item['_id'] = str(item['_id'])

    return jsonify(data)

@app.route('/GetStudentData', methods=['GET'])
def GetStudentData():
    student_data = db.get_collection('student_data')

    result = student_data.find()
    data = list(result)

    for item in data :
        item['_id'] = str(item['_id'])

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)    

