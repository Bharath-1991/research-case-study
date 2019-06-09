#coding: utf-8

from flask import Flask, Response, request, jsonify
import json
import pymongo
import re
app = Flask(__name__)

# myclient = pymongo.MongoClient("mongodb://172.28.5.0:27017")
MYCLIENT = pymongo.MongoClient("mongodb://mongo-db:27017")
# MYCLIENT = pymongo.MongoClient("mongodb://localhost:27017")
MYDB = MYCLIENT["mydatabase"]
MYCOL = MYDB["customers"]


@app.route("/")
def health_check():
    data =  {'status':'Good'}
    js = json.dumps(data)

    resp = Response(js, status=200, mimetype='application/json')
    resp.status_code = 200
    return resp


@app.route("/customers/<name>", methods=['GET','HEAD'])
def get_customer(name):
    try:
        if request.method == 'HEAD':
            value = customer_details(key=name)
            if any(value):
                return send_response(status=200)
            else:
                return send_response(status=404)
        else:
            value = customer_details(key=name)
            data = {"customer_details":value}
            if not any(data['customer_details']):
                raise Exception("Key doesnot exist")
        return send_response(data=data,status=200)
    except Exception as ex:
        return internal_error(error=ex, status=500)


@app.route("/customers/<name>", methods=['DELETE'])
def delete_customer_detail(name):
    try:
        new_values = customer_details()
        print('VALUES',new_values)
        if name in new_values.keys():
            del new_values[name]
        print('VALUES after loop',new_values)
        id = MYCOL.find_one({},{"_id":1})
        print('iiiid',id)
        MYCOL.delete_one(MYCOL.find_one())
        MYCOL.insert_one(new_values)

        data = {'message':"Values updated successfully",
                "updated_values":[MYCOL.find_one({},{"_id":0})]}

        return send_response(data=data,status=200)
    except Exception as ex:
        return internal_error(error=ex, status=500)  


@app.route("/customers", methods=['GET','PUT'])
def get_or_put_customer():
    data={}
    try:
        if request.method == 'PUT':
            new_values = {}
            new_values = MYCOL.find_one({},{"_id":1})
            if not new_values:
                new_values = {}
                MYCOL.insert_one(new_values)
            new_values.update(request.get_json())
            try:
                new_values['expire_in'] = request.args['expire_in']
            except KeyError:
                pass

            old_values = MYCOL.find_one({},{"_id":0})
            MYCOL.update_many(old_values, { "$set": new_values })
            data = {'message':"Values updated successfully",
                    "updated_values":[MYCOL.find_one({},{"_id":0})]}
        else:
            filter = request.args.get('filter')
            data = {'customer_details': all_customer_details(filter)}

        return send_response(data,200)
    except Exception as ex:
        return internal_error(error=ex, status=500)


@app.route("/customers", methods=['DELETE'])
def delete_all_customer_details():
    try:
        values = customer_details()
        MYCOL.delete_many(values)
        data = {"message":"Successfully Deleted"}
        return send_response(data=data,status=200)
    except Exception as ex:
        return internal_error(error=ex, status=500)  


def send_response(data=None, status=None):
    try:
        data = json.dumps(data)
        response = Response(data, status=status, mimetype='application/json')
        return response
    except Exception as ex:
        return internal_error(error=ex, status=500)


def internal_error(error=None, status=None):
    message = {
            'status': 500,
            'message': 'Internal error: ' + str(error),
    }
    data = json.dumps(message)
    response = Response(data, status=status, mimetype='application/json')
    return response


def all_customer_details(filter):
    if filter:
        result = {}
        cols = MYCOL.find_one({},{"_id":0})
        filt = filter.split('$')
        regex = "^" + filt[0] + ".*" + filt[1] + "$"

        for each in cols.keys():
            if re.match(regex, each):
                result[each]=cols[each]
        return result
    else:
        return customer_details()

def customer_details(key=None):
    if key:
        return MYCOL.find_one({},{"_id":0,key:1})
    else:
        return MYCOL.find_one({},{"_id":0})

if __name__ == '__main__':
    app.run(debug=False,host='0.0.0.0')
