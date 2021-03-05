from selenium import webdriver # ブラウザを自動操作するためseleniumをimport
from selenium.webdriver.common.keys import Keys # seleniumでEnterキーを送信する際に使用するのでimport
from selenium.webdriver.chrome.options import Options # seleniumでヘッドレスモードを指定するためにimport
import time # 待ち時間を指定するためにtimeをimport

class Scrap:
    def srape(self, keyword, URL_dct, driver):

        for url in URL_dct.items():
            # 関連キーワード（ラッコキーワード）
            # 2秒待機（読み込みのため）
            url_keyword = url[1]+f'{keyword}'
            driver.get(url_keyword)
            time.sleep(10)

            try:
                # csvファイルの出力
                if url[0] == 'URL_cooccurrence':
                    driver.find_elements_by_class_name('sc-1kt4t6s-8')[1].click()
                    driver.find_elements_by_class_name('sc-1rktuvo-0')[0].find_elements_by_tag_name('button')[0].click()
                else:
                    driver.find_elements_by_class_name('sc-1kt4t6s-8')[1].click()
            except Exception as e:
                print(e)

            time.sleep(3)
        # ブラウザを閉じて終了する
        driver.quit()