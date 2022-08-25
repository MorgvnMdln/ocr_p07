
from flask import Flask, render_template, redirect, url_for, request, jsonify
from werkzeug.wrappers import Request, Response

from prediction_model import PredictionModel


pred_model = PredictionModel()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard/')
def dashboard():
    return render_template("dashboard.html")

@app.route("/api/predict", methods=["GET", "POST"])

def predict():
    msg_data = {}
    arr_results = None

    for k in request.args.keys():
        val = request.args.get(k)
        msg_data[k] = val

    arr_results = pred_model.predict(msg_data)
    print(arr_results)
    return jsonify({
                    'status': 'ok',
                    'data': arr_results
                    })

if __name__ == "__main__":
    app.run()
