import streamlit as st
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import pandas as pd
load_dotenv()

# Initialize connection.
# Uses st.cache_resource to only run once.

def init_connection():
    url = os.getenv('db_url')
    key = os.getenv('db_key')
    return create_client(url, key)

supabase = init_connection()

school_option = 'Glencliff High School'

def find_students():
    return supabase.table("recipients").select('*').eq('school_name', school_option).execute()
students_df = pd.DataFrame(find_students().data)

edited_df = st.data_editor(students_df, num_rows="dynamic")

def click():
    st.dataframe(edited_df) 

st.button('Save', on_click=click())