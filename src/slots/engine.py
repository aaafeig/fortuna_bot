import random

from main import bot


def slots_bet(message):
    user_id = str(message.chat.id)
    if not message.text.isdigit():
        bot.send_message(user_id, "⚠️ Введите корректное число (целое и положительное):")
        bot.register_next_step_handler(message, slots_bet)
        return

    bet = int(message.text)
    balance = get_balance(user_id)

    if balance == 0:
        bot.send_message(user_id, "❌ У вас недостаточно средств для игры. Пополните баланс, чтобы начать играть!")
        markup = types.InlineKeyboardMarkup()
        btn_plus_balance = types.InlineKeyboardButton("🔄 Пополнить баланс", callback_data="plus")
        markup.add(btn_plus_balance)
        bot.send_message(user_id, "💰 Ваш баланс: 0 монет. Пополните баланс, чтобы начать играть.", reply_markup=markup)
        return

    if bet <= 0:
        bot.send_message(user_id, "⚠️ Ставка должна быть больше 0. Попробуйте снова:")
        bot.register_next_step_handler(message, slots_bet)
        return

    if bet > balance:
        bot.send_message(user_id, f"❌ У вас недостаточно средств для ставки! Ваш баланс: 💵 {balance} монет.")
        bot.send_message(user_id, "Введите ставку заново:")
        bot.register_next_step_handler(message, slots_bet)
        return
    result, winnings, loss = play_slots(bet)
    update_balance(user_id, balance - bet + winnings)

    if winnings > 0:
        bot.send_message(user_id, f"🎰 {result}\n"
                                  f"🎉 Поздравляем, вы выиграли 💵 {round(winnings)} монет!\n"
                                  f"Ваш текущий баланс: 💵 {get_balance(user_id)} монет.")
    else:
        bot.send_message(user_id, f"🎰 {result}\n"
                                  f"😢 Увы, вы проиграли.\n"
                                  f"Ваш текущий баланс: 💵 {get_balance(user_id)} монет.")

    markup = types.InlineKeyboardMarkup()
    btn_play_again = types.InlineKeyboardButton("🔄 Сыграть еще раз", callback_data="play_again")
    btn_main_menu = types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    markup.row(btn_play_again, btn_main_menu)
    bot.send_message(user_id, "Хотите сыграть еще раз или вернуться в главное меню?", reply_markup=markup)
def play_slots(bet):
    slots = ["🍒", "🍋", "🔔", "🍉", "⭐", "7️⃣"]
    spin = random.choices(slots, k=3)
    result = " | ".join(spin)

    multipliers = {
        "🍒🍒🍒": 5,
        "🍋🍋🍋": 4,
        "🔔🔔🔔": 8,
        "🍉🍉🍉": 10,
        "⭐⭐⭐": 12,
        "7️⃣7️⃣7️⃣": 25,
    }

    two_symbol_multipliers = {
        "🍒🍒": 1.1,
        "🍋🍋": 1.2,
        "🔔🔔": 1.3,
        "🍉🍉": 1.4,
        "⭐⭐": 1.5,
        "7️⃣7️⃣": 2,
    }


    spin_key = "".join(spin)

    if spin[0] == spin[1] == spin[2]:
        winnings = bet * multipliers.get(spin_key, 0)
    elif spin[0] == spin[1] or spin[1] == spin[2] or spin[0] == spin[2]:
        if spin[0] == spin[1]:
            two_key = spin[0] + spin[1]
        elif spin[1] == spin[2]:
            two_key = spin[1] + spin[2]
        else:
            two_key = spin[0] + spin[2]
        winnings = bet * two_symbol_multipliers.get(two_key, 0)
    else:
        winnings = 0

    return result, winnings, 0