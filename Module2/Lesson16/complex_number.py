"""Lesson 16 Task 1: Implementation of a Complex Number Class."""

import math


class ComplexNumber:
    """A class to represent a complex number in either algebraic or polar form."""

    def __init__(self, real=None, imag=None, r=None, theta=None):
        self._complex_number_type = self.get_complex_number_type(real, imag, r, theta)
        self._real, self._imag, self._r, self._theta = self.get_complex_number_args(
            real, imag, r, theta, self._complex_number_type
        )

    def __add__(self, other):
        if isinstance(other, ComplexNumber):
            res = ComplexNumber(
                real=self._real + other._real, imag=self._imag + other._imag
            )
        elif isinstance(other, (int, float)):
            res = ComplexNumber(real=self._real + other, imag=self._imag)
        else:
            raise TypeError(
                "You can add a ComplexNumber, int or float to a ComplexNumber!"
            )
        res._complex_number_type = self._complex_number_type
        return res

    def __sub__(self, other):
        if isinstance(other, ComplexNumber):
            res = ComplexNumber(
                real=self._real - other._real, imag=self._imag - other._imag
            )
        elif isinstance(other, (int, float)):
            res = ComplexNumber(real=self._real - other, imag=self._imag)
        else:
            raise TypeError(
                "You can subtract a ComplexNumber, int or float from a ComplexNumber!"
            )
        res._complex_number_type = self._complex_number_type
        return res

    def __mul__(self, other):
        if isinstance(other, ComplexNumber):
            res = ComplexNumber(r=self._r * other._r, theta=self._theta + other._theta)
        elif isinstance(other, (int, float)):
            res = ComplexNumber(r=self._r * other, theta=self._theta)
        else:
            raise TypeError(
                "You can multiply a ComplexNumber by a ComplexNumber, int or float!"
            )
        res._complex_number_type = self._complex_number_type
        return res

    def __truediv__(self, other):
        if isinstance(other, ComplexNumber):
            if other._r == 0:
                raise ZeroDivisionError("Cannot divide by a complex number with r=0!")
            res = ComplexNumber(r=self._r / other._r, theta=self._theta - other._theta)
        elif isinstance(other, (int, float)):
            if other == 0:
                raise ZeroDivisionError("Cannot divide by 0!")
            res = ComplexNumber(r=self._r / other, theta=self._theta)
        else:
            raise TypeError(
                "You can divide a ComplexNumber by a ComplexNumber, int or float!"
            )
        res._complex_number_type = self._complex_number_type
        return res

    def __round__(self, n=0):
        if self._complex_number_type == "algebraic":
            return ComplexNumber(real=round(self._real, n), imag=round(self._imag, n))
        if self._complex_number_type == "polar":
            return ComplexNumber(r=round(self._r, n), theta=round(self._theta, n))
        return None

    def __str__(self):
        res = None
        if self._complex_number_type == "algebraic":
            if not self._real and not self._imag:
                res = f"{0}"
            elif self._real and not self._imag:
                res = f"{self._real}"
            elif not self._real and self._imag:
                res = f"{self._imag}i"
            else:
                res = (
                    f"{self._real} {'+' if self._imag > 0 else '-'} {abs(self._imag)}i"
                )
        elif self._complex_number_type == "polar":
            if not self._r:
                res = f"{0}"
            elif self._r and not self._theta:
                res = f"{self._r}"
            elif self._r == 1 and self._theta:
                res = f"e^{self._theta}i"
            else:
                res = f"{self._r} * e^{self._theta}i"
        return f"({res})"

    def __repr__(self):
        if self._complex_number_type == "algebraic":
            return f"ComplexNumber(real={self._real}, imag={self._imag})"
        if self._complex_number_type == "polar":
            return f"ComplexNumber(r={self._r}, theta={self._theta})"
        return None

    def to_polar(self):
        """Convert the complex number to polar (exponential) form."""
        return ComplexNumber(r=self._r, theta=self._theta)

    def to_algebraic(self):
        """Convert the complex number to algebraic form."""
        return ComplexNumber(real=self._real, imag=self._imag)

    def scale_theta(self):
        """Scale the angle theta to be within the range [0, 2*pi)."""
        if self._complex_number_type == "polar":
            return ComplexNumber(r=self._r, theta=self._theta % (2 * math.pi))
        return self

    def round(self, n=0):
        """
        Round the real and imaginary parts of the complex number
        to the given number of decimal places.
        """
        return round(self, n)

    @property
    def complex_number_type(self):
        """Return the type of complex number representation."""
        return self._complex_number_type

    @property
    def real(self):
        """Return the real part of the complex number (if in algebraic form)."""
        if self._complex_number_type == "algebraic":
            return self._real
        return None

    @property
    def imag(self):
        """Return the imaginary part of the complex number (if in algebraic form)."""
        if self._complex_number_type == "algebraic":
            return self._imag
        return None

    @property
    def r(self):
        """Return the modulus (r) of the complex number (if in polar form)."""
        if self._complex_number_type == "polar":
            return self._r
        return None

    @property
    def theta(self):
        """Return the argument (theta) of the complex number (if in polar form)."""
        if self._complex_number_type == "polar":
            return self._theta
        return None

    @staticmethod
    def get_complex_number_type(real, imag, r, theta):
        """Determine the type of complex number representation based on provided arguments."""
        if (real is not None and imag is not None) and (r is None and theta is None):
            if not isinstance(real, (int, float)) or not isinstance(imag, (int, float)):
                raise TypeError("Arguments must be int or float")
            return "algebraic"
        if (real is None and imag is None) and (r is not None and theta is not None):
            if not isinstance(r, (int, float)) or not isinstance(theta, (int, float)):
                raise TypeError("Arguments must be int or float")
            if r < 0:
                raise ValueError("The argument r must be more or equal to 0!")
            return "polar"
        raise TypeError(
            "Check ComplexNumber arguments! Set [real, imag] or [r, theta]."
        )

    @staticmethod
    def get_complex_number_args(real, imag, r, theta, complex_number_type):
        """Calculate and return the complete set of attributes for the complex number."""
        if complex_number_type == "algebraic":
            return real, imag, math.sqrt(real**2 + imag**2), math.atan2(imag, real)
        if complex_number_type == "polar":
            return r * math.cos(theta), r * math.sin(theta), r, theta
        return None
