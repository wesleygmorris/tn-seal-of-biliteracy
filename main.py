import streamlit as st
from supabase import create_client, Client
import os
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt 
from dotenv import load_dotenv

sns.set_theme(context='notebook', style='darkgrid', palette='deep', font='sans-serif', font_scale=1, color_codes=True, rc=None)
load_dotenv()

languages = ['Afar', 'Abkhazian', 'Afrikaans', 'Akan', 'Albanian', 'American Sign Language', 'Amharic', 'Arabic', 'Aragonese', 'Armenian', 'Assamese', 'Avaric', 'Avestan', 'Aymara', 'Azerbaijani', 'Bashkir', 'Bambara', 'Basque', 'Belarusian', 'Bengali', 'Bihari languages', 'Bislama', 'Tibetan', 'Bosnian', 'Breton', 'Bulgarian', 'Burmese', 'Catalan; Valencian', 'Czech', 'Chamorro', 'Chechen', 'Chinese', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic', 'Chuvash', 'Cornish', 'Corsican', 'Cree', 'Welsh', 'Czech', 'Danish', 'German', 'Divehi; Dhivehi; Maldivian', 'Dutch; Flemish', 'Dzongkha', 'Greek, Modern (1453-)', 'English', 'Esperanto', 'Estonian', 'Basque', 'Ewe', 'Faroese', 'Persian', 'Fijian', 'Finnish', 'French', 'Western Frisian', 'Fulah', 'Georgian', 'German', 'Gaelic; Scottish Gaelic', 'Irish', 'Galician', 'Manx', 'Greek, Modern (1453-)', 'Guarani', 'Gujarati', 'Haitian; Haitian Creole', 'Hausa', 'Hebrew', 'Herero', 'Hindi', 'Hiri Motu', 'Croatian', 'Hungarian', 'Armenian', 'Igbo', 'Icelandic', 'Ido', 'Sichuan Yi; Nuosu', 'Inuktitut', 'Interlingue; Occidental', 'Interlingua (International Auxiliary Language Association)', 'Indonesian', 'Inupiaq', 'Icelandic', 'Italian', 'Javanese', 'Japanese', 'Kalaallisut; Greenlandic', 'Kannada', 'Kashmiri', 'Georgian', 'Kanuri', 'Kazakh', 'Central Khmer', 'Kikuyu; Gikuyu', 'Kinyarwanda', 'Kirghiz; Kyrgyz', 'Komi', 'Kongo', 'Korean', 'Kuanyama; Kwanyama', 'Kurdish', 'Lao', 'Latin', 'Latvian', 'Limburgan; Limburger; Limburgish', 'Lingala', 'Lithuanian', 'Luxembourgish; Letzeburgesch', 'Luba-Katanga', 'Ganda', 'Macedonian', 'Marshallese', 'Malayalam', 'Maori', 'Marathi', 'Malay', 'Micmac', 'Macedonian', 'Malagasy', 'Maltese', 'Mongolian', 'Maori', 'Malay', 'Burmese', 'Nauru', 'Navajo; Navaho', 'Ndebele, South; South Ndebele', 'Ndebele, North; North Ndebele', 'Ndonga', 'Nepali', 'Dutch; Flemish', 'Norwegian Nynorsk; Nynorsk, Norwegian', 'Bokmål, Norwegian; Norwegian Bokmål', 'Norwegian', 'Occitan (post 1500)', 'Ojibwa', 'Oriya', 'Oromo', 'Ossetian; Ossetic', 'Panjabi; Punjabi', 'Persian', 'Pali', 'Polish', 'Portuguese', 'Pushto; Pashto', 'Quechua', 'Romansh', 'Romanian; Moldavian; Moldovan', 'Romanian; Moldavian; Moldovan', 'Rundi', 'Russian', 'Sango', 'Sanskrit', 'Sinhala; Sinhalese', 'Slovak', 'Slovak', 'Slovenian', 'Northern Sami', 'Samoan', 'Shona', 'Sindhi', 'Somali', 'Sotho, Southern', 'Spanish; Castilian', 'Albanian', 'Sardinian', 'Serbian', 'Swati', 'Sundanese', 'Swahili', 'Swedish', 'Tahitian', 'Tamil', 'Tatar', 'Telugu', 'Tajik', 'Tagalog', 'Thai', 'Tibetan', 'Tigrinya', 'Tonga (Tonga Islands)', 'Tswana', 'Tsonga', 'Turkmen', 'Turkish', 'Twi', 'Uighur; Uyghur', 'Ukrainian', 'Urdu', 'Uzbek', 'Venda', 'Vietnamese', 'Volapük', 'Welsh', 'Walloon', 'Wolof', 'Xhosa', 'Yiddish', 'Yoruba', 'Zhuang; Chuang', 'Chinese', 'Zulu']
english_criteria = ['AAPPL, ESL (for ELs Only)', 'ACT Reading Portion', 'AP Literature', 
                    'Cambridge AICE Language & Literature', 'Dual Enrollment ELA Course', 
                    'IB English Language & Literature', 'SAT Evidence-Based Reading & Writing Sub-Part', 
                    'TNReady ELA EOC Assessments', 'WIDA ACCESS-Composite (for ELs only)']     
world_criteria = ['AP World Language', 'ACTFL-Aligned Asses (AAPPL, STAMP4S, ALTA, etc.)', 'ASLPI', 'Cambridge AICE World Language', 'CEFR-Aligned Assessment', 'CLEP', 'Foreign Government\'s Language Exam', 'IB World Language', 'SLPI:ASL']
states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']

def init_connection():
    url = os.getenv('db_url')
    key = os.getenv('db_key')
    return create_client(url, key)

supabase = init_connection() 



def upload_school(package):
    data, count = supabase.table('schools').insert(package).execute()

def upload_package(table, package):
    return supabase.table(table).insert(package).execute()  

st.image('./seal.jpg')

login_info = supabase.table("schools").select("school_name, password").execute()
schools = pd.DataFrame(login_info.data)

def login_user(username, password):
    if schools[schools['school_name']==username].iloc[0,1] == password:
        return True
    else:
        return False

school = st.sidebar.selectbox('School Name', list(schools['school_name']))
password = st.sidebar.text_input('Password', type='password')



if st.sidebar.checkbox("Login"):
    result = login_user(school, password)
    if result:
        st.success(f'Logged in as {school}')

        tab1, tab2, tab3 = st.tabs(["Edit School Contact Information", "Submit Recipients", "Data and Visualizations"])
        # Add schools tab
        with tab1:
            add_school_output = {}
            st.header("Edit Contact Info")
            st.write(f'Edit Contact Information for {school}')
            view, edit = st.columns(2)
            info = supabase.table("contacts").select('*').eq('school_name', school).execute().data 
            
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
                        if len(info) > 0:
                            update_package = {'contact_first_name':contact_first_name, 'contact_last_name':contact_last_name,
                                            'contact_title':contact_title, 'contact_email':contact_email, 'contact_phone_number':contact_phone_number}
                            def update_table(package):
                                return supabase.table('contacts').update(package).eq('school_name',school).execute()
                            update_table(update_package)
                        else:
                            update_package = {'school_name':school, 'contact_first_name':contact_first_name, 'contact_last_name':contact_last_name,
                                            'contact_title':contact_title, 'contact_email':contact_email, 'contact_phone_number':contact_phone_number}
                            upload_package('contacts', update_package)
                        st.rerun()
            with view:
                st.subheader('Current Contact')
                def show_contact():     
                    if len(info) > 0:
                        info_df = pd.DataFrame(info)[['contact_first_name', 'contact_last_name', 'contact_title', 'contact_email', 'contact_phone_number']].transpose()   
                        info_df.columns = ['Info']
                        st.dataframe(info_df)
                    else:
                        st.write('No current contact information')
                show_contact()

        # add edit students tab
        with tab2:
            st.header("Edit Recipients")
            # first select the school
            st.write(f'Adding Recipients for {school}')
            def show_students():
                students = supabase.table("recipients").select('*').execute()
                students_df = pd.DataFrame(students.data)
                students_df = students_df[students_df['school_name'] == school]   
                st.dataframe(students_df.drop(['school_name', 'created_at'], axis=1))
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
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        student_demographics = st.text_input('Student Demographics').lower()
                    level_of_award = st.selectbox('Level of Award', ['Pathway to Biliteracy for Middle Grades', 'Seal of Biliteracy', 'Seal of Bilingualism', 'Seal of Biliteracy Honors']).lower()
                    c3, c4, c5 = st.columns(3)
                    with c3:
                        ela_average = st.number_input('ELA Average')       
                    with c4:
                        english_proficiency_criteria = st.selectbox('English Proficiency Criteria', english_criteria).lower()
                    with c5:
                        english_proficiency_criteria_score = st.number_input('English Proficiency Critera Score')
                    c6, c7, c8 = st.columns(3)
                    with c6:
                        language_for_seal = st.multiselect('World Language for Seal', languages)
                    with c7:
                        language_proficiency_criteria = st.selectbox('Language Proficiency Criteria', world_criteria).lower()
                    with c8:
                        language_criteria_score = st.number_input('Language Criteria Score')
                    volunteer_hours = st.radio('OPTIONAL: 10+ Documented Volunteer Hours, if applying for Honors', ['Yes', 'No'])
                    spring_semester = st.radio('Student will take a national assessment during spring semester and will not receive score by Ap. 15', ['Yes', 'No'])
                    # submit the new student information
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        update_data = {'school_name':school, 'recipient_first_name':recipient_first_name, 'recipient_last_name':recipient_last_name, 'student_demographics':student_demographics,
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
    else:
        st.warning('Incorrect password')

