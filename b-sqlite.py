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
    sql = "select received_time, boardtemp, board_rel_hum, lon*180/3.1415926, lat*180/3.1415926, opcpma,(opcbin_0+opcbin_1+opcbin_2+opcbin_3+opcbin_4+opcbin_5), opcpmc from messages where sysid = "+str(sysid)
    result = conn.execute(sql).fetchmany(max_points)
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
    return HTTPResponse(body=dumps(['17dh0cf43jg77n', '17dh0cf43jg77j', '17dh0cf43jg77l', '17dh0cf43jg783', '17dh0cf43jg781', '17dh0cf43jg6n4', '17dh0cf43jg7ka']),
                        headers={'Content-Type': 'application/json'})


@app.post('/query')
def query():
    body = []
    request_json = request.json
    max_points = request_json["maxDataPoints"]
    if request.json['targets'][0]['type'] == 'table':
        series = request.json['targets'][0]['target']
        bodies  = {
            '17dh0cf43jg77n': [{
                "columns":[
                    {"text": "Date", "type": "time"},
                    {"text": "Temperature", "type": "number"},
                    {"text": "Humidity", "type": "number"},
                    {"text": "Longitude", "type": "number"},
                    {"text": "Latitude", "type": "number"},
                    {"text": "PM 1.0", "type": "number"},
                    {"text": "PM 2.5", "type": "number"},
                    {"text": "PM 10", "type": "number"}
                ],
                "rows": get_all_rows(max_points, 357518080233232),            
                "type": "table"        
            }],
            '17dh0cf43jg77j': [{
                "columns":[
                    {"text": "Date", "type": "time"},
                    {"text": "Temperature", "type": "number"},
                    {"text": "Humidity", "type": "number"},
                    {"text": "Longitude", "type": "number"},
                    {"text": "Latitude", "type": "number"},
                    {"text": "PM 1.0", "type": "number"},
                    {"text": "PM 2.5", "type": "number"},
                    {"text": "PM 10", "type": "number"}
                ],
                "rows": get_all_rows(max_points, 357518080249493),
                "type": "table"
            }],
            '17dh0cf43jg77l': [{
                "columns":[
                    {"text": "Date", "type": "time"},
                    {"text": "Temperature", "type": "number"},
                    {"text": "Humidity", "type": "number"},
                    {"text": "Longitude", "type": "number"},
                    {"text": "Latitude", "type": "number"},
                    {"text": "PM 1.0", "type": "number"},
                    {"text": "PM 2.5", "type": "number"},
                    {"text": "PM 10", "type": "number"}
                ],
                "rows": get_all_rows(max_points, 357518080231574),
                "type": "table"
            }],
            '17dh0cf43jg783': [{
                "columns":[
                    {"text": "Date", "type": "time"},
                    {"text": "Temperature", "type": "number"},
                    {"text": "Humidity", "type": "number"},
                    {"text": "Longitude", "type": "number"},
                    {"text": "Latitude", "type": "number"},
                    {"text": "PM 1.0", "type": "number"},
                    {"text": "PM 2.5", "type": "number"},
                    {"text": "PM 10", "type": "number"}
                ],
                "rows": get_all_rows(max_points, 357518080249428),
                "type": "table"
            }],
            '17dh0cf43jg781': [{
                "columns":[
                    {"text": "Date", "type": "time"},
                    {"text": "Temperature", "type": "number"},
                    {"text": "Humidity", "type": "number"},
                    {"text": "Longitude", "type": "number"},
                    {"text": "Latitude", "type": "number"},
                    {"text": "PM 1.0", "type": "number"},
                    {"text": "PM 2.5", "type": "number"},
                    {"text": "PM 10", "type": "number"}
                ],
                "rows": get_all_rows(max_points, 357518080249352),
                "type": "table"
            }],
            '17dh0cf43jg6n4': [{
                "columns":[
                    {"text": "Date", "type": "time"},
                    {"text": "Temperature", "type": "number"},
                    {"text": "Humidity", "type": "number"},
                    {"text": "Longitude", "type": "number"},
                    {"text": "Latitude", "type": "number"},
                    {"text": "PM 1.0", "type": "number"},
                    {"text": "PM 2.5", "type": "number"},
                    {"text": "PM 10", "type": "number"}
                ],
                "rows": get_all_rows(max_points, 357518080231251),
                "type": "table"
            }],
            '17dh0cf43jg7ka': [{
                "columns":[
                    {"text": "Date", "type": "time"},
                    {"text": "Temperature", "type": "number"},
                    {"text": "Humidity", "type": "number"},
                    {"text": "Longitude", "type": "number"},
                    {"text": "Latitude", "type": "number"},
                    {"text": "PM 1.0", "type": "number"},
                    {"text": "PM 2.5", "type": "number"},
                    {"text": "PM 10", "type": "number"}
                ],
                "rows": get_all_rows(max_points, 357518080231095),
                "type": "table"
        }]}
    body = dumps(bodies[series])
    return HTTPResponse(body=body,
                        headers={'Content-Type': 'application/json'})


if __name__ == '__main__':
    run(app=app, host='localhost', port=8091)
