import os
import json
from telethon import TelegramClient
from telethon.tl.functions.auth import ResendCodeRequest

# কালার কোড
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
RESET = '\033[0m'

# API credentials
API_ID = 26108693
API_HASH = "3bc54f318fb35b9d82c3f885f18e7028"

# ফাইল পাথ
NUMBERS_FILE = "numbers.json"

def load_numbers():
    if os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_numbers(numbers):
    with open(NUMBERS_FILE, 'w') as f:
        json.dump(numbers, f, indent=4)

def print_banner():
    banner = f"""
{CYAN}╔═════════════════════════════════════════════╗
║                                             ║
║   Telegram Number Adder 🔢 v1.0            ║
║   {GREEN}Add Unlimited Numbers to Database        {CYAN}║
║                                             ║
╚═════════════════════════════════════════════╝
{RESET}
"""
    print(banner)

async def verify_number(phone_number):
    try:
        client = TelegramClient(f'session_{phone_number}', API_ID, API_HASH)
        await client.connect()
        
        # Send code request
        sent_code = await client.send_code_request(phone_number)
        print(f"{GREEN}[+] Verification code sent to {phone_number}{RESET}")
        
        # Ask for code
        code = input(f"{YELLOW}[?] Enter the code: {RESET}")
        
        # Try to sign in
        try:
            await client.sign_in(phone_number, code)
            print(f"{GREEN}[+] Number verified successfully!{RESET}")
            return True, None
        except Exception as e:
            # If password is needed
            if "password" in str(e):
                password = input(f"{YELLOW}[?] Enter 2FA password: {RESET}")
                try:
                    await client.sign_in(password=password)
                    print(f"{GREEN}[+] Number verified successfully!{RESET}")
                    return True, password
                except Exception as e2:
                    print(f"{RED}[-] Error: {str(e2)}{RESET}")
                    return False, None
            else:
                print(f"{RED}[-] Error: {str(e)}{RESET}")
                return False, None
        
        await client.disconnect()
        
    except Exception as e:
        print(f"{RED}[-] Error: {str(e)}{RESET}")
        return False, None

async def add_number():
    print_banner()
    
    numbers = load_numbers()
    print(f"{YELLOW}[!] Currently stored numbers: {len(numbers)}{RESET}")
    
    while True:
        phone_number = input(f"\n{BLUE}[?] Enter phone number (with country code) or 'exit' to finish: {RESET}").strip()
        
        if phone_number.lower() == 'exit':
            break
            
        if any(num['phone'] == phone_number for num in numbers):
            print(f"{YELLOW}[!] This number is already in the database{RESET}")
            continue
            
        # Verify the number
        verified, password = await verify_number(phone_number)
        
        if verified:
            numbers.append({
                "phone": phone_number, 
                "verified": True,
                "password": password
            })
            save_numbers(numbers)
            print(f"{GREEN}[+] Number added successfully!{RESET}")
        else:
            print(f"{RED}[-] Failed to verify number{RESET}")
    
    print(f"\n{GREEN}[+] Total numbers in database: {len(numbers)}{RESET}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(add_number())