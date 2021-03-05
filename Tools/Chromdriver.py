from selenium import webdriver # ブラウザを自動操作するためseleniumをimport
from selenium.webdriver.common.keys import Keys # seleniumでEnterキーを送信する際に使用するのでimport
from selenium.webdriver.chrome.options import Options # seleniumでヘッドレスモードを指定するためにimport
import time # 待ち時間を指定するためにtimeをimport
import os
import json

class Chromdriver:
    def __init__(self, keyword_path):
        self.keyword_path = keyword_path

    def openDriver(self,isHeadless):
        # クロームオプションの設定
        options = webdriver.ChromeOptions()

        # seleniumで自動操作するブラウザはGoogleChrome
        # Optionsオブジェクトを作成
        options = Options()

        if isHeadless:
            # ヘッドレスモードを有効にする
            options.add_argument('--headless')

        # Seleniumでダウンロードするデフォルトディレクトリ
        download_directory = self.keyword_path
        # デフォルトのダウンロードディレクトリの指定
        prefs = {"download.default_directory" : download_directory}  

        # オプションを指定してクロームドライバーの起動
        options.add_experimental_option("prefs", prefs)


        # ChromeのWebDriverオブジェクトを作成
        PWD = os.getcwd()
        driver = webdriver.Chrome(options=options, executable_path=fr"{PWD}\Tools\chromedriver.exe")
        return driver