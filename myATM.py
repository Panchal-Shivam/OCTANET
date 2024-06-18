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
            amount = float(st.text_input("Enter amount to deposit (INR): "))
            self.deposit_money(amount)
            return self.ask_see_balance()
        elif choice == '3':
            amount = float(st.text_input("Enter amount to withdraw (INR): "))
            self.withdraw_money(amount)
            return self.ask_see_balance()
        elif choice == '4':
            target_card = st.text_input("Enter the target card number: ")
            amount = float(st.text_input("Enter amount to transfer (INR): "))
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
        st.write(f"₹{amount} deposited successfully.")

    def withdraw_money(self, amount):
        if amount <= self.users[self.current_user]['balance']:
            self.users[self.current_user]['balance'] -= amount
            self.users[self.current_user]['transactions'].append(f"Withdrew: ₹{amount}")
            st.write(f"₹{amount} withdrawn successfully.")
        else:
            st.write("Insufficient balance.")

    def transfer_money(self, target_card, amount):
        if target_card in self.users and amount <= self.users[self.current_user]['balance']:
            self.users[self.current_user]['balance'] -= amount
            self.users[target_card]['balance'] += amount
            self.users[self.current_user]['transactions'].append(f"Transferred ₹{amount} to {target_card}")
            self.users[target_card]['transactions'].append(f"Received ₹{amount} from {self.current_user}")
            st.write(f"₹{amount} transferred successfully.")
        else:
            st.write("Transfer failed. Check the card number and balance.")

    def transaction_history(self):
        return "Transaction History:\n" + "\n".join(self.users[self.current_user]['transactions'])

    def ask_see_balance(self):
        choice = st.selectbox("Do you want to see your balance?", ["Yes", "No"])
        if choice == 'Yes':
            st.write(self.view_balance())
            return self.ask_quit_or_menu()
        else:
            return self.show_menu()

    def ask_quit_or_menu(self):
        choice = st.selectbox("What would you like to do next?", ["Return to Main Menu", "Quit"])
        if choice == 'Quit':
            self.current_user = None
            return "Thank you for using the ATM. Goodbye!"
        else:
            return self.show_menu()

    def show_menu(self):
        choice = st.selectbox(
            "Main Menu:",
            ["View Balance", "Deposit Money", "Withdraw Money", "Transfer Money", "Transaction History", "Quit"]
        )
        return self.main_menu(str(choice.split()[0]))

atm = ATM()

# Main menu loop
while True:
    card_number = st.text_input("Enter your card number:")
    pin = st.text_input("Enter your PIN:", type="password")
    message = atm.authenticate(card_number, pin)
    st.write(message)

    if atm.current_user:
        response = atm.show_menu()
        if response == "Thank you for using the ATM. Goodbye!":
            break
