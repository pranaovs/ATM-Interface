from tinydb import Query, TinyDB
from tinydb.operations import add, subtract
from tinydb.table import Document

from ..exceptions import (
    AccountNotFound,
    BalanceInsufficient,
    InvalidAmount,
    MultipleAccounts,
)


class Database:
    def __init__(self) -> None:
        self._db = TinyDB("atm_db.json")
        query = Query()

    def query(self, accid: int) -> dict[str, int | str]:
        accid = int(accid)

        if result := self._db.get(doc_id=accid):
            return dict(result)  # type: ignore

        else:
            raise AccountNotFound(f"Account id not found: {accid}")

    def balance(self, accid: int) -> int:
        accid = int(accid)

        details = self.query(accid=accid)
        balance = int(details["balance"])
        return int(balance)  # type: ignore

    def new(self, name: str, phone: int, pin: str) -> int:

        # TODO: add date to transactions list
        data = {
            "name": str(name),
            "phone": int(phone),
            "balance": 0,
            "pin": str(pin),
            "transactions": [],
        }

        return int(self._db.insert(data))

    def update(self, accid, key, value):
        accid = int(accid)
        self._db.update(Document({key: value}, doc_id=accid))

    def withdraw(self, accid: int, amount: int) -> int:
        accid = int(accid)
        details = self.query(accid=accid)

        if amount <= 0:
            raise InvalidAmount(f"Amount is not valid: {amount}")

        balance = int(details.get("Balance")) - int(amount)  # type: ignore

        if balance < 0:
            raise BalanceInsufficient(balance)

        self._db.update(subtract(accid, amount))
        return balance

    def deposit(self, accid: int, amount: int) -> int:
        accid = int(accid)
        details = self.query(accid=accid)

        if amount <= 0:
            raise InvalidAmount(f"Amount is not valid: {amount}")

        balance = int(details.get("Balance")) - int(amount)  # type: ignore

        self._db.update(add(accid, amount))

        return balance

    def delete(self, accid: int) -> None:
        accid = int(accid)
        balance = self.balance(accid)

        if balance != 0:
            raise BalanceInsufficient(
                "Empty balance before deleting account: ", balance
            )

        else:
            self._db.remove(doc_ids=[accid])

    def check_pin(self, accid: int, pin: str) -> bool:
        accid = int(accid)
        details = self.query(accid=accid)
        if str(pin) == details.get("pin"):
            return True
        else:
            return False

    def set_pin(self, accid: int, pin: str) -> None:
        accid = int(accid)
        self.update(accid, "pin", str(pin))
