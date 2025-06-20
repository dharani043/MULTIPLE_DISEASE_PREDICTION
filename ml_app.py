
import pickle
import streamlit as st
from streamlit_option_menu import option_menu
from fpdf import FPDF
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Health Assistant", layout="wide", page_icon="🧑‍⚕️")


model_paths = {
    "diabetes": "Diabetes_prediction_trained_model.sav",
    "heart": "Heart_Disease_prediction_trained_model.sav",
    "parkinsons": "Parkinson_prediction_trained_model.sav",
    "insurance": "Medical_insurance_prediction_trained_model.sav",
    "breast": "Breast_cancer_prediction_trained_model.sav",
    "calories": "Calories_burnt_prediction_trained_model.sav"
}

models = {key: pickle.load(open(path, 'rb')) for key, path in model_paths.items()}

st.markdown("""
    <h1 style='text-align: center; color: #0A74DA;'>💼 Health Prediction Assistant</h1>
    <h4 style='text-align: center; color: #444;'>Powered by Machine Learning</h4>
    <hr style='border: 1px solid #0A74DA;'>
""", unsafe_allow_html=True)

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4320/4320425.png", width=100)
    selected = option_menu(
        menu_title="Disease Predictor",
        options=[
            "Diabetes", "Heart Disease", "Parkinsons",
            "Insurance Charges", "Breast Cancer", "Calories Burnt"
        ],
        icons=["activity", "heart", "person", "currency-dollar", "droplet", "flame"],
        default_index=0,
        menu_icon="hospital",
        orientation="vertical"
    )

