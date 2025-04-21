import requests
import json
import urllib3
import pandas as pd

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BaseUrl = ""
OpsRampSecret = ''  # Replace with your OpsRamp Secret
OpsRampKey = ''  # Replace with your OpsRamp Key

def create_site(data):
    token_url = BaseUrl + "auth/oauth/token"
    auth_data = {
        'client_secret': OpsRampSecret,
        'grant_type': 'client_credentials',
        'client_id': OpsRampKey
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    # Obtain access token
    token_response = requests.post(token_url, data=auth_data, headers=headers, verify=True)

    if token_response.status_code == 200:
        access_token = token_response.json().get('access_token')
        if access_token:
            auth_header = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
            api_endpoint = f'{BaseUrl}/api/v2/tenants/{data["Client_ID"]}/sites'

            payload ={

                    "name": data["Site_Name"]
                }
            
            response = requests.post(api_endpoint, headers=auth_header, json=payload, verify=True)
            
            if response.status_code == 200:
                print("Site created successfully.")
            else:
                print(f"Failed to create site. Status code: {response.status_code}, Response: {response.text}")

# Specify the correct path to your Excel file
excel_path = 'Site_creation.xlsx'
df = pd.read_excel(excel_path)

# Iterate through rows and call create_site function
for index, row in df.iterrows():
    create_site(row.to_dict())
