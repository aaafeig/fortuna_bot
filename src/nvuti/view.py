import math

from telebot import types

from conf import bot
from src.balance import get_balance, user_balances, save_balances


def nvuti_menu(user_id):
    markup = types.InlineKeyboardMarkup()
    btn_play = types.InlineKeyboardButton("▶️ Начать играть", callback_data="nvuti_play")
    btn_rules = types.InlineKeyboardButton(
        "📚 Правила игры", callback_data="nvuti_rules"
    )
    btn_bck = types.InlineKeyboardButton("⬅️ Назад", callback_data="main_menu")
    markup.row(btn_play, btn_rules)
    markup.row(btn_bck)
    bot.send_message(
        user_id,
        "🎲 Добро пожаловать в игру Nvuti! Выберите действие:",
        reply_markup=markup,
    )


def send_nvuti_rules(user_id):
    markup = types.InlineKeyboardMarkup()
    btn_bck = types.InlineKeyboardButton("🏠 Меню", callback_data="main_menu")
    btn_play = types.InlineKeyboardButton("▶️Играть", callback_data="nvuti_play")
    markup.row(btn_play, btn_bck)
    bot.send_message(
        user_id,
        (
            "🎲 Правила игры Nvuti:\n"
            "1️⃣ Выберите шанс на победу (в процентах).\n"
            "2️⃣ Сделайте ставку.\n"
            "3️⃣ Выберите 'Больше'(больший диапазон) или 'Меньше'(меньший диапазон).\n"
            "4️⃣ Если сгенерированное число находиться в выбранном диапазоне, вы выиграли!\n"
            "💰 Чем ниже шанс на победу, тем выше выигрыш (и наоборот)."
        ),
        reply_markup=markup,
    )


def nvuti_chance(message):
    user_id = str(message.chat.id)
    if not message.text.isdigit():
        bot.send_message(user_id, "⚠️ Введите число от 1 до 100:")
        bot.register_next_step_handler(message, nvuti_chance)
        return

    chance = int(message.text)
    if chance < 1 or chance > 100:
        bot.send_message(user_id, "⚠️ Введите число от 1 до 100:")
        bot.register_next_step_handler(message, nvuti_chance)
        return

    bot.send_message(user_id, "💵 Введите сумму ставки (целое число):")
    bot.register_next_step_handler(message, nvuti_bet, chance)


def nvuti_bet(message, chance):
    user_id = str(message.chat.id)
    if not message.text.isdigit():
        bot.send_message(user_id, "⚠️ Введите корректное число (целое и положительное):")
        bot.register_next_step_handler(message, nvuti_bet, chance)
        return

    bet = int(message.text)
    balance = get_balance(user_id)
    if balance == 0:
        bot.send_message(
            user_id,
            "❌ У вас недостаточно средств для игры. Пополните баланс, чтобы начать играть!",
        )
        markup = types.InlineKeyboardMarkup()
        btn_plus_balance = types.InlineKeyboardButton(
            "🔄 Пополнить баланс", callback_data="plus"
        )
        markup.add(btn_plus_balance)
        bot.send_message(
            user_id,
            "💰 Ваш баланс: 0 монет. Пополните баланс, чтобы начать играть.",
            reply_markup=markup,
        )

    if bet <= 0:
        bot.send_message(user_id, "⚠️ Ставка должна быть больше 0. Попробуйте снова:")
        bot.register_next_step_handler(message, nvuti_bet, chance)
        return
    if bet > balance:
        bot.send_message(
            user_id,
            f"❌ У вас недостаточно средств! Ваш баланс: 💵 {balance} монет.\nВведите ставку заново:",
        )
        bot.register_next_step_handler(message, nvuti_bet, chance)
        return
    user_balances[user_id]["current_nvuti"] = {"chance": chance, "bet": bet}
    save_balances()
    less_max = math.floor((chance / 100) * 999999)
    more_min = 999999 - less_max

    markup = types.InlineKeyboardMarkup()
    btn_less = types.InlineKeyboardButton(
        f"Меньше (0 - {less_max})", callback_data="nvuti_less"
    )
    btn_more = types.InlineKeyboardButton(
        f"Больше ({more_min} - 999999)", callback_data="nvuti_more"
    )
    markup.row(btn_less, btn_more)
    bot.send_message(
        user_id,
        f"Вы выбрали шанс {chance}%.\n"
        f"Ставка: {bet} монет.\n"
        "Ваш выбор: меньше или больше?",
        reply_markup=markup,
    )
