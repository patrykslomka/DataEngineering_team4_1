# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__)


@app.route('/housing_predict/', methods=["GET", "POST"])
def housing_predict():
    if request.method == "GET":
        return render_template("input_form_page.html")

    elif request.method == "POST":
        prediction_input = [
            {
                "Median_Income": float(request.form.get("Median_Income")),
                "Median_Age": int(request.form.get("Median_Age")),
                "Tot_Rooms": int(request.form.get("Tot_Rooms")),
                "Tot_Bedrooms": float(request.form.get("Tot_Bedrooms")),
                "Households": float(request.form.get("Households")),
                "Latitude": int(request.form.get("Latitude")),
                "Population": int(request.form.get("Population")),
                "Longitude": float(request.form.get("Longitude")),
                "Distance_to_coast": float(request.form.get("Distance_to_coast")),
                "Distance_to_LA": float(request.form.get("Distance_to_LA")),
                "Distance_to_SanDiego": float(request.form.get("Distance_to_SanDiego")),
                "Distance_to_SanJose": float(request.form.get("Distance_to_SanJose")),
                "Distance_to_SanFrancisco": float(request.form.get("Distance_to_SanFrancisco"))
            }
        ]

        logging.debug("Prediction input : %s", prediction_input)

        predictor_api_url = os.getenv('PREDICTOR_API', 'http://default-api-url:5000/housing_predict/')

        try:
            res = requests.post(predictor_api_url, json=prediction_input)
            res.raise_for_status()  # Check for HTTP errors

            # Inspect response content before parsing
            logging.info("Status Code: %s", res.status_code)
            logging.info("Response Content: %s", res.text)

            prediction_value = res.json().get('result', 'No result found')
            logging.info("Prediction Output : %s", prediction_value)
            return render_template("response_page.html", prediction_variable=prediction_value)

        except requests.exceptions.JSONDecodeError:
            logging.error("Failed to decode JSON response. Response text: %s", res.text)
            return jsonify(message="Failed to retrieve prediction"), 500
        except requests.exceptions.RequestException as e:
            logging.error("API request error: %s", e)
            return jsonify(message="Error connecting to predictor API"), 500

    else:
        return jsonify(message="Method Not Allowed"), 405
