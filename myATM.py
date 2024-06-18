import streamlit as st

class ATM:
    def __init__(self):
        self.users = {
            '123456': {'pin': '1234', 'balance': 5000, 'transactions': []},
            '987654': {'pin': '5678', 'balance': 10000, 'transactions': []}
        }

    def authenticate(self, card_number, pin):
        if card_number in self.users:
            if self.users[card_number]['pin'] == pin:
                st.session_state.current_user = card_number
                return "Login successful!"
            else:
                return "Invalid PIN."
        else:
            return "Invalid card number."

    def view_balance(self):
        balance = self.users[st.session_state.current_user]['balance']
        return f"Your current balance is: ₹{balance}"

    def deposit_money(self, amount):
        self.users[st.session_state.current_user]['balance'] += amount
        self.users[st.session_state.current_user]['transactions'].append(f"Deposited: ₹{amount}")
        return f"₹{amount} deposited successfully."

atm = ATM()

st.title("ATM Simulator")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

if 'main_menu' not in st.session_state:
    st.session_state.main_menu = False

if 'transaction_done' not in st.session_state:
    st.session_state.transaction_done = False

if not st.session_state.authenticated:
    card_number = st.text_input("Enter your card number:")
    pin = st.text_input("Enter your PIN:", type="password")
    
    if st.button("Login"):
        message = atm.authenticate(card_number, pin)
        st.session_state.authenticated = st.session_state.current_user is not None
        st.session_state.message = message

    if 'message' in st.session_state:
        st.write(st.session_state.message)

if st.session_state.authenticated and st.session_state.current_user:
    if not st.session_state.main_menu:
        st.session_state.option = st.selectbox(
            "Choose an option:",
            ["Select", "View Balance", "Deposit Money", "Quit"]
        )
        if st.session_state.option != "Select":
            st.session_state.main_menu = True
            st.session_state.transaction_done = False

    if st.session_state.main_menu:
        if st.session_state.option == "View Balance":
            st.write(atm.view_balance())
            st.session_state.display_balance_option = True
            st.session_state.main_menu = False

        elif st.session_state.option == "Deposit Money":
            amount = st.number_input("Enter amount to deposit (INR):", min_value=0.0, step=100.0)
            if st.button("Deposit"):
                st.write(atm.deposit_money(amount))
                st.session_state.transaction_done = True

        elif st.session_state.option == "Quit":
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.main_menu = False
            st.session_state.option = "Select"
            st.write("Thank you for using the ATM. Goodbye!")

if st.session_state.transaction_done:
    if 'display_balance_option' not in st.session_state:
        see_balance = st.radio("Do you want to see your balance?", ("Yes", "No"))
        if see_balance == "Yes":
            st.write(atm.view_balance())
            st.session_state.display_balance_option = True
    else:
        next_step = st.radio("What would you like to do next?", ("Return to Main Menu", "Quit"))
        if next_step == "Return to Main Menu":
            st.session_state.main_menu = False
            st.session_state.transaction_done = False
            st.session_state.display_balance_option = False
        elif next_step == "Quit":
            st.session_state.authenticated = False
            st.session_state.current_user = None
            st.session_state.main_menu = False
            st.session_state.transaction_done = False
            st.session_state.option = "Select"
            st.write("Thank you for using the ATM. Goodbye!")
