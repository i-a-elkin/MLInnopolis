"Lesson18 Task2: Implementation of CyclicIerator class iterator"


class CyclicIterator:
    """Class for cyclic iteration of input data"""

    def __init__(self, data):
        self._data = data
        self._iter = iter(self._data)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._data})"

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return next(self._iter)
        except StopIteration:
            self._iter = iter(self._data)
            return next(self._iter)

    def show_iterator_work(self, num_elts):
        """Demonstration of CyclicIterator class work"""
        cnt = 0
        while cnt < num_elts - 1:
            print(next(self), end=" ")
            cnt += 1
        print(next(self))
