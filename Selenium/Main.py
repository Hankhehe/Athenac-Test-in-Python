import user_config
from web_controller import WebController


config = user_config.LoginData('http://192.168.21.180:8000','1','1')
acction = WebController(config)
logPath='C:\\Users\\Public\\log.txt'
urlfile = 'C:\\Users\\Public\\url.txt'
acction.Login()
#acction.GetUrl(urlfile)
acction.CheckUrlAuth(logPath)
