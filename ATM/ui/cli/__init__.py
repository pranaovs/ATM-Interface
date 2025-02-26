import cmd
from getpass import getpass

from ATM.accounts import Account, Administrator
from ATM.exceptions import AccountNotFound, BalanceInsufficient, InvalidPin


class interface(cmd.Cmd):
    intro = "Welcome to ATM cli interface. Type help or ? to list commands"
    prompt = "ATM> "

    def do_exit(self, _):
        "Exit the ATM interface"
        return True

    def do_login(self, _):
        "Interactively login to your account"
        accid = str(input("Enter your account number: "))
        password = str(getpass("Enter your password: "))

        if accid.lower() == "admin":
            try:
                user = Administrator(password)
                AdminLogin(user).cmdloop()
            except InvalidPin:
                print("Invalid pin")

            return

        try:
            user = Account(int(accid), password)
        except AccountNotFound:
            print("Account not found")
            return
        except InvalidPin:
            print("Invalid pin")
            return
        PostLogin(user).cmdloop()


class AdminLogin(cmd.Cmd):
    def __init__(self, admin: Administrator):
        super().__init__()
        self.admin = admin
        self.intro = "Welcome Admin. Type help of ? to list commands"
        self.prompt = "Admin> "

    def do_logout(self, _):
        "Logout from the account"
        return True

    def do_new(self, _):
        "Create a new account"
        name = input("Enter name: ")
        phone = int(input("Enter phone: "))
        pin = getpass("Enter pin: ")
        accid = self.admin.new_account(name, phone, pin)
        print(f"Account created with accid: {accid}")

    def do_set_pin(self, accid: int):
        "Set a new pin for an account"
        pin = getpass("Enter new pin: ")
        self.admin.set_pin(accid, pin)
        print(f"Pin updated for accid: {accid}")


class PostLogin(cmd.Cmd):

    def __init__(self, user: Account):
        super().__init__()
        self.user: Account = user
        self.intro = f"Welcome {user.name}. Type help of ? to list commands"
        self.prompt = f"{user.name}> "

    def onecmd(self, line):  # type: ignore
        try:
            return super().onecmd(line)
        except Exception as e:
            print(f"Error: {e}")

    def do_logout(self, _):
        "Logout from the account"
        return True

    def do_balance(self, _):
        "Check account balance"
        print(f"Your balance is: {self.user.balance()}")

    def do_deposit(self, amount: int):
        "Deposit money to your account"
        if amount == "":
            amount = int(input("Enter amount to deposit: "))
        print(f"Deposited: {amount}.\nCurrent balance: {self.user.deposit(amount)}")

    def do_withdraw(self, amount: int):
        "Withdraw money from your account"
        if amount == "":
            amount = int(input("Enter amount to withdraw: "))
        try:
            print(
                f"Withdrawn: {amount}.\nCurrent balance: {self.user.withdraw(amount)}"
            )
        except BalanceInsufficient:
            print(f"Insufficient balance.\nCurrent balance: {self.user.balance()}")

    def do_delete(self, _):
        "Delete your account"

        pin = getpass("Enter your pin to delete your account: ")
        if not self.user.check_pin(pin):
            print("Invalid pin")
            return
        else:
            self.user.delete()
            print("Account deleted")

    def do_set_pin(self, _):
        "Set a new pin for your account"
        old_pin = getpass("Enter old pin: ")
        if not self.user.check_pin(old_pin):
            print("Invalid pin")
            return

        new_pin = getpass("Enter new pin: ")
        self.user.set_pin(new_pin)
        print("Pin updated")


if __name__ == "__main__":
    interface().cmdloop()
