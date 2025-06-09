from flask import Flask, render_template, request, jsonify, redirect, url_for
import pickle
import pandas as pd
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Load model and CSV data once on startup
model = pickle.load(open('riskmodel.pkl', 'rb'))
df = pd.read_csv("eye_health_risk_dataset_10000.csv")  # For API/chart data

# ----------------- ROUTES -----------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/prediction_table.html')
def prediction_form():
    return render_template('prediction_table.html')

@app.route('/graphs')
def graphs():
    return render_template('graphs.html')

# UPDATED API ROUTE to send dataset + latest record
@app.route('/api/data')
def get_data():
    # Get latest record as dict
    latest_record = df.iloc[-1].to_dict()
    return jsonify({
        "dataset": df.to_dict(orient='records'),
        "latest": latest_record
    })


# ----------------- PREDICTION -----------------

@app.route('/predict', methods=['POST'])
def predict():
    try:
        name = request.form.get('name', 'User')
        age = float(request.form['age'])
        eye_pressure = float(request.form['eye_pressure'])
        vision_clarity = float(request.form['vision_clarity'])
        retina_thickness = float(request.form['retina_thickness'])
        cornea_health = float(request.form['cornea_health'])
        blood_pressure = float(request.form['blood_pressure'])
        blood_sugar = float(request.form['blood_sugar'])
        cholesterol = float(request.form['cholesterol'])
        screen_time = float(request.form['screen_time'])
        sleep_hours = float(request.form['sleep_hours'])

        input_data = [[
            age, eye_pressure, vision_clarity, retina_thickness, cornea_health,
            blood_pressure, blood_sugar, cholesterol, screen_time, sleep_hours
        ]]
        feature_names = [
            'age', 'eye_pressure', 'vision_clarity', 'retina_thickness', 'cornea_health',
            'blood_pressure', 'blood_sugar', 'cholesterol', 'screen_time', 'sleep_hours'
        ]
        input_df = pd.DataFrame(input_data, columns=feature_names)

        prediction = model.predict(input_df)
        prediction_proba = model.predict_proba(input_df)[0]

        risk_map = {0: "Low", 1: "Medium", 2: "High"}
        risk_class_map = {0: "low-risk", 1: "medium-risk", 2: "high-risk"}
        risk = risk_map[prediction[0]]
        result_class = risk_class_map[prediction[0]]

        prob_text = (
            f"Probabilities — "
            f"<strong>Low:</strong> {prediction_proba[0]:.2f}, "
            f"<strong>Medium:</strong> {prediction_proba[1]:.2f}, "
            f"<strong>High:</strong> {prediction_proba[2]:.2f}"
        )

        # Insert into MySQL
        try:
            connection = mysql.connector.connect(
                host='localhost',
                database='eye_risk_prediction',
                user='root',
                password='Indu@2003'
            )
            if connection.is_connected():
                cursor = connection.cursor()
                insert_query = '''
                INSERT INTO patients
                (name, age, eye_pressure, vision_clarity, retina_thickness, cornea_health,
                 blood_pressure, blood_sugar, cholesterol, screen_time, sleep_hours, risk_level)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                '''
                cursor.execute(insert_query, (
                    name, age, eye_pressure, vision_clarity, retina_thickness, cornea_health,
                    blood_pressure, blood_sugar, cholesterol, screen_time, sleep_hours, risk
                ))
                connection.commit()
                cursor.close()
        except Error as e:
            print("❌ MySQL Error:", e)
        finally:
            if connection.is_connected():
                connection.close()

        return render_template(
            'prediction_table.html',
            prediction_result=f"{name}'s Eye Risk Level: <strong>{risk}</strong>",
            result_class=result_class,
            prediction_probs=prob_text
        )

    except Exception as e:
        print("❌ Error during prediction:", str(e))
        return f"Error during prediction: {e}", 400


@app.route('/delete/<int:patient_id>', methods=['POST'])
def delete_patient(patient_id):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='eye_risk_prediction',
            user='root',
            password='Indu@2003'
        )
        cursor = connection.cursor()
        delete_query = "DELETE FROM patients WHERE id = %s"
        cursor.execute(delete_query, (patient_id,))
        connection.commit()
        cursor.close()
        connection.close()
        return redirect(url_for('recent'))
    except Exception as e:
        print("❌ Error deleting record:", e)
        return f"Error deleting record: {e}", 500


@app.route('/recent')
def recent():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='eye_risk_prediction',
            user='root',
            password='Indu@2003'
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM patients ORDER BY created_at DESC LIMIT 10")
        records = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('recent.html', records=records)
    except Exception as e:
        print("❌ Error fetching records:", str(e))
        return f"Error fetching records: {str(e)}", 500


if __name__ == '__main__':
    app.run(debug=True)
