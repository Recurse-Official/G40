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

        #JSON credentials file
        json_path = os.path.join(os.getcwd(), "credentials.json")

        creds = ServiceAccountCredentials.from_json_keyfile_name(json_path, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"Error authenticating with Google Sheets: {e}")
        return None

# Loading credentials from Google Sheets
def load_credentials():
    try:
        client = authenticate_google_sheets()
        if not client:
            return pd.DataFrame()

        # Accessing the Google Sheet and worksheet
        sheet = client.open("Nishkah").sheet1
        data = sheet.get_all_records()  # Fetching all data as a list of dictionaries
        df = pd.DataFrame(data)  # Converting to a DataFrame
        return df
    except Exception as e:
        st.error(f"Error loading credentials: {e}")
        return pd.DataFrame()
    
# Function to simulate the transaction
def process_transaction(recipient, amount_inr):
    # Simulate the transaction process
    return f"Transaction to {recipient} for ₹{amount_inr:,.2f} has been processed successfully!"

# Login functionality
def login():

    # Nishkah logo
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, "Images", "Nishkah_logo_withoutbg.png")
    st.image(image_path, width=120)

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
                st.session_state["phone_number"] = user_record.iloc[0]["phone_number"]
                st.session_state["DOB"] = user_record.iloc[0]["DOB"]
                st.session_state["year"] = user_record.iloc[0]["year"]
                st.session_state["current_page"] = "Dashboard"
                st.success("Login successful!")
                st.write("Click on the login button again to enter your dashboard")
            else:
                st.error("Invalid password.")

# Function to render the Profile page
def render_profile_page(name, rollnumber, email, phone_number, DOB, year):

    # Sidebar
    st.sidebar.title(f"{name}")
    st.sidebar.selectbox(f"{rollnumber}", ["Settings", "About", "Sign Out"])

    st.title(f"{name}")
    st.write(f"### {rollnumber}")
    st.write(f"**Phone number:** {phone_number}")
    st.write(f"**Email:** {email}")
    st.write(f"**DOB:** {DOB}")
    st.write(f"**Year:** {year}")

    st.button("TRACK EXPENSES")

    if st.button("Back to Dashboard"):
        st.session_state["current_page"] = "Dashboard"

# Function to render the Dashboard page
def render_dashboard_page(name, rollnumber):
    cols = st.columns([9, 1])
    with cols[1]:
        if st.button("Profile"):
            st.session_state["current_page"] = "Profile"

    # Nishkah logo
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, "Images", "Nishkah_logo_withoutbg.png")
    st.image(image_path, width=120)

    # Sidebar
    st.sidebar.title(f"{name}")
    st.sidebar.selectbox(f"{rollnumber}", ["Settings", "About", "Sign Out"])

    st.title("Dashboard")
    st.write(f"### Welcome, {name}!")
    st.markdown('<h1 class="header">Monthly Expenditure</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="header">Services</h2>', unsafe_allow_html=True)

    # Adding QR code button to navigate to payment overview
    if st.button("QR Code"):
        st.session_state["current_page"] = "Payment Overview"

# Function to render the Payment overview page
def render_payment_overview(name, rollnumber):

    # Sidebar
    st.sidebar.title(f"{name}")
    st.sidebar.selectbox(f"{rollnumber}", ["Settings", "About", "Sign Out"])

    st.title("Payment Overview")
    st.write("Please enter the payment details below.")

    # Form for transaction input
    with st.form(key='transaction_form'):
        recipient = st.text_input("Vendor: ")
        amount_inr = st.number_input("Amount: ", min_value=0.01, format="%.2f")
        submit_button = st.form_submit_button("PAY")

    # Processes the transaction when the form is submitted
    if submit_button:
        if recipient and amount_inr > 0:
            result = process_transaction(recipient, amount_inr)
            st.success(result)
        else:
            st.error("Please fill in all the fields with valid information.")

    if st.button("Back to Dashboard"):
        st.session_state["current_page"] = "Dashboard"



# Main application logic
def main():
    if not st.session_state.get("is_logged_in", False):
        st.session_state["current_page"] = "Login"

    if st.session_state["current_page"] == "Login":
        login()
    elif st.session_state["current_page"] == "Dashboard":
        render_dashboard_page(st.session_state["name"], st.session_state["rollnumber"])
    elif st.session_state["current_page"] == "Profile":
        render_profile_page(
            st.session_state["name"],
            st.session_state["rollnumber"],
            st.session_state["email"],
            st.session_state["phone_number"],
            st.session_state["DOB"],
            st.session_state["year"],
        )
    elif st.session_state["current_page"] == "Payment Overview":
        render_payment_overview(st.session_state["name"], st.session_state["rollnumber"],)

# Runs the app
if __name__ == "__main__":
    main()


