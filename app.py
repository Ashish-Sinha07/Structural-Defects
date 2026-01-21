import streamlit as st
import google.generativeai as genai
from PIL import Image
import datetime as dt
import os

# Configure the model
gemini_api_key = os.getenv('GEMINI-API-KEY-3') 
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash-lite') # Updated to a standard model name, change back if you have specific access

# Lets create sidebar for image uploads
st.sidebar.title(':red[Upload the Images Here:]')
uploaded_files = st.sidebar.file_uploader('Image', type=['jpeg','png','jpg','jfif'], accept_multiple_files=True)

# List to store the PIL images to send to Gemini
pil_image_list = []

if uploaded_files:
    st.sidebar.success('Images have been uploaded Successfully.')
    st.sidebar.subheader(':blue[Uploaded Images]')
    
    # Iterate through the list of uploaded files
    for file in uploaded_files:
        img = Image.open(file)
        pil_image_list.append(img)
        st.sidebar.image(img, caption=file.name)

# Lets Create the main page
st.title(':orange[STRUCTURAL DEFECT:-] :blue[AI Assisted Structural Defect Indentifier]')
st.markdown('### :green[ This application takes the images of the structural defect from the construction Images and detect the defects. ]')

title = st.text_input('Enter the title of the report:')
name = st.text_input('Enter the name of person who has prepare the report.')
desig = st.text_input('Enter the designation who has prepare the report.')
orgz = st.text_input('Enter the name of organization.')


if st.button('Submit'):
    # st.session_state.show()
    if not pil_image_list:
        st.error("Please upload at least one image.")
    else:
        with st.spinner('Processing...'):
            prompt = f'''
            <Role> You are an expert structural enginner with 20+ year experience in construction industry.
            <Goal> You need to preprare a detailed report on the structural defect shown in the images provide by the user.
            <Context> The images shared by user has been attached.
            <Format> Follow the steps to prepare the report:
            * Add title at the top of the report. The title provided by the user is {title}.
            * next add name, designationa and organization of the person who prepare the report
            also include the date. Followings are the detailed provided by the user:
            name: {name}
            desig: {desig} 
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
            
            # Combine the prompt string with the list of images
            # Gemini expects [prompt, image1, image2, image3...]
            input_content = [prompt] + pil_image_list

            try:
                response = model.generate_content(
                    input_content,
                    generation_config={'temperature':0.7}
                )
                st.write(response.text)

                st.download_button(
                    label='Click to Download',
                    data = response.text,
                    file_name='structural_defect_report.txt',
                    mime='text/plain'
                )
            except Exception as e:
                st.error(f"An error occurred: {e}")