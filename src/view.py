from telebot import types

from conf import bot
from src.balance import update_username, ensure_user_data, user_balances


@bot.message_handler(commands=["start"])
def start(message):
    """Обрабатывает команду старт и выводит действия"""
    user_id = str(message.chat.id)
    username = message.chat.username or message.chat.first_name or "Unknown"
    ensure_user_data(user_id, username)
    update_username(user_id, username)

    markup = types.InlineKeyboardMarkup()
    btn_slots = types.InlineKeyboardButton("🎰 Слоты", callback_data="slots_menu")
    btn_nvuti = types.InlineKeyboardButton("🎲 Nvuti", callback_data="nvuti")
    btn_leaderboard = types.InlineKeyboardButton(
        "🏆 Лидерборд", callback_data="leaderboard"
    )
    btn_mines = types.InlineKeyboardButton("💣 Мины", callback_data="mines_menu")
    markup.row(btn_slots, btn_nvuti, btn_mines)
    btn_menu = types.InlineKeyboardButton("Меню", callback_data="main_menu")
    markup.row(btn_leaderboard)
    markup.row(btn_menu)
    bot.send_message(
        user_id,
        "👋Привет! 🤖Это бот Fortuna. 🎮В какую игру вы хотите сыграть?",
        reply_markup=markup,
    )


@bot.message_handler(commands=["menu"])
def menu(message):
    """Функция для показа меню"""
    user_id = str(message.chat.id)
    markup = types.InlineKeyboardMarkup()
    btn_mines = types.InlineKeyboardButton("💣 Мины", callback_data="mines_menu")
    btn_slots = types.InlineKeyboardButton("🎰 Слоты", callback_data="slots_menu")
    btn_nvuti = types.InlineKeyboardButton("🎲 Nvuti", callback_data="nvuti")
    btn_balance = types.InlineKeyboardButton(
        "💰 Узнать баланс", callback_data="balance"
    )
    btn_leaderboard = types.InlineKeyboardButton(
        "🏆 Лидерборд", callback_data="leaderboard"
    )
    markup.row(btn_slots, btn_nvuti)
    markup.row(btn_mines)
    markup.row(btn_balance, btn_leaderboard)
    btn_plus_balance = types.InlineKeyboardButton(
        "➕ Пополнить баланс", callback_data="plus"
    )
    markup.row(btn_plus_balance)
    bot.send_message(
        user_id, "🎮 Главное меню. В какую игру вы хотите сыграть?", reply_markup=markup
    )


def show_leaderboard(user_id):
    leaderboard = sorted(
        user_balances.items(), key=lambda x: x[1]["balance"], reverse=True
    )[:10]
    leaderboard_text = "🏆 ТОП-10 игроков:\n\n"
    for i, (uid, data) in enumerate(leaderboard, start=1):
        leaderboard_text += f"{i}. {data['username']} — {data['balance']} монет\n"

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
    bot.send_message(user_id, leaderboard_text, reply_markup=markup)
