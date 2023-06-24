import tkinter as tk
from tkinter import messagebox, ttk
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
import joblib

import pymysql
connection=pymysql.connect("localhost","root","123","heart_disease_prediction")
cursor=connection.cursor()

# Function to predict heart disease
def predict_heart_disease():
    try:
        age = float(age_entry.get())
        sex = float(sex_entry.get())
        cp = float(cp_entry.get())
        trestbps = float(trestbps_entry.get())
        chol = float(chol_entry.get())
        fbs = float(fbs_entry.get())
        restecg = float(restecg_entry.get())
        thalach = float(thalach_entry.get())
        exang = float(exang_entry.get())
        oldpeak = float(oldpeak_entry.get())
        slope = float(slope_entry.get())
        ca = float(ca_entry.get())
        thal = float(thal_entry.get())
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")
        return

    # Feature names
    feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

    # importing Trained model
    model = joblib.load("Trained_model.pkl")

    # Predicting heart disease for the input features
    input_data = pd.DataFrame([[age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal]], columns=feature_names)
    prediction = model.predict(input_data)

    # Displaying the prediction
    if prediction[0] == 0:
        messagebox.showinfo("Prediction Result", "No Heart Disease Detected")
    else:
        messagebox.showinfo("Prediction Result", "Heart Disease Detected")
    # Convert prediction value to Python integer
    prediction = int(prediction[0])
    
    # Inserting data into MySQL table
    try:
        insert_query = "INSERT INTO heart_data (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, target) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data = (age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal, prediction)
        cursor.execute(insert_query, data)
        connection.commit()
        messagebox.showinfo("Data Inserted", "Entered and predicted data inserted into the database.")
    except Exception as e:
        connection.rollback()
        messagebox.showerror("Error", f"An error occurred while inserting data into the database:\n{str(e)}")


# Creating the GUI window
window = tk.Tk()
window.title("Heart Disease Prediction")
window.geometry("400x600")
# Set the background color to light black (dark gray)
window.configure(background="#333333")

# Creating a gradient background
style = ttk.Style()
style.theme_use("clam")
style.configure("TFrame", background="#a8c0ff")
style.configure("TLabel", background="#a8c0ff")
style.configure("TButton", background="#007bff", foreground="white", font=("Helvetica", 14))

# Title
title_label = tk.Label(window, text="Heart Disease Prediction", font=("Helvetica", 16), bg="#a8c0ff")
title_label.pack(pady=10)

# Frame for input fields
input_frame = ttk.Frame(window)
input_frame.pack()

# Creating labels and entry fields for each feature
features = ['Age', 'Sex', 'Chest Pain', 'Resting BP', 'Cholesterol', 'Fasting Sugar', 'Resting ECG',
            'Max Heart Rate', 'Exercise Angina', 'ST Depression', 'Slope', 'Major Vessels', 'Thal']

entries = []
for i, feature in enumerate(features):
    label = ttk.Label(input_frame, text=feature + ':', font=("Helvetica", 12))
    label.grid(row=i, column=0, padx=10, pady=5)

    entry = ttk.Entry(input_frame, font=("Helvetica", 12))
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries.append(entry)

    # Assigning the entry widget to corresponding variables
    if feature == 'Age':
        age_entry = entry
    elif feature == 'Sex':
        sex_entry = entry
    elif feature == 'Chest Pain':
        cp_entry = entry
    elif feature == 'Resting BP':
        trestbps_entry = entry
    elif feature == 'Cholesterol':
        chol_entry = entry
    elif feature == 'Fasting Sugar':
        fbs_entry = entry
    elif feature == 'Resting ECG':
        restecg_entry = entry
    elif feature == 'Max Heart Rate':
        thalach_entry = entry
    elif feature == 'Exercise Angina':
        exang_entry = entry
    elif feature == 'ST Depression':
        oldpeak_entry = entry
    elif feature == 'Slope':
        slope_entry = entry
    elif feature == 'Major Vessels':
        ca_entry = entry
    elif feature == 'Thal':
        thal_entry = entry

# Button to predict heart disease
predict_button = ttk.Button(window, text="Predict Heart Disease", command=predict_heart_disease)
predict_button.pack(pady=10)

# Running the GUI window
window.mainloop()
