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

    def withdraw_money(self, amount):
        if amount <= self.users[st.session_state.current_user]['balance']:
            self.users[st.session_state.current_user]['balance'] -= amount
            self.users[st.session_state.current_user]['transactions'].append(f"Withdrew: ₹{amount}")
            return f"₹{amount} withdrawn successfully."
        else:
            return "Insufficient balance."

    def transfer_money(self, target_card, amount):
        if target_card in self.users and amount <= self.users[st.session_state.current_user]['balance']:
            self.users[st.session_state.current_user]['balance'] -= amount
            self.users[target_card]['balance'] += amount
            self.users[st.session_state.current_user]['transactions'].append(f"Transferred ₹{amount} to {target_card}")
            self.users[target_card]['transactions'].append(f"Received ₹{amount} from {st.session_state.current_user}")
            return f"₹{amount} transferred successfully."
        else:
            return "Transfer failed. Check the card number and balance."

    def transaction_history(self):
        return "Transaction History:\n" + "\n".join(self.users[st.session_state.current_user]['transactions'])

atm = ATM()

st.title("ATM Simulator")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'current_user' not in st.session_state:
    st.session_state.current_user = None

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
    option = st.selectbox(
        "Choose an option:",
        ["Select", "View Balance", "Deposit Money", "Withdraw Money", "Transfer Money", "Transaction History", "Quit"]
    )

    if option == "View Balance":
        st.write(atm.view_balance())
    elif option == "Deposit Money":
        amount = st.number_input("Enter amount to deposit (INR):", min_value=0.0, step=100.0)
        if st.button("Deposit"):
            st.write(atm.deposit_money(amount))
    elif option == "Withdraw Money":
        amount = st.number_input("Enter amount to withdraw (INR):", min_value=0.0, step=100.0)
        if st.button("Withdraw"):
            st.write(atm.withdraw_money(amount))
    elif option == "Transfer Money":
        target_card = st.text_input("Enter the target card number:")
        amount = st.number_input("Enter amount to transfer (INR):", min_value=0.0, step=100.0)
        if st.button("Transfer"):
            st.write(atm.transfer_money(target_card, amount))
    elif option == "Transaction History":
        st.write(atm.transaction_history())
    elif option == "Quit":
        st.session_state.authenticated = False
        st.session_state.current_user = None
        st.write("Thank you for using the ATM. Goodbye!")

    # Adding an option to return to the main menu after each transaction
    if option in ["View Balance", "Deposit Money", "Withdraw Money", "Transfer Money", "Transaction History"]:
        if st.button("Return to Main Menu"):
            st.session_state.option = "Select"
