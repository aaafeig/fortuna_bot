import os

import telebot
from telebot import types

from src.balance import ensure_user_data, get_balance, update_balance
from src.slots.engine import slots_bet
from src.slots.view import slots_menu, send_slots_rules
from src.view import menu

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    """Обработчик коллбеков"""
    user_id = str(callback.message.chat.id)
    username = callback.message.chat.username or callback.message.chat.first_name or "Unknown"
    ensure_user_data(user_id, username)

    if callback.data.startswith("mine_"):
        _, x, y = callback.data.split("_")
        x, y = int(x), int(y)

        try:
            game = active_games[user_id]
        except KeyError:
            bot.answer_callback_query(callback.id, "❌ Игра не найдена!")
            return

        if (x, y) in game["revealed"]:
            bot.answer_callback_query(callback.id, "⚠️ Эта клетка уже открыта!")
            return

        game["revealed"].add((x, y))
        cell = game["field"][x][y]

        if cell == "💣":
            game_over(callback.message, user_id, x, y)
        elif cell == "⬜":
            # Пустая клетка
            bot.answer_callback_query(callback.id, "🔲 Пустая клетка. Продолжайте!")
            send_field(user_id)
        else:
            multiplier = {
                "⭐": 4,
                "🔔": 6,
                "💎": 8
            }[cell]

            game["current_win"] += game["bet"] * multiplier
            bot.answer_callback_query(
                callback.id,
                f"🎉 Вы нашли множитель x{multiplier}!\n"
                f"Ваш текущий выигрыш: {game['current_win']} монет."
            )
            send_field(user_id)

    if callback.data == "cashout":
        try:
            game = active_games[user_id]
        except KeyError:
            bot.answer_callback_query(callback.id, "❌ Игра не найдена!")
            return
        current_win = game["current_win"]
        update_balance(user_id, get_balance(user_id) + current_win)
        del active_games[user_id]
        bot.edit_message_text(
            f"💵 Вы забрали выигрыш: {current_win} монет!\nИгра завершена.",
            chat_id=callback.message.chat.id,
            message_id=callback.message.message_id
        )
        markup = types.InlineKeyboardMarkup()
        btn_play_again = types.InlineKeyboardButton("🔄 Сыграть еще раз", callback_data="mines")
        btn_main_menu = types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
        markup.row(btn_play_again, btn_main_menu)
        bot.send_message(user_id, "Хотите сыграть еще раз или вернуться в главное меню?", reply_markup=markup)
    if callback.data == "slots":
        bot.send_message(user_id, "💵 Введите сумму ставки (целое число):")
        bot.register_next_step_handler(callback.message, slots_bet)
    elif callback.data == "nvuti":
        nvuti_menu(user_id)
    elif callback.data == "nvuti_rules":
        send_nvuti_rules(user_id)
    elif callback.data == "nvuti_play":
        bot.send_message(user_id, "🎲 Введите шанс на победу (1-100):")
        bot.register_next_step_handler(callback.message, nvuti_chance)
    elif callback.data == "nvuti_less":
        nvuti_process(user_id, "less")
    elif callback.data == "nvuti_more":
        nvuti_process(user_id, "more")
    elif callback.data == "balance":
        balance = get_balance(user_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
        bot.send_message(user_id, f"💰 Ваш баланс: {balance} монет.", reply_markup=markup)
    elif callback.data == "plus":
        if get_balance(user_id) <= 0:
            update_balance(user_id, 500)
            bot.send_message(user_id, "📈 Баланс пополнен на 500 монет.")
        else:
            bot.send_message(user_id, "❌ Пополнение невозможно. Ваш баланс больше 0.\nСначала используйте текущий баланс.")
    elif callback.data == "leaderboard":
        show_leaderboard(user_id)
    elif callback.data == "play_again":
        bot.send_message(user_id, "🎰 Добро пожаловать в игру 'Слоты'!\nВведите сумму ставки (целое число):")
        bot.register_next_step_handler(callback.message, slots_bet)
    elif callback.data == "main_menu":
        menu(callback.message)
    elif callback.data == "slots_menu":
        slots_menu(user_id)
    elif callback.data == "slots_rules":
        send_slots_rules(user_id)
    elif callback.data == "mines":
        start_mines_game(callback.message)
    elif callback.data == "mines_menu":
        mines_menu(user_id)
    elif callback.data == "mines_rules":
        send_mines_rules(user_id)
bot.polling(none_stop=True)