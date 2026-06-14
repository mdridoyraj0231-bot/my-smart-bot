import telebot
from telebot import types
import google.generativeai as genai
import http.server
import socketserver
import threading

# আপনার তথ্যসমূহ
BOT_TOKEN = "8887971553:AAGefLBl1nBBLtGPMwldt7oNyD5hwD4IgVI"
GEMINI_API_KEY = "AIzaSyCX8w4vH1-N5nE8Sg7bL-Qz0mXvV9T0yYk"
ADMIN_ID = "8762376045"
BKASH_NUMBER = "01727671230"
SUPPORT_LINK = "https://t.me/Ridoy_Official_penal"
PANEL_VIDEO_LINK = "https://vt.tiktok.com/ZSQQkQVFr/"
PANEL_GROUP_LINK = "https://t.me/+oe_rcewUi142ZmNl"

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

# মেনু বাটন ফাংশন
def get_main_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("কাস্টমার সার্ভিস", url=SUPPORT_LINK))
    markup.add(types.InlineKeyboardButton("প্যানেল রিভিউ ভিডিও", url=PANEL_VIDEO_LINK))
    markup.add(types.InlineKeyboardButton("ক্রয় প্যানেল", callback_data="buy_panel"))
    return markup

# নিচের স্থায়ী মেনু বাটন
def get_reply_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    markup.add(types.KeyboardButton("🏠 মেনু"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    text = "স্বাগতম Boss!" if str(message.from_user.id) == ADMIN_ID else "স্বাগতম! আমি আপনার স্মার্ট বট।"
    bot.send_message(message.chat.id, text, reply_markup=get_main_markup())
    bot.send_message(message.chat.id, "নিচে মেনু বাটনটি দেখুন:", reply_markup=get_reply_keyboard())

@bot.message_handler(commands=['health'])
def health_check(message):
    bot.reply_to(message, "বট একদম সচল আছে, Boss!")

@bot.message_handler(func=lambda message: message.text == "🏠 মেনু")
def show_menu(message):
    bot.reply_to(message, "আবার শুরুতে স্বাগতম, মেনু থেকে বেছে নিন:", reply_markup=get_main_markup())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "buy_panel":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("ক্রয় করুন", callback_data="payment_info"))
        bot.send_message(call.message.chat.id, "৬ মাসের জন্য ২৫০ টাকা। আপনি কি ইচ্ছুক?", reply_markup=markup)
    elif call.data == "payment_info":
        bot.send_message(call.message.chat.id, f"আমাদের বিকাশ নাম্বার: {BKASH_NUMBER}\nপেমেন্ট করে স্ক্রিনশট পাঠান।")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text.lower()
    
    if "প্যানেল" in text or "panel" in text:
        bot.reply_to(message, "আমাদের প্যানেলটি হলো এভারগ্রিন! এতে কোনো প্রকার ব্যান ইস্যু নেই এবং এটি বাজারের সেরা প্যানেল।", reply_markup=get_reply_keyboard())
    elif "এডমিন" in text or "admin" in text or "ridoy" in text:
        bot.reply_to(message, "আমাদের এডমিন Ridoy ভাই একজন জিনিয়াস! প্যানেল নিয়ে তার নলেজ অতুলনীয় এবং সবসময় আমাদের জন্য বেস্ট সাপোর্ট নিশ্চিত করেন।", reply_markup=get_reply_keyboard())
    
    else:
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = (
                f"তুমি একজন স্মার্ট অ্যাসিস্ট্যান্ট। যদি ইউজার তার দেশের নাম উল্লেখ করে, তবে সেই দেশের ভাষায় উত্তর দাও। "
                f"যদি ইউজার কোন দেশের নাম না বলে, তবে সব সময় বাংলা ভাষায় উত্তর দাও। "
                f"ইউজারের প্রশ্ন: {message.text}"
            )
            response = model.generate_content(prompt)
            bot.reply_to(message, response.text, reply_markup=get_reply_keyboard())
        except Exception as e:
            print(f"Error: {e}")
            bot.reply_to(message, "দুঃখিত Boss, এই মুহূর্তে সার্ভারে সমস্যা হচ্ছে। মেনু বাটনে ক্লিক করুন।", reply_markup=get_reply_keyboard())

# রেন্ডার ফ্রি সার্ভার সচল রাখার জন্য হালকা ব্যাকগ্রাউন্ড পিং পোর্ট
def run_dummy_server():
    handler = http.server.SimpleHTTPRequestHandler
    # রেন্ডার ডিফল্টভাবে ১০000 বা ৮০৮০ পোর্ট খোঁজে
    with socketserver.TCPServer(("", 8080), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    # মেইন বট পোলিং এর সাথে প্যারালাল সার্ভার রান করার বুদ্ধি
    server_thread = threading.Thread(target=run_dummy_server, daemon=True)
    server_thread.start()
    
    bot.infinity_polling()
