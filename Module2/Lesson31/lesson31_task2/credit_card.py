"""Lesson31 Task2: Implementation the CreditCard and PaymentForm classes."""


class CreditCard:
    """A class representing a credit card."""

    def __init__(self, card_number, card_holder, expiry_date, cvv, balance=1000):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiry_date = expiry_date
        self.cvv = cvv
        self.balance = balance

    def get_card_number(self):
        """Returns the credit card number."""
        return self.card_number

    def get_card_holder(self):
        """Returns the name of the cardholder."""
        return self.card_holder

    def get_expiry_date(self):
        """Returns the expiration date of the card."""
        return self.expiry_date

    def get_cvv(self):
        """Returns the security code."""
        return self.cvv

    def charge(self, amount: float):
        """Charges a specified amount to the credit card."""
        if amount <= 0:
            raise ValueError("The charge amount must be positive")
        if amount > self.balance:
            raise ValueError("Not enough funds on the card")
        self.balance -= amount
        return True


class PaymentForm:
    """A class that processes payments using a credit card."""

    def __init__(self, credit_card):
        self.credit_card = credit_card

    def pay(self, amount: float):
        """Processes a payment using the associated credit card."""
        return self.credit_card.charge(amount)
