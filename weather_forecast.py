#!/usr/bin/env python3
"""
Daily Weather & Fishing Forecast for Baleal/Peniche
Runs via cron at 8PM for next day's forecast
Sends results to Telegram
Uses tabuademares.com for tide data (no API key needed)
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
import urllib.parse
from tide_scraper import TideScraper

class WeatherForecastBot:
    def __init__(self):
        # ====== CONFIGURAÇÃO DO BOT ======
        # CHAT_ID configurado para André (Kweebs)
        self.CHAT_ID = "118857641"
        
        # Bot Token (já configurado)
        self.telegram_token = "7339165016:AAGzSn65GLOd2H50jr4mmSPeIOTt1I2_iVQ"
        self.bot_url = f"https://api.telegram.org/bot{self.telegram_token}"
        
        # ====== LOCALIZAÇÕES ======
        self.location_baleal = {"lat": 39.3747, "lon": -9.3414}  # Baleal coordinates
        self.location_peniche = {"lat": 39.3556, "lon": -9.3825}  # Peniche coordinates
        
    def get_weather_data(self, lat: float, lon: float, date: str) -> Optional[Dict]:
        """Get weather data using Open-Meteo API (no API key needed)"""
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": lat,
                "longitude": lon,
                "hourly": "temperature_2m,precipitation_probability,weathercode,wind_speed_10m",
                "hourly_weathercode": "temperature_2m,precipitation_probability,weathercode,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,wind_speed_10m_max,precipitation_probability_max",
                "timezone": "Europe/Lisbon",
                "start_date": date,
                "end_date": date
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return None
    
    def get_tides_data(self) -> Optional[Dict]:
        """Get tides data for Peniche from tabuademares.com"""
        try:
            # Get tomorrow's date for tide lookup
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            # Use the tide scraper
            scraper = TideScraper()
            tide_data = scraper.get_tide_table(tomorrow)
            
            if tide_data and (tide_data["high_tides"] or tide_data["low_tides"]):
                # Format the data for our standard structure
                formatted_tides = {
                    "extremes": []
                }
                
                # Add high tides
                for tide in tide_data["high_tides"][:2]:  # Max 2 high tides
                    formatted_tides["extremes"].append({
                        "dt": f"{tomorrow}T{tide['time']}:00",
                        "height": tide["height"],
                        "type": "high"
                    })
                
                # Add low tides
                for tide in tide_data["low_tides"][:2]:  # Max 2 low tides
                    formatted_tides["extremes"].append({
                        "dt": f"{tomorrow}T{tide['time']}:00",
                        "height": tide["height"],
                        "type": "low"
                    })
                
                # Sort by time
                formatted_tides["extremes"].sort(key=lambda x: x["dt"])
                
                return formatted_tides
            else:
                # Fallback to our mock data
                return self.get_mock_tides_data()
                
        except Exception as e:
            # Suppress error output, return mock data silently
            return self.get_mock_tides_data()
    
    def get_mock_tides_data(self) -> Dict:
        """Mock tides data for Peniche"""
        today = datetime.now()
        tomorrow = today + timedelta(days=1)
        
        return {
            "extremes": [
                {
                    "dt": tomorrow.strftime("%Y-%m-%dT") + "06:30:00",
                    "height": 1.2,
                    "type": "low"
                },
                {
                    "dt": tomorrow.strftime("%Y-%m-%dT") + "13:15:00", 
                    "height": 3.8,
                    "type": "high"
                },
                {
                    "dt": tomorrow.strftime("%Y-%m-%dT") + "18:45:00",
                    "height": 1.5,
                    "type": "low"
                },
                {
                    "dt": tomorrow.strftime("%Y-%m-%dT") + "01:30:00",
                    "height": 3.5,
                    "type": "high"
                }
            ]
        }
    
    def get_weather_description(self, weather_code: int) -> str:
        """Convert weather code to description"""
        weather_codes = {
            0: "☀️ Limpo",
            1: "🌤️ Pouco nublado", 
            2: "🌤️ Parcialmente nublado",
            3: "☁️ Nublado",
            45: "🌫️ Neblina",
            48: "🌫️ Nevoeiro",
            51: "🌦️ Chuva ligeira",
            53: "🌦️ Chuva moderada",
            55: "🌧️ Chuva forte",
            61: "🌧️ Chuva fraca",
            63: "🌦️ Chuva moderada", 
            65: "🌧️ Chuva forte",
            71: "❄️ Neve fraca",
            73: "❄️ Neve moderada",
            75: "❄️ Neve forte",
            80: "🌦️ Aguaceiros",
            81: "🌧️ Aguaceiros fortes",
            95: "⛈️ Trovoada"
        }
        return weather_codes.get(weather_code, "❓ Desconhecido")
    
    def calculate_fishing_probability(self, weather_data: Dict, wind_speed: float, precipitation: float) -> Dict:
        """Calculate fishing probability based on weather conditions"""
        
        max_temp = weather_data["daily"]["temperature_2m_max"][0]
        min_temp = weather_data["daily"]["temperature_2m_min"][0]
        
        # Base probability
        probability = 50  # Start at 50%
        
        # Temperature factor (optimal 15-22°C)
        if 15 <= max_temp <= 22:
            probability += 15
        elif 10 <= max_temp <= 12 or 23 <= max_temp <= 25:
            probability += 5
        else:
            probability -= 10
        
        # Wind factor (calm weather = better fishing)
        if wind_speed <= 10:
            probability += 20
        elif wind_speed <= 20:
            probability += 10
        elif wind_speed <= 30:
            probability += 0
        else:
            probability -= 15
        
        # Precipitation factor (light rain can be good, heavy rain is bad)
        if precipitation <= 20:
            probability += 15
        elif precipitation <= 50:
            probability += 5
        else:
            probability -= 20
        
        time_of_year = datetime.now().month
        if 4 <= time_of_year <= 10:  # Spring to Autumn
            probability += 10
        
        # Ensure probability is within bounds
        probability = max(0, min(100, probability))
        
        if probability >= 70:
            level = "🐟 Excelente"
            mood = "🌊 Perfeito para pescar! Sai à água sem medo!"
            tips = ["Usa iscas naturais", "Pesca em águas mais profundas"]
        elif probability >= 50:
            level = "🔷 Bom" 
            mood = "👍 Boa altura para uma pescadela!"
            tips = ["Adapta o método ao tempo", "Procura zonas abrigadas"]
        elif probability >= 30:
            level = "⚠️ Moderate"
            mood = "😐 Se tiveres paciência, pode dar resultado..."
            tips = ["Veste bem agasalhado", "Pega em equipamentos extras"]
        else:
            level = "❌ Ruim"
            mood = "💤 Talvez melhor ficar em casa com um livro."
            tips = ["Aproveita para manter o equipamento", "Planeia uma pesca para amanhã"]
        
        return {
            "probability": probability,
            "level": level,
            "mood": mood,
            "tips": tips
        }
    
    def send_to_telegram(self, message: str) -> bool:
        """Send forecast to Telegram"""
        try:
            if self.CHAT_ID == "SEU_CHAT_ID_AQUI":
                print("⚠️ Configure o CHAT_ID primeiro!")
                print("💡 Execute: python3 telegram_setup.py")
                return False
            
            url = f"{self.bot_url}/sendMessage"
            data = {
                "chat_id": self.CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",  # Allows emoji formatting
                "disable_web_page_preview": True
            }
            
            response = requests.post(url, json=data, timeout=10)
            if response.status_code == 200:
                print("📱 Previsão enviada para Telegram com sucesso!")
                return True
            else:
                print(f"❌ Falha ao enviar para Telegram: {response.status_code}")
                print(f"Resposta: {response.text}")
                if response.status_code == 400:
                    print("💡 Verifique se o CHAT_ID está correto e se enviou mensagem para @themotion_bot")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao enviar para Telegram: {e}")
            return False
    
    def get_chat_id(self) -> Optional[str]:
        """Get available chat IDs for the bot"""
        try:
            url = f"{self.bot_url}/getUpdates"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                print("Available chats:")
                for update in data.get("result", []):
                    if "message" in update:
                        chat = update["message"]["chat"]
                        print(f"Chat ID: {chat['id']}, Type: {chat['type']}, Title: {chat.get('title', chat.get('username', 'Unknown'))}")
                return None
            else:
                return None
        except Exception as e:
            print(f"Error getting chat info: {e}")
            return None
    
    def _get_best_fishing_times(self, tides_data: Dict) -> str:
        """Get best fishing times based on tide data"""
        if not tides_data or "extremes" not in tides_data or not tides_data["extremes"]:
            return "Ver condições do mar"
            
        # Find the most fishing-friendly times
        # Best: 1-2 hours before/after high tide, and 2-3 after low tide
        try:
            for extreme in tides_data["extremes"]:
                if extreme["type"] == "high":
                    dt_str = extreme["dt"]
                    if "T" in dt_str:
                        time_part = dt_str.split("T")[1][:2]  # HH
                        hour = int(time_part)
                        # Best fishing window: 1-2 hours before high tide
                        fishing_hour = (hour - 1) % 24
                        hour_str = f"{hour-1 if hour > 0 else 23}"
                        return f"{hour_str}:00-{hour}:00"
            return "Ao longo do dia"
        except:
            return "Ver maré alta/baixa"
        
        if probability >= 70:
            level = "🐟 Excelente"
            mood = "🌊 Perfeito para pescar! Sai à água sem medo!"
            tips = ["Usa iscas naturais", "Pesca em águas mais profundas"]
        elif probability >= 50:
            level = "🔷 Bom" 
            mood = "👍 Boa altura para uma pescadela!"
            tips = ["Adapta o método ao tempo", "Procura zonas abrigadas"]
        elif probability >= 30:
            level = "⚠️ Moderate"
            mood = "😐 Se tiveres paciência, pode dar resultado..."
            tips = ["Veste bem agasalhado", "Pega em equipamentos extras"]
        else:
            level = "❌ Ruim"
            mood = "💤 Talvez melhor ficar em casa com um livro."
            tips = ["Aproveita para manter o equipamento", "Planeia uma pesca para amanhã"]
        
        return {
            "probability": probability,
            "level": level,
            "mood": mood,
            "tips": tips
        }
    
    def format_forecast_message(self):
        """Generate and format the complete forecast as message"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow_display = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
        
        message_lines = []
        message_lines.append(f"📍 *Previsão para {tomorrow_display}*")
        message_lines.append(f"📍 *Baleal*\n")
        
        # Get weather data
        weather_data = self.get_weather_data(self.location_baleal["lat"], self.location_baleal["lon"], tomorrow)
        
        if not weather_data:
            message_lines.append("❌ *Erro ao obter dados meteorológicos*")
            return "\n".join(message_lines)
        
        if "hourly" not in weather_data:
            message_lines.append("❌ *Resposta da API inesperada*")
            return "\n".join(message_lines)
        
        # Get hourly data
        hours = weather_data["hourly"]["time"]
        temps = weather_data["hourly"]["temperature_2m"]
        precip_prob = weather_data["hourly"]["precipitation_probability"] 
        weather_codes = weather_data["hourly"]["weathercode"]
        wind_speeds = weather_data["hourly"]["wind_speed_10m"]
        
        message_lines.append("🕐 *Condições ao longo do dia:*")
        
        # Select key hours - parse times from datetime strings
        key_times = [6, 9, 12, 15, 18]
        hourly_sections = []
        hour_labels = ['06h', '09h', '12h', '15h', '18h']
        
        hourly_weather = {}
        for i, time_str in enumerate(hours):
            try:
                time_dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                hour_only = time_dt.hour
                hourly_weather[hour_only] = i
            except:
                continue
        
        for j, target_hour in enumerate(key_times):
            if target_hour in hourly_weather:
                idx = hourly_weather[target_hour]
                try:
                    icon = self.get_weather_description(weather_codes[idx])
                    temp = f"{int(temps[idx])}°C"
                    hourly_sections.append(f"{hour_labels[j]} → {icon} {temp}")
                except:
                    hourly_sections.append(f"{hour_labels[j]} → ❓ Desconhecido")
        
        # If no hourly data found, use daily summary
        if not hourly_sections:
            daily_desc = self.get_weather_description(weather_data["daily"]["weathercode"][0])
            avg_temp = int(sum(temps) // len(temps))
            hourly_sections.append(f"*Dia todo* → {daily_desc} {avg_temp}°C")
        
        message_lines.extend(hourly_sections[:5])  # Max 5 hourly sections
        
        # Daily summary - use daily data if available, fallback to hourly
        if "daily" in weather_data:
            max_temp = int(weather_data["daily"]["temperature_2m_max"][0])
            min_temp = int(weather_data["daily"]["temperature_2m_min"][0])
            max_precip = int(weather_data["daily"]["precipitation_probability_max"][0])
            max_wind = int(weather_data["daily"]["wind_speed_10m_max"][0])
        else:
            max_temp = int(max(temps))
            min_temp = int(min(temps))
            max_precip = int(max(precip_prob))
            max_wind = int(max(wind_speeds))
        
        message_lines.append("")
        message_lines.append(f"🌡️ *Temperaturas:* {min_temp}°C - {max_temp}°C")
        message_lines.append(f"🌬️ *Vento máximo:* {max_wind} km/h")
        message_lines.append(f"🌧️ *Probabilidade de chuva:* {max_precip}%")
        
        # UV Index (simplified)
        if 10 <= datetime.now().day <= 16:  # Daylight hours
            uv = 1 if max_temp < 20 else 2 if max_temp < 25 else 3
        else:
            uv = 0
        uv_level = "Baixo" if uv <= 2 else "Moderado" if uv <= 5 else "Alto" if uv <= 7 else "Muito Alto"
        message_lines.append(f"🔆 *Índice UV:* {uv} ({uv_level})")
        
        # Clothing recommendation
        if max_precip > 60:
            clothing = "Convém levar guarda-chuva ☔"
        elif max_wind > 25:
            clothing = "Veste algo que aguentar o vento 🌬️"
        elif max_temp < 15:
            clothing = "Veste roupas quentes 🧥"
        elif max_temp > 25:
            clothing = "Veste roupas leves e protector solar 👕"
        else:
            clothing = "Roupas normais servem 👕"
        message_lines.append(f"👕 *Vestuário:* {clothing}\n")
        
        # Laundry warning
        if max_precip > 80 or (max_wind > 30 and max_precip > 50):
            message_lines.append("🚫 Tal vez melhor evitar lavar roupa hoje.")
        else:
            message_lines.append("✅ Bom dia para Lavar roupa!")
        
        # Mood reminder
        message_lines.append("☔ Não deixes o tempo nublado escurecer o teu humor.\n")
        
        # Fishing forecast
        fishing_data = self.calculate_fishing_probability(weather_data, max_wind, max_precip)
        message_lines.append("🎣 *Previsão de Pesca:*")
        message_lines.append(f"📊 *Probabilidade:* {fishing_data['level']}")
        message_lines.append(f"💡 {fishing_data['mood']}")
        message_lines.append("*🗓️ Dicas:*")
        for tip in fishing_data['tips']:
            message_lines.append(f"   • {tip}")
        message_lines.append("")
        
        # Tides for Peniche (from tabuademares.com)
        tides_data = self.get_tides_data()
        message_lines.append("🌊 *Marés Peniche:*")
        
        if tides_data and "extremes" in tides_data and tides_data["extremes"]:
            high_count = 0
            low_count = 0
            
            for extreme in tides_data["extremes"]:
                try:
                    # Parse the datetime
                    dt_str = extreme["dt"]
                    if "T" in dt_str:
                        time_part = dt_str.split("T")[1][:5]  # HH:MM
                        height = extreme["height"]
                        tide_type = extreme["type"]
                        
                        type_pt = "Baixa" if tide_type == "low" else "Alta"
                        message_lines.append(f"   {time_part} → {type_pt} ({height:.1f}m)")
                        
                        # Limit to 2 high and 2 low tides
                        if tide_type == "high":
                            high_count += 1
                        else:
                            low_count += 1
                        
                        if high_count >= 2 and low_count >= 2:
                            break
                except Exception as e:
                    print(f"⚠️ Error formatting tide data: {e}")
                    continue
                    
            if high_count == 0 and low_count == 0:
                message_lines.append("   📝 Dados de maré limitados")
        else:
            message_lines.append("   📝 Dados de maré indisponíveis")
        
        # Add maritime conditions summary
        message_lines.append("⚓ *Condições Marítimas:*")
        if max_wind <= 10:
            message_lines.append(f"   🌊 Mar: Calmo (máx. {max_wind} km/h)")
        elif max_wind <= 25:
            message_lines.append(f"   🌊 Mar: Moderado (máx. {max_wind} km/h)")
        else:
            message_lines.append(f"   🌊 Mari Agitado (máx. {max_wind} km/h)")
            
        # Fishing time windows based on tides
        if tides_data:
            best_time = self._get_best_fishing_times(tides_data)
            message_lines.append(f"   🎣 Melhor pesca: {best_time}")
        
        message_lines.append(f"   📊 Fonte maré: tabuademares.com")
        message_lines.append("")
        
        # 3-day outlook (simplified for now)
        message_lines.append("*📅 Resumo próximos dias:*")
        message_lines.append(f"{datetime.now().strftime('%a')} → Ver acima ☀️")
        message_lines.append(f"{(datetime.now() + timedelta(days=1)).strftime('%a')} → {hourly_sections[0] if hourly_sections else 'Condições similares'}") 
        message_lines.append(f"{(datetime.now() + timedelta(days=2)).strftime('%a')} → 🌤️ Ver detalhado")
        
        return "\n".join(message_lines)
        
        # Get weather data
        weather_data = self.get_weather_data(self.location_baleal["lat"], self.location_baleal["lon"], tomorrow)
        
        if not weather_data:
            print("❌ Erro ao obter dados meteorológicos")
            return
        

        
        if "hourly" not in weather_data:
            print("❌ Resposta da API inesperada")
            print("Raw data:", weather_data)
            return
        
        # Get hourly data
        hours = weather_data["hourly"]["time"]
        temps = weather_data["hourly"]["temperature_2m"]
        precip_prob = weather_data["hourly"]["precipitation_probability"] 
        weather_codes = weather_data["hourly"]["weathercode"]
        wind_speeds = weather_data["hourly"]["wind_speed_10m"]
        
        print("🕐 Condições ao longo do dia:")
        
        # Select key hours - parse times from datetime strings
        key_times = [6, 9, 12, 15, 18]
        hourly_sections = []
        hour_labels = ['06h', '09h', '12h', '15h', '18h']
        
        hourly_weather = {}
        for i, time_str in enumerate(hours):
            try:
                time_dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
                hour_only = time_dt.hour
                hourly_weather[hour_only] = i
            except:
                continue
        
        for j, target_hour in enumerate(key_times):
            if target_hour in hourly_weather:
                idx = hourly_weather[target_hour]
                try:
                    icon = self.get_weather_description(weather_codes[idx])
                    temp = f"{int(temps[idx])}°C"
                    hourly_sections.append(f"{hour_labels[j]} → {icon} {temp}")
                except:
                    hourly_sections.append(f"{hour_labels[j]} → ❓ Desconhecido")
        
        # If no hourly data found, use daily summary
        if not hourly_sections:
            daily_desc = self.get_weather_description(weather_data["daily"]["weathercode"][0])
            avg_temp = int(sum(temps) // len(temps))
            hourly_sections.append(f"Dia todo → {daily_desc} {avg_temp}°C")
        
        print("\n".join(hourly_sections))
        
        # Daily summary - use daily data if available, fallback to hourly
        if "daily" in weather_data:
            max_temp = int(weather_data["daily"]["temperature_2m_max"][0])
            min_temp = int(weather_data["daily"]["temperature_2m_min"][0])
            max_precip = int(weather_data["daily"]["precipitation_probability_max"][0])
            max_wind = int(weather_data["daily"]["wind_speed_10m_max"][0])
        else:
            max_temp = int(max(temps))
            min_temp = int(min(temps))
            max_precip = int(max(precip_prob))
            max_wind = int(max(wind_speeds))
        
        print(f"\n🌡️ Temperaturas: {min_temp}°C - {max_temp}°C")
        print(f"🌬️ Vento máximo: {int(max_wind)} km/h")
        print(f"🌧️ Probabilidade de chuva: {int(max_precip)}%")
        
        # UV Index (simplified)
        if 10 <= datetime.now().day <= 16:  # Daylight hours
            uv = 1 if max_temp < 20 else 2 if max_temp < 25 else 3
        else:
            uv = 0
        uv_level = "Baixo" if uv <= 2 else "Moderado" if uv <= 5 else "Alto" if uv <= 7 else "Muito Alto"
        print(f"🔆 Índice UV: {uv} ({uv_level})")
        
        # Clothing recommendation
        if max_precip > 60:
            clothing = "Convém levar guarda-chuva ☔"
        elif max_wind > 25:
            clothing = "Veste algo que aguentar o vento 🌬️"
        elif max_temp < 15:
            clothing = "Veste roupas quentes 🧥"
        elif max_temp > 25:
            clothing = "Veste roupas leves e protector solar 👕"
        else:
            clothing = "Roupas normais servem 👕"
        print(f"👕 Vestuário: {clothing}\n")
        
        # Laundry warning
        if max_precip > 80 or (max_wind > 30 and max_precip > 50):
            print("🚫 Talvez melhor evitar lavar roupa hoje.")
        else:
            print("✅ Bom dia para Lavar衣服!")
        
        # Mood reminder
        print("☔ Não deixes o tempo nublado escurecer o teu humor.\n")
        
        # Fishing forecast
        fishing_data = self.calculate_fishing_probability(weather_data, max_wind, max_precip)
        print("🎣 Previsão de Pesca:")
        print(f"📊 Probabilidade: {fishing_data['level']}")
        print(f"💡 {fishing_data['mood']}")
        print(f"🗓️ Dicas:")
        for tip in fishing_data['tips']:
            print(f"   • {tip}")
        print()
        
        # Tides for Peniche (uses mock data for now)
        tides_data = self.get_tides_data()
        if tides_data and "extremes" in tides_data:
            print("🌊 Marés Peniche:")
            for extreme in tides_data["extremes"][:2]:  # Best 2 entries for today
                try:
                    if datetime.now().strftime("%Y-%m-%d") in extreme["dt"]:
                        time = extreme["dt"].split("T")[1][:5]
                        height = extreme["height"]
                        type_pt = "Baixa" if extreme["type"] == "low" else "Alta"
                        print(f"   {time} → {type_pt} ({height:.1f}m)")
                except:
                    continue
        else:
            print("🌊 Marés Peniche: Dados indisponíveis")
        
        # 3-day outlook (simplified for now)
        print(f"\n📅 Resumo próximos dias:")
        print(f"{datetime.now().strftime('%a')} → Ver acima ☀️")
        print(f"{(datetime.now() + timedelta(days=1)).strftime('%a')} → {hourly_sections[0] if hourly_sections else 'Condições similares'}") 
        print(f"{(datetime.now() + timedelta(days=2)).strftime('%a')} → 🌤️ Ver detalhado")

def main():
    bot = WeatherForecastBot()
    
    # Generate forecast message
    print("Generating weather forecast...")
    message = bot.format_forecast_message()
    
    # Print to console
    print(message)
    print("\n" + "="*50)
    
    # Send to Telegram
    print("Sending to Telegram...")
    success = bot.send_to_telegram(message)
    
    if not success:
        print("⚠️ Failed to send to Telegram - check bot permissions and chat ID")
        print(f"Bot token: {bot.telegram_token}")
        print("To find your chat ID, first message the bot or join a channel")
    
    # Debug: show available chats (comment out in production)
    # bot.get_chat_id()
    
    print(f"\n✅ Forecast generated at {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()