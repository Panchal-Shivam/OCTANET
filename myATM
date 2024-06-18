import streamlit as st

class ATM:
    def __init__(self):
        self.users = {
            '123456': {'pin': '1234', 'balance': 5000, 'transactions': []},
            '987654': {'pin': '5678', 'balance': 10000, 'transactions': []}
        }
        self.current_user = None

    def authenticate(self, card_number, pin):
        if card_number in self.users:
            if self.users[card_number]['pin'] == pin:
                self.current_user = card_number
                return "Login successful!"
            else:
                return "Invalid PIN."
        else:
            return "Invalid card number."

    def view_balance(self):
        balance = self.users[self.current_user]['balance']
        return f"Your current balance is: ₹{balance}"

    def deposit_money(self, amount):
        self.users[self.current_user]['balance'] += amount
        self.users[self.current_user]['transactions'].append(f"Deposited: ₹{amount}")
        return f"₹{amount} deposited successfully."

    def withdraw_money(self, amount):
        if amount <= self.users[self.current_user]['balance']:
            self.users[self.current_user]['balance'] -= amount
            self.users[self.current_user]['transactions'].append(f"Withdrew: ₹{amount}")
            return f"₹{amount} withdrawn successfully."
        else:
            return "Insufficient balance."

    def transfer_money(self, target_card, amount):
        if target_card in self.users and amount <= self.users[self.current_user]['balance']:
            self.users[self.current_user]['balance'] -= amount
            self.users[target_card]['balance'] += amount
            self.users[self.current_user]['transactions'].append(f"Transferred ₹{amount} to {target_card}")
            self.users[target_card]['transactions'].append(f"Received ₹{amount} from {self.current_user}")
            return f"₹{amount} transferred successfully."
        else:
            return "Transfer failed. Check the card number and balance."

    def transaction_history(self):
        return "Transaction History:\n" + "\n".join(self.users[self.current_user]['transactions'])

atm = ATM()

# Streamlit interface
st.title("ATM Simulator")

card_number = st.text_input("Enter your card number:")
pin = st.text_input("Enter your PIN:", type="password")

if st.button("Login"):
    message = atm.authenticate(card_number, pin)
    st.write(message)
    
    if atm.current_user:
        while True:
            option = st.selectbox(
                "Choose an option:",
                ["View Balance", "Deposit Money", "Withdraw Money", "Transfer Money", "Transaction History"]
            )
            
            if option == "View Balance":
                st.write(atm.view_balance())
            elif option == "Deposit Money":
                amount = st.number_input("Enter amount to deposit (INR):")
                st.write(atm.deposit_money(amount))
            elif option == "Withdraw Money":
                amount = st.number_input("Enter amount to withdraw (INR):")
                st.write(atm.withdraw_money(amount))
            elif option == "Transfer Money":
                target_card = st.text_input("Enter the target card number:")
                amount = st.number_input("Enter amount to transfer (INR):")
                st.write(atm.transfer_money(target_card, amount))
            elif option == "Transaction History":
                st.write(atm.transaction_history())
