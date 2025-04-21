import random

from telebot import types
from src.balance import get_balance, update_balance
from conf import bot

active_games = {}


def generate_field(user_id):
    if user_id not in active_games:
        active_games[user_id] = {}

    field = [["⬜"] * 5 for _ in range(5)]
    mines_count = 12
    multiplier_symbols = ["⭐", "🔔", "💎"]

    for _ in range(mines_count):
        while True:
            x, y = random.randint(0, 4), random.randint(0, 4)
            if field[x][y] == "⬜":
                field[x][y] = "💣"
                break

    for symbol, count in zip(multiplier_symbols, [3, 2, 2]):
        for _ in range(count):
            while True:
                x, y = random.randint(0, 4), random.randint(0, 4)
                if field[x][y] == "⬜":
                    field[x][y] = symbol
                    break

    active_games[user_id]["field"] = field
    active_games[user_id]["revealed"] = set()
    active_games[user_id]["current_win"] = 0


def send_field(user_id):
    if user_id not in active_games:
        return

    game = active_games[user_id]
    field = game["field"]
    revealed = game["revealed"]
    current_win = game["current_win"]

    markup = types.InlineKeyboardMarkup(row_width=5)  # Поле 5x5
    for i in range(5):
        buttons = []
        for j in range(5):
            if (i, j) in revealed:
                buttons.append(
                    types.InlineKeyboardButton(field[i][j], callback_data=f"noop")
                )
            else:
                buttons.append(
                    types.InlineKeyboardButton("❔", callback_data=f"mine_{i}_{j}")
                )
        markup.row(*buttons)

    chat_id = game.get("chat_id")
    message_id = game.get("message_id")
    markup.add(
        types.InlineKeyboardButton("💰 Забрать выигрыш", callback_data="cashout")
    )
    if chat_id and message_id:
        # Обновляем существующее сообщение
        bot.edit_message_text(
            f"💣 Выберите клетку, чтобы открыть её.\n"
            f"💵 Ваш текущий выигрыш: {current_win} монет.",
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=markup,
        )
    else:
        sent_message = bot.send_message(
            user_id,
            f"💣 Выберите клетку, чтобы открыть её.\n"
            f"💵 Ваш текущий выигрыш: {current_win} монет.",
            reply_markup=markup,
        )
        game["chat_id"] = sent_message.chat.id
        game["message_id"] = sent_message.message_id


def start_mines_game(message):
    user_id = str(message.chat.id)
    active_games[user_id] = {
        "round": 1,
        "bet": 0,
        "current_win": 0,
        "field": [],
        "revealed": set(),
    }
    bot.send_message(user_id, "💵 Введите сумму ставки (целое число):")
    if user_id not in active_games:
        active_games[user_id] = {
            "field": generate_field(user_id, 1),
            "revealed": set(),
            "current_win": 0,
            "bet": 0,
        }
    bot.register_next_step_handler(message, set_mines_bet)


def set_mines_bet(message):
    user_id = str(message.chat.id)
    if not message.text.isdigit():
        bot.send_message(user_id, "⚠️ Введите корректное число (целое и положительное):")
        bot.register_next_step_handler(message, set_mines_bet)
        return

    bet = int(message.text)
    balance = get_balance(user_id)

    if bet <= 0:
        bot.send_message(user_id, "⚠️ Ставка должна быть больше 0. Попробуйте снова:")
        bot.register_next_step_handler(message, set_mines_bet)
        return

    if bet > balance:
        bot.send_message(
            user_id,
            f"❌ Ставка превышает ваш баланс! Ваш баланс: 💵 {balance} монет.\nВведите ставку заново:",
        )
        bot.register_next_step_handler(message, set_mines_bet)
        return
    active_games[user_id]["bet"] = bet
    update_balance(user_id, balance - bet)
    bot.send_message(user_id, f"💰 Ставка принята: {bet} монет.\nНачнем игру!")

    generate_field(user_id)
    send_field(user_id)


def game_over(message, user_id, x, y):
    if user_id not in active_games:
        bot.send_message(user_id, "❌ Игра не найдена или уже завершена.")
        return
    game = active_games[user_id]
    field = game["field"]
    field[x][y] = "💥"
    revealed_field = "\n".join(" ".join(row) for row in field)

    del active_games[user_id]
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🔄 Сыграть ещё раз", callback_data="mines"),
        types.InlineKeyboardButton("🏠 В меню", callback_data="main_menu"),
    )
    bot.send_message(
        user_id,
        f"💥 Вы попали на мину!\n\nИгровое поле:\n{revealed_field}",
        reply_markup=markup,
    )
