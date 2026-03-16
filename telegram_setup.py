#!/usr/bin/env python3
"""
Telegram Weather Bot Setup & Test Tool
"""

import requests
import os

# Configuration from file (or manually set)
TELEGRAM_TOKEN = "7339165016:AAGzSn65GLOd2H50jr4mmSPeIOTt1I2_iVQ"
bot_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def test_bot_connection():
    """Test if bot is working"""
    try:
        url = f"{bot_url}/getMe"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data["result"]
                print(f"✅ Bot conectado com sucesso!")
                print(f"Bot Name: {bot_info['first_name']}")
                print(f"Username: @{bot_info['username']}")
                print(f"ID: {bot_info['id']}")
                return True
        print(f"❌ Erro: {response.text}")
        return False
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return False

def get_chat_list():
    """Get available chats for the bot"""
    try:
        url = f"{bot_url}/getUpdates"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("result"):
                print("\n📱 Chats disponíveis para o bot:")
                print("=" * 50)
                for i, update in enumerate(data["result"][-5:], 1):  # Last 5 updates
                    if "message" in update:
                        chat = update["message"]["chat"]
                        chat_id = chat["id"]
                        chat_type = chat["type"]
                        chat_title = chat.get("title", chat.get("username", chat.get("first_name", "Unknown")))
                        print(f"{i}. Chat ID: {chat_id}")
                        print(f"   Tipo: {chat_type}")
                        print(f"   Título: {chat_title}")
                        if chat_type == "private":
                            print(f"   💡 Use este ID: {chat_id}")
                        print("")
                        
                # Also show recent messages
                print("📝 Mensagens recentes:")
                for update in data["result"][-3:]:  # Last 3
                    if "message" in update:
                        msg = update["message"]
                        from_user = msg.get("from", {}).get("username", msg.get("first_name", "Unknown"))
                        text = msg.get("text", "")[:50] + "..." if len(msg.get("text", "")) > 50 else msg.get("text", "")
                        print(f"   De {from_user}: {text}")
            else:
                print("❌ Nenhuma mensagem encontrada. Envie uma mensagem para o bot primeiro.")
                print("💡 Para começar: mensagem @YourBotName")
        return True
    except Exception as e:
        print(f"❌ Erro obtendo chats: {e}")
        return False

def test_message(chat_id):
    """Send test message to specific chat"""
    try:
        message = "🤖 *Teste do Bot de Meteorologia*\n\nEste é um teste do bot! O bot está a funcionar corretamente.\n\nReceberás relatórios meteorológicos diários às 20:00.\n\n🌤️ Boa pesca, André!"
        
        url = f"{bot_url}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=data, timeout=10)
        if response.status_code == 200:
            print(f"✅ Mensagem de teste enviada para chat {chat_id}!")
            return True
        else:
            print(f"❌ Erro enviando mensagem: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def main():
    print("🔧 Setup do Bot Telegram - Weather Forecast")
    print("=" * 50)
    
    if not test_bot_connection():
        return
    
    print()
    get_chat_list()
    
    print("\n📋 Como configurar o bot:")
    print("1. Encontre o Chat ID na lista acima")
    print("2. Para mensagem privada: use o ID direto (ex: 123456789)")
    print("3. Para grupos: use o ID negativo (ex: -123456789)")
    print("4. Para canais: use @nomecanal ou ID")
    
    # Try to send a test message if we found any chats
    try:
        url = f"{bot_url}/getUpdates"
        response = requests.get(url, timeout=10)
        if response.status_code == 200 and response.json().get("result"):
            chats = response.json()["result"]
            if chats:
                recent_chat = chats[-1]["message"]["chat"]["id"]
                print(f"\n📱 Teste uma mensagem para o chat {recent_chat}? (s/n): ", end="")
                choice = input().lower()
                if choice == 's':
                    test_message(recent_chat)
    except:
        pass
    
    print(f"\n🔧 Para configurar o bot permanentemente:")
    print(f"Edite o arquivo weather_forecast.py e adicione:")
    print(f"   CHAT_ID = {recent_chat if 'recent_chat' in locals() else 'SEU_CHAT_ID'}")
    print(f"   chat_id = CHAT_ID  # Na função send_to_telegram")

if __name__ == "__main__":
    main()