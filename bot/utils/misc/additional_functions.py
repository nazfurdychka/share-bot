from loader import db

from bot.keyboards.inline.CardsKeyboards.CardListKeyboard import EditButton
from bot.keyboards.inline.CardsKeyboards.UserCardsKeyboard import UserCard
from bot.utils.misc.parsers import get_buyers_payers_amount_from_purchase


def edit_button_window(chat_id: int):
    keyboard = EditButton.keyboard
    cards = db.get_cards_from_group(group_id=chat_id)
    res = str()
    for k in cards.keys():
        res += "\t\t\t" + k[0] + ": \n"
        for key in cards[k].keys():
            res += "\t\t\t\t\t\t" + '`' + key + '`' + " " + cards[k][key] + "\n"
    return res, keyboard


def user_cards_window(user_id: str, user_name: str):
    keyboard = UserCard(user_id).keyboard
    user_cards = db.get_user_cards(telegram_id=int(user_id))
    check = "card" if len(user_cards.keys()) == 1 else "cards"
    res = user_name.replace(", ", " ") + " " + check + ": \n"
    for card, bank in user_cards.items():
        res += "\t\t\t " + '`' + card + '`' + " " + bank + "\n"
    return res, keyboard


def make_purchase_text(purchase_id: str):
    purchase = db.get_purchase(purchase_id)
    text = "`{} - {}`\n".format(purchase["title"], purchase["amount"])
    text += "Buyers:\n"
    for _, buyer_amount in purchase["buyers"].items():
        amount = buyer_amount[0]
        user = buyer_amount[1]
        text += f"`{user} - {amount}`\n"
    text += "Payers:\n"
    for payer in purchase["payers"]:
        user = payer[1]
        text += f"`{user}`"
        text += '\n'
    return text


def calculate(buyers: dict[str, int], payers: list[str], amount: float) -> dict:
    cnt = len(payers)
    d = amount / cnt
    result = dict()

    for payer in payers:
        result[payer] = d

    for payer in payers:
        if payer in buyers:
            diff = result[payer] - buyers[payer]
            result[payer] = diff
            del buyers[payer]

    for buyer in buyers:
        result[buyer] = -1 * buyers[buyer]

    return result


def check_if_purchase_correct(purchase: dict):
    # if res == -2: -> can`t calculate purchase!
    # elif res == -1: -> can calculate purchase but with some nuances
    # elif res == 0: -> everything is ok
    res, output = 0, ""
    buyers, payers, amount = get_buyers_payers_amount_from_purchase(purchase)
    if len(payers) == 0:
        res, output = -2, "_Payers_ field is empty! Can't calculate this purchase!"
    elif len(buyers) == 0:
        res, output = -1, "Take into account that _buyers_ field is empty, something may be wrong!\n"
    elif sum(buyers.values()) != amount:
        res, output = -1, "Please be aware that total cost of the purchase is different from the amount of money that buyers paid!\n"
    return res, output


def make_calculate_text(result: dict) -> str:
    output = "Result: \n"
    for k, v in result.items():
        output += "\t\t\t\t" + "`" + k + '\t' + "`" + " `" + str(v) + "` \n"

    return output


def help_text() -> str:
    text = "Groups commands: \n" \
           "/manage_cards - here you can add your cards and see another cards \n" \
           "/create_purchase - use this command if you want to distribute money \n" \
           "/get_all_purchases - will help you to get all purchases that you created \n" \
           "/add_card - if you want me to add your card"
    return text
