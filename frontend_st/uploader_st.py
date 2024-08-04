import streamlit as st
import requests

user_name = st.text_input("User Name", "streamlit_user")
# file_name = st.text_input("File Name", "local_test.pdf")
uploaded_file = st.file_uploader(
    "Choose a file", type=["pdf"]
    )
# uploaded_file = {'file': open(file_name, 'rb')}

if st.button("Upload File"):
    if uploaded_file is not None:
        pdf_file = {'file': (uploaded_file.name, uploaded_file.read(), 'application/pdf')}
        file_name = uploaded_file.name
        upload_url_response = requests.post(
                "https://i0tt4mr1fh.execute-api.us-east-1.amazonaws.com/prod/uploadFile",
                json={"user": user_name, "filename": file_name},
        )
        # print(f"Upload URL response: {upload_url_response}")
        # print(upload_url_response.json()['url'])
        # print(upload_url_response.json()['fields'])
        r = requests.post(
                upload_url_response.json()['url'], 
                data=upload_url_response.json()['fields'], 
                files=pdf_file)
        st.write(r)
        listfiles_response = requests.post(
                "https://i0tt4mr1fh.execute-api.us-east-1.amazonaws.com/prod/listFiles",
                json={"user": user_name},
        )   
        
        st.write(listfiles_response.json())
        uploaded_file = None       