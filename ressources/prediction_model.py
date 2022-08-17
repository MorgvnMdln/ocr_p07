import joblib
import pandas as pd
import pickle
import string
import sklearn
import scipy

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
    # TAGS_PATH = './models/tags_list'
    
    def __init__(self) -> None:
        self._model = self.import_predict_model()
        pass
    def format_input(self, input_dict) -> pd.DataFrame:
        scaler=MinMaxScaler()
        data = np.array([[input_dict['amt_annuity'], input_dict['ext_source_2'], input_dict['days_birth'],
        input_dict['ext_source_3'], input_dict['amt_credit'], input_dict['days_id_publish'],
        input_dict['days_employed'], input_dict['days_last_phone_change'],
        input_dict['days_registration'], input_dict['amt_goods_price']]])
        return pd.DataFrame(scaler.fit_transform(data.astype(np.float)))
    
    def predict(self, X):
        arr_results = []
        # preparation input
        formated_input = self.format_input(X)
        print('informative data :', formated_input)
        
        # prediction
        arr_results = self._model.predict(formated_input)#.todense()
        
        # conversion vecteur en tags
        label = "bad" if arr_results[0] == 1 else "good"
        print('tags predicted :', label)
        return label
    
    def import_predict_model(self):
        model = joblib.load(self.MODEL_PATH)
        return model

if __name__ =='__main__':
    test = PredictionModel()
    input_test = {}
    input_test['txt_question'] = 'Convert a Python list of lists to a single string'
    input_test['txt_body'] = "<p>I have list of lists consisting of chars and integers like this:</p><pre><code>list = [[65], [119, 'e', 's', 'i'], [111, 'd', 'l'], [111, 'l', 'w'], [108, 'd', 'v', 'e', 'i'], [105, 'n'], [97, 'n'], ['111', 'k', 'a']]</code></pre><p>I want to convert this into a single string like this:</p><pre><code>&quot;65 119esi 111dl 111lw 108dvei 105n 97n 111ka&quot;</code></pre><p>I have tried this:</p><pre><code>new_list = [' '.join(x for x in list)]</code></pre><p>but it is giving me this error:</p><pre><code>TypeError: sequence item 0: expected str instance, list found</code></pre><p>So what am i supposed to do, I'm new to coding!</p>"
    test.predict(input_test)
