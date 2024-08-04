import requests

user_name="script_user"
file_name="local_test.pdf"

upload_url_response = requests.post(
    "https://i0tt4mr1fh.execute-api.us-east-1.amazonaws.com/prod/uploadFile",
    json={"user": user_name, "filename": file_name},
    )
print(f"Upload URL response: {upload_url_response}")
print(upload_url_response.json()['url'])
print(upload_url_response.json()['fields'])

files = {'file': open(file_name, 'rb')}
    
r = requests.post(
    upload_url_response.json()['url'], 
    data=upload_url_response.json()['fields'], 
    files=files)
print(r)                