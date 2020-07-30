# -*- coding: utf-8 -*-
import os
import telebot     # pip install pyTelegramBotApi
import xml.etree.ElementTree as XmlTree
from typing import Tuple
import requests

# Обход роскомнадзора
#from telebot import apihelper
#apihelper.proxy = { 'https': 'socks5h://77.81.226.18:1080' }     

token     = 'Тут ваш токен' # ТОКЕН
AdminList = 'Тут ваш id'    # ВАШ ID
bot       = telebot.TeleBot(token)

# Сообщение при старте (/start)
ComStart  = 'Тут должна быть помощь... ' + '   /start, ' + '/mac' 

R  = '\033[31m' # red
G  = '\033[32m' # green
C  = '\033[36m' # cyan
W  = '\033[0m'  # white
B  = '\033[30m' # black
LG = "\033[37m" # LightGray
M  = "\033[35m" # Magenta

version = 'v0.0.1'

def banner():
	os.system('clear')
	print (LG +  '''
████████████████████████████████
████░░██░░░░██░░████████████████
██░░██░░████░░██░░██████████████
░░██░░██░░░░██░░██░░████████████
░░██░░████░░██░░██░░░░██████████
██░░░░░░░░██░░░░░░░░██░░████████
██████░░██░░████░░██░░██░░██████
████░░██░░░░██████░░░░██░░██████
████░░████████████████░░████████
██████░░██░░░░░░░░░░██░░████████
████████░░░░██████░░░░██████████
██░░░░████░░░░░░░░░░████████████
██░░██░░████████████████████████
██░░░░██████░░████░░░░░░████████
██░░██░░██░░██░░████░░██████████
██░░░░██████░░██████░░██████████''' + W)
	print('\n' + G + '[>]' + W + ' Created By : ' + W + '@Oirefive')
	print(G + '[>]' + W + ' Version    : ' + W + version) 
def InfoAdminList():  
    print('\n' + G + '[>]' + M + ' AdminList  : ' + W + AdminList + '\n')



 # /start  -  помощь по командам
@bot.message_handler(commands=['start']) 
def start(message):
    bot.send_message(message.chat.id, ComStart)
 
# Отправка mac адреса на сайт
@bot.message_handler(content_types=['text'])
def mac(message):
    if message.text.lower() == '/mac': 
       mac = bot.send_message(message.chat.id, "Напишите MAC адрес без знака ':', большими буквами:")
       bot.register_next_step_handler(mac, id_for_mac) 
def id_for_mac(message):   
    if len(message.text) != 12: 
#       print(len(message.text)) # Колличество символов в сообщении (вывод в консоль) 
       bot.send_message(message.chat.id, "Ошибочка! Проверьте данные на ошибки и повторите снова ;)") 
       return
    bot.send_message(message.chat.id, "MAC: «" + message.text + "»")
    bot.send_message(message.chat.id, "Поиск..")
# Приём координат MAC адреса    

    URL = "http://mobile.maps.yandex.net/cellid_location/?clid=1866854&lac=-1&cellid=-1&operatorid=null&countrycode=null&signalstrength=-1&wifinetworks=" + message.text + ":-65&app=ymetro"
#    print(message.text) # Выбранный MAC
    try:
        def get_coordinates(content: str) -> Tuple[float, float]:
             root = XmlTree.fromstring(content)
		 
             coordinates = root[0].attrib
		 
		 
             return float(coordinates["latitude"]), float(coordinates["longitude"])
		 
		 
        def fetch(url: str) -> str:
             return requests.get(url).text
        latitude, longitude = get_coordinates(fetch(URL))
        bot.send_message(message.chat.id, f"Latitude: {latitude}\nLongitude: {longitude}") # Отправка координат в чат
        bot.send_location(message.chat.id, f"{latitude}", f"{longitude}")
#        print(f"Latitude: {latitude}\nLongitude: {longitude}")
    except:
#        print("Not found!")
	    bot.send_message(message.chat.id, "Местоположение не найдено :(")
	
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'add': 
       bot.answer_callback_query(callback_query_id=call.id, text='----------(###)---7---(###)----------')

banner(); InfoAdminList();
 
if __name__ == '__main__':
    bot.polling(none_stop=True)
	
	
