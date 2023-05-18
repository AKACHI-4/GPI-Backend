from flask import Flask, request, Response
from flask_cors import CORS
import yaml
from flask_pymongo import PyMongo 
from bson import json_util

app = Flask(__name__)
app.config['YAML_AS_TEXT'] = True
app.config["MONGO_URI"] = "mongodb://localhost:27017/admin"
mongo = PyMongo(app)
db = mongo.db

@app.route('/class-data', methods=['POST', 'GET'])
def classdata():
    if request.data:
        data = yaml.safe_load(request.data)

        admin_id = data.get('admin_id')

        classdata = db.get_collection('class_data')
        classdata.insert_one(data)

        studentdata = db.get_collection('student_data')
        studentdata.update_many(
            {'admin_id': {'$exists': False}},  
            {'$set': {'admin_id': admin_id}} 
        )

        return { 'Output' : 'Data inserted successfully' }
    else:
        return { 'Error' : 'No data provided' }, 400

@app.route('/student-data', methods=['POST', 'GET'])    
def studentdata():
    if request.data:
        data = yaml.safe_load(request.data)

        classdata = db.get_collection('class_data')
        data['admin_id'] = classdata.find_one({})['admin_id']

        studentdata = db.get_collection('student_data')
        studentdata.insert_one(data)
        return { 'Output' : 'Data inserted successfully' }
    else:
        return { 'Error' : 'No data provided' }, 400

@app.route('/class-room', methods=['POST', 'GET'])
def classRoom():
    class_data = db.get_collection('class_data')

    # Retrieve data from the collection
    result = class_data.find()
    data = list(result)

    # Convert data to YAML
    yaml_data = yaml.dump(data)

    # Set response headers to indicate YAML content
    headers = {
        'Content-Type': 'text/yaml',
        'Content-Disposition': 'attachment; filename="classDetails.yaml"'
    }

    return Response(yaml_data, headers=headers)

if __name__ == "__main__":
    app.run(debug=True)    

