import telebot
import google.generativeai as genai
import http.server
import socketserver
import threading
import time

BOT_TOKEN = "8757500280:AAGv_4TJhBDfKobD4amKFKDn4_aQgBVLVk4"
# সরাসরি কোডের ভেতরেই আপনার সঠিক কি-টি সেট করে দেওয়া হলো
GEMINI_API_KEY = "AIzaSyCX8w4vH1-N5nE8Sg7bL-Qz0mXvV9T0yYk"

bot = telebot.TeleBot(BOT_TOKEN)

# রেন্ডারের এনভায়রনমেন্ট ওভাররাইড এড়াতে সরাসরি কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "স্বাগতম Boss! আমি এখন শুধু জিমিনাই এআই (Gemini AI) দিয়ে রিপ্লাই দেওয়ার জন্য রেডি। যেকোনো প্রশ্ন জিজ্ঞেস করুন।")

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    try:
        # মডেল জেনারেট করার ফ্রেশ লজিক
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"সব সময় সংক্ষেপে বাংলা ভাষায় উত্তর দাও। ইউজারের প্রশ্ন: {message.text}"
        response = model.generate_content(prompt)
        
        if response.text:
            bot.reply_to(message, response.text)
        else:
            bot.reply_to(message, "দুঃখিত Boss, জিমিনাই কোনো রেসপন্স তৈরি করতে পারেনি।")
            
    except Exception as e:
        print(f"Gemini Error: {e}")
        bot.reply_to(message, f"দুঃখিত Boss, জিমিনাই এপিআই কানেক্ট করতে কোনো সমস্যা হচ্ছে।")

def run_dummy_server():
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", 8080), handler) as httpd:
        httpd.serve_forever()

if __name__ == "__main__":
    server_thread = threading.Thread(target=run_dummy_server, daemon=True)
    server_thread.start()
    
    try:
        bot.delete_webhook(drop_pending_updates=True)
        time.sleep(1)
    except Exception as e:
        print(f"Webhook error: {e}")
        
    bot.infinity_polling()
