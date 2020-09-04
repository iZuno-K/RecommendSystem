import base64
import json
import logging

from flask import Flask, jsonify, request, Response, session

from six.moves import http_client

from flask import render_template

from make_response import make_response_two_ai
from boring import make_response_boring1, make_response_boring2

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def _base64_decode(encoded_str):
    # Add paddings manually if necessary.
    num_missed_paddings = 4 - len(encoded_str) % 4
    if num_missed_paddings != 4:
        encoded_str += b'=' * num_missed_paddings
    return base64.b64decode(encoded_str).decode('utf-8')


@app.route('/echo', methods=['POST'])
def echo():
    """Simple echo service."""
    message = request.get_json().get('message', '')
    return jsonify({'message': message})


@app.route('/post', methods=['POST'])
def post_json():
    json = request.get_json()  # Get POST JSON
    NAME = json['name']
    result = {
        "data": {
            "id": 1,
            "name": NAME
        }
    }
    return jsonify(result)


app.route('/hoge', methods=['POST'])


@app.errorhandler(http_client.INTERNAL_SERVER_ERROR)
def unexpected_error(e):
    """Handle exceptions by returning swagger-compliant json."""
    logging.exception('An error occured while processing the request.')
    response = jsonify({
        'code': http_client.INTERNAL_SERVER_ERROR,
        'message': 'Exception: {}'.format(e)})
    response.status_code = http_client.INTERNAL_SERVER_ERROR
    return response


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/2ai")
def index():
    return render_template("2ai.html")

@app.route("/boring1")
def boring1():
    return render_template("boring1.html")

@app.route("/boring2")
def boring2():
    return render_template("boring2.html")

@app.route('/postText', methods=['POST'])
def respond_two_ai():
    json_dict = request.json['talks']
    responses, _classes = make_response_two_ai(json_dict)
    return_data = {"responses": responses, "_classes": _classes}
    return jsonify(ResultSet=json.dumps(return_data))

@app.route('/boring1post', methods=['POST'])
def respond_boring_ai1():
    json_dict = request.json['talks']
    responses, _classes = make_response_boring1(json_dict)
    return_data = {"responses": responses, "_classes": _classes}
    return jsonify(ResultSet=json.dumps(return_data))

@app.route('/boring2post', methods=['POST'])
def respond_boring_ai2():
    json_dict = request.json['talks']
    responses, _classes = make_response_boring2(json_dict)
    return_data = {"responses": responses, "_classes": _classes}
    return jsonify(ResultSet=json.dumps(return_data))


if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='0.0.0.0')