def export_results(result_str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.multi_cell(0, 10, result_str)
    pdf_buffer = BytesIO()
    pdf_buffer.write(pdf.output(dest='S').encode('latin1'))
    pdf_buffer.seek(0)
    st.download_button("📄 Download PDF", data=pdf_buffer.getvalue(), file_name="prediction_result.pdf")

if selected == "Diabetes":
    st.subheader("🌿 Diabetes Prediction")
    inputs = []
    input_labels = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']
    for label in input_labels:
        value = st.text_input(label)
        if value:
            try:
                inputs.append(float(value))
            except:
                st.warning(f"Please enter a valid number for {label}")

    if st.button("Predict"):
        if len(inputs) == len(input_labels):
            prediction = models['diabetes'].predict([inputs])[0]
            result = 'The person is diabetic.' if prediction == 1 else 'The person is not diabetic.'
            st.success(result)
            export_results(result)
        else:
            st.warning("Please fill in all fields correctly.")

elif selected == "Heart Disease":
    st.subheader("💓 Heart Disease Prediction")
    fields = ['Age', 'Sex', 'Chest Pain', 'RestBP', 'Cholesterol', 'FBS', 'RestECG', 'Max HR', 'Exang', 'Oldpeak', 'Slope', 'CA', 'Thal']
    inputs = []
    for label in fields:
        value = st.text_input(label)
        if value:
            try:
                inputs.append(float(value))
            except:
                st.warning(f"Please enter a valid number for {label}")

    if st.button("Predict"):
        if len(inputs) == len(fields):
            prediction = models['heart'].predict([inputs])[0]
            result = 'The person has heart disease.' if prediction == 1 else 'No heart disease detected.'
            st.success(result)
            export_results(result)
        else:
            st.warning("Please fill in all fields correctly.")

elif selected == "Parkinsons":
    st.subheader("🌟 Parkinson's Disease Prediction")
    fields = ["MDVP:Fo(Hz)", "MDVP:Fhi(Hz)", "MDVP:Flo(Hz)", "MDVP:Jitter(%)", "MDVP:Jitter(Abs)",
              "MDVP:RAP", "MDVP:PPQ", "Jitter:DDP", "MDVP:Shimmer", "MDVP:Shimmer(dB)",
              "Shimmer:APQ3", "Shimmer:APQ5", "MDVP:APQ", "Shimmer:DDA", "NHR", "HNR",
              "RPDE", "DFA", "spread1", "spread2", "D2", "PPE"]
    inputs = []
    for field in fields:
        value = st.text_input(field)
        if value:
            try:
                inputs.append(float(value))
            except:
                st.warning(f"Invalid input for {field}")

    if st.button("Predict"):
        if len(inputs) == len(fields):
            prediction = models['parkinsons'].predict([inputs])[0]
            result = "Parkinson's detected." if prediction == 1 else "No Parkinson's disease."
            st.success(result)
            export_results(result)
        else:
            st.warning("Please fill in all fields correctly.")

elif selected == "Insurance Charges":
    st.subheader("💰 Medical Insurance Cost Prediction")
    age = st.text_input("Age")
    sex = st.selectbox("Sex", ["male", "female"])
    bmi = st.text_input("BMI")
    children = st.text_input("Children")
    smoker = st.selectbox("Smoker", ["yes", "no"])
    region = st.selectbox("Region", ["southwest", "southeast", "northwest", "northeast"])

    map_vals = {
        "male": 1, "female": 0,
        "yes": 1, "no": 0,
        "southwest": 0, "southeast": 1, "northwest": 2, "northeast": 3
    }

    if st.button("Predict"):
        try:
            features = [float(age), map_vals[sex], float(bmi), float(children), map_vals[smoker], map_vals[region]]
            prediction = models['insurance'].predict([features])[0]
            result = f"Estimated Insurance Charge: ${prediction:.2f}"
            st.success(result)
            export_results(result)
        except:
            st.warning("Please enter valid numeric values.")

elif selected == "Breast Cancer":
    st.subheader("🧬 Breast Cancer Prediction")
    st.caption("Input 30 features extracted from tumor mass")
    cols = st.columns(3)
    features = []
    for i in range(30):
        col = cols[i % 3]
        val = col.text_input(f"Feature {i+1}")
        if val:
            try:
                features.append(float(val))
            except:
                st.warning(f"Feature {i+1} should be a number")

    if st.button("Predict"):
        if len(features) == 30:
            prediction = models['breast'].predict([features])[0]
            result = "Malignant Tumor" if prediction == 0 else "Benign Tumor"
            st.success(result)
            export_results(result)
        else:
            st.warning("Please fill all 30 features with valid numbers.")

elif selected == "Calories Burnt":
    st.subheader("🔥 Calories Burnt Prediction")
    gender = st.selectbox("Gender", ["Male", "Female"])
    age = st.text_input("Age")
    height = st.text_input("Height (cm)")
    weight = st.text_input("Weight (kg)")
    duration = st.text_input("Exercise Duration (min)")
    heart_rate = st.text_input("Heart Rate")
    body_temp = st.text_input("Body Temperature (°C)")

    gender_val = 1 if gender == "Male" else 0

    if st.button("Predict"):
        try:
            features = [
                gender_val,
                float(age), float(height), float(weight),
                float(duration), float(heart_rate), float(body_temp)
            ]
            prediction = models['calories'].predict([features])[0]
            result = f"Estimated Calories Burnt: {prediction:.2f} kcal"
            st.success(result)
            export_results(result)
        except:
            st.warning("Please enter all values correctly.")
st.markdown("""
    <style>
    .footer {
        bottom: 0;
        width:100%;
        color: black;
        text-align: center;
        padding: 10px 0;
    }
    </style>
    <div class="footer">
        Made with ❤️ by <b>Dharani</b>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .footer {
        left: 0;
        bottom: 0;
        width: 100%;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }

    .footer a {
        color: black;
        text-decoration: none;
        margin: 0 10px;
        font-weight: bold;
    }

    .footer a:hover {
        text-decoration: underline;
    }
    </style>

    <div class="footer">
        <a href="https://github.com/dharani043" target="_blank">GitHub</a> &nbsp; | &nbsp;
        <a href="https://www.linkedin.com/in/dharanishankar-s-bb20ba290?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app " target="_blank">LinkedIn</a> &nbsp; | &nbsp;
        © 2025
    </div>
""", unsafe_allow_html=True)
