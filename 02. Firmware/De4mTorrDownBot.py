#!A:/!Soft/00_DEV_LANG/Python34/pythonw.exe
#-*- coding: utf-8 -*-

#
#
#
#
#
#

import config
import telebot
#import torrent
import request
import json
import sys
import re
import time

import Rutracker

# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text':
            # print the sent message to the console
            print str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + m.text

bot = telebot.TeleBot(config.token)
bot.set_update_listener(listener)  # register listener
RC = Rutracker.RutrackerCR(config.rutracker_login, config.rutracker_pass)




knownUsers = [123,196328772]
torrents_urls = []
context =   [
                'All',
                'Periodic'
            ]

context_item = 0


# Проверим полномочия пользователея
def check_user(message):
    cid = message.from_user.id
    if cid not in knownUsers:
        bot.send_message(message.chat.id, "Доступ запрещен")
        return 0
    else:
        return 0

# Обработчик команд '/start'
@bot.message_handler(commands=['start'])
def handle_start(message):
    if check_user(message) == 0:
        bot.send_message(message.chat.id, 'Домашняя система скачивания контента')
        handle_help(message)

# Обработчик команд '/help'
@bot.message_handler(commands=['help'])
def handle_help(message):
    if check_user(message) == 0:
        bot.send_message(message.chat.id,   '/help - помощь \n'
                                            '-----------  управление областями -----------\n'
                                            '/all - переключится на общий раздел \n'
                                            '/periodic - переключится на разле с периодикой. \n'
                                            '/get_context - показать область \n'
                                            '-----------  управление ссылками  -----------\n'
                                            '/move - перенести все файлы в другую область \n'
                                            '/print - показать все строки для скачивания\n'
                                            '/clear_url - удаление всех ссылок\n'
                                            '-----------  управление закачками -----------\n'
                                            '/start_download - начать скачивание \n'
                                            '/start_download_file - скачать torrent файлы\n'
                                            '---------------------------------------------\n'
                                            '/get_user_id - получить ID пользователя')

# Обработчик команд '/all - установить контекст ALL'
@bot.message_handler(commands=['all'])
def handle_all(message):
    global context_item,context
    if check_user(message) == 0:
            context_item = 0
            bot.send_message(message.chat.id, 'Контекст переключен на ['+str(context[context_item])+']')

# Обработчик команд '/periodic - Установить контекст PERIODIC'
@bot.message_handler(commands=['periodic'])
def handle_periodic(message):
    global context_item,context
    if check_user(message) == 0:
            context_item = 1
            bot.send_message(message.chat.id, 'Контекст переключен на ['+str(context[context_item])+']')

# Обработчик команд '/get_context - Сообщить текущий контекст'
@bot.message_handler(commands=['get_context'])
def handle_get_context(message):
    global context_item,context
    if check_user(message) == 0:
            bot.send_message(message.chat.id, 'Вы сейчас работаете в контексте: ['+str(context[context_item])+']')

# Обработчик команд '/clear_url- печать перечня файлов для скачивания'
@bot.message_handler(commands=['clear_url'])
def handle_clear_url(message):
    global context_item,context,torrents_urls
    if check_user(message) == 0:
        bot.send_message(message.chat.id, 'Список ссылок очищен')
        torrents_urls  = []

# Обработчик команд '/print- печать перечня файлов для скачивания'
@bot.message_handler(commands=['print'])
def handle_print(message):
    global context_item,context,torrents_urls
    all_torrents_urls = ''
    item = 0
    if check_user(message) == 0:
            bot.send_message(message.chat.id, 'Список для закачки')
            for torrents_url in torrents_urls:
                #all_torrents_urls = all_torrents_urls+'\n'+torrents_url
                all_torrents_urls = '['+str(item)+'] '+torrents_url
                bot.send_message(message.chat.id, all_torrents_urls)
                item = item +1
            bot.send_message(message.chat.id, 'Текущий контекст: ['+str(context[context_item])+']\nКол-во торрентов для скачивания: '+str(len(torrents_urls)))

# Обработчик команд '/move- перенести ссылки в другой контекст
@bot.message_handler(commands=['move'])
def handle_move(message):
    global context_item,context,torrents_urls
    if check_user(message) == 0:
        context_item_old = context_item
        if context_item == 0:
            context_item =1
        else:
            context_item = 0
        bot.send_message(message.chat.id, 'Исходный контекст: ['+str(context[context_item_old])+']\nТекущий контекст: ['+str(context[context_item])+']\nПеренесено торрентов : '+str(len(torrents_urls)))


# Обработчик команд '/start_download_file - скачивает torrent файлы'
@bot.message_handler(commands=['start_download_file'])
def handle_start_download_file(message):
    global context_item,context,torrents_urls
    all_torrents_urls = ''
    item = 0
    tmp_torrents_urls=[] # Здесь храним скачанные торренты
    if check_user(message) == 0: # Проверим полномочия
            bot.send_message(message.chat.id, 'Скачивание файлов началось') # Оповестим о начале скачивания
            for torrents_url in torrents_urls: # Идем по каждой записе
                if (RC.get_torrent_file ('http://rutracker.cr/forum/dl.php?t='+re.findall(r'[\d]+', torrents_url)[0],config.download_path[context_item] )==0): # Скачаем и проверим результата
                    # файл скачали успешно
                    item = item +1 # посчитаем успешные закачки
                    tmp_torrents_urls.append(torrents_url) # Сохраним успешно скачанную ссылку что бы потов вычестить основной список
                    bot.send_message(message.chat.id, 'Скачано по ссылке:'+str(torrents_url)) # Порадуем пользоватлеф
                else:
                    # файл не скачался
                    bot.send_message(message.chat.id, 'ПРОБЛЕМА:'+torrents_url) # Сообщим пользоатделю
            bot.send_message(message.chat.id, 'Текущий контекст: ['+str(context[context_item])+']\nСкачано торрентов: '+str(item)+' из '+str(len(torrents_urls)))

            for torrents_url in tmp_torrents_urls: # Почистим основной список.  В результате останутся только проблемные ссылки
                torrents_urls.remove(torrents_url)

# Обработчик сообщений  - поиск url.
@bot.message_handler(commands=None,content_types=['text'])
def handle_message (message):
    if check_user(message) == 0:
        global torrents_urls
        item = len(torrents_urls)
        torrents_urls.extend(re.findall(r'(https?://\S+)',message.text))
        item = len(torrents_urls) - item
        bot.send_message(message.chat.id, 'Текущий контекст: ['+str(context[context_item])+']\nДобавлено позиций: '+str(item))

        #print (torrents_urls)
        #pprint (message)


def main():
    # main function

    print("\n\nBot is starting - [ОК]")
    print("\nPython version - "+sys.version)
    print (sys.executable)
    context_item = 0
    #bot.polling(none_stop=True)
    #while 1:
    #    pass


    while 1:
        try:
            bot.polling(none_stop=True )
        except Exception as e:
            print ('Error:'+ str(e))
            time.sleep (20)
        pass

if __name__ == '__main__':
    main()
