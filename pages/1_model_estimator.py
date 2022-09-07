import streamlit as st
import pandas as pd
import numpy as np
from geopy.geocoders import Nominatim
from models import model1, model2
from database import init_connection

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

st.header("Step 1: Choose feeding model")
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

st.header("Step 2: Choose breed type")
selected_breed = st.selectbox('Select your breed type', breed_types)
model_bw_data = growth_data_file.parse(selected_breed,index_col=0)


st.header("Step 3: Upload your data")

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

    
    st.header("Step 4: Estimate model parameters")

    if selected_model_index == 0:
        
        st.markdown("""
        The following chart shows the DMI growth of the user data in comparison with the top and bottom acceptable percentiles. 
        
        **Click on +/- to change the model parameteres** to match the user curve somewhere between the top and bottomm percentiles""")

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

    
    st.header("Step 5: Submit your model")
    st.write("You can submit your model with the custom parameters to the database so other can use it.")
    st.warning('Please do not submit the same model twice!', icon="⚠️")

    st.subheader("Location")
    st.write("Type your location and click the Find button. Repeat until the location is correct")
    
    

    
    with st.form("location_form"):
        city = st.text_input("County, city, town, village", placeholder = "ex. Katerini, Pieria")
        country = st.text_input("Country", placeholder = "Greece")
        submitted1 = st.form_submit_button("Find location")
        if submitted1:
            geolocator = Nominatim(user_agent="feeding-model-app")
            location = geolocator.geocode(f"{city}, {country}")
            st.write("Acording to your data your location is:")
            st.write(location.address)
            st.write(f"Latitude: {location.latitude}, Longiture: {location.longitude}")
            st.info("Enter address again if the location is not correct, otherwise continue below to submit your model to the database")
            st.map(pd.DataFrame({'lat':[location.latitude],'lon':[location.longitude]}))

            # Save location info to session, required to pass this info to the next form
            st.session_state.location = location.address
            st.session_state.lat = location.latitude
            st.session_state.lon = location.longitude
            
    st.write("Enter your name and/or company name and click Submit")
    with st.form("model_form"):
        model_name = st.text_input("Your name, or company name")

        # Every form must have a submit button.
        submitted2 = st.form_submit_button("Submit")
        if submitted2:
            st.write(model_name)
            
            custom_model = dict()
            custom_model['model_name'] = model_name
            custom_model['location'] = st.session_state.location
            custom_model['lat'] = st.session_state.lat
            custom_model['lon'] = st.session_state.lon
            custom_model['base_type'] ="A"
            custom_model['pa'] = parameter_a
            custom_model['pb'] = parameter_b

            # custom_model
            try:
                supabase = init_connection()
                supabase.table("custom_models").insert(custom_model).execute()
                st.success("Model submited to the database", icon='👍')
            except:
                st.error("Something went wrong. Could connect or write to the database")

   # TODO
   # SETUP DATABASE SCHEMA
   # WRITE MODEL TO DATABASE




#parameter_a = st.number_input('Parameter a', min_value=1.0, max_value=20.0, value=15.36, step=0.5)
#parameter_b = st.number_input('Parameter b', min_value=0.001, max_value=0.003, value=0.0022, step=0.0001, format='%.4f')

