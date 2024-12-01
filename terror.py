import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Function to authenticate and connect to Google Sheets API
def authenticate_google_sheets():
    # Define the scope of access required for Google Sheets and Google Drive
    scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]
    
    # Authenticate using the service account credentials file (replace with your actual file path)
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    return client

# Function to retrieve current balance from Google Sheet (cell A1)
def get_current_balance(sheet):
    # Get the current balance from cell A1
    balance = sheet.cell(1, 1).value  # Assuming balance is in cell A1 (row 1, column 1)
    
    try:
        return float(balance)
    except ValueError:
        # If the value in A1 isn't a valid float, return 0.0 as default
        return 0.0

# Function to update the balance in Google Sheet (cell A1)
def update_balance(sheet, new_balance):
    # Update the balance in cell A1
    sheet.update_cell(1, 1, new_balance)

# Function to update Google Sheet with the transaction details
def update_google_sheet(amount, sheet):
    # Get the current balance
    current_balance = get_current_balance(sheet)
    
    # Deduct the transaction amount
    new_balance = current_balance - amount
    
    # Update the balance in the sheet
    update_balance(sheet, new_balance)
    
    # Append the transaction to the transactions sheet (to record this transaction)
    sheet.append_row([amount, new_balance])  # You can add a timestamp or other details if needed
    
    st.success(f"Payment of ₹{amount} successful! Current Balance: ₹{new_balance}")

# Streamlit UI for user input 
def main():
    st.title("KMIT Canteen - Payment Portal")
    
    # Authenticate and get the Google Sheets client
    client = authenticate_google_sheets()
    
    # Open the specific Google Sheet (replace with your actual Google Sheet name)
    try:
        sheet = client.open("Nishkah").worksheet("Canteen_transaction")
    except Exception as e:
        st.error(f"Error accessing the Google Sheet: {e}")
        return
    
    # Show current balance on the UI
    current_balance = get_current_balance(sheet)
    st.write(f"Current balance: ₹ {current_balance} ")
    
    # Input form for transaction amount
    amount = st.number_input("Enter the amount: ", min_value=0, step=1)
    
    # Submit button
    if st.button("Submit Transaction"):
        if amount > 0:
            # Update Google Sheet with the provided data
            update_google_sheet(amount, sheet)
        else:
            st.warning("Please enter a positive amount for the transaction!")

if __name__ == "__main__":
    main()
