import telebot
import google.generativeai as genai
import http.server
import socketserver
import threading

BOT_TOKEN = "8757500280:AAGv_4TJhBDfKobD4amKFKDn4_aQgBVLVk4"
GEMINI_API_KEY = "AIzaSyCX8w4vH1-N5nE8Sg7bL-Qz0mXvV9T0yYk"

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম Boss! আমি এখন শুধু জিমিনাই এআই (Gemini AI) দিয়ে রিপ্লাই দেওয়ার জন্য রেডি। যেকোনো প্রশ্ন জিজ্ঞেস করুন।")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"সব সময় সংক্ষেপে বাংলা ভাষায় উত্তর দাও। ইউজারের প্রশ্ন: {message.text}"
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "দুঃখিত Boss, জিমিনাই এপিআই কানেক্ট করতে কোনো সমস্যা হচ্ছে।")

def run_dummy_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8080), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_dummy_server, daemon=True)
    server_thread.start()
    bot.infinity_polling()
