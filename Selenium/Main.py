import time
from web_controller import WebController
from file_operator import ImportDataByFile

acction = WebController('http://192.168.28.189:8000')
acction.LogintoAtheNAC('admin','admin')
time.sleep(10)
urls = acction.GetHrefbyCorrentPage()

for i in urls :
    acction.GotoUrl(i)
