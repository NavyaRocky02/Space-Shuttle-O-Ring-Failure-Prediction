# Step 1. Flask Application

import joblib
import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# Load trained machine learning model
model = joblib.load("space_shuttle_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    try:
        number_of_o_rings = float(request.form["Number_of_O_Rings"])
        temperature = float(request.form["Temperature"])
        pressure = float(request.form["Pressure"])
        flight_number = float(request.form["Flight_Number"])

        input_data = pd.DataFrame([[
            number_of_o_rings,
            temperature,
            pressure,
            flight_number
        ]], columns=[
            "Number_of_O_Rings",
            "Temperature",
            "Pressure",
            "Flight_Number"
        ])

        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0][1] * 100

        if prediction == 1:
            result = "O-Ring Distress Predicted"
        else:
            result = "No O-Ring Distress Predicted"

        return render_template(
            "index.html",
            result=result,
            probability=round(probability, 2)
        )

    except Exception as e:
        return f"Prediction Error: {e}"


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )