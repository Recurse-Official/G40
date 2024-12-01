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

        # JSON credentials file
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

# Sidebar function to handle the navigation and sign-out functionality
def render_sidebar(name, rollnumber):
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, "Elements", "Profile_Icon.png")
    st.sidebar.image(image_path, width=120)
    st.sidebar.title(f"{name}")
    option = st.sidebar.selectbox(f"{rollnumber}", ["Settings", "About", "Sign Out",])

    # Check if "Sign Out" is selected
    if option == "Sign Out":
        st.session_state["is_logged_in"] = False
        st.session_state["name"] = None
        st.session_state["rollnumber"] = None
        st.session_state["email"] = None
        st.session_state["phone_number"] = None
        st.session_state["DOB"] = None
        st.session_state["year"] = None
        st.session_state["current_page"] = "Login"
        st.success("You have been logged out successfully!")
        return True  # Return True to indicate the user logged out
    return False  # Return False if no sign out action

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
                st.write("Click on the login button again to enter into your dashboard")
            else:
                st.error("Invalid password.")

# Function to render the Profile page
def render_profile_page(name, rollnumber, email, phone_number, DOB, year):

    # Sidebar
    if render_sidebar(name, rollnumber):
        return  # Return after logging out

    st.title(f"{name}")
    st.write(f"### {rollnumber}")
    st.write(f"**Phone number:** {phone_number}")
    st.write(f"**Email:** {email}")
    st.write(f"**DOB:** {DOB}")
    st.write(f"**Year:** {year}")

    if st.button("TRACK EXPENSES"):
        st.session_state["current_page"] = "MY EXPENSES"

    if st.button("Back to Dashboard"):
        st.session_state["current_page"] = "Dashboard"

# Function to render the Dashboard page
def render_dashboard_page(name, rollnumber):
    cols = st.columns([8, 1])
    with cols[1]:
        # Nishkah logo
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, "Elements", "Profile_Icon.png")
        st.image(image_path, width=80)
        if st.button("Profile"):
            st.session_state["current_page"] = "Profile"

    # Nishkah logo
    current_dir = os.getcwd()
    image_path = os.path.join(current_dir, "Images", "Nishkah_logo_withoutbg.png")
    st.image(image_path, width=120)

    # Sidebar
    if render_sidebar(name, rollnumber):
        return  # Return after logging out

    st.title("Dashboard")
    st.write(f"### Welcome, {name}!")
    st.write(" ")

    col11, col12 = st.columns(2)

    with col11:
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, "Elements", "Campus.png")
        st.image(image_path, caption="Campus", width=220)

    with col12:
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, "Elements", "Coupons.png")
        st.image(image_path, caption="My Coupons", width=200)

    # Services
    st.markdown('<h1 class="header">Services</h2>', unsafe_allow_html=True)
    st.write(" ")

    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)

    # Service icons as buttons
    with col1:
        image_path = os.path.join(current_dir, "Elements", "Canteen.png")
        st.image(image_path, width=100)
        if st.button("Canteen", key="canteen"):
            st.session_state["current_page"] = "CANTEEN"
    with col2:
        image_path = os.path.join(current_dir, "Elements", "Stationery.png")
        st.image(image_path, width=75)
        if st.button("Stationery", key="stationery"):
            st.session_state["current_page"] = "STATIONERY"
    with col3:
        image_path = os.path.join(current_dir, "Elements", "Library.png")
        st.image(image_path, width=80)
        if st.button("Library", key="library"):
            st.session_state["current_page"] = "Library"
    with col4:
        image_path = os.path.join(current_dir, "Elements", "Sports.png")
        st.image(image_path, width=90)
        if st.button("Sports", key="sports"):
            st.session_state["current_page"] = "Sports"
    with col5:
        image_path = os.path.join(current_dir, "Elements", "Laundry.png")
        st.image(image_path, width=90)
        if st.button("Laundry", key="laundry"):
            st.session_state["current_page"] = "Laundry"
    with col6:
        image_path = os.path.join(current_dir, "Elements", "Events.png")
        st.image(image_path, width=90)
        if st.button("Events", key="events"):
            st.session_state["current_page"] = "Events"

    st.write(" ")
    st.write(" ")
    st.write(" ")
    st.write(" ")

    # Adding QR code button to navigate to payment overview
    if st.button("QR Code"):

        #canteen payment portal: runs on .8504
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, "QR_code", "canteen_qr.png")
        st.image(image_path,caption="Canteen", width=300)

        #stationery payment portal: runs on .8502
        current_dir = os.getcwd()
        image_path = os.path.join(current_dir, "QR_code", "stationery_qr.png")
        st.image(image_path,caption="Stationery", width=300)

