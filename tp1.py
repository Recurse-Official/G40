import streamlit as st

# Function to simulate the transaction
def process_transaction(recipient, amount_inr):
    # Simulate the transaction process
    return f"Transaction to {recipient} for ₹{amount_inr:,.2f} has been processed successfully!"

# Set up the Streamlit page
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

