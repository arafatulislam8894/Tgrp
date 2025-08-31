import os
import json
import asyncio
import random
from telethon import TelegramClient
from telethon.tl.functions.messages import ReportRequest
from telethon.tl.types import (
    InputReportReasonSpam, 
    InputReportReasonViolence,
    InputReportReasonChildAbuse,
    InputReportReasonPornography,
    InputReportReasonCopyright,
    InputReportReasonFake,
    InputReportReasonIllegalDrugs,
    InputReportReasonPersonalDetails,
    InputReportReasonOther
)

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

# প্রি-ডিফাইন্ড রিপোর্ট মেসেজ
REPORT_MESSAGES = {
    "child_abuse": [
        "This content exploits minors and violates child protection laws",
        "Child exploitation material that must be removed immediately",
        "Contains inappropriate content involving minors"
    ],
    "violence": [
        "Promotes extreme violence and harmful behavior",
        "Graphic violent content that violates community guidelines",
        "Contains threats and incitement to violence"
    ],
    "illegal_goods": [
        "Offering prohibited and illegal goods for sale",
        "Distribution of banned substances and illegal products",
        "Illegal trading activity violating platform rules"
    ],
    "adult_content": [
        "Non-consensual adult content and explicit material",
        "Sharing inappropriate adult content without consent",
        "Violates adult content policies and community standards"
    ],
    "personal_data": [
        "Sharing private personal information without authorization",
        "Doxing and unauthorized disclosure of personal data",
        "Privacy violation through personal information exposure"
    ],
    "terrorism": [
        "Promoting terrorist activities and extremist ideology",
        "Content supporting terrorism and violent extremism",
        "Terrorist propaganda that must be removed immediately"
    ],
    "spam": [
        "Mass spamming and fraudulent activity detected",
        "Engaging in coordinated spam and scam operations",
        "Automated spam behavior violating platform rules"
    ],
    "copyright": [
        "Unauthorized use of copyrighted material",
        "Copyright infringement and intellectual property violation",
        "Distributing pirated content without permission"
    ],
    "fake": [
        "Impersonation and fake identity representation",
        "False representation and deceptive identity claims",
        "Fake account engaging in malicious activities"
    ],
    "drugs": [
        "Illegal drug promotion and substance abuse advocacy",
        "Distribution of prohibited pharmaceutical substances",
        "Promoting illegal drug trade and substance abuse"
    ],
    "other": [
        "This content violates platform community guidelines",
        "Inappropriate material requiring immediate moderation",
        "Content that creates harmful environment for users"
    ]
}

def load_numbers():
    if os.path.exists(NUMBERS_FILE):
        with open(NUMBERS_FILE, 'r') as f:
            return json.load(f)
    return []

def print_banner():
    banner = f"""
{CYAN}╔═════════════════════════════════════════════╗
║                                             ║
║   Telegram Mass Reporter 🚨 v3.0           ║
║   {RED}Fixed Reporting System                 {CYAN}║
║                                             ║
╚═════════════════════════════════════════════╝
{RESET}
"""
    print(banner)

async def login_with_number(phone_number, password=None):
    try:
        client = TelegramClient(f'session_{phone_number}', API_ID, API_HASH)
        await client.connect()
        
        if not await client.is_user_authorized():
            if password:
                try:
                    await client.sign_in(password=password)
                    return client, True
                except:
                    return None, False
            return None, False
        
        return client, True
    except Exception as e:
        print(f"{RED}[✗] Login error for {phone_number}: {str(e)}{RESET}")
        return None, False

async def report_with_new_method(client, entity, message_id, reason, report_text):
    """নতুন Telethon ভার্সনের জন্য রিপোর্ট মেথড"""
    try:
        # সরাসরি client.report() মেথড ব্যবহার
        result = await client.report(
            entity=entity,
            message_ids=[message_id],
            reason=reason
        )
        return True
    except Exception as e:
        print(f"{RED}[✗] New report method failed: {str(e)}{RESET}")
        return False

async def report_with_old_method(client, entity, message_id, reason, report_text):
    """পুরানো Telethon ভার্সনের জন্য রিপোর্ট মেথড"""
    try:
        result = await client(ReportRequest(
            peer=entity,
            id=[message_id],
            reason=reason,
            message=report_text
        ))
        return True
    except Exception as e:
        print(f"{RED}[✗] Old report method failed: {str(e)}{RESET}")
        return False

async def report_message(client, entity, message_id, reason, report_text):
    """সব ধরনের Telethon ভার্সন সাপোর্ট করে"""
    # প্রথমে নতুন মেথড ট্রাই করুন
    success = await report_with_new_method(client, entity, message_id, reason, report_text)
    if success:
        return True
    
    # যদি নতুন মেথড ফেইল হয়, পুরানো মেথড ট্রাই করুন
    return await report_with_old_method(client, entity, message_id, reason, report_text)

async def main():
    print_banner()
    
    numbers = load_numbers()
    if not numbers:
        print(f"{RED}[✗] No numbers found in database. Run addnumber.py first.{RESET}")
        return
    
    print(f"{GREEN}[+] Found {len(numbers)} numbers in database{RESET}")
    
    # Get target username
    username = input(f"\n{BLUE}[?] Enter Telegram username/channel to report: {RESET}").strip()
    if not username.startswith('@'):
        username = '@' + username
    
    # Get message IDs
    msg_ids_input = input(f"{BLUE}[?] Enter message IDs to report (comma separated): {RESET}").strip()
    message_ids = [int(msg_id.strip()) for msg_id in msg_ids_input.split(',')]
    
    # Official Telegram report options
    print(f"\n{YELLOW}╔═════════════════════════════════════════════╗")
    print(f"║          Official Report Reasons           ║")
    print(f"╠═════════════════════════════════════════════╣{RESET}")
    print(f"{YELLOW}║ 1.  Child abuse                          ║")
    print(f"║ 2.  Violence                             ║")
    print(f"║ 3.  Illegal goods                        ║")
    print(f"║ 4.  Illegal adult content                ║")
    print(f"║ 5.  Personal data                        ║")
    print(f"║ 6.  Terrorism                            ║")
    print(f"║ 7.  Scam or spam                         ║")
    print(f"║ 8.  Copyright                            ║")
    print(f"║ 9.  Fake account                         ║")
    print(f"║ 10. Illegal drugs                        ║")
    print(f"║ 11. Other                                ║")
    print(f"╚═════════════════════════════════════════════╝{RESET}")
    
    reason_choice = input(f"\n{BLUE}[?] Enter choice (1-11): {RESET}").strip()
    
    # Define reason and message based on choice
    reason_map = {
        "1": (InputReportReasonChildAbuse(), "child_abuse"),
        "2": (InputReportReasonViolence(), "violence"),
        "3": (InputReportReasonOther(), "illegal_goods"),
        "4": (InputReportReasonPornography(), "adult_content"),
        "5": (InputReportReasonPersonalDetails(), "personal_data"),
        "6": (InputReportReasonOther(), "terrorism"),
        "7": (InputReportReasonSpam(), "spam"),
        "8": (InputReportReasonCopyright(), "copyright"),
        "9": (InputReportReasonFake(), "fake"),
        "10": (InputReportReasonIllegalDrugs(), "drugs"),
        "11": (InputReportReasonOther(), "other")
    }
    
    if reason_choice in reason_map:
        reason, reason_type = reason_map[reason_choice]
        report_text = random.choice(REPORT_MESSAGES[reason_type])
    else:
        print(f"{RED}[✗] Invalid choice. Using 'Other' as default.{RESET}")
        reason = InputReportReasonOther()
        report_text = random.choice(REPORT_MESSAGES["other"])
    
    print(f"\n{YELLOW}[!] Report message: {report_text}{RESET}")
    
    # Confirm before proceeding
    confirm = input(f"{RED}[!] Are you sure you want to report {username}? (y/n): {RESET}").strip().lower()
    if confirm != 'y':
        print(f"{YELLOW}[!] Report cancelled.{RESET}")
        return
    
    print(f"\n{YELLOW}[!] Starting mass report process...{RESET}")
    
    # Report from each number
    successful_reports = 0
    total_attempted = 0
    
    for i, number_data in enumerate(numbers, 1):
        phone_number = number_data['phone']
        password = number_data.get('password')
        
        print(f"\n{BLUE}[{i}/{len(numbers)}] Processing: {phone_number}{RESET}")
        
        try:
            # Login with number
            client, logged_in = await login_with_number(phone_number, password)
            
            if not logged_in or not client:
                print(f"{YELLOW}[!] Login failed for {phone_number}, skipping...{RESET}")
                continue
            
            # Get the entity
            try:
                entity = await client.get_entity(username)
                print(f"{GREEN}[✓] Successfully accessed {username}{RESET}")
            except Exception as e:
                print(f"{YELLOW}[!] Cannot access {username} with {phone_number}: {str(e)}{RESET}")
                await client.disconnect()
                continue
            
            # Report messages
            reported_count = 0
            for msg_id in message_ids:
                try:
                    success = await report_message(client, entity, msg_id, reason, report_text)
                    if success:
                        reported_count += 1
                        print(f"{GREEN}[✓] Successfully reported message {msg_id}{RESET}")
                    else:
                        print(f"{RED}[✗] Failed to report message {msg_id}{RESET}")
                    
                    # Random delay between reports
                    await asyncio.sleep(random.uniform(3, 8))
                    
                except Exception as e:
                    print(f"{RED}[✗] Error reporting message {msg_id}: {str(e)}{RESET}")
            
            successful_reports += reported_count
            total_attempted += len(message_ids)
            
            print(f"{GREEN}[+] {reported_count}/{len(message_ids)} reports successful from this number{RESET}")
            
            await client.disconnect()
            await asyncio.sleep(random.uniform(10, 20))  # Longer delay between numbers
            
        except Exception as e:
            print(f"{RED}[✗] Error with {phone_number}: {str(e)}{RESET}")
    
    print(f"\n{GREEN}[✓] Mass report process completed!{RESET}")
    print(f"{GREEN}[✓] Total successful reports: {successful_reports}/{total_attempted}{RESET}")
    print(f"{GREEN}[✓] Target: {username}{RESET}")
    print(f"{GREEN}[✓] Used {len(numbers)} accounts for reporting{RESET}")

if __name__ == "__main__":
    asyncio.run(main())