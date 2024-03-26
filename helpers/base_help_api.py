from helpers.__init__ import datetime


class HelperApiTests:
    @staticmethod
    def is_time_close(expected, actual, delta_seconds=60):
        expected_time = datetime.strptime(expected, '%a, %d %b %Y %H:%M')
        actual_time = datetime.strptime(actual, '%a, %d %b %Y %H:%M:%S GMT')
        return abs((expected_time - actual_time).total_seconds()) <= delta_seconds
