"""Lesson31 Task2: Implementation the TestPaymentForm class."""

import unittest
from unittest.mock import MagicMock
from credit_card import PaymentForm


class TestPaymentForm(unittest.TestCase):
    """Unit tests for the PaymentForm class."""

    def setUp(self):
        """Set up a mock CreditCard object for testing."""
        self.mock_card = MagicMock()
        self.mock_card.charge.return_value = True

        # Create a PaymentForm instance with the mock card
        self.payment_form = PaymentForm(self.mock_card)

    def test_successful_payment(self):
        """Test a successful payment scenario."""
        amount = 100.0
        result = self.payment_form.pay(amount)

        self.mock_card.charge.assert_called_once_with(amount)
        self.assertTrue(result)

    def test_insufficient_funds(self):
        """Test payment failure due to insufficient funds."""
        self.mock_card.charge.side_effect = ValueError("Not enough funds on the card")

        with self.assertRaises(ValueError) as context:
            self.payment_form.pay(1500.0)

        self.assertEqual(str(context.exception), "Not enough funds on the card")
        self.mock_card.charge.assert_called_once_with(1500.0)

    def test_invalid_amount(self):
        """Test payment failure due to an invalid amount (negative value)."""
        self.mock_card.charge.side_effect = ValueError(
            "The charge amount must be positive"
        )

        with self.assertRaises(ValueError) as context:
            self.payment_form.pay(-50.0)

        self.assertEqual(str(context.exception), "The charge amount must be positive")
        self.mock_card.charge.assert_called_once_with(-50.0)


if __name__ == "__main__":
    unittest.main()
