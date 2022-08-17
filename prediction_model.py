import joblib
import pandas as pd
import pickle
import string
import sklearn
import scipy
from pickle import load

# ----------------------------------------------------
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler

# ----------------------------------------------------
from lightgbm import LGBMClassifier

# ----------------------------------------------------


print('Tags transformer loaded.')
from scipy import sparse
import re
import numpy as np

class PredictionModel:
    MODEL_PATH = './model/model_10.pkl'
    SCALER_PATH = './model/scaler.pkl'
    # TAGS_PATH = './models/tags_list'
    
    def __init__(self) -> None:
        self._model = self.import_predict_model()
        self.scaler = load(open(self.SCALER_PATH, 'rb')) # load scaler
        pass
    def format_input(self, input_dict) -> pd.DataFrame:
        data = np.array([[input_dict['amt_annuity'], input_dict['ext_source_2'], input_dict['days_birth'],
        input_dict['ext_source_3'], input_dict['amt_credit'], input_dict['days_id_publish'],
        input_dict['days_employed'], input_dict['days_last_phone_change'],
        input_dict['days_registration'], input_dict['amt_goods_price']]])
        print("Print de format_input :\n", data)
        print(self.scaler.transform(data.astype(np.float)))
        return pd.DataFrame(self.scaler.transform(data.astype(np.float))).to_numpy()


    def predict(self, X):
        arr_results = []
        # preparation input
        formated_input = self.format_input(X)
        print('informative data :', formated_input)
        

        # prediction
        arr_results = self._model.predict_proba(formated_input) #.todense()

        # conversion vecteur en tags
        label = {'label_1':'good', 'score_1':float(arr_results[0][0]), 'label_2':'bad', 'score_2':float(arr_results[0][1])}
        print(f'label predicted :{label}')
        return label['score_1'], label['score_2']
    
    def import_predict_model(self):
        model = joblib.load(self.MODEL_PATH)
        return model

if __name__ =='__main__':
    test = PredictionModel()
    input_test = {}
    input_test['txt_question'] = 'Convert a Python list of lists to a single string'
    input_test['txt_body'] = "<p>I have list of lists consisting of chars and integers that I want to convert into a single string"
    test.predict(input_test)
