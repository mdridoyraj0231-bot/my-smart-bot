import telebot
from telebot import types
import google.generativeai as genai
from flask import Flask
from threading import Thread

BOT_TOKEN = "8887971553:AAGefLBl1nBBLtGPMwldt7oNyD5hwD4IgVI"
GEMINI_API_KEY = "AIzaSyCX8w4vH1-N5nE8Sg7bL-Qz0mXvV9T0yYk"
ADMIN_ID = "8762376045"
BKASH_NUMBER = "01727671230"
SUPPORT_LINK = "https://t.me/Ridoy_Official_penal"
PANEL_VIDEO_LINK = "https://vt.tiktok.com/ZSQQkQVFr/"
PANEL_GROUP_LINK = "https://t.me/+oe_rcewUi142ZmNl"

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if str(message.from_user.id) == ADMIN_ID:
        greeting = "স্বাগতম Boss! আমি আপনার অপেক্ষায় ছিলাম।"
    else:
        greeting = "স্বাগতম! আমি আপনার স্মার্ট বট। আপনাকে কীভাবে সাহায্য করতে পারি?"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("কাস্টমার সার্ভিস", url=SUPPORT_LINK))
    markup.add(types.InlineKeyboardButton("প্যানেল রিভিউ ভিডিও", url=PANEL_VIDEO_LINK))
    markup.add(types.InlineKeyboardButton("ক্রয় প্যানেল", callback_data="buy_panel"))
    bot.reply_to(message, greeting, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "buy_panel")
def buy_panel(call):
    text = "৬ মাসের জন্য ২৫০ টাকা। এটি ক্রয় করলে আপনি কোনো সমস্যা ছাড়াই ৬ মাস নিশ্চিন্তে উপভোগ করতে পারবেন। আপনি কি ইচ্ছুক?"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("ক্রয় করুন", callback_data="payment_info"))
    bot.send_message(call.message.chat.id, text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "payment_info")
def payment_info(call):
    bot.send_message(call.message.chat.id, f"আমাদের বিকাশ পার্সোনাল নাম্বার: {BKASH_NUMBER}\n\n২৫০ টাকা পাঠিয়ে পেমেন্ট প্রুফ হিসেবে একটি স্ক্রিনশট পাঠান।")

@bot.message_handler(content_types=['photo'])
def handle_payment_screenshot(message):
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    bot.reply_to(message, "আপনার পেমেন্ট স্ক্রিনশটটি এডমিনের কাছে পাঠানো হয়েছে। তিনি চেক করে আপনাকে গ্রুপ লিংক দেবেন।")
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("এপ্রুভ করুন", callback_data=f"approve_{message.chat.id}"))
    markup.add(types.InlineKeyboardButton("রিজেক্ট করুন", callback_data=f"reject_{message.chat.id}"))
    bot.send_message(ADMIN_ID, "নতুন পেমেন্ট প্রুফ এসেছে!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('approve_'))
def approve_user(call):
    chat_id = call.data.split('_')[1]
    bot.send_message(chat_id, f"আপনার পেমেন্ট এপ্রুভ হয়েছে! এই লিংকে জয়েন করুন: {PANEL_GROUP_LINK}")
    bot.edit_message_text("এপ্রুভ করা হয়েছে। ✅", chat_id=call.message.chat.id, message_id=call.message.message_id)

@bot.callback_query_handler(func=lambda call: call.data.startswith('reject_'))
def reject_user(call):
    chat_id = call.data.split('_')[1]
    bot.send_message(chat_id, "দুঃখিত, আপনার পেমেন্ট রিজেক্ট করা হয়েছে।")
    bot.edit_message_text("রিজেক্ট করা হয়েছে। ❌", chat_id=call.message.chat.id, message_id=call.message.message_id)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    if "লিংক দাও" in text or "প্যানেল লিংক" in text:
        if str(message.from_user.id) == ADMIN_ID:
            bot.reply_to(message, f"অবশ্যই Boss, এই নিন আপনার প্যানেল গ্রুপের লিংক: {PANEL_GROUP_LINK}")
        return
    if "প্যানেল" in text or "panel" in text:
        bot.reply_to(message, "আমাদের প্যানেলটি সেরা এবং অত্যন্ত নির্ভরযোগ্য! এন্টি-ব্যান এবং এন্টি-ব্ল্যাকলিস্ট সুবিধা সম্পন্ন।")
    elif "এডমিন" in text or "admin" in text or "ridoy" in text:
        bot.reply_to(message, "আমাদের এডমিন Ridoy খুবই দক্ষ এবং প্যানেলের জন্য সবসময় প্রস্তুত!")
    else:
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(message.text)
            if str(message.from_user.id) == ADMIN_ID:
                bot.reply_to(message, f"Boss, {response.text}")
            else:
                bot.reply_to(message, response.text)
        except:
            bot.reply_to(message, "দুঃখিত, কোনো সমস্যার কারণে আমি উত্তর দিতে পারছি না।")

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

if __name__ == "__main__":
    Thread(target=run).start()
    bot.polling()
