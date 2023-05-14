from flask import Flask, request
from flask_cors import CORS
import yaml

app = Flask(__name__)
app.config['YAML_AS_TEXT'] = True

@app.route('/members', methods=['GET'])
def members():    
    return {"members": ["member1", "member2", "member3"]}

@app.route('/class-data', methods=['POST', 'GET'])
def classdata():
    data = yaml.safe_load(request.data)

    return { 'data' : data }

@app.route('/student-data', methods=['POST', 'GET'])    
def studentdata():
    data = yaml.safe_load(request.data)

    return { 'data' : data }

if __name__ == "__main__":
    app.run(debug=True)

    
