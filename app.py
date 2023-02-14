from flask import Flask, make_response, jsonify, request
from dbcreds import production_mode
from dbhelpers import run_statement

app = Flask(__name__)

@app.get('/api/candy')
def get_candy():
    result = run_statement("CALL get_candy")
    keys = ["title", "body"]
    response = []
    if (type(result) == list):
        for candy in result:
            response.append(dict(zip(keys, candy)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)

@app.post('/api/candy')
def add_candy():
    keys = ["title", "body"]
    post = request.json.get('title')
    body = request.json.get('body')
    if post == None:
        return "You must specify an item name."
    result = run_statement("CALL post_candy(?,?)", [post, body])
    response = []
    if (type(result) == list):
        for candy in result:
            response.append(dict(zip(keys, candy)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)

@app.patch('/api/candy')
def edit_candy():
    keys = ["title", "body"]
    post = request.json.get('title')
    body = request.json.get('body')
    if post == None:
        return "You must specify an item name."
    result = run_statement("CALL edit_candy(?,?)", [post, body])
    response = []
    if (type(result) == list):
        for candy in result:
            response.append(dict(zip(keys, candy)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)

@app.delete('/api/candy')
def delete_candy():
    keys = ["title", "body"]
    post = request.json.get('title')
    if post == None:
        return "You must specify an item Id."
    result = run_statement("CALL delete_candy(?)", [post])
    response = []
    if (type(result) == list):
        for candy in result:
            response.append(dict(zip(keys, candy)))
        return make_response(jsonify(response), 200)
    else:
        return make_response(jsonify(result), 500)



if (production_mode == True):
    print("Running server in production mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Running in testing mode")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)