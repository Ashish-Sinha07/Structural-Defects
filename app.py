import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# Configure the model
gemini_api_key = os.getenv('GEMINI-API-KEY-3')
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite')

# Lets create sidebar for image uploads
st.sidebar.title(':red[Upload the Images Here:]')
uploaded_img = st.sidebar.file_uploader('Image',type=['jpeg','png','jpg','jfif'],accept_multiple_files=True)
 
if uploaded_img:
    uploaded_img = Image.open(uploaded_img)
    st.sidebar.success('Image have been uploaded Successfully.')
    st.sidebar.subheader(':blue[Uploaded Images]')
    st.sidebar.image(uploaded_img)

# Lets Create the main page
st.title(':orange[STRUCTURAL DEFECT:-] :blue[AI Assisted Structural Defect Indentifier]')
st.markdown('### :green[ This application takes the images of the structural defect from the construction Images and detect the defects. ]')
title = st.text_input('Enter the title of the report:')
name = st.text_input('Enter the name of person who has prepare teh report.')
desig = st.text_input('Enter the designation who has prepare the report.')
orgz = st.text_input('Enter the name of organization.')


if st.button('Submit') : 
    with st.spinner('Processing......'):
        prompt = f'''
        <Role> You are an expert structural enginner with 20+ year experience in construction industry.
        <Goal> You need to preprare a detailed report on the structural defect shown in the images provide by the user.
        <Context> The images shared by user has been attached.
        <Format> Follow the steps to prepare the report:
        * Add title at the top of the report. The title provided by the user is {title}.
        * next add name, designationa and organization of the person who prepare the report
        also include the date. Followings are the detailed provided by the user:
        name: {name}
        designation: {desig} 
        organization: {orgz}
        date: {dt.datetime.now().date()}
        * Indentify and classify the defect for eg: crack,spalling, corossion, honeycombing,etc.
        * There could be more than one defect in images. Identify all the defects seperately.
        * For each defect identified ,provide a short description of the defect and its potential impact on the structure.
        * For each defect measure the sevearity of defect as low, medium or high. Also mentioning if defect is avoidable or inevited.
        * Provide short and long term solution for the repair along with estimated cost in INR and estimataed time it take.
        * What precautionary measure can to taken to avoid defect in the future.
        <Instructions>
        * Do not incude HTML foramat like <br> or any other formats.
        * The report generated in word format.
        * Use bullet points and tabular format wherever possible.
        * Make sure report does not exceed 3 pages.
        '''
    
        response = model.generate_content([prompt,uploaded_img],
                       generation_config={'temperature':0.7})
        st.write(response.text)

        if st.download_button(
            label='Click to Download',
            data = response.text,
            file_name='structural_defect_report.txt',
            mime='text/plain'
        ):
            st.success('Your File is Downloaded !!!')
        


