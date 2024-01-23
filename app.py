from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image #python image library
import google.generativeai as genai 

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
#genai.configure(api_key="AIzaSyB7GKVgv8B3nv7x-z9su4UDY_yKVKC9rzQ")

model= genai.GenerativeModel('gemini-pro-vision')

def get_gemini_response(input,image_data,user_prompt):
    response = model.generate_content([input,image_data[0],user_prompt])
    return response.text

def input_image_details(upload_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts = [{
            'mime_type':uploaded_file.type,
            'data':bytes_data
        }]
        return image_parts
    else:
        raise FileNotFoundError('No file uploaded')
    
st.header('Make New Story With Gemini-Vision-Pro')

input = st.text_input('write feeling',key='input')
uploaded_file=st.file_uploader('Image',type=['jpg','jpeg','png'])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption='uploaded File',use_column_width=True)

sub = st.button('generate story')

input_prompt = """you are expert in understanding feelings or emotion.
we will upload an image and you will have to make conversational story using 500 words based 
on the uploded image with using given input and give abstract of story in bold"""

input_prompt1="""Give story title based on image"""
if sub:
    with st.spinner('wait'):
        image_data = input_image_details(uploaded_file)
        response=get_gemini_response(input_prompt,image_data,input)
        newresponse=get_gemini_response(input_prompt1,image_data,input_prompt1)
        st.subheader(newresponse)
        st.text_area(label="",value=response,height=500)
