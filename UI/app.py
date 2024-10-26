# importing Flask and other modules
import json
import os
import logging
import requests
from flask import Flask, request, render_template, jsonify

# Flask constructor
app = Flask(__name__)


# A decorator used to tell the application
# which URL is associated function
@app.route('/housing_predict/', methods=["GET", "POST"])
def housing_predict():
    if request.method == "GET":
        return render_template("input_form_page.html")

    elif request.method == "POST":
        prediction_input = [
            {
                "Median_Income": float(request.form.get("Median_Income")),  # getting input with name = ntp in HTML form
                "Median_Age": int(request.form.get("Median_Age")),  # getting input with name = pgc in HTML form
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

        # use requests library to execute the prediction service API by sending an HTTP POST request
        # use an environment variable to find the value of the diabetes prediction API
        # json.dumps() function will convert a subset of Python objects into a json string.
        # json.loads() method can be used to parse a valid JSON string and convert it into a Python Dictionary.
        predictor_api_url = os.environ['PREDICTOR_API']
        res = requests.post(predictor_api_url, json=json.loads(json.dumps(prediction_input)))

        prediction_value = res.json()['result']
        logging.info("Prediction Output : %s", prediction_value)
        return render_template("response_page.html",
                               prediction_variable=prediction_value)

    else:
        return jsonify(message="Method Not Allowed"), 405  # The 405 Method Not Allowed should be used to indicate
    # that our app that does not allow the users to perform any other HTTP method (e.g., PUT and  DELETE) for
    # '/checkdiabetes' path


# The code within this conditional block will only run the python file is executed as a
# script. See https://realpython.com/if-name-main-python/
if __name__ == '__main__':
    app.run(port=int(os.environ.get("PORT", 5000)), host='0.0.0.0', debug=True)
