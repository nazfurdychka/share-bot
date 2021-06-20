from . import Purchase


class User:
    def __init__(self, user_id: int, cards: dict[int, str], username: str, first_name: str, last_name: str, list_of_purchases: list[Purchase]):
        self.user_id = user_id
        self.cards = cards
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.list_of_purchases = list_of_purchases
