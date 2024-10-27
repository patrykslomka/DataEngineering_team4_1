import os

from flask import Flask, request

from housing_predict import HousingPredictor

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/housing_predict/', methods=['PUT'])  # trigger updating the model
def refresh_model():
    return dp.download_model()


@app.route('/housing_predict/', methods=['POST'])  # path of the endpoint. Except only HTTP POST request
def predict_str():
    # the prediction input data in the message body as a JSON payload
    prediction_inout = request.get_json()
    return dp.predict_single_record(prediction_inout)


dp = HousingPredictor()
app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
