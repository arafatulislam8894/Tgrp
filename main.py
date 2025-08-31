import time, os, platform

# কালার কোড
rd, gn, lgn, yw, lrd, be, pe = '\033[00;31m', '\033[00;32m', '\033[01;32m', '\033[01;33m', '\033[01;31m', '\033[94m', '\033[01;35m'
cn, k, g = '\033[00;36m', '\033[90m', '\033[38;5;130m'

# ASCII Banner লাইব্রেরি
try:
    from pyfiglet import Figlet
except ImportError:
    os.system("pip install pyfiglet")
    from pyfiglet import Figlet

def re(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.001)

if 'Windows' in platform.uname():
    from colorama import init
    init()

# 🔵 ব্যানার (Blue)
banner = f"""{be}
 /$$$$$$$$ /$$   /$$       /$$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$ /$$$$$$$       
|_____ $$ | $$  / $$      | $$__  $$ /$$__  $$| $$  /$$/|_  $$_/| $$__  $$      
     /$$/ |  $$/ $$/      | $$  \ $$| $$  \ $$| $$ /$$/   | $$  | $$  \ $$      
    /$$/   \  $$$$/       | $$$$$$$/| $$$$$$$$| $$$$$/    | $$  | $$$$$$$       
   /$$/     >$$  $$       | $$__  $$| $$__  $$| $$  $$    | $$  | $$__  $$      
  /$$/     /$$/\  $$      | $$  \ $$| $$  | $$| $$\  $$   | $$  | $$  \ $$      
 /$$$$$$$$| $$  \ $$      | $$  | $$| $$  | $$| $$ \  $$ /$$$$$$| $$$$$$$/      
|________/|__/  |__/      |__/  |__/|__/  |__/|__/  \__/|______/|_______/       
                                                                                
                                                                                
                                                                                
"""

# 🔹 Telegram Banner
fig = Figlet(font='slant')  # 'slant', 'block', 'banner3-D' ইত্যাদি ফন্ট ব্যবহার করা যাবে
telegram_banner = fig.renderText("Telegram = https://t.me/zx_devil_gang")

while True:
    os.system("clear")  # স্ক্রিন ক্লিয়ার
    re(banner)
    print(f"{be}{telegram_banner}")  # বড় আকারে Telegram লিংক প্রিন্ট
    print(f"{lrd}")

    # রঙের সাথে ক্রমিক লাইন আউটপুট
    print(f"{lgn}1{lrd}  {gn}Report Channel{lrd}")
    print(f"{lgn}2{lrd}  {gn}Report Channel{lrd}")

    number = input(f"{gn}Enter Number : {cn}")
    if number == "1":
        os.system("python addnumber.py")
        input(f"{yw}Press Enter to continue...{lrd}")
    elif number == "2":
        os.system("python admin.py")
        input(f"{yw}Press Enter to continue...{lrd}")
    else:
        print(f"{lrd}Invalid option! Try again.{rd}")
        time.sleep(1)