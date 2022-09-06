import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from models import model1, model2


st.set_page_config(
     page_title="Model Estimator",
     page_icon="📊")

st.title('Dairy Heifer Model Prameter Estimator')
st.write('Estimate parameters from various feeding models to specific farmer requirements')


m1 = model1()
m2 = model2()

base_models = [m1, m2]

# Section 1 - Choose base feeding models
model_names = [m1.name, m2.name]

st.subheader("1. Choose feeding model")
selected_model_name = st.selectbox('Select the base feeding model', model_names)
selected_model_index = model_names.index(selected_model_name)
base_model = base_models[selected_model_index]
st.latex(base_model.latex)
st.write(f"Default model parameters a = {base_model.a}, b={base_model.b}")


# Section 2 - Select breed type and show BW and DMI graphs

# Read excel file with growth charts
growth_data_file = pd.ExcelFile('data/growth_charts_1.xlsx')
# For each breed type there is a separate sheet
breed_types = growth_data_file.sheet_names  # see all sheet names

st.subheader("2. Choose breed type")
selected_breed = st.selectbox('Select your breed type', breed_types)
model_bw_data = growth_data_file.parse(selected_breed,index_col=0)




# bw_model = model_data.iloc[:,0]
# dmi_model = base_model.dmicalc(bw_model)


st.subheader("3. Upload your data")


st.markdown("""Upload a **spreadsheet** file with body weight data growth of all your animals.
The app will **calculate the average of all animals** and use this in the model estimation.
Each column must be a separate animal. Body weight sampling must be by **month** and you must have **exactly 24 rows** of data.""")

st.write("Example data:")
example_data = pd.DataFrame(data={'animal1': [60, 70, 80], 'animal2': [62, 74, 84], 'animal3': [58, 71, 89]})
st.table(example_data)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    user_bw_data = pd.read_excel(uploaded_file,index_col=0)
    # calculate average of every animal
    user_bw_data_mean=user_bw_data.mean(axis=1)
    
    estimator_bw = model_bw_data
    estimator_bw['user'] = user_bw_data_mean

    # st.write("BW growth")
    # st.line_chart(estimator_bw)

    
    st.subheader("4. Estimate model parameters")

    if selected_model_index == 0:
        
        st.write("The following chart shows the comparison of model and user DMI growth")
        st.write("Change the model parameters to match the ideal DMI boundaries")
        parameter_a = st.number_input('Parameter a', min_value=1.0, max_value=20.0, value=15.36, step=0.5)
        parameter_b = st.number_input('Parameter b', min_value=0.001, max_value=0.003, value=0.0022, step=0.0001, format='%.4f')
        base_model = model1()
        user_model = model1("User model from base 1",a=parameter_a,b=parameter_b)

        

        estimator_dmi = estimator_bw.apply(lambda x: base_model.dmicalc(x))
        estimator_dmi['user'] = estimator_bw['user'].apply(lambda x: user_model.dmicalc(x))
        #estimator_dmi
        # st.write(f"The following chart shows the ideal body weight growth of {breed_option} breed. For normal growth the weight must be between the bottom and top percentiles")
        st.line_chart(estimator_dmi)
        
    else:
        user_model = model1("User base 2")

    
    st.subheader("5. Submit your model")
    st.write("First help us to validate your location")

    with st.form("location_form"):
        city = st.text_input("City", placeholder = "Katerini")
        country = st.text_input("Country", placeholder = "Greece")
        submitted = st.form_submit_button("Find location")
        if submitted:
            geolocator = Nominatim(user_agent="feeding-model-app")
            location = geolocator.geocode(f"{city}, {country}")
            st.write("Acording to your data your location is:")
            st.write("Enter address again if these are wrong, otherwise continue below to submit your model to the database")
            st.write(location)
            st.write(location.latitude, location.longitude)
            st.map(pd.DataFrame({'lat':[location.latitude],'lon':[location.longitude]}))
            

    with st.form("model_form"):
        st.write("Inside the form")
        model_name = st.text_input("Your name, or company name")

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write(model_name)

   # TODO
   # SETUP DATABASE SCHEMA
   # WRITE MODEL TO DATABASE




#parameter_a = st.number_input('Parameter a', min_value=1.0, max_value=20.0, value=15.36, step=0.5)
#parameter_b = st.number_input('Parameter b', min_value=0.001, max_value=0.003, value=0.0022, step=0.0001, format='%.4f')

