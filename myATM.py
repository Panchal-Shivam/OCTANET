import streamlit as st

class ATM:
    def __init__(self):
        self.users = {
            '123456': {'pin': '1234', 'balance': 5000, 'transactions': []},
            '987654': {'pin': '5678', 'balance': 10000, 'transactions': []}
        }

    def authenticate(self, card_number, pin):
        if card_number in self.users and self.users[card_number]['pin'] == pin:
            return True
        return False

    def view_balance(self, user):
        balance = self.users[user]['balance']
        return f"Your current balance is: ₹{balance}"

    def deposit_money(self, user, amount):
        self.users[user]['balance'] += amount
        self.users[user]['transactions'].append(f"Deposited: ₹{amount}")
        return f"₹{amount} deposited successfully."

    def withdraw_money(self, user, amount):
        if amount <= self.users[user]['balance']:
            self.users[user]['balance'] -= amount
            self.users[user]['transactions'].append(f"Withdrew: ₹{amount}")
            return f"₹{amount} withdrawn successfully."
        else:
            return "Insufficient balance."

    def transfer_money(self, user, target_card, amount):
        if target_card in self.users and amount <= self.users[user]['balance']:
            self.users[user]['balance'] -= amount
            self.users[target_card]['balance'] += amount
            self.users[user]['transactions'].append(f"Transferred ₹{amount} to {target_card}")
            self.users[target_card]['transactions'].append(f"Received ₹{amount} from {user}")
            return f"₹{amount} transferred successfully."
        else:
            return "Transfer failed. Check the card number and balance."

    def transaction_history(self, user):
        transactions = "\n".join(self.users[user]['transactions'])
        return f"Transaction History:\n{transactions}"

def main():
    st.title("ATM Interface")
    st.write("Made by Shivam Panchal")

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'action' not in st.session_state:
        st.session_state.action = None

    atm = ATM()

    if not st.session_state.authenticated:
        card_number = st.text_input("Enter your card number:")
        pin = st.text_input("Enter your PIN:", type="password")
        if st.button("Login"):
            if atm.authenticate(card_number, pin):
                st.session_state.authenticated = True
                st.session_state.user = card_number
                st.session_state.action = None
                st.write("Login successful!")
            else:
                st.write("Invalid card number or PIN.")
    else:
        options = ['View Balance', 'Deposit Money', 'Withdraw Money', 'Transfer Money', 'Transaction History', 'Quit']
        choice = st.selectbox("Choose an option:", options)

        if choice == 'View Balance':
            balance = atm.view_balance(st.session_state.user)
            st.write(balance)
        elif choice == 'Deposit Money':
            amount = st.number_input("Enter amount to deposit (INR): ", min_value=0)
            if st.button("Deposit"):
                message = atm.deposit_money(st.session_state.user, amount)
                st.write(message)
        elif choice == 'Withdraw Money':
            amount = st.number_input("Enter amount to withdraw (INR): ", min_value=0)
            if st.button("Withdraw"):
                message = atm.withdraw_money(st.session_state.user, amount)
                st.write(message)
        elif choice == 'Transfer Money':
            target_card = st.text_input("Enter the target card number: ")
            amount = st.number_input("Enter amount to transfer (INR): ", min_value=0)
            if st.button("Transfer"):
                message = atm.transfer_money(st.session_state.user, target_card, amount)
                st.write(message)
        elif choice == 'Transaction History':
            history = atm.transaction_history(st.session_state.user)
            st.write(history)
        elif choice == 'Quit':
            st.session_state.authenticated = False
            st.session_state.user = None
            st.write("Thank you for using the ATM. Goodbye!")

        if choice != 'Quit':
            view_balance = st.radio("Do you want to see your balance?", ('Yes', 'No'))
            if view_balance == 'Yes':
                balance = atm.view_balance(st.session_state.user)
                st.write(balance)

if __name__ == "__main__":
    main()
