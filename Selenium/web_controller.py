import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from file_input import FileInput


class WebController:
    def __init__(self, config) -> None:
        self._driver = webdriver.Chrome(
            'Selenium\Driver\chromedriver.exe')
        self._config = config
        return

# region 開啟 driver 和登入
    def Login(self):

        self._driver.get(self._config.TestUrl)
        accinput = self._driver.find_element(
            By.XPATH, '/html/body/div[1]/div[1]/div[3]/form/div[2]/span[1]/input')
        accinput.send_keys(self._config.LoginAccount)
        pwdinput = self._driver.find_element(
            By.XPATH, '/html/body/div[1]/div[1]/div[3]/form/div[2]/span[2]/input')
        pwdinput.send_keys(self._config.LoginPwd)
        loginbutton = self._driver.find_element(
            By.XPATH, '/html/body/div[1]/div[1]/div[3]/form/div[2]/button')
        loginbutton.click()
# endregion

    def GetUrl(self, logPathName: str) -> None:
        #driver = self.__login()
        urlfile = open(logPathName, 'w')
        time.sleep(10)
        b = ''
        try:
            a = self._driver.find_elements(By.XPATH, '//a[@href]')
            for i in a:
                b = i.get_attribute('href')
                urlfile.write(b+'\n')
        except:
            pass
        urlfile.close()

    def CheckUrlAuth(self, logPathName: str) -> None:
        BlockUrlList = FileInput.UrlList()
        logFile = open(logPathName, 'w')
        time.sleep(10)
        for BlockUrl in BlockUrlList:
            self._driver.get(self._config.TestUrl+BlockUrl)
            if self._config.TestUrl+BlockUrl == self._driver.current_url:
                logFile.write('False： '+self._config.TestUrl+BlockUrl + '\n')
        logFile.write(time.strftime("%Y-%m-%d %H:%M",
                      time.localtime())+'  Test Finished')
        logFile.close()
