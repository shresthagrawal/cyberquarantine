from flask import Flask
from flask import request, jsonify
import json 

# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
# current_reading = "init"

susceptible = {}
infected = {}

@app.route('/location', methods=['POST'])
def log_location():
    data = request.get_json()
    if data['infected'] is 1:
        if data['id'] in infected.keys(): 
            infected[data['id']].append(data['loc'])
        else:
            infected[data['id']] = [data['loc']]
    else:
        if data['id'] in susceptible.keys(): 
            susceptible[data['id']].append(data['loc'])
        else:
            susceptible[data['id']] = [data['loc']]
    print(infected, susceptible)
    return jsonify({'is_infected': True})

@app.route('/location/all', methods=['GET'])
def get_location():
    return jsonify({'infected': infected, 'susceptible': susceptible})


if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')