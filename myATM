class ATM:
    def __init__(self):
        self.users = {
            '123456': {'pin': '1234', 'balance': 5000, 'transactions': []},
            '987654': {'pin': '5678', 'balance': 10000, 'transactions': []}
        }
        self.current_user = None

    def authenticate(self, card_number, pin):
        if card_number in self.users and self.users[card_number]['pin'] == pin:
            self.current_user = card_number
            return True
        return False

    def logout(self):
        self.current_user = None

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
        transactions = "\n".join(self.users[self.current_user]['transactions'])
        return f"Transaction History:\n{transactions}"

def main():
    atm = ATM()
    
    while True:
        card_number = input("Enter your card number: ")
        pin = input("Enter your PIN: ")
        
        if atm.authenticate(card_number, pin):
            print("Login successful!")
            while True:
                print("\nMain Menu:")
                print("1. View Balance")
                print("2. Deposit Money")
                print("3. Withdraw Money")
                print("4. Transfer Money")
                print("5. Transaction History")
                print("6. Quit")
                choice = input("Choose an option: ")

                if choice == '1':
                    print(atm.view_balance())
                elif choice == '2':
                    amount = float(input("Enter amount to deposit (INR): "))
                    print(atm.deposit_money(amount))
                elif choice == '3':
                    amount = float(input("Enter amount to withdraw (INR): "))
                    print(atm.withdraw_money(amount))
                elif choice == '4':
                    target_card = input("Enter the target card number: ")
                    amount = float(input("Enter amount to transfer (INR): "))
                    print(atm.transfer_money(target_card, amount))
                elif choice == '5':
                    print(atm.transaction_history())
                elif choice == '6':
                    atm.logout()
                    print("Thank you for using the ATM. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please try again.")
        else:
            print("Invalid card number or PIN.")

if __name__ == "__main__":
    main()
