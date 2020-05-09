import math
import sqlite3

from datetime import datetime
from calendar import timegm
from bottle import (Bottle, HTTPResponse, run, request, response,
                    json_dumps as dumps)

app = Bottle()


def convert_to_time_unixepoch(timestamp):
    return timegm(
            datetime.strptime(
                timestamp, '%Y-%m-%dT%H:%M:%S.%fZ').timetuple())

def get_all_rows(max_points, sysid):
    #conn = sqlite3.connect("all.db") 
    conn = sqlite3.connect("aq.db")
    sql = "select received_time, board_rel_hum, lon*180/3.1415926, lat*180/3.1415926, device_id from messages where sysid = "+str(sysid)
    result = conn.execute(sql).fetchmany(max_points)
    conn.close()
    return result


def create_data_points(start, end, max_points):
    start = convert_to_time_unixepoch(start)
    end = convert_to_time_unixepoch(end)
    conn = sqlite3.connect("../aq.db") 
    sql = "select board_rel_hum, received_time*1000 from messages where received_time > ? and received_time < ?"
    result = conn.execute(sql, (start, end)).fetchmany(max_points)
    conn.close()
    return result


@app.hook('after_request')
def enable_cors():
    print("after_request hook")
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = \
        'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@app.route("/", method=['GET', 'OPTIONS'])
def index():
    return "OK"


@app.post('/search')
def search():
    return HTTPResponse(body=dumps(['17dh0cf43jg77n', '17dh0cf43jg77j']),
                        headers={'Content-Type': 'application/json'})


@app.post('/query')
def query():
    body = []
    request_json = request.json
    max_points = request_json["maxDataPoints"]
    if request.json['targets'][0]['type'] == 'table':
        series = request.json['targets'][0]['target']
        bodies  = {'17dh0cf43jg77n': [{
			"columns":[
			    {"text": "Date", "type": "time"},
                            {"text": "Humidity", "type": "number"},
			    {"text": "Longitude", "type": "number"},
			    {"text": "Latitude", "type": "number"},
			    {"text": "Device ID", "type": "number"}
		  	 ],
                 "rows": get_all_rows(max_points, 357518080233232),            
        	 "type": "table"        
		 }],
		 '17dh0cf43jg77j': [{
			"columns":[
			    {"text": "Date", "type": "time"},
                            {"text": "Humidity", "type": "number"},
                            {"text": "Longitude", "type": "number"},
                            {"text": "Latitude", "type": "number"},
                            {"text": "Device ID", "type": "number"}
                           ],
                 "rows": get_all_rows(max_points, 357518080249493),
                 "type": "table"
                }]}
#    else:
#        start, end = request_json['range']['from'], request_json['range']['to']
#        for target in request.json['targets']:
#            name = target['target']
#            datapoints = create_data_points(start, end, max_points)
#            body.append({'target': name, 'datapoints': datapoints})

    body = dumps(bodies[series])
    return HTTPResponse(body=body,
                        headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    run(app=app, host='localhost', port=8091)
