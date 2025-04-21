import requests
import json
import pandas as pd  # For reading the Excel file

BaseUrl = "https://netenrich.opsramp.com/"
key = "cHrCgP3TWVtv3EwMzah3hfjH34eXUHM8"
secret = "c55PPRzMPg3BWp5tXZMwwT8Gzpq6GmUbBwWnAfdhJZjmVHfXB59ZMM5rZY3kA5wf"

# Function to generate the token
def token_generation():
    tokenUrl = BaseUrl + "auth/oauth/token"
    auth = {
        'grant_type': 'client_credentials',
        'client_id': key,
        'client_secret': secret        
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    try:
        token_creation = requests.post(tokenUrl, data=auth, headers=headers, verify=True)
        token_creation.raise_for_status()  # Raises HTTPError for bad responses (4xx or 5xx)
        
        token = token_creation.json()
        print("Got the token")
        return token.get('access_token')
    
    except requests.exceptions.RequestException as e:
        print(f"Error during token generation: {e}")
        return None

# Function to create a device group
def groupcreation(access_token, clientID, device_uuids):
    try:
        auth_header = {'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json'}
        API_url = BaseUrl + f"api/v2/tenants/{clientID}/deviceGroups"
        
        # Build the search query from the device UUIDs
        search_query = "uuid IN ( " + " , ".join([f'\"{uuid}\"' for uuid in device_uuids]) + " )"
        
        payload = json.dumps([{
            "name": "UD_Group",
            "id" : "DGP-a9be3a6f-d213-4ebb-ac79-08b0bfde66fa",
            "entityType": "DEVICE_GROUP",
            "filterCriteria": {
                "matchType": "ALL",
                "rules": [],
                "searchQuery": search_query,
                "clientMatchingType": "ALL"
            }
        }])
        
        response = requests.post(API_url, headers=auth_header, data=payload)
        response.raise_for_status()  # Raises HTTPError for bad responses
        
        print(f"Response for client ID {clientID}: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error during group creation for client ID {clientID}: {e}")

# Read data from the Excel file and process the device UUIDs for each client
def read_excel_and_process(file_path):
    # Read the Excel file into a pandas DataFrame
    df = pd.read_excel(file_path, engine='openpyxl')
    
    # Ensure the Excel file has columns for 'clientID' and 'deviceUUID'
    if 'clientID' not in df.columns or 'deviceUUID' not in df.columns:
        print("Excel file must have 'clientID' and 'deviceUUID' columns.")
        return
    
    # Group device UUIDs by clientID
    grouped_data = df.groupby('clientID')['deviceUUID'].apply(list).reset_index()
    
    # Loop through each group (clientID and its corresponding device UUIDs)
    for index, row in grouped_data.iterrows():
        clientID = row['clientID']
        device_uuids = row['deviceUUID']
        
        # Generate the token and create the device group
        token = token_generation()
        if token:
            groupcreation(token, clientID, device_uuids)

# Example usage
if __name__ == "__main__":
    excel_file_path = "client_device_data.xlsx"  # Replace with your actual file path
    read_excel_and_process(excel_file_path)
