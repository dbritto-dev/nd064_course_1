import logging

from flask import Flask, json


app = Flask(__name__)
app.debug = True


@app.route('/status')
def healthcheck():
    response = app.response_class(
        response=json.dumps({"result": "OK - healthy"}),
        status=200,
        mimetype='application/json'
    )

    # log line
    app.logger.info('Status request successfull')
    return response


@app.route('/metrics')
def metrics():
    response = app.response_class(
        response=json.dumps({"status": "success", "code": 0, "data": {
                            "UserCount": 140, "UserCountActive": 23}}),
        status=200,
        mimetype='application/json'
    )

    # log line
    app.logger.info('Metrics request successfull')
    return response


@app.route("/")
def hello():
    # log line
    app.logger.info('Main request successfull')

    return "Hello World!"


if __name__ == "__main__":

    # stream logs to app.log file
    logging.basicConfig(filename='app.log', level=logging.DEBUG)

    app.run(host='0.0.0.0')
