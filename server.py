from flask import Flask
from flask import request, jsonify
import numpy
import json 

# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)
# current_reading = "init"

susceptible = {}
infected = {}


def check_dist(loc1, loc2, th=1):
    dist = (((loc1[1] - loc2[1]) ** 2) + ((loc1[0] - loc2[0]) ** 2)) ** 0.5
    if dist > th:
        return 0
    return 1

def detect_collision(loc):
    cntr = 0
    for index in infected:
        for infect_loc in infected[index]:
            if check_dist(infect_loc, loc):
                cntr += 1
    return cntr

@app.route('/location', methods=['POST'])
def log_location():
    data = request.get_json()
    if data['infected'] is 1:
        if data['id'] in infected.keys(): 
            infected[data['id']].append(data['loc'])
        else:
            infected[data['id']] = [data['loc']]
        return jsonify("Success")
    else:
        if data['id'] in susceptible.keys(): 
            susceptible[data['id']].append(data['loc'])
        else:
            susceptible[data['id']] = [data['loc']]
        return jsonify({'infected_collisions': detect_collision(data['loc'])})

@app.route('/location/all', methods=['GET'])
def get_location():
    return jsonify({'infected': infected, 'susceptible': susceptible})






if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0')