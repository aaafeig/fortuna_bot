import json
import math

DEFAULT_BALANCE = 1000
SAVE_FILE = "user_balances.json"

try:
    with open(SAVE_FILE, "r") as file:
        user_balances = json.load(file)
except FileNotFoundError:
    user_balances = {}

def ensure_user_data(user_id, username=None):
    """Записывает новых игроков в лидерборд"""
    if user_id not in user_balances or not isinstance(user_balances[user_id], dict):
        user_balances[user_id] = {"balance": DEFAULT_BALANCE, "username": username or "Unknown"}
    if "balance" not in user_balances[user_id] or not isinstance(user_balances[user_id]["balance"], (int, float)):
        user_balances[user_id]["balance"] = DEFAULT_BALANCE
    if "username" not in user_balances[user_id] or not isinstance(user_balances[user_id]["username"], str):
        user_balances[user_id]["username"] = username or "Unknown"
def save_balances():
    with open(SAVE_FILE, "w") as file_balances:
        json.dump(user_balances, file_balances)

def get_balance(user_id):
    ensure_user_data(user_id)
    user_balance = user_balances[user_id]["balance"]
    return math.floor(user_balance)

def update_balance(user_id, new_balance):
    ensure_user_data(user_id)
    user_balances[user_id]["balance"] = math.floor(new_balance)
    save_balances()

def update_username(user_id, username):
    ensure_user_data(user_id, username)
    user_balances[user_id]["username"] = username
    save_balances()