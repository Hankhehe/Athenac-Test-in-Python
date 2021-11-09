import Userconfig
from WebController import WebController


config = Userconfig.LoginData('http://192.168.21.180:8000','1','1')
acction = WebController(config)
logPath='C:\\Users\\Public\\log.txt'
urlfile = 'C:\\Users\\Public\\url.txt'
acction.Login()
#acction.GetUrl(urlfile)
acction.CheckUrlAuth(logPath)
