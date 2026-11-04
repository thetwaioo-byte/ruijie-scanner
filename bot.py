import telebot
import requests

TOKEN = "9137803689:AAGYQD_F7IfK2Q6KKptNU3UWW7DpCA65RL4"
bot = telebot.TeleBot(TOKEN)

# သင့်ရဲ့ GitHub အချက်အလက်များကို ဒီမှာ ထည့်ပါ
GH_TOKEN = "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"
GH_REPO = "thetwaioo-byte/ruijie-scanner"  # သင့် GitHub Username နှင့် Repository နာမည်

current_portal = "http://ยังမထည့်ရသေးပါ/portal"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "👋 Ruijie Scanner Bot သို့ ကြိုဆိုပါသည်!\n\nPortal URL ထည့်ရန်:\n`/setportal သင့်ရဲ့PortalURL` ဟု ရိုက်ထည့်ပါ။", parse_mode="HTML")

@bot.message_handler(commands=['setportal'])
def set_portal(message):
    global current_portal
    try:
        current_portal = message.text.split(' ', 1)[1]
        
        # GitHub Actions သို့ Portal URL နှင့်တကွ လှမ်းခေါ်ခြင်း (Trigger)
        url = f"https://api.github.com/repos/{GH_REPO}/dispatches"
        headers = {
            "Authorization": f"Bearer {GH_TOKEN}",
            "Accept": "application/vnd.github+json"
        }
        data = {
            "event_type": "start_scanner",
            "client_payload": {"portal_url": current_portal}
        }
        
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 204:
            bot.reply_to(message, f"✅ <b>Portal URL အောင်မြင်စွာ သိမ်းဆည်းပြီး GitHub Actions စတင်နေပါပြီ!</b>\n🔗 <code>{current_portal}</code>", parse_mode="HTML")
        else:
            bot.reply_to(message, f"❌ မအောင်မြင်ပါ: {response.text}")
            
    except IndexError:
        bot.reply_to(message, "❌ ကျေးဇူးပြု၍ URL ထည့်ပါ။ ဥပမာ - <code>/setportal http://192.168.1.1/portal</code>", parse_mode="HTML")

if __name__ == "__main__":
    print("🤖 Telegram Bot စတင်လည်ပတ်နေပါပြီ...")
    bot.infinity_polling()
    
