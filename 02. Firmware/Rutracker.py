#!A:/!Soft/00_DEV_LANG/Python34/pythonw.exe
# -*- coding: utf-8 -*-

#
#
#
#
#
#
import requests
import cookielib
import re
class RutrackerCR:

    # class variables

    # header
    headers = {
     'Origin': 'http://rutracker.cr',
     'Accept-Encoding': 'gzip, deflate', #Перечень поддерживаемых способов кодирования содержимого сущности при передаче.
     'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4', # Список поддерживаемых естественных языков.
     'Upgrade-Insecure-Requests': '1',
     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', # Список названий и версий клиента и его компонентов с комментариями.
     'Content-Type': 'application/x-www-form-urlencoded', # Формат и способ представления сущности.
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', # Список допустимых форматов ресурса.
     'Cache-Control': 'max-age=0', # Основные директивы для управления кэшированием.
     'Referer': 'http://rutracker.cr/forum/', # URI ресурса, после которого клиент сделал текущий запрос.
     'Connection': 'keep-alive', # Сведения о проведении соединения.
     }

    # Data for request
    data = ''

    session = None  # Session descriptor
    cookies = None  # Cookies




    def __init__(self, tracker_username=None, tracker_password=None ):               # init procedure
        """ Hello """
        #
        #
        #
        #
        # Data for request
        self.data = 'login_username={}&login_password={}&login=%E2%F5%EE%E4'.format(tracker_username, tracker_password)
        # Creating session to save cookies
        self.session = requests.session()   # Create session
        page = self.session.post('http://rutracker.cr/forum/login.php', headers=self.headers, data=self.data) # create connection
        self.cookies = requests.utils.dict_from_cookiejar(self.session.cookies) # get cookies
        #print (self.cookies)



    def get_torrent_file(self, url, fpath):    # Metod #1
        """ Hello """
        #
        #
        #
        fname = ''
        page = requests.get(url, cookies=self.cookies,stream=True)
        if re.search(r'application/x-bittorrent;', page.headers.get('Content-Type')) != None:
            #print (page.headers)
            #print (page.headers.get('Content-Type')) # Sample OUT: application/x-bittorrent; name="[rutracker.org].t5210207.torrent"
            fname= fpath + re.findall(r'\[rutracker.org\]\.t[\d]+\.torrent', page.headers.get('Content-Type'))[0] # find [rutracker.org].t5210207.torrent
            with open(fname, 'wb') as f:
                    f.write(page.content)
                    f.close()
                    return 0
        else:
            return 1



    def get_download_url(self, url):    # Metod #1
        """
            get_download_url - find download url

            param:
                url - url web page
        """

        pass




def main():
    # main function
    print ('Start Rutracker class')
    RC=RutrackerCR('De4m','De4mTR')

    print (RC.get_torrent_file('http://rutracker.cr/forum/dl.php?t=5210207','d:\\'))
if __name__ == '__main__':
    main()
