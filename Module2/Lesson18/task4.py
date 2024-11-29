"""Lesson18 Task4: Implementation of Movie class iterator"""

from datetime import timedelta


class Movie:
    """Class for movie schedule demostration"""

    def __init__(self, title, schedule_periods):
        self._title = title
        self._schedule = schedule_periods
        self._schedule_generator = self.schedule_generator(self._schedule)

    def __repr__(self):
        return f"{self.__class__.__name__}(title='{self._title}', schedule={self._schedule})"

    def __iter__(self):
        return self

    def __next__(self):
        return next(self._schedule_generator)

    def schedule(self):
        """Print movie schedule"""
        schedule = self.schedule_generator(self._schedule)
        while True:
            try:
                print(next(schedule))
            except StopIteration:
                break

    @staticmethod
    def schedule_generator(schedule_periods):
        """Schedule generator function"""
        for period in schedule_periods:
            start, end = period
            current_date = start
            while current_date <= end:
                yield current_date
                current_date += timedelta(days=1)
