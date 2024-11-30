import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os

# Initialize session state
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Login"
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False
if "name" not in st.session_state:
    st.session_state["name"] = None
if "rollnumber" not in st.session_state:
    st.session_state["rollnumber"] = None
if "email" not in st.session_state:
    st.session_state["email"] = None

# Authenticate with Google Sheets
def authenticate_google_sheets():
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        # Replace with the path to your JSON credentials file
        json_path = os.path.join(os.getcwd(), "credentials.json")

        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error authenticating with Google Sheets: {e}")
        return None

# Load credentials from Google Sheets
def load_credentials():
    try:
        client = authenticate_google_sheets()
        if not client:
            return pd.DataFrame()

        # Access the Google Sheet and worksheet
        sheet = client.open("Nishkah").sheet1  # Replace with worksheet name
        data = sheet.get_all_records()  # Fetch all data as a list of dictionaries
        df = pd.DataFrame(data)  # Converts to a DataFrame
        return df
    except Exception as e:
        st.error(f"Error loading credentials: {e}")
        return pd.DataFrame()

# Login functionality
def login():

    st.image("Nishkah_logo_withoutbg.png", width=90)  # Adjust width as needed

    st.title("Login to Nishkah")

    credentials = load_credentials()
    if credentials.empty:
        st.error("Could not load credentials. Please check your setup.")
        return

    rollnumber = st.text_input("Roll Number")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user_record = credentials[credentials["rollnumber"] == rollnumber]

        if user_record.empty:
            st.error("Invalid roll number.")
        else:
            stored_password = user_record.iloc[0]["password"]
            if stored_password == password:
                st.session_state["is_logged_in"] = True
                st.session_state["name"] = user_record.iloc[0]["name"]
                st.session_state["rollnumber"] = rollnumber
                st.session_state["email"] = user_record.iloc[0]["email"]
                st.session_state["current_page"] = "Dashboard"
                st.success("Login successful!")
            else:
                st.error("Invalid password.")

# Function to render the Profile page
def render_profile_page(name, rollnumber, email):
    st.title("Student Profile")
    st.write("Welcome to your profile!")
    st.write("### Profile Information")
    st.write(f"**Name:** {name}")
    st.write(f"**Roll Number:** {rollnumber}")
    st.write(f"**Email:** {email}")

    if st.button("Back to Dashboard"):
        st.session_state["current_page"] = "Dashboard"

# Function to render the Dashboard page
def render_dashboard_page(name):
    cols = st.columns([9, 1])
    with cols[1]:
        if st.button("Profile"):
            st.session_state["current_page"] = "Profile"
            
    st.title("Dashboard")
    st.write(f"Welcome, {name}!")
    st.markdown('<h1 class="header">Monthly Expenditure</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="subheader">Services</h2>', unsafe_allow_html=True)
    
    st.title("Payment Overview")

    st.write("Please enter the payment details below.")

    # Form for transaction input
    with st.form(key='transaction_form'):
        recipient = st.text_input("Vendor: ")
        amount_inr = st.number_input("Amount: ", min_value=0.01, format="%.2f")
        submit_button = st.form_submit_button("PAY")

    # Process the transaction when the form is submitted
    if submit_button:
        if recipient and amount_inr > 0:
            result = process_transaction(recipient, amount_inr)
            st.success(result)
        else:
            st.error("Please fill in all the fields with valid information.")

# Main application logic
def main():
    if not st.session_state.get("is_logged_in", False):
        st.session_state["current_page"] = "Login"

    if st.session_state["current_page"] == "Login":
        login()
    elif st.session_state["current_page"] == "Dashboard":
        render_dashboard_page(st.session_state["name"])
    elif st.session_state["current_page"] == "Profile":
        render_profile_page(
            st.session_state["name"],
            st.session_state["rollnumber"],
            st.session_state["email"],
        )
        
# Function to simulate the transaction
def process_transaction(recipient, amount_inr):
    # Simulate the transaction process
    return f"Transaction to {recipient} for ₹{amount_inr:,.2f} has been processed successfully!"

# Run the app
if __name__ == "__main__":
    main()

