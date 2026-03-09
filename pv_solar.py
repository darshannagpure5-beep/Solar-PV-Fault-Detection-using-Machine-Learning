import pickle
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import os

st.title('🌞 Solar PV Fault Detection App')

st.info('This app predicts the fault type in Solar PV Panels using Machine Learning!')

# ===============================
# Load Dataset
# ===============================

with st.expander('Data'):

    file_path = r"C:\\Users\\darsh\\OneDrive\\Desktop\\Machine_learning_projects\\solar_pv_fault_dataset_500.xlsx"

    # df = pd.read_excel(file_path)

    st.write('**Raw data**')
    df = pd.read_excel(file_path)
    st.write(df)

    st.write('**X**')
    X_raw = df.drop('Panel_Class', axis=1)
    st.write(X_raw)

    st.write('**y**')
    y_raw = df.Panel_Class
    st.write(y_raw)


# ===============================
# Data Visualization
# ===============================

with st.expander('Data visualization'):

    st.scatter_chart(
        data=df,
        x='Irradiance',
        y='AC_Power_(W)',
        color='Panel_Class'
    )


# ===============================
# Input Features
# ===============================

with st.sidebar:

    st.header('Input Features')

    Irradiance = st.slider('Irradiance (W/m²)', 0, 1200, 600)
    Avg_Temperature = st.slider('Panel Temperature (°C)', 0, 80, 35)
    Humidity = st.slider('Humidity (%)', 0, 100, 50)
    PV_Current = st.slider('PV Current (A)', 0.0, 15.0, 5.0)
    AC_Voltage = st.slider('AC Voltage (V)', 0, 500, 230)
    AC_Current = st.slider('AC Current (A)', 0.0, 20.0, 5.0)
    AC_Power = st.slider('AC Power (W)', 0, 5000, 1500)
    DC_power = st.slider('DC Power (W)', 0, 5000, 1600)
    Efficiency = st.slider('Efficiency (%)', 0.0, 100.0, 85.0)
    avg_voltage = st.slider('Average Voltage', 0.0, 100.0, 40.0)

    # Create DataFrame for input
    data = {
        'Irradiance': Irradiance,
        'Avg_Temperature': Avg_Temperature,
        'Humidity_%': Humidity,
        'PV_Current_(A)': PV_Current,
        'AC_Voltage_(V)': AC_Voltage,
        'AC_Current_(A)': AC_Current,
        'AC_Power_(W)': AC_Power,
        'DC_power_(W)': DC_power,
        'Efficiency': Efficiency,
        'avg_voltage': avg_voltage
    }

    input_df = pd.DataFrame(data, index=[0])
    input_pv = pd.concat([input_df, X_raw], axis=0)


# ===============================
# Show Input Data
# ===============================

with st.expander('Input Features'):

    st.write('**Input Solar PV Data**')
    st.write(input_df)

    st.write('**Combined Dataset**')
    st.write(input_pv)


# ===============================
# Data Preparation
# ===============================

X = input_pv[1:]
input_row = input_pv[:1]

# Encode target
target_mapper = {
    'Clean': 0,
    'Dusty': 1,
    'Bird-drop': 2,
    'Electrical-damage': 3,
    'Physical-damage': 4,
    'Snow-covered': 5
}


def target_encode(val):
    return target_mapper[val]


y = y_raw.apply(target_encode)


with st.expander('Data Preparation'):

    st.write('**Encoded Input**')
    st.write(input_row)

    st.write('**Encoded Target**')
    st.write(y)


# ===============================
# Model Training
# ===============================
model = pickle.load(open("solar_fault_model.pkl", "rb"))


# ===============================
# Prediction
# ===============================

prediction = model.predict(input_row)
prediction_proba = model.predict_proba(input_row)


df_prediction_proba = pd.DataFrame(prediction_proba)

df_prediction_proba.columns = [
    'Clean',
    'Dusty',
    'Bird-drop',
    'Electrical-damage',
    'Physical-damage',
    'Snow-covered'
]


# ===============================
# Show Prediction
# ===============================

st.subheader('Fault Prediction Probability')

st.dataframe(
    df_prediction_proba,
    column_config={
        'Clean': st.column_config.ProgressColumn('Clean', min_value=0, max_value=1),
        'Dusty': st.column_config.ProgressColumn('Dusty', min_value=0, max_value=1),
        'Bird-drop': st.column_config.ProgressColumn('Bird-drop', min_value=0, max_value=1),
        'Electrical-damage': st.column_config.ProgressColumn('Electrical-damage', min_value=0, max_value=1),
        'Physical-damage': st.column_config.ProgressColumn('Physical-damage', min_value=0, max_value=1),
        'Snow-covered': st.column_config.ProgressColumn('Snow-covered', min_value=0, max_value=1)
    },
    hide_index=True
)


fault_types = np.array([
    'Clean',
    'Dusty',
    'Bird-drop',
    'Electrical-damage',
    'Physical-damage',
    'Snow-covered'
])

st.subheader('Predicted Fault Type')

st.success(str(fault_types[prediction][0]))

# ===================================
# accuracy
# ==================================

accuracy = pickle.load(open("accuracy.pkl", "rb"))

st.subheader("Model Performance")

st.metric("Model Accuracy", f"{round(accuracy*100,2)}%")


# ===============================
# Feature Importance
# ===============================

st.subheader("Feature Importance")

importance = model.feature_importances_

features = X_raw.columns

importance_df = pd.DataFrame({
    "Feature": features,
    "Importance": importance
})

importance_df = importance_df.sort_values(by="Importance", ascending=False)

st.bar_chart(importance_df.set_index("Feature"))
