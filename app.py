from flask import Flask, request, Response, jsonify, redirect
from flask_cors import CORS
import yaml
from haversine import haversine, Unit
from google.cloud import firestore 
import google.cloud.exceptions
import uuid
import os

app = Flask(__name__)
app.config['YAML_AS_TEXT'] = True
firestore_client = firestore.Client()
    
@app.route('/')
def home():
    return "Secure, You are in GPI Backend !!"

unique_id = str(uuid.uuid4())
@app.route('/generate-link/<string:admin_id>', methods=['GET'])
def generate_link(admin_id):
    unique_link = f"http://gpi.software/student-form/{admin_id}/{unique_id}"
    return { 'link' : unique_link }

@app.route('/class-data', methods=['POST', 'GET'])
def classdata():
    if request.data:
        data = yaml.safe_load(request.data)

        classData = firestore_client.collection('class_data').document()
        classData.set(data)

        return { 'Output' : 'Data inserted successfully' }
    else:
        return { 'Error' : 'No data provided' }, 400

@app.route('/student-data/<string:admin_id>/<string:provided_id>', methods=['POST'])    
def studentdata(admin_id, provided_id):
    print(provided_id, unique_id)
    if provided_id == unique_id:
        if request.data:
            data = yaml.safe_load(request.data)

            class_data = firestore_client.collection('class_data')
            class_info = class_data.limit(1).get()

            if len(class_info) > 0:
                # Access the first document in the list
                first_doc = class_info[0].to_dict()

                radius = float(first_doc['radius'])

                admin_coord = (first_doc['latitude'], first_doc['longitude'])
                user_coord = (data['latitude'], data['longitude'])

                distance = float(haversine(admin_coord, user_coord, unit=Unit.METERS))

                data['present'] = distance < radius

                studentData = firestore_client.collection('student_data').document()
                studentData.set(data)
                return {'Output': 'Data inserted successfully'}
            else:
                return {'Error': 'No class data found'}, 400
        else:
            return { 'Error' : 'No data provided' }, 400
    else:
        return { 'Error' : 'Invalid Unique ID' }, 400

@app.route('/getClassData', methods=['GET'])
def GetClassData():
    class_data = firestore_client.collection('class_data')
    results = class_data.limit(1).get()

    if len(results) > 0:
        data = []
        for doc in results:
            data.append(doc.to_dict())

        return jsonify(data)
    else:
        return jsonify({})

@app.route('/getStudentData', methods=['GET'])
def GetStudentData():
    student_data = firestore_client.collection('student_data')
    results = student_data.get()

    if len(results) > 0:
        data = []
        for doc in results:
            data.append(doc.to_dict())

        return jsonify(data)
    else:
        return jsonify({})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
 