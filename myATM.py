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
            amount = st.number_input("Enter amount to deposit (INR): ")
            self.deposit_money(amount)
            return self.ask_see_balance()
        elif choice == '3':
            amount = st.number_input("Enter amount to withdraw (INR): ")
            self.withdraw_money(amount)
            return self.ask_see_balance()
        elif choice == '4':
            target_card = st.text_input("Enter the target card number: ")
            amount = st.number_input("Enter amount to transfer (INR): ")
            self.transfer_money(target_card, amount)
            return self.ask_see_balance()
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

    def ask_see_balance(self):
        choice = st.radio("Do you want to see your balance?", ('Yes', 'No'))
        if choice == 'Yes':
            return self.view_balance()
        else:
            return self.ask_quit_or_menu()

    def ask_quit_or_menu(self):
        choice = st.radio("What would you like to do next?", ('Return to Main Menu', 'Quit'))
        if choice == 'Quit':
            self.current_user = None
            return "Thank you for using the ATM. Goodbye!"
        else:
            return self.show_menu()

    def show_menu(self):
        st.subheader("Main Menu:")
        options = ['View Balance', 'Deposit Money', 'Withdraw Money', 'Transfer Money', 'Transaction History', 'Quit']
        choice = st.selectbox("Choose an option:", options)
        return self.main_menu(str(options.index(choice) + 1))

atm = ATM()

# Main menu loop
card_number = st.text_input("Enter your card number:")
pin = st.text_input("Enter your PIN:", type="password")
message = atm.authenticate(card_number, pin)
st.write(message)

if atm.current_user:
    while True:
        response = atm.show_menu()
        if response == "Thank you for using the ATM. Goodbye!":
            break
        else:
            st.write(response)
else:
    st.warning("Invalid credentials. Please try again.")
