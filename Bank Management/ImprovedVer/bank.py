import json
import random
import string
from pathlib import Path
from typing import Optional


class Bank:
    DATABASE = Path(__file__).parent / "data.json"

    def __init__(self):
        self.data: list[dict] = self._load_data()

    def _load_data(self) -> list[dict]:
        """Load account data from JSON file."""
        try:
            if self.DATABASE.exists():
                with open(self.DATABASE, "r") as fs:
                    return json.loads(fs.read())
        except (json.JSONDecodeError, IOError) as err:
            print(f"Error loading data: {err}")
        return []

    def _save_data(self) -> None:
        """Persist account data to JSON file."""
        with open(self.DATABASE, "w") as fs:
            json.dump(self.data, fs, indent=2)

    @staticmethod
    def _generate_account_number() -> str:
        """Generate a unique random account number."""
        alpha = random.choices(string.ascii_uppercase, k=3)
        num = random.choices(string.digits, k=3)
        parts = alpha + num
        random.shuffle(parts)
        return "ACC-" + "".join(parts)

    def _find_account(self, account_no: str, pin: int) -> Optional[dict]:
        """Find an account by account number and PIN."""
        for account in self.data:
            if account["account_no"] == account_no and account["pin"] == pin:
                return account
        return None

    def get_all_account_numbers(self) -> list[str]:
        """Return all existing account numbers."""
        return [acc["account_no"] for acc in self.data]

    def create_account(self, name: str, age: int, email: str, pin: int) -> dict:
        """Create a new bank account."""
        errors = []

        if not name.strip():
            errors.append("Name cannot be empty.")
        if age < 18:
            errors.append("You must be at least 18 years old.")
        if len(str(pin)) != 4:
            errors.append("PIN must be exactly 4 digits.")
        if not email.strip() or "@" not in email:
            errors.append("Please enter a valid email address.")

        if errors:
            return {"success": False, "errors": errors}

        # Ensure unique account number
        account_no = self._generate_account_number()
        while any(acc["account_no"] == account_no for acc in self.data):
            account_no = self._generate_account_number()

        account = {
            "name": name.strip(),
            "age": age,
            "email": email.strip(),
            "pin": pin,
            "account_no": account_no,
            "balance": 0,
            "transactions": []
        }

        self.data.append(account)
        self._save_data()

        return {"success": True, "account": account}

    def deposit(self, account_no: str, pin: int, amount: float) -> dict:
        """Deposit money into an account."""
        account = self._find_account(account_no, pin)

        if not account:
            return {"success": False, "error": "Invalid account number or PIN."}

        if amount <= 0:
            return {"success": False, "error": "Amount must be greater than 0."}

        if amount > 100000:
            return {"success": False, "error": "Single deposit cannot exceed ₹1,00,000."}

        account["balance"] += amount
        account["transactions"].append({
            "type": "DEPOSIT",
            "amount": amount,
            "balance_after": account["balance"]
        })

        self._save_data()
        return {
            "success": True,
            "new_balance": account["balance"],
            "message": f"₹{amount:,.2f} deposited successfully."
        }

    def withdraw(self, account_no: str, pin: int, amount: float) -> dict:
        """Withdraw money from an account."""
        account = self._find_account(account_no, pin)

        if not account:
            return {"success": False, "error": "Invalid account number or PIN."}

        if amount <= 0:
            return {"success": False, "error": "Amount must be greater than 0."}

        if amount > account["balance"]:
            return {
                "success": False,
                "error": f"Insufficient balance. Current balance: ₹{account['balance']:,.2f}"
            }

        account["balance"] -= amount
        account["transactions"].append({
            "type": "WITHDRAWAL",
            "amount": amount,
            "balance_after": account["balance"]
        })

        self._save_data()
        return {
            "success": True,
            "new_balance": account["balance"],
            "message": f"₹{amount:,.2f} withdrawn successfully."
        }

    def get_details(self, account_no: str, pin: int) -> dict:
        """Get account details."""
        account = self._find_account(account_no, pin)

        if not account:
            return {"success": False, "error": "Invalid account number or PIN."}

        return {"success": True, "account": account}

    def update_details(
        self, account_no: str, pin: int,
        new_name: str = "", new_email: str = "", new_pin: int = 0
    ) -> dict:
        """Update account details."""
        account = self._find_account(account_no, pin)

        if not account:
            return {"success": False, "error": "Invalid account number or PIN."}

        changes = []

        if new_name.strip() and new_name.strip() != account["name"]:
            account["name"] = new_name.strip()
            changes.append("Name")

        if new_email.strip() and new_email.strip() != account["email"]:
            if "@" not in new_email:
                return {"success": False, "error": "Invalid email address."}
            account["email"] = new_email.strip()
            changes.append("Email")

        if new_pin and new_pin != pin:
            if len(str(new_pin)) != 4:
                return {"success": False, "error": "New PIN must be exactly 4 digits."}
            account["pin"] = new_pin
            changes.append("PIN")

        if not changes:
            return {"success": False, "error": "No changes were made."}

        self._save_data()
        return {
            "success": True,
            "message": f"Updated: {', '.join(changes)}",
            "account": account
        }

    def delete_account(self, account_no: str, pin: int) -> dict:
        """Delete an account."""
        account = self._find_account(account_no, pin)

        if not account:
            return {"success": False, "error": "Invalid account number or PIN."}

        if account["balance"] > 0:
            return {
                "success": False,
                "error": f"Please withdraw remaining balance (₹{account['balance']:,.2f}) before deleting."
            }

        self.data.remove(account)
        self._save_data()
        return {"success": True, "message": "Account deleted successfully."}