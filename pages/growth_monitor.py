import streamlit as st
import pandas as pd
import numpy as np



st.title('Dairy Heifer Growth monitor')
st.write('Compare and monitor Heifer growth with breed standards. Growth charts and references:')
"""
- https://extension.psu.edu/growth-charts-for-dairy-heifers
- https://lactanet.ca/en/growth-chart-by-breed/
"""


# Read excel file with growth charts
growth_data = pd.ExcelFile('data/growth_charts_1.xlsx')
# For each breed type there is a separate sheet
breed_types = growth_data.sheet_names  # see all sheet names

#xl.parse(sheet_name)  # read a specific sheet to DataFrame
st.subheader("Choose breed type")
option = st.selectbox('Select breed type', breed_types)

data = growth_data.parse(option,index_col=0)

st.write(f"The following chart shows the recommended range of body weight of {option} breed. For normal growth the weight must be between the bottom and top percentiles")
st.line_chart(data)


st.subheader("Upload your data")
st.write("Upload an excel file with body weight data growth of your animals. Each column must be a separate animal. Body weight sampling must be by month.")
st.write("")
st.write("Example data:")
example_data = pd.DataFrame(data={'col1': [60, 70, 80], 'col2': [62, 74, 84], 'col3': [58, 71, 89]})
st.table(example_data)

uploaded_file = st.file_uploader("Choose a file")



if uploaded_file is not None:
    user_data = pd.read_excel(uploaded_file,index_col=0)

    st.write('Your uploaded data growth chart')
    st.line_chart(user_data)
    
    animals = user_data.shape[1]
    st.subheader("Select animal to compare")
    selected_animal = st.slider('Select animal', min_value=1, max_value=animals, value=1, step=1)
   
    animal_data = user_data.iloc[:,selected_animal-1]

    data['compare'] = animal_data

    st.line_chart(data)
    # data.iloc[:,0] - animal_data
    mae1 = np.mean(np.abs((data.iloc[:,0]-animal_data)))
    mae2 = np.mean(np.abs((data.iloc[:,1]-animal_data)))
    treshold = 30
    (mae1,mae2)
    ok = (mae1 <= 10) or (mae2 <=10) or (mae1 <=treshold) and (mae2 <=treshold)
    if ok:
        st.subheader("Inside growth limits 😀")
    else:
        st.subheader("Outside growth limits 😨")


    #result = pd.concat([data, user_data], axis=1)

    #st.line_chart(result)