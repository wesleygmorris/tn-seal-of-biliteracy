import streamlit as st
from supabase import create_client, Client
import os
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt 
from dotenv import load_dotenv

save=''

sns.set_theme(context='notebook', style='darkgrid', palette='deep', font='sans-serif', font_scale=1, color_codes=True, rc=None)
load_dotenv()

def init_connection():
    url = os.getenv('db_url')
    key = os.getenv('db_key')
    return create_client(url, key)

supabase = init_connection() 

def upload_school(package):
    data, count = supabase.table('schools').insert(package).execute()

def upload_package(table, package):
    return supabase.table(table).insert(package).execute()  
states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

 
def find_schools():
    return supabase.table("schools").select("school_name").execute()

schools =[i['school_name'] for i in find_schools().data]

st.image('./seal.jpg')
tab1, tab2, tab3 = st.tabs(["Add School", "Edit Recipients", "Data and Visualizations"])
# Add schools tab
with tab1:
    add_school_output = {}
    st.header("Edit Schools")
    add_schools, edit_contact = st.tabs(["Add School", "Edit Contact Information"])
    # Add schools subtab
    with add_schools:
        with st.form("new_school", clear_on_submit=True):
            # Collect information
            c1, c2 = st.columns(2)
            with c1:
                contact_first_name = st.text_input('Contact First Name').lower()
            with c2:
                contact_last_name = st.text_input('Contact Last Name').lower()
            contact_title = st.text_input('Contact Title or Position').lower()
            contact_email = st.text_input('Contact Email').lower()
            contact_phone_number = st.text_input('Contact Phone Number')
            participate_as = st.selectbox('I am applying to participate as a:', ['School', 'District', 'Network of Schools'])
            level = st.multiselect('I am applying to participate at the ____ level(s)', ['Middle Grades', 'High School', 'Post-Secondary'])
            school_name = st.text_input('Participating School, Network, or District Name').lower()
            st.subheader('School/District Mailing Address')
            school_address_1 = st.text_input("Address Line 1").lower()
            school_address_2 = st.text_input("Address Line 2").lower()
            c3, c4, c5 = st.columns(3)
            with c3:
                school_city = st.text_input('City').lower()
            with c4:
                school_state = st.selectbox('State', states)
            with c5:
                school_zip = st.text_input('Zip Code')
            school_title_I = st.radio('Is your school designated as Title I or Title I eligible?', ['Yes', 'No'])
            school_goals = st.text_area('What are your goals in offering the award program in your community?').lower()
            # Submit information
            submitted = st.form_submit_button("Submit")
            if submitted:
                # Validate fields - Required
                required = [contact_first_name, contact_last_name, contact_title, contact_email, contact_phone_number, participate_as, level, 
                            school_name, school_address_1, school_city, school_state, school_zip, school_title_I, school_goals]
                if any(not i for i in required):
                    st.write('Please make sure that all fields are filled in.')
                else:
                    upload_data = {'contact_first_name': contact_first_name, 'contact_last_name':contact_last_name, 'contact_title':contact_title, 
                            'contact_email':contact_email, 'contact_phone_number':contact_phone_number, 'participate_as':participate_as, 'level':str(level), 
                            'school_name':school_name, 'school_address_1':school_address_1, 'school_address_2':school_address_2, 
                            'school_city':school_city, 'school_state':school_state, 'school_zip':school_zip, 'school_title_I':school_title_I, 
                            'school_goals':school_goals}
                    
                    def check_school_name(name):
                        data, count = supabase.table('schools').select('*').eq('school_name', name).execute()
                        if len(data) > 0:
                            return False
                        else:
                            return True                   
                    if check_school_name(school_name):
                        data, count = upload_package('schools', upload_data)
                    else:
                        st.write(f'The school {school_name} is already in the system.')
    # edit contact information
    with edit_contact:
        st.subheader('Edit Contact Information')
        school_selection = st.selectbox('Please select your school', schools, key='edit_contact_school_selection')
        view, edit = st.columns(2)
        with edit:
            st.subheader('New Contact Information')
            with st.form("new_contact", clear_on_submit=True):
                c1, c2 = st.columns(2)
                with c1:
                    contact_first_name = st.text_input('First Name').lower()
                with c2:
                    contact_last_name = st.text_input('Last Name').lower()
                contact_title = st.text_input('Title or Position').lower()
                contact_email = st.text_input('Email').lower()
                contact_phone_number = st.text_input('Phone Number')
                # submit the new contact info
                submitted = st.form_submit_button("Submit")
                if submitted:
                    update_package = {'contact_first_name':contact_first_name, 'contact_last_name':contact_last_name,
                                    'contact_title':contact_title, 'contact_email':contact_email, 'contact_phone_number':contact_phone_number}
                    def update_table(package):
                        return supabase.table('schools').update(package).eq('school_name',school_selection).execute()
                    update_table(update_package)
        # view school contact
        with view:
            st.subheader('Current Contact')
            def show_contact():
                info = supabase.table("schools").select('*').eq('school_name', school_selection).execute().data 
                info_df = pd.DataFrame(info)[['contact_first_name', 'contact_last_name', 'contact_title', 'contact_email', 'contact_phone_number']].transpose()   
                info_df.columns = ['Info']
                st.dataframe(info_df)
            show_contact()
