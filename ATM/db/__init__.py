from tinydb import TinyDB, Query
from tinydb.table import Document
from tinydb.operations import add, subtract
from ..exceptions.exceptions import (
    AccountNotFound,
    MultipleAccounts,
    BalanceInsufficient,
    InvalidAmount,
)


class database:
    def __init__(self) -> None:
        self.db = TinyDB("atm_db.json")
        query = Query()

    def query(self, accid: int) -> dict[str, int | str]:
        accid = int(accid)

        if result := self.db.get(doc_id=accid):
            return dict(result)

        else:
            raise AccountNotFound(f"Account id not found: {accid}")

    def balance(self, accid: int) -> int:
        accid = int(accid)

        details = self.query(accid=accid)
        balance = int(details["balance"])
        return int(balance)  # type: ignore

    def new(self, name: str, phone: int) -> int:

        # TODO: add date to transactions list
        data = {
            "name": str(name),
            "phone": int(phone),
            "balance": 0,
            "transactions": [],
        }

        return int(self.db.insert(data))

    def update(self, accid, key, value):
        accid = int(accid)
        self.db.update(Document({key: value}, doc_id=accid))

    def withdraw(self, accid: int, amount: int) -> int:
        accid = int(accid)
        details = self.query(accid=accid)

        if amount <= 0:
            raise InvalidAmount(f"Amount is not valid: {amount}")

        balance = int(details.get("Balance")) - int(amount)  # type: ignore

        if balance < 0:
            raise BalanceInsufficient(balance)

        self.db.update(subtract(accid, amount))
        return balance

    def deposit(self, accid: int, amount: int) -> int:
        accid = int(accid)
        details = self.query(accid=accid)

        if amount <= 0:
            raise InvalidAmount(f"Amount is not valid: {amount}")

        balance = int(details.get("Balance")) - int(amount)  # type: ignore

        self.db.update(add(accid, amount))

        return balance

    def delete(self, accid: int) -> None:
        accid = int(accid)
        balance = self.balance(accid)

        if balance != 0:
            raise BalanceInsufficient(
                "Empty balance before deleting account: ", balance
            )

        else:
            self.db.remove(doc_ids=[accid])
