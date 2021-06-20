from datetime import datetime
import pytz


class Purchase:
    def __init__(self, title, buyers, payers, amount):
        self.title = title
        self.date = Purchase._get_current_date()
        self.buyers = buyers
        self.payers = payers
        self.amount = amount

    @staticmethod
    def _get_current_date() -> str:
        tz = "Europe/Kiev"
        timezone = pytz.timezone(tz)

        date = datetime.now(tz=timezone)
        return date.strftime(fmt="%m/%d/%Y, %H:%M:%S")  # 12/24/2018, 04:59:31
