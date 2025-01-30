"""Lesson31 Task2: Implementation the TestCreditCard class."""

import unittest
from credit_card import CreditCard


class TestCreditCard(unittest.TestCase):
    """Unit tests for the CreditCard class."""

    def setUp(self):
        """Initialization before each test"""
        self.card = CreditCard(
            "1234567812345678", "Ivan Ivanov", "12/25", "123", 1000.00
        )

    def test_get_card_number(self):
        """Test the get_card_number() method."""
        self.assertEqual(self.card.get_card_number(), "1234567812345678")

    def test_get_card_holder(self):
        """Test the get_card_holder() method."""
        self.assertEqual(self.card.get_card_holder(), "Ivan Ivanov")

    def test_get_expiry_date(self):
        """Test the get_expiry_date() method."""
        self.assertEqual(self.card.get_expiry_date(), "12/25")

    def test_get_cvv(self):
        """Test the get_cvv() method."""
        self.assertEqual(self.card.get_cvv(), "123")

    def test_charge_success(self):
        """Test successful charge when the amount is within the available balance."""
        self.assertTrue(self.card.charge(200.00))
        self.assertEqual(self.card.balance, 800.00)

    def test_charge_exceed_balance(self):
        """Test charging an amount that exceeds the available balance."""
        with self.assertRaises(ValueError) as context:
            self.card.charge(1500.00)
        self.assertEqual(str(context.exception), "Not enough funds on the card")

    def test_charge_exact_balance(self):
        """Test charging an amount equal to the available balance."""
        self.assertTrue(self.card.charge(1000.00))
        self.assertEqual(self.card.balance, 0.00)

    def test_charge_zero_amount(self):
        """Test attempting to charge a zero amount (should raise ValueError)."""
        with self.assertRaises(ValueError) as context:
            self.card.charge(0.00)
        self.assertEqual(str(context.exception), "The charge amount must be positive")

    def test_charge_negative_amount(self):
        """Test attempting to charge a negative amount."""
        with self.assertRaises(ValueError) as context:
            self.card.charge(-50.0)
        self.assertEqual(str(context.exception), "The charge amount must be positive")


if __name__ == "__main__":
    unittest.main()
