import hashlib

from ATM.exceptions import InvalidPin
import ATM.db
from os import environ

database = ATM.db.Database()


class Account:
    def __init__(self, accid: int, pin: str) -> None:
        if database.check_pin(accid=int(accid), pin=hash_pin(pin)):
            self._accid = accid

        else:
            raise InvalidPin(f"Incorrect pin for accid {accid}")

    def balance(self) -> int:
        return database.balance(self._accid)

    def deposit(self, amount: int) -> int:
        return database.deposit(self._accid, amount)

    def withdraw(self, amount: int) -> int:
        return database.withdraw(self._accid, amount)

    def delete(self) -> None:
        return database.delete(self._accid)

    def set_pin(self, pin: str) -> None:
        return database.set_pin(self._accid, hash_pin(pin))

    def update_phone(self, phone: int) -> None:
        database.update(accid=self._accid, key="phone", value=phone)

    def update_name(self, name: str) -> None:
        database.update(accid=self._accid, key="name", value=name)


class Administrator:
    def __init__(self, pin: str) -> None:
        if not environ.get("ATM_ADMIN_PIN"):
            raise InvalidPin("Admin pin not set")
        if hash_pin(pin) == hash_pin(environ.get("ATM_ADMIN_PIN")):  # type:ignore
            pass
        else:
            raise InvalidPin("Incorrect admin pin")

    def new_account(self, name: str, phone: int, pin: str) -> int:
        pin = hash_pin(pin)
        accid = database.new(str(name), int(phone), str(pin))
        return accid

    def set_pin(self, accid: int, pin: str) -> None:
        return database.set_pin(accid, hash_pin(pin))


def hash_pin(pin: str) -> str:
    return str(hashlib.sha256(pin.encode()).hexdigest())
