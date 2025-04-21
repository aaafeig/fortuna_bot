import math
import random

from telebot import types

from conf import bot
from src.balance import user_balances, get_balance, update_balance, save_balances


def nvuti_process(user_id, choice):
    current_game = user_balances[user_id].get("current_nvuti")
    if not current_game:
        bot.send_message(
            user_id, "❌ Ошибка: текущая игра не найдена. Попробуйте начать заново."
        )
        return

    chance = current_game["chance"]
    bet = current_game["bet"]
    balance = get_balance(user_id)
    random_number = random.randint(0, 999999)

    less_max = math.floor((chance / 100) * 999999)
    more_min = 999999 - less_max
    if choice == "less":
        is_win = 0 <= random_number <= less_max
    elif choice == "more":
        is_win = more_min <= random_number <= 999999

    if is_win:
        winnings = bet * (100 / chance)
        update_balance(user_id, balance - bet + winnings)
        bot.send_message(
            user_id,
            f"🎉 Число: {random_number}. Вы выиграли {math.floor(winnings)} монет! Ваш баланс: {get_balance(user_id)}.",
        )
    else:
        update_balance(user_id, balance - bet)
        bot.send_message(
            user_id,
            f"😢 Число: {random_number}. Вы проиграли {bet} монет. Ваш баланс: {get_balance(user_id)}.",
        )

    user_balances[user_id].pop("current_nvuti", None)
    save_balances()

    markup = types.InlineKeyboardMarkup()
    btn_play_again = types.InlineKeyboardButton(
        "🔄 Сыграть еще раз", callback_data="nvuti_play"
    )
    btn_main_menu = types.InlineKeyboardButton(
        "🏠 Главное меню", callback_data="main_menu"
    )
    markup.row(btn_play_again, btn_main_menu)
    bot.send_message(
        user_id,
        "Хотите сыграть еще раз или вернуться в главное меню?",
        reply_markup=markup,
    )


def nvuti_result(callback):
    user_id = str(callback.message.chat.id)
    data = callback.data.split("_")
    choice = data[1]  # "less" или "more"
    chance = int(data[2])
    bet = int(data[3])

    balance = get_balance(user_id)
    random_number = int(random.randint(0, 999999))

    less_max = int(chance * 10000) - 1
    more_min = 1000000 - chance * 10000
    if choice == "less":
        if 0 <= random_number <= less_max:
            is_win = True
        else:
            is_win = False
    elif choice == "more":
        if more_min <= random_number <= 999999:
            is_win = True
        else:
            is_win = False
    if is_win:
        winnings = bet * (100 / chance)
        update_balance(user_id, balance - bet + winnings)
        bot.send_message(
            user_id,
            f"🎉 Число: {random_number}. Вы выиграли {math.floor(winnings)} монет! Ваш баланс: {get_balance(user_id)}.",
        )
    else:
        update_balance(user_id, balance - bet)
        bot.send_message(
            user_id,
            f"😢 Число: {random_number}. Вы проиграли {bet} монет. Ваш баланс: {get_balance(user_id)}.",
        )
