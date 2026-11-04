import telebot
import requests

# သင်၏ Telegram Bot အချက်အလက်များ
TOKEN = "9137803689:AAGYQD_F7IfK2Q6KKptNU3UWW7DpCA65RL4"
bot = telebot.TeleBot(TOKEN)

# GitHub Actions ဆိုင်ရာ အချက်အလက်များ (သင့်အကောင့်အမည်နှင့် နေရာများကို ထည့်ပါ)
GH_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
GH_REPO = "YOUR_GITHUB_USERNAME/ruijie-scanner"

# သိမ်းဆည်းထားမည့် Portal URL (Default အနေဖြင့်)
user_portal = "http://ยังမထည့်ရသေးပါ/portal"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = telebot.types.InlineKeyboardMarkup()
    btn_start = telebot.types.InlineKeyboardButton("🚀 စကန်ဖတ်ရန် စတင်မည်", callback_data="start_scan")
    btn_status = telebot.types.InlineKeyboardButton("📊 အခြေအနေစစ်ဆေးရန်", callback_data="check_status")
    markup.add(btn_start, btn_status)
    
    welcome_text = (
        "👋 <b>Ruijie Scanner Bot မှ ကြိုဆိုပါတယ်!</b>\n\n"
        f"🔗 <b>လက်ရှိ Portal URL:</b> <code>{user_portal}</code>\n\n"
        "Portal URL အသစ်ပြောင်းရန်: <code>/setportal သင့်ရဲ့URL</code> လို့ ရိုက်ထည့်ပါ။"
    )
    bot.reply_to(message, welcome_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(commands=['setportal'])
def set_portal(message):
    global user_portal
    try:
        # /setportal နောက်က URL ကို ယူခြင်း
        url = message.text.split(' ', 1)[1]
        user_portal = url
        bot.reply_to(message, f"✅ <b>Portal URL အောင်မြင်စွာ သိမ်းဆည်းပြီးပါပြီ:</b>\n<code>{user_portal}</code>", parse_mode="HTML")
    except IndexError:
        bot.reply_to(message, "❌ ကျေးဇူးပြု၍ URL ထည့်ပါ။ ဥပမာ - <code>/setportal http://192.168.1.1/portal</code>", parse_mode="HTML")

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "start_scan":
        bot.answer_callback_query(call.id, "GitHub Actions သို့ အချက်ပြနေသည်...")
        
        # GitHub Actions သို့ လှမ်းခေါ်ရန် (Trigger)
        url = f"https://api.github.com/repos/{GH_REPO}/dispatches"
        headers = {
            "Authorization": f"Bearer {GH_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        data = {"event_type": "start_scanner"}
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 204:
            bot.send_message(call.message.chat.id, f"🚀 <b>GitHub Actions စတင်အလုပ်လုပ်နေပါပြီ!</b>\n🔗 Portal: <code>{user_portal}</code>", parse_mode="HTML")
        else:
            bot.send_message(call.message.chat.id, f"❌ မအောင်မြင်ပါ: {response.text}")
            
    elif call.data == "check_status":
        bot.answer_callback_query(call.id, "အခြေအနေ စစ်ဆေးနေသည်...")
        bot.send_message(call.message.chat.id, f"📊 လက်ရှိ Portal URL: <code>{user_portal}</code>", parse_mode="HTML")

if __name__ == "__main__":
    print("🤖 Telegram Bot စတင်လည်ပတ်နေပါပြီ...")
    bot.infinity_polling()
