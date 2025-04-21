from telebot import types
from conf import bot


def slots_menu(user_id):
    markup = types.InlineKeyboardMarkup()
    btn_play = types.InlineKeyboardButton("▶️ Начать играть", callback_data="slots")
    btn_rules = types.InlineKeyboardButton(
        "📚 Правила игры", callback_data="slots_rules"
    )
    btn_bck = types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")
    markup.row(btn_play, btn_rules)
    markup.row(btn_bck)
    bot.send_message(
        user_id,
        "🎰 Добро пожаловать в игру 'Слоты'! Выберите действие:",
        reply_markup=markup,
    )


def send_slots_rules(user_id):
    markup = types.InlineKeyboardMarkup()
    btn_bck = types.InlineKeyboardButton("🏠 Меню", callback_data="main_menu")
    btn_play = types.InlineKeyboardButton("▶️ Играть", callback_data="slots")
    markup.row(btn_play, btn_bck)
    bot.send_message(
        user_id,
        (
            "🎰 Правила игры слотов:\n"
            "1️⃣ выберите ставку не превосходящаю ваш баланс.\n"
            "2️⃣ ждите результатов игры.\n"
            "получаете свой выйигрыш исходя из выпавшей комбинации."
        ),
        reply_markup=markup,
    )
