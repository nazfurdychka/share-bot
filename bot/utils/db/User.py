class User:
    def __init__(self, user_id: int, cards: dict[int, str], username: str, full_name: str, list_of_purchases: list):
        self.telegram_id = user_id
        self.cards = cards
        self.username = username
        self.full_name = full_name
        self.list_of_purchases = list_of_purchases