# add edit students tab
with tab2:
    st.header("Edit Recipients")
    # first select the school
    school_option = st.selectbox('Please select your school', schools, key='edit_students_school_selection')
    def show_students():
        students = supabase.table("recipients").select('*').eq('school_name', school_option).execute() 
        students_df = pd.DataFrame(students.data).drop(['school_name', 'created_at'], axis=1)   
        st.dataframe(students_df)
    show_students()
    
    add_student, remove_student = st.tabs(["Add Student", "Remove Student"])
    # add student tab
    with add_student:
        with st.form("new_recipient", clear_on_submit=True):
            st.subheader('Add a Student to the Record')
            c1, c2 = st.columns(2)
            with c1:
                recipient_first_name = st.text_input('Recipient First Name').lower()
            with c2:
                recipient_last_name = st.text_input('Recipient Last Name').lower()
            student_demographics = st.text_input('Student Demographics').lower()
            level_of_award = st.text_input('Level of Award').lower()
            c3, c4, c5 = st.columns(3)
            with c3:
                ela_average = st.number_input('ELA Average')
            with c4:
                english_proficiency_criteria = st.text_input('English Proficiency Criteria').lower()
            with c5:
                english_proficiency_criteria_score = st.number_input('English Proficiency Critera Score')
            c6, c7, c8 = st.columns(3)
            with c6:
                language_for_seal = st.text_input('World Language for Seal').lower()
            with c7:
                language_proficiency_criteria = st.text_input('Language Proficiency Criteria').lower()
            with c8:
                language_criteria_score = st.number_input('Language Criteria Score')
            volunteer_hours = st.radio('OPTIONAL: 10+ Documented Volunteer Hours, if applying for Honors', ['Yes', 'No'])
            spring_semester = st.radio('Student will take a national assessment during spring semester and will not receive score by Ap. 15', ['Yes', 'No'])
            # submit the new student information
            submitted = st.form_submit_button("Submit")
            if submitted:
                update_data = {'school_name':school_option, 'recipient_first_name':recipient_first_name, 'recipient_last_name':recipient_last_name, 'student_demographics':student_demographics,
                            'level_of_award':level_of_award, 'ela_average':ela_average, 'english_proficiency_criteria':english_proficiency_criteria,
                            'english_proficiency_criteria_score':english_proficiency_criteria_score, 'language_for_seal':language_for_seal, 'language_proficiency_criteria':language_proficiency_criteria,
                            'language_criteria_score':language_criteria_score, 'volunteer_hours':volunteer_hours, 'spring_semester': spring_semester}     
                def upload_recipient(package):
                        return supabase.table('recipients').insert(package).execute()  
                upload_recipient(update_data)
                # show the new students at the end.
                show_students()
    # remove students tab
    with remove_student:
        st.subheader('Remove a Student from the Record')
        with st.form('remove_recipient', clear_on_submit=True):
            remove_number = st.number_input('Please select ID of student to remove', step=1)
            submitted = st.form_submit_button("Submit")
            if submitted:
                def remove_student(num):
                    data, count = supabase.table('recipients').delete().eq('id', num).execute()
                remove_student(remove_number)    
                show_students()
# tab for data and analysis
with tab3:
    st.header("Data")
    # get dataframes for all schools
    def get_data(table):
        data = supabase.table(table).select("*").execute().data
        return pd.DataFrame(data)
    schools_df = get_data('schools')
    recipients_df = get_data('recipients')
    
    dataframes, viz = st.tabs(["Dataframes", "Visualizations"])
    with dataframes:
        st.subheader('Dataframes')
        schools, recipients = st.tabs(['Schools', 'Recipients'])
        with schools:
            st.dataframe(schools_df)
        with recipients:
            st.dataframe(recipients_df)
    
    with viz:
        st.subheader('Visualization')
        tab1, tab2 = st.tabs(["Scores", "Languages"])
        with tab1:
            outcome = st.selectbox('Outcome', ['ela_average', 'english_proficiency_criteria_score', 'language_criteria_score'])
            fig, ax = plt.subplots()
            sns.barplot(data=recipients_df, x='school_name', y=outcome, ci=None)
            plt.xlabel('School Name')
            plt.ylabel('Mean Score')
            st.pyplot(fig)
        with tab2:
            st.write('Language Representation')
            fig, ax = plt.subplots()
            sns.countplot(recipients_df, x='language_for_seal', ax=ax)
            plt.xlabel('World Language')
            st.pyplot(fig)
            
