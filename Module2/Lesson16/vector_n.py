"""Lesson 16 Task 2: Implementation of a N-dimensional Vector Class."""


class VectorN:
    """
    A class representing a N-dimensional vector with support for
    vector operations such as dot product, cosine similarity, and norm.
    """

    def __init__(self, data):
        if not isinstance(data, list):
            raise ValueError("Data must be a list!")
        if not data or not all((isinstance(item, (int, float))) for item in data):
            raise ValueError("Data must be a list of numbers!")
        self._values = data

    def __str__(self):
        return f"{self._values}"

    def __repr__(self):
        return f"VectorN({self._values})"

    def __len__(self):
        return len(self._values)

    def __add__(self, other):
        self.check_instances(self, other)
        return VectorN(
            [
                value_self + value_other
                for value_self, value_other in zip(self.values, other.values)
            ]
        )

    def __sub__(self, other):
        self.check_instances(self, other)
        return VectorN(
            [
                value_self - value_other
                for value_self, value_other in zip(self.values, other.values)
            ]
        )

    def __matmul__(self, other):
        self.check_instances(self, other)
        return sum(
            value_self * value_other
            for value_self, value_other in zip(self.values, other.values)
        )

    def dot_product(self, other):
        """Calculates the dot product between this vector and another."""
        return self @ other

    def norm(self):
        """Computes the Euclidean norm (magnitude) of the vector."""
        return sum(item**2 for item in self.values) ** 0.5

    def cosine_similarity(self, other):
        """
        Calculates the cosine similarity (cosine of angle)
        between this vector and another.
        """
        self.check_instances(self, other)
        if not self.norm() or not other.norm():
            raise ValueError("Both operands must have non zero length!")
        return (self @ other) / (self.norm() * other.norm())

    @property
    def values(self):
        """The coordinates of the vector as a list of numbers."""
        return self._values

    @staticmethod
    def check_instances(instance1, instance2):
        """Validates instances of VectorN."""
        if not isinstance(instance1, VectorN) or not isinstance(instance2, VectorN):
            raise ValueError("Both operands must be VectorN!")
        if len(instance1) != len(instance2):
            raise ValueError("Both operands must be of the same dimension!")
