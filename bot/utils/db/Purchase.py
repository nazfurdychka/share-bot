from datetime import datetime
import pytz


class Purchase:
    def __init__(self, title, amount):
        self.title = title
        self.date = Purchase._get_current_date()
        self.buyers = dict()
        self.payers = []
        self.amount = amount

    @staticmethod
    def _get_current_date() -> str:
        tz = "Europe/Kiev"
        timezone = pytz.timezone(tz)

        date = datetime.now(tz=timezone)
        return date.strftime("%d/%m/%Y, %H:%M:%S")  # 12/24/2018, 04:59:31
