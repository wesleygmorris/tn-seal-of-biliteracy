

import streamlit as st
from supabase import create_client, Client
import os
import pandas as pd
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt 
from dotenv import load_dotenv
import numpy as np

sns.set_theme(context='notebook', style='darkgrid', palette='deep', font='sans-serif', font_scale=1, color_codes=True, rc=None)
load_dotenv()

languages = ['Afar', 'Abkhazian', 'Afrikaans', 'Akan', 'Albanian', 'American Sign Language', 'Amharic', 'Arabic', 'Aragonese', 'Armenian', 'Assamese', 'Avaric', 'Avestan', 'Aymara', 'Azerbaijani', 'Bashkir', 'Bambara', 'Basque', 'Belarusian', 'Bengali', 'Bihari languages', 'Bislama', 'Tibetan', 'Bosnian', 'Breton', 'Bulgarian', 'Burmese', 'Catalan; Valencian', 'Czech', 'Chamorro', 'Chechen', 'Chinese', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic', 'Chuvash', 'Cornish', 'Corsican', 'Cree', 'Welsh', 'Czech', 'Danish', 'German', 'Divehi; Dhivehi; Maldivian', 'Dutch; Flemish', 'Dzongkha', 'Greek, Modern (1453-)', 'English', 'Esperanto', 'Estonian', 'Basque', 'Ewe', 'Faroese', 'Persian', 'Fijian', 'Finnish', 'French', 'Western Frisian', 'Fulah', 'Georgian', 'German', 'Gaelic; Scottish Gaelic', 'Irish', 'Galician', 'Manx', 'Greek, Modern (1453-)', 'Guarani', 'Gujarati', 'Haitian; Haitian Creole', 'Hausa', 'Hebrew', 'Herero', 'Hindi', 'Hiri Motu', 'Croatian', 'Hungarian', 'Armenian', 'Igbo', 'Icelandic', 'Ido', 'Sichuan Yi; Nuosu', 'Inuktitut', 'Interlingue; Occidental', 'Interlingua (International Auxiliary Language Association)', 'Indonesian', 'Inupiaq', 'Icelandic', 'Italian', 'Javanese', 'Japanese', 'Kalaallisut; Greenlandic', 'Kannada', 'Kashmiri', 'Georgian', 'Kanuri', 'Kazakh', 'Central Khmer', 'Kikuyu; Gikuyu', 'Kinyarwanda', 'Kirghiz; Kyrgyz', 'Komi', 'Kongo', 'Korean', 'Kuanyama; Kwanyama', 'Kurdish', 'Lao', 'Latin', 'Latvian', 'Limburgan; Limburger; Limburgish', 'Lingala', 'Lithuanian', 'Luxembourgish; Letzeburgesch', 'Luba-Katanga', 'Ganda', 'Macedonian', 'Marshallese', 'Malayalam', 'Maori', 'Marathi', 'Malay', 'Micmac', 'Macedonian', 'Malagasy', 'Maltese', 'Mongolian', 'Maori', 'Malay', 'Burmese', 'Nauru', 'Navajo; Navaho', 'Ndebele, South; South Ndebele', 'Ndebele, North; North Ndebele', 'Ndonga', 'Nepali', 'Dutch; Flemish', 'Norwegian Nynorsk; Nynorsk, Norwegian', 'Bokmål, Norwegian; Norwegian Bokmål', 'Norwegian', 'Occitan (post 1500)', 'Ojibwa', 'Oriya', 'Oromo', 'Ossetian; Ossetic', 'Panjabi; Punjabi', 'Persian', 'Pali', 'Polish', 'Portuguese', 'Pushto; Pashto', 'Quechua', 'Romansh', 'Romanian; Moldavian; Moldovan', 'Romanian; Moldavian; Moldovan', 'Rundi', 'Russian', 'Sango', 'Sanskrit', 'Sinhala; Sinhalese', 'Slovak', 'Slovak', 'Slovenian', 'Northern Sami', 'Samoan', 'Shona', 'Sindhi', 'Somali', 'Sotho, Southern', 'Spanish; Castilian', 'Albanian', 'Sardinian', 'Serbian', 'Swati', 'Sundanese', 'Swahili', 'Swedish', 'Tahitian', 'Tamil', 'Tatar', 'Telugu', 'Tajik', 'Tagalog', 'Thai', 'Tibetan', 'Tigrinya', 'Tonga (Tonga Islands)', 'Tswana', 'Tsonga', 'Turkmen', 'Turkish', 'Twi', 'Uighur; Uyghur', 'Ukrainian', 'Urdu', 'Uzbek', 'Venda', 'Vietnamese', 'Volapük', 'Welsh', 'Walloon', 'Wolof', 'Xhosa', 'Yiddish', 'Yoruba', 'Zhuang; Chuang', 'Chinese', 'Zulu']
hs_english_criteria = ['AAPPL, ESL (for ELs Only)', 'ACT Reading Portion', 'AP Literature', 
                    'Cambridge AICE Language & Literature', 'Dual Enrollment ELA Course', 
                    'IB English Language & Literature', 'SAT Evidence-Based Reading & Writing Sub-Part', 
                    'TNReady ELA EOC Assessments', 'WIDA ACCESS-Composite (for ELs only)']     
ms_english_criteria = ['8th Grade ELA or ELD grade of 85+ (Fall Semester)', "7th Grade ELA TN Ready score of 'On Track'+"]
world_criteria = ['AP World Language', 'ACTFL-Aligned Asses (AAPPL, STAMP4S, ALTA, etc.)', 'ASLPI', 'Cambridge AICE World Language', 'CEFR-Aligned Assessment', 'CLEP', 'Foreign Government\'s Language Exam', 'IB World Language', 'SLPI:ASL']
ms_world_criteria = ['8th Grade World Language Course grade of 85+', 'ACTFL-Aligned Asses (AAPPL, STAMP4S, ALTA, etc.)']
states = [ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
           'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
           'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
           'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
           'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY']
language_backgrounds = ['Current English Language Learner', 'Non-English Language Background Student/Native Speaker', 'Native English Speaker']
year = 2024

def init_connection():
    url = os.getenv('db_url')
    key = os.getenv('db_key')
    return create_client(url, key)

supabase = init_connection() 



def upload_school(package):
    data, count = supabase.table('schools').insert(package).execute()

def upload_package(table, package):
    return supabase.table(table).insert(package).execute()  

def show_students(school, year=False):
    students = supabase.table("recipients").select('*').eq('school_name', school).execute()
    students_df = pd.DataFrame(students.data)
    if len(students_df) == 0:
        st.write('No students currently registered for this school')
    else:
        
        if year:
            st.write(f'Students currently enrolled in {school} for {year}')
            st.dataframe(students_df[(students_df['year'] == year)].drop(['school_name'], axis=1).style.format({"Serial Number": "{}"}, precision=0))
        else:
            st.write(f'Students currently enrolled in {school}')
            st.dataframe(students_df.drop(['school_name'], axis=1).style.format({"Serial Number": "{}"}, precision=0))

def collect_prof_scores():
    st.write('World Language Proficiency Scores (Fill in only applicable boxes below)')
    d1,d2,d3,d4,d5 = st.columns(5)
    with d1:
        overall = st.text_input('Overall')
    with d2:
        speaking = st.text_input('Speaking')
    with d3:
        listening = st.text_input('Listening')
    with d4:
        reading = st.text_input('Reading')
    with d5:
        writing = st.text_input('Writing')
    return overall, speaking, listening, reading, writing

def contact_form():
    st.write('Contact Information')
    c1, c2 = st.columns(2)
    with c1:
        contact_first_name = st.text_input('First Name').lower()
    with c2:
        contact_last_name = st.text_input('Last Name').lower()
    contact_title = st.text_input('Title or Position').lower()
    contact_email = st.text_input('Email').lower()
    contact_phone_number = st.text_input('Phone Number')
    st.write('Mailing Address for Award')
    address_1 = st.text_input('Mailing Address 1')
    address_2 = st.text_input('Mailing Address 2')
    g1, g2, g3 = st.columns(3)
    with g1:
        city = st.text_input('City')
    with g2:
        state = st.selectbox('State', states)
    with g3:
        zip_code = st.text_input('Zip Code')
    st.write('School Information')
    h1, h2 = st.columns(2)
    with h1:
        title1 = st.radio('Is your school eligible for Title 1?', ['yes', 'no'])
    with h2:
        #st.write('Which year(s) has your school participated in the award program through the Volunteer State Seal of Biliteracy?')
        years = [i for i in range(2014, year)]
        awarded_last_year = st.multiselect('Which year(s) has your school participated in the award program through the Volunteer State Seal of Biliteracy?', years)
    i1, i2 = st.columns(2)
    with i1:
        school_location = st.selectbox('School Location', ['West Tennessee', 'Middle Tennessee', 'East Tennessee']).lower()
    with i2:
        school_type = st.selectbox('School Type', ['Public', 'Public Charter', 'Private / Independent']).lower()
    full_package = {'school_name':school, 'contact_first_name':contact_first_name, 'contact_last_name':contact_last_name,
                    'contact_title':contact_title, 'contact_email':contact_email, 'contact_phone_number':contact_phone_number,
                    'address_1':address_1, 'address_2':address_2, 'city':city, 'state':state, 'zip':zip_code,
                    'title1': title1, 'awarded_last_year':awarded_last_year, 'school_location':school_location, 'school_type':school_type}
    return full_package


def show_contact(info):     
    if len(info) > 0:
        info_df = pd.DataFrame(info).transpose()   
        info_df.columns = ['Info']
        st.dataframe(info_df)
    else:
        st.write('No current contact information')



# Build app
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

if st.sidebar.checkbox(":red[**Click this Checkbox to Login**]"):
    result = login_user(school, password)
    if result:
        st.success(f'Logged in as {school} for {year}')
        tab1, tab2, tab3 = st.tabs(["Submit Recipients", "Edit School Contact Information", "School Data"])
        
        # edit students tab
        with tab1:
            st.header("Edit Recipients")
            # first select the award
            st.write(f'Adding Recipients for {school} for {year}')
            level_of_award = st.selectbox('Level of Award', ['Pathway to Biliteracy for Middle Grades', 'Seal of Biliteracy', 'Seal of Bilingualism', 'Seal of Biliteracy Honors']).lower()
            add_button = st.checkbox('Add Students')
            if add_button:
                show_students(school=school, year=year)
                add_student, remove_student = st.tabs(["Add Student", "Remove Student"])
                # add student tab
                with add_student:
                    with st.form("new_recipient", clear_on_submit=True):
                        st.subheader('Add a Student to the Record')
                        c1, c2, c3 = st.columns(3)
                        with c1:
                            student_id = st.text_input('Recipient Student ID').lower()
                        with c2:
                            recipient_first_name = st.text_input('Recipient First Name').lower()
                        with c3:
                            recipient_last_name = st.text_input('Recipient Last Name').lower()

                        student_demographics = st.selectbox('Student Language Background', language_backgrounds).lower()
                        
                        if level_of_award == 'pathway to biliteracy for middle grades':
                            c3, c4, c5 = st.columns(3)
                            with c3:
                                academic_progress = st.selectbox('Graduates to High School', ['yes', 'no'])       
                            with c4:
                                english_proficiency_criteria = st.selectbox('ELA Criteria', ms_english_criteria).lower()
                            with c5:
                                english_proficiency_criteria_score = st.text_input('Score')
                            c6, c7 = st.columns(2)
                            with c6:
                                language_for_seal = st.multiselect('World Language for Seal', languages)
                            with c7:
                                language_proficiency_criteria = st.selectbox('World Language Proficiency Criteria', ms_world_criteria).lower()
                            overall, speaking, listening, reading, writing = collect_prof_scores()
                            volunteer_hours = ''
                            spring_semester = ''
                            rubric = st.number_input('Rubric')
                        
                        elif level_of_award in ['seal of biliteracy', 'seal of bilingualism', 'seal of biliteracy honors']:
                            c3, c4, c5 = st.columns(3)
                            with c3:
                                academic_progress = st.selectbox('ELA GPA', ['3+', '3.5+'])       
                            with c4:
                                english_proficiency_criteria = st.selectbox('English Proficiency Criteria', hs_english_criteria).lower()
                            with c5:
                                english_proficiency_criteria_score = st.text_input('English Proficiency Critera Score')
                            c6, c7 = st.columns(2)
                            with c6:
                                language_for_seal = st.multiselect('World Language for Seal', languages)
                            with c7:
                                language_proficiency_criteria = st.selectbox('World Language Proficiency Criteria', world_criteria).lower()
                            overall, speaking, listening, reading, writing = collect_prof_scores()
                            volunteer_hours = st.radio('10+ Documented Volunteer Hours, if applying for Honors', ['No', 'Yes'])
                            spring_semester = st.radio("Student will take a national assessment during spring semester and will not receive score by Ap. 15. \n Please be aware that this student should be listed as 'candidate' for the Seal until their score is verified and updated in the database.", ['No', 'Yes'])
                            rubric = ''
                        

                        # submit the new student information
                        submitted = st.form_submit_button("Submit")
                        if submitted:
                            update_data = {'school_name':school, 'year': year, 'student_id': student_id, 'first_name':recipient_first_name, 'last_name':recipient_last_name, 'linguistic_background':student_demographics,
                                        'level_of_award':level_of_award, 'academic_progress':academic_progress, 'english_proficiency_criteria':english_proficiency_criteria,
                                        'english_proficiency_criteria_score':english_proficiency_criteria_score, 'language_for_seal':language_for_seal, 'language_proficiency_criteria':language_proficiency_criteria,
                                        'language_overall':overall, 'language_speaking':speaking, 'language_listening': listening, 'language_reading':reading, 'language_writing':writing,
                                        'volunteer_hours':volunteer_hours, 'spring_semester': spring_semester, 'rubric':rubric}     
                            def upload_recipient(package):
                                    return supabase.table('recipients').insert(package).execute()  
                            upload_recipient(update_data)
                            # show the new students at the end.
                            show_students(school=school, year=year)
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
                            st.rerun()        
        
        # Add schools tab
        with tab2:
            add_school_output = {}
            st.header("Edit Mailing Address and Program Lead")
            st.write(f'Edit Mailing Address and Program Lead for {school}')
            view, edit = st.columns(2)
            info = supabase.table("contacts").select('*').eq('school_name', school).execute().data            
            with edit:
                st.subheader('New Contact Information')
                with st.form("new_contact", clear_on_submit=True):
                    full_package = contact_form()
                    # submit the new contact info
                    submitted = st.form_submit_button("Submit")
                    if submitted:
                        if len(info) > 0:
                            update_package = full_package
                            del update_package['school_name']
                            def update_table(update_package):
                                return supabase.table('contacts').update(update_package).eq('school_name',school).execute()
                            update_table(update_package)
                        else:
                            upload_package('contacts', full_package)
                        st.rerun()
            with view:
                st.subheader('Current Contact')
                show_contact(info)

        with tab3:
            st.header(f"All Data for {school}")
            st.write('Hover over spreadsheet to reveal download button')
            show_students(school=school)

        # tab for data and analysis
        # with tab3:
        #     st.header("Data")
        #     # get dataframes for all schools
        #     def get_data(table):
        #         data = supabase.table(table).select("*").execute().data
        #         return pd.DataFrame(data)
        #     schools_df = get_data('schools')
        #     recipients_df = get_data('recipients')
            
        #     dataframes, viz = st.tabs(["Dataframes", "Visualizations"])
        #     with dataframes:
        #         st.subheader('Dataframes')
        #         schools, recipients = st.tabs(['Schools', 'Recipients'])
        #         with schools:
        #             st.dataframe(schools_df)
        #         with recipients:
        #             st.dataframe(recipients_df)
            
        #     with viz:
        #         st.subheader('Visualization')
        #         tab1, tab2 = st.tabs(["Scores", "Languages"])
        #         with tab1:
        #             outcome = st.selectbox('Outcome', ['academic_progress', 'english_proficiency_criteria_score', 'language_criteria_score'])
        #             fig, ax = plt.subplots()
        #             sns.barplot(data=recipients_df, x='school_name', y=outcome, ci=None)
        #             plt.xlabel('School Name')
        #             plt.ylabel('Mean Score')
        #             st.pyplot(fig)
        #         with tab2:
        #             st.write('Language Representation')
        #             fig, ax = plt.subplots()
        #             sns.countplot(recipients_df, x='language_for_seal', ax=ax)
        #             plt.xlabel('World Language')
        #             st.pyplot(fig)
    else:
        st.warning('Incorrect password')



report = st.sidebar.text_area('This data entry tool is in testing. Please report any bugs or confusions when inputing test data', key='report_box')   

def clear_text():
    st.session_state["report_box"] = ""

submitted = st.sidebar.button("Submit", on_click=clear_text)
if submitted:
    package = {'report': report}
    upload_package('bug-reports', package)
    st.sidebar.write('Thank you for your feedback!!')