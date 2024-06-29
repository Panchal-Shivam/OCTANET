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
        st.write(f"Your current balance is: ₹{balance}")

    def deposit_money(self, user, amount):
        self.users[user]['balance'] += amount
        self.users[user]['transactions'].append(f"Deposited: ₹{amount}")
        st.write(f"₹{amount} deposited successfully.")

    def withdraw_money(self, user, amount):
        if amount <= self.users[user]['balance']:
            self.users[user]['balance'] -= amount
            self.users[user]['transactions'].append(f"Withdrew: ₹{amount}")
            st.write(f"₹{amount} withdrawn successfully.")
        else:
            st.write("Insufficient balance.")

    def transfer_money(self, user, target_card, amount):
        if target_card in self.users and amount <= self.users[user]['balance']:
            self.users[user]['balance'] -= amount
            self.users[target_card]['balance'] += amount
            self.users[user]['transactions'].append(f"Transferred ₹{amount} to {target_card}")
            self.users[target_card]['transactions'].append(f"Received ₹{amount} from {user}")
            st.write(f"₹{amount} transferred successfully.")
        else:
            st.write("Transfer failed. Check the card number and balance.")

    def transaction_history(self, user):
        st.write("Transaction History:")
        for transaction in self.users[user]['transactions']:
            st.write(transaction)

def main():
    st.title("ATM Interface")

    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

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
        if 'action' not in st.session_state or st.session_state.action is None:
            options = ['View Balance', 'Deposit Money', 'Withdraw Money', 'Transfer Money', 'Transaction History', 'Quit']
            choice = st.selectbox("Choose an option:", options)

            if choice == 'View Balance':
                atm.view_balance(st.session_state.user)
            elif choice == 'Deposit Money':
                amount = st.number_input("Enter amount to deposit (INR): ", min_value=0)
                if st.button("Deposit"):
                    atm.deposit_money(st.session_state.user, amount)
                    st.session_state.action = 'balance_option'
            elif choice == 'Withdraw Money':
                amount = st.number_input("Enter amount to withdraw (INR): ", min_value=0)
                if st.button("Withdraw"):
                    atm.withdraw_money(st.session_state.user, amount)
                    st.session_state.action = 'balance_option'
            elif choice == 'Transfer Money':
                target_card = st.text_input("Enter the target card number: ")
                amount = st.number_input("Enter amount to transfer (INR): ", min_value=0)
                if st.button("Transfer"):
                    atm.transfer_money(st.session_state.user, target_card, amount)
                    st.session_state.action = 'balance_option'
            elif choice == 'Transaction History':
                atm.transaction_history(st.session_state.user)
            elif choice == 'Quit':
                st.session_state.authenticated = False
                st.session_state.user = None
                st.write("Thank you for using the ATM. Goodbye!")
        else:
            choice = st.radio("Do you want to see your balance?", ('Yes', 'No'))
            if choice == 'Yes':
                atm.view_balance(st.session_state.user)
            st.session_state.action = None

if __name__ == "__main__":
    main()
