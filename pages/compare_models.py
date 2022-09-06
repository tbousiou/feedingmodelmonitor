import streamlit as st
import pandas as pd



st.title("Compare Models")

df = pd.read_excel('models.xlsx')

model_names = list(df.columns)
print(model_names)

st.subheader("Select feeding model")
selected_model = st.selectbox('Select the feeding model from the list', model_names)

st.write('You selected:', selected_model)

selected_model_data = df[selected_model]
st.line_chart(selected_model_data)
print(selected_model_data)

st.subheader("Upload your data")
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    user_data = pd.read_excel(uploaded_file)
    plot_data = user_data.copy()
    plot_data['Model'] = selected_model_data
    # st.dataframe(user_data)
    st.line_chart(plot_data)

    means = user_data.mean()
    results = pd.DataFrame(means,columns=['Mean'])
    print(results)
    model_mean = selected_model_data.mean()
    print(model_mean)

    results['Diference'] = abs(results['Mean'] - model_mean)

    results['status'] = results['Diference'].apply(lambda x: 'OK' if x < 20 else 'ERROR')
    
    st.subheader("Compare model for each animal")
    st.write('This table shows which sheeps are in accordance with the model')

    st.dataframe(results)