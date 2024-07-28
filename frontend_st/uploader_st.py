import streamlit as st
import requests

user_name = st.text_input("User Name", "streamlit_user")

uploaded_file = st.file_uploader(
    "Choose a file", accept_multiple_files=False, type=["pdf"]
    )
if uploaded_file is not None:
   
    file = uploaded_file.read()
    file_name = uploaded_file.name
    upload_url_response = requests.post(
            "https://i0tt4mr1fh.execute-api.us-east-1.amazonaws.com/prod/uploadFile",
            json={"user": user_name, "filename": file_name},
    )
    print(upload_url_response)
    print(upload_url_response.json()['url'])
    # print(upload_url_response.json()['fields'])
    r = requests.post(upload_url_response.json()['url'], data=upload_url_response.json()['fields'], files=uploaded_file)
    st.write(r.status_code)
    listfiles_response = requests.post(
            "https://i0tt4mr1fh.execute-api.us-east-1.amazonaws.com/prod/listFiles",
            json={"user": user_name},
    )   
    
    st.write(listfiles_response.json())   