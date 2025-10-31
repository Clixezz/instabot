from telebot import TeleBot, types
from langs import LANGS  # <--- bu orqali tillarni chaqiramiz

bot = TeleBot("8307260139:AAFDb1BT85DAky4PJhNBstR8nNvXm6B6JRs", parse_mode="HTML")

# Foydalanuvchi tanlagan tillarni saqlash uchun
user_langs = {}

@bot.message_handler(commands=['start'])
def start(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("🇺🇿 O‘zbekcha", callback_data='lang_uz'),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru'),
        types.InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')
    )
    bot.send_message(
        msg.chat.id,
        "Tilni tanlang / Choose language / Выберите язык:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("lang_"))
def set_lang(call):
    lang = call.data.split("_")[1]
    user_langs[call.from_user.id] = lang
    bot.answer_callback_query(call.id, f"✅ Til tanlandi: {lang.upper()}")
    bot.send_message(call.message.chat.id, LANGS[lang]["menu"])

@bot.message_handler(commands=['about'])
def about(msg):
    bot.send_message(
        msg.chat.id,
        "🤖 <b>Instagram Video Downloader Bot</b>\n\n"
        "Bu bot orqali Instagram’dagi videoni osongina yuklab olishingiz mumkin.\n\n"
        "👨‍💻 Dasturchi: @your_username"
    )

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    user_id = message.from_user.id
    lang = user_langs.get(user_id, "uz")  # default til — o‘zbek
    link = message.text.strip()

    if "instagram.com" not in link:
        bot.reply_to(message, LANGS[lang]["wrong"])
        return

    new_link = link.replace("www.", "kk")
    bot.send_message(message.chat.id, new_link, disable_web_page_preview=False)

bot.infinity_polling()
