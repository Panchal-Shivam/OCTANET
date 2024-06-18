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

    def main_menu(self, choice):
        if choice == '1':
            return self.view_balance()
        elif choice == '2':
            amount = st.number_input("Enter amount to deposit (INR):", min_value=0.0, step=100.0)
            if st.button("Deposit Money"):
                return self.deposit_money(amount)
        elif choice == '3':
            amount = st.number_input("Enter amount to withdraw (INR):", min_value=0.0, step=100.0)
            if st.button("Withdraw Money"):
                return self.withdraw_money(amount)
        elif choice == '4':
            target_card = st.text_input("Enter the target card number:")
            amount = st.number_input("Enter amount to transfer (INR):", min_value=0.0, step=100.0)
            if st.button("Transfer Money"):
                return self.transfer_money(target_card, amount)
        elif choice == '5':
            return self.transaction_history()
        elif choice == '6':
            self.current_user = None
            return "Thank you for using the ATM. Goodbye!"
        else:
            return "Invalid choice. Please try again."

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

if atm.current_user is None:
    card_number = st.text_input("Enter your card number:")
    pin = st.text_input("Enter your PIN:", type="password")
    
    if st.button("Login"):
        message = atm.authenticate(card_number, pin)
        st.write(message)
else:
    option = st.selectbox(
        "Choose an option:",
        ["View Balance", "Deposit Money", "Withdraw Money", "Transfer Money", "Transaction History", "Quit"]
    )
    
    response = atm.main_menu(option)
    
    if response:
        st.write(response)
    
    if option == "Quit":
        atm.current_user = None
        st.write("Thank you for using the ATM. Goodbye!")
