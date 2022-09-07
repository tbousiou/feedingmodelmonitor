import streamlit as st
from supabase import create_client, Client

# Initialize connection.
# Uses st.experimental_singleton to only run once.


@st.experimental_singleton
def init_connection():
    url = st.secrets["supabase_url"]
    key = st.secrets["supabase_key"]
    return create_client(url, key)








# import sqlite3


# def get_user_models():
#     connection = sqlite3.connect("data.db")
#     connection.row_factory = sqlite3.Row

#     cursor = connection.cursor()

#     results = cursor.execute("SELECT * FROM user_models").fetchall()

#     cursor.close()
#     connection.close()

#     return results

