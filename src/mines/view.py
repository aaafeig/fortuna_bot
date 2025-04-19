from telebot import types

from conf import bot


def mines_menu(user_id):
    markup = types.InlineKeyboardMarkup()
    btn_play = types.InlineKeyboardButton("▶️ Начать играть", callback_data="mines")
    btn_rules = types.InlineKeyboardButton(
        "📚 Правила игры", callback_data="mines_rules"
    )
    btn_bck = types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")
    markup.row(btn_play, btn_rules)
    markup.row(btn_bck)
    bot.send_message(
        user_id,
        "💣 Добро пожаловать в игру Мины! Выберите действие:",
        reply_markup=markup,
    )


def send_mines_rules(user_id):
    markup = types.InlineKeyboardMarkup()
    btn_bck = types.InlineKeyboardButton("🏠 Меню", callback_data="main_menu")
    btn_play = types.InlineKeyboardButton("▶️ Играть", callback_data="mines")
    markup.row(btn_play, btn_bck)
    bot.send_message(
        user_id,
        (
            "💣 Правила игры мин:\n"
            "1️⃣ Сделайте ставку.\n"
            "2️⃣ Открывайте клетки, избегая мин (💣).\n"
            "3️⃣ Находите множители: ⭐️ (x1), 🔔 (x2), 💎 (x4)"
            "💰 После каждого раунда вы можете забрать выигрыш или продолжить."
        ),
        reply_markup=markup,
    )