# Function to render track the expenses
def render_track_expenses(name, rollnumber):

    # Sidebar
    if render_sidebar(name, rollnumber):
        return  # Return after logging out

    st.title("MY EXPENSES")
    st.write("### This Month")

    if st.button("Back to Profile"):
        st.session_state["current_page"] = "Profile"

# Function to render the Canteen page
def render_canteen(name, rollnumber):

    #Sidebar
    if render_sidebar(name, rollnumber):
        return  # Return after logging out
    
    st.title("CANTEEN")

    st.write("### Your Top Picks")
    st.number_input("Peri Peri Fries: 80 Nishkah", min_value=0, step=1)
    st.number_input("Aloo Toast: 40 Nishkah", min_value=0, step=1)
    st.number_input("Tawa Pav: 60 Nishkah", min_value=0, step=1)

    st.write(" ")
    st.write(" ")

    st.write("### Bestsellers")
    st.number_input("Manchuria: 40 Nishkah", min_value=0, step=1)
    st.number_input("Mix Veg Pasta: 50 Nishkah", min_value=0, step=1)
    st.number_input("Fried Rice: 40 Nishkah", min_value=0, step=1)
    st.number_input("Pav Bhaji: 60 Nishkah", min_value=0, step=1)
    st.number_input("Paani Puri: 30 Nishkah", min_value=0, step=1)

    st.write(" ")
    st.write(" ")

    st.button("PROCEED")

    st.write(" ")
    st.write(" ")

    if st.button("Back to Dashboard"):
        st.session_state["current_page"] = "Dashboard"

# Function to render the Stationery page
def render_stationery(name, rollnumber):

    #Sidebar
    if render_sidebar(name, rollnumber):
        return  # Return after logging out
    
    st.title("STATIONERY")

    st.write("### Frequently purchased")
    st.number_input("200 Pages Long Unruled Notebook: 40 Nishkah", min_value=0, step=1)
    st.number_input("Colour Xerox (per page): 05 Nishkah", min_value=0, step=1)
    st.number_input("Pentel Energel Black Refill: 20 Nishkah", min_value=0, step=1)

    st.write(" ")
    st.write(" ")

    st.write("### Bestsellers")
    st.number_input("Lab Manual: 100 Nishkah", min_value=0, step=1)
    st.number_input("Geometric Box: 120 Nishkah", min_value=0, step=1)
    st.number_input("Graph Sheet: 08 Nishkah", min_value=0, step=1)
    st.number_input("30cm Ruler: 10 Nishkah", min_value=0, step=1)
    st.number_input("Lab Coat (Blue/White): 90 Nishkah", min_value=0, step=1)

    st.write(" ")
    st.write(" ")

    st.button("PROCEED")

    st.write(" ")
    st.write(" ")

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
    elif st.session_state["current_page"] == "MY EXPENSES":
        render_track_expenses(st.session_state["name"], st.session_state["rollnumber"],)
    elif st.session_state["current_page"] == "CANTEEN":
        render_canteen(st.session_state["name"], st.session_state["rollnumber"],)
    elif st.session_state["current_page"] == "STATIONERY":
        render_stationery(st.session_state["name"], st.session_state["rollnumber"],)

# Runs the app
if __name__ == "__main__":
    main()
    