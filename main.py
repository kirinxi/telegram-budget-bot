import telebot
import json
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

DATA_FILE = "budgetdata.json"

# Инициализация данных
def load_data():
    if not os.path.exists(DATA_FILE):
        return {"balance": 0, "income": [], "expenses": [], "obligations": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

# Команды
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет! Я помогу вести твою финансовую жизнь.\nОтправь /help, чтобы увидеть список команд.")

@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, """
📘 Доступные команды:
/add_income сумма комментарий — добавить доход
/add_expense сумма комментарий — добавить расход
/balance — текущий остаток
/plan — список обязательных платежей
""")

@bot.message_handler(commands=["add_income"])
def add_income(message):
    try:
        parts = message.text.split(maxsplit=2)
        amount = float(parts[1])
        comment = parts[2] if len(parts) > 2 else ""
        data = load_data()
        data["income"].append({"amount": amount, "comment": comment})
        data["balance"] += amount
        save_data(data)
        bot.send_message(message.chat.id, f"✅ Доход {amount:.2f}₽ добавлен: {comment}")
    except:
        bot.send_message(message.chat.id, "❗ Используй формат: /add_income сумма комментарий")

@bot.message_handler(commands=["add_expense"])
def add_expense(message):
    try:
        parts = message.text.split(maxsplit=2)
        amount = float(parts[1])
        comment = parts[2] if len(parts) > 2 else ""
        data = load_data()
        data["expenses"].append({"amount": amount, "comment": comment})
        data["balance"] -= amount
        save_data(data)
        bot.send_message(message.chat.id, f"💸 Расход {amount:.2f}₽ добавлен: {comment}")
    except:
        bot.send_message(message.chat.id, "❗ Используй формат: /add_expense сумма комментарий")

@bot.message_handler(commands=["balance"])
def show_balance(message):
    data = load_data()
    balance = data["balance"]
    bot.send_message(message.chat.id, f"💰 Текущий остаток: {balance:.2f}₽")

@bot.message_handler(commands=["plan"])
def show_plan(message):
    obligations = [
        {"comment": "Автокредит 25.07", "amount": 58000},
        {"comment": "Озон рассрочка 28.07", "amount": 14535},
        {"comment": "Детский сад до 31.07", "amount": 75000}
    ]
    text = "📅 Обязательные платежи:\n"
    for item in obligations:
        text += f"— {item['comment']}: {item['amount']}₽\n"
    bot.send_message(message.chat.id, text)

bot.infinity_polling()
