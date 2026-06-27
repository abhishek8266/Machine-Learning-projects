import streamlit as st
import joblib
import numpy as np

model = joblib.load("house_price_model.pkl")

st.title("🏠 House Price Prediction")

st.write("Enter house details")

lot_area = st.number_input("Lot Area")
overall_qual = st.number_input("Overall Quality")
year_built = st.number_input("Year Built")
gr_liv_area = st.number_input("Ground Living Area")


if st.button("Predict Price"):

    input_data = np.array(
        [[
            lot_area,
            overall_qual,
            year_built,
            gr_liv_area
        ]]
    )

    prediction = model.predict(input_data)

    st.success(
        f"Estimated House Price: ${prediction[0]:,.2f}"
    )


