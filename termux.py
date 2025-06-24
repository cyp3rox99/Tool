import requests import random import string import time from colorama import Fore, Style, init

init(autoreset=True)

-----------------------------

إعداد الواجهة البسيطة

-----------------------------

def banner(): print(Fore.RED + Style.BRIGHT + """


---

/ / ___  / / / / __ \ / -) _ / _  / -) _  / -)/ //_////_,/_/_,/_(_)
2ZOLKA | Instagram Username Checker """)

-----------------------------

توليد يوزرات

-----------------------------

def generate_usernames(length, count): usernames = [] characters = string.ascii_lowercase + string.digits + "._" for _ in range(count): uname = ''.join(random.choice(characters) for _ in range(length)) usernames.append(uname) return usernames

-----------------------------

التحقق من توفر اليوزر

-----------------------------

def check_username(username): url = f"https://www.instagram.com/{username}/" headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)" } response = requests.get(url, headers=headers) if response.status_code == 404: return True  # متاح return False  # غير متاح أو موجود

-----------------------------

الواجهة الرئيسية

-----------------------------

def main(): banner() length = int(input(Fore.CYAN + "[+] Enter username length (3-4): ")) count = int(input(Fore.CYAN + "[+] How many usernames to check: ")) save_file = open("available.txt", "w")

usernames = generate_usernames(length, count)
for username in usernames:
    print(Fore.YELLOW + f"[*] Checking: {username}...", end="")
    try:
        if check_username(username):
            print(Fore.GREEN + " [AVAILABLE]")
            save_file.write(username + "\n")
        else:
            print(Fore.RED + " [TAKEN]")
    except:
        print(Fore.MAGENTA + " [ERROR]")
    time.sleep(1.5)  # تهدئة بسيطة لتجنب الحظر

save_file.close()
print(Fore.CYAN + "\n[✓] Done. Available usernames saved in available.txt")

if name == "main": main()

