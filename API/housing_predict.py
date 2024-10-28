
import sklearn
import pickle
import json
import os
import pandas as pd
from flask import jsonify
import logging
from io import StringIO
import pandas as pd

# Create a DataFrame with your data
# #data = {
#     "Median_Income": [8.3252],
#     "Median_Age": [41],
#     "Tot_Rooms": [880],
#     "Tot_Bedrooms": [129],
#     "Population": [322],
#     "Households": [126],
#     "Latitude": [37.88],
#     "Longitude": [-122.23],
#     "Distance_to_coast": [9263.04077285038],
#     "Distance_to_LA": [556529.1583418],
#     "Distance_to_SanDiego": [735501.80698384],
#     "Distance_to_SanJose": [67432.5170008434],
#     "Distance_to_SanFrancisco": [21250.2137667799]
# }

# Convert the dictionary to a DataFrame
#df = pd.DataFrame(data)
def download_model(self):
    project_id = os.environ.get('PROJECT_ID', 'Specified environment variable is not set.')
    model_repo = os.environ.get('MODEL_REPO', 'Specified environment variable is not set.')
    model_name = os.environ.get('MODEL_NAME', 'Specified environment variable is not set.')
    client = storage.Client(project=project_id)
    bucket = client.bucket(model_repo)
    blob = bucket.blob(model_name)
    blob.download_to_filename('lr_model.pkl')
    self.model = load_model('lr_model.pkl')
    return jsonify({'message': " the model was downloaded"}), 200
class HousingPredictor:
    def __init__(self):
        self.model = None

    def predict_single_record(self, prediction_input):
        logging.debug(prediction_input)
        if self.model is None:
            try:
                file_path = 'lr_model.pkl'
                with open(file_path, 'rb') as file_path:    
                    self.model = pickle.load(file_path)
            except KeyError:
                print("MODEL_REPO is undefined")
                with open('lr_model.pkl', 'rb') as file_path:
                    self.model = pickle.load('lr_model.pkl')

        df = pd.read_json(StringIO(json.dumps(prediction_input)), orient='records')
        #df = pd.DataFrame([prediction_input])
        print(df)
        y_pred = self.model.predict(df)
        logging.info(y_pred[0])
        #print(f"Prediction Result: {y_pred[0]}")
        status = (y_pred[0] > 0.5)
        #logging.info(f"Prediction Status: {status}")
        # return the prediction outcome as a json message. 200 is HTTP status code 200, indicating successful completion
        return jsonify({'result': str(y_pred[0])}), 200
if __name__ == "__main__":
    
    logging.basicConfig(level=logging.DEBUG)


    
    predictor = HousingPredictor()
    result, status_code = predictor.predict_single_record(None)


    print(f"Housing price: {result}")
