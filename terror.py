#edit google sheets

#pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib gspread oauth2client streamlit

'''import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
'''
import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

# Function to authenticate and connect to Google Sheets API
def authenticate_google_sheets():
    # Define the scope of access required for Google Sheets and Google Drive
    scope = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
    
    # Authenticate using the service account credentials file (replace with your actual file path)
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    return client

# Function to update Google Sheet with user input
def update_google_sheet(amount):
    # Authenticate and get the Google Sheets client
    client = authenticate_google_sheets()
    
    try:
        # Open the specific Google Sheet by its name (replace with your actual Google Sheet name)
        sheet = client.open("Nishkah").worksheet("Canteen_transaction")
        
        # Append the data to the sheet (assuming you want to add data to the first available row)
        sheet.append_row([amount])
        st.success("Payment to KMIT Canteen done successfully! ")
    except Exception as e:
        st.error(f"Error updating Google Sheet: {e}")

# Streamlit UI for user input
def main():
    st.title("KMIT Canteen")
    
    # Input form for user
    
    amount = st.number_input("Enter the amount in rupees: ", min_value=0, step=1)
    
    # Submit button
    if st.button("Submit"):
        if amount >= 0:
            # Update Google Sheet with the provided data
            update_google_sheet(amount)
        else:
            st.warning("Please fill in both fields!")

if __name__ == "__main__":
    main()
