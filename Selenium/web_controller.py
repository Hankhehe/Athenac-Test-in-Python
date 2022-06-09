from selenium import webdriver
from selenium.webdriver.common.by import By

class WebController:
    def __init__(self,url) -> None:
        self._driver = webdriver.Chrome(
            'Selenium\\Driver\\chromedriver.exe')
        self.url = url
        self.GotoUrl(self.url)

    def GotoUrl(self,url) -> None:
        self._driver.get(url)

    def LogintoAtheNAC(self,account,pwd):
        accinput = self._driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div[4]/form/div[2]/span[1]/input')
        accinput.send_keys(account)
        pwdinput = self._driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div[4]/form/div[2]/span[2]/input')
        pwdinput.send_keys(pwd)
        loginbutton = self._driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div[4]/form/div[2]/button')
        loginbutton.click()

    def GetHrefbyCorrentPage(self) -> list:
        result = []
        a = self._driver.find_elements(By.XPATH, '//a[@href]')
        for i in a:
            result.append(i.get_attribute('href'))
        return result