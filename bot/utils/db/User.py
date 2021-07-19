class User:
    def __init__(self, user_id: int, cards, username: str, full_name: str):
        self.telegram_id = user_id
        self.cards = cards
        self.username = username
        self.full_name = full_name
