import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="⭕")


st.warning("## 🚧 This app is under construction 🚧")

# Title of the main page
st.title("Feeding model application")

st.header("Intro")
'''
This application consists of three separate tools:
* **Growth monitor**: Monitor the body weight growth of your animals and compare it with the recommended growth.
* **Feeding models map and catalogue**: Explore custom feeding models that other users have created.
* **Model estimator**: Create a custom model to meet your requirements.
* **Find model**: Find a model suitable for your requirements.

More instructions you will find at the page of each tool.
'''


st.header("How to use this app")
'''
Use the growth monitor tool to monitor the growth of your animals. You compare the growth against the standard ideal feeding
models or a custom model created by another user. To find more info about the custom models use the models map and catalogue tool.
Finally you can create your custom model and submit it to the database using the model estimator tool.
'''


st.header("About")
'''
This app is part of the Atlas programe blah blah blah ...

### Team 
- **Supervisor**: Thomas Kotsopoulos, Professor, Aristotle University of Thessaloniki
- **Research**: Vasilis Firfiris
- **Developer**: Theodoros Bousiou, Data Scientist, Develooper

### Licence
This work is licensed under the xxxx licence

'''