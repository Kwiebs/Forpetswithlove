#!/usr/bin/env python3
"""
Quick Chat ID finder for André's weather bot
"""

import requests

TELEGRAM_TOKEN = "7339165016:AAGzSn65GLOd2H50jr4mmSPeIOTt1I2_iVQ"
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def get_my_chat_id():
    """Get chat ID for André"""
    try:
        url = f"{bot_url}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("result"):
                print("🤖 Found recent messages:")
                print("=" * 40)
                
                for update in data["result"][-3:]:  # Last 3
                    if "message" in update:
                        msg = update["message"]
                        chat = msg["chat"]
                        from_user = msg.get("from", {})
                        user_name = from_user.get("username") or from_user.get("first_name", "Unknown")
                        text = msg.get("text", "")[:50] + "..." if len(msg.get("text", "")) > 50 else msg.get("text", "")
                        
                        print(f"💬 From: {user_name} (ID: {chat['id']})")
                        print(f"📝 Message: {text}")
                        print(f"🆔 Chat ID: {chat['id']}")
                        print("-" * 40)
                        
                        if "André" in user_name.lower() or "kweebs" in user_name.lower():
                            print(f"\n🎯 YOUR CHAT ID IS: {chat['id']}")
                            return chat['id']
            else:
                print("❌ No messages found. Send a message to @themotion_bot first!")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

if __name__ == "__main__":
    print("🔍 Finding your Chat ID...")
    print("Make sure you sent a message to @themotion_bot first!")
    print()
    
    chat_id = get_my_chat_id()
    
    if chat_id:
        print(f"\n📝 Next step:")
        print(f"Edit weather_forecast.py line ~15:")
        print(f"CHAT_ID = \"{chat_id}\"")
    
    print(f"\n🔧 Or use this to update automatically:")
    print(f"sed -i 's/CHAT_ID = \"SEU_CHAT_ID_AQUI\"/CHAT_ID = \"{chat_id}\"/' weather_forecast.py")