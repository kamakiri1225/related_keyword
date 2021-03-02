# ブラウザを自動操作するためseleniumをimport
from selenium import webdriver

# seleniumでEnterキーを送信する際に使用するのでimport
from selenium.webdriver.common.keys import Keys

# seleniumでヘッドレスモードを指定するためにimport
from selenium.webdriver.chrome.options import Options
# 待ち時間を指定するためにtimeをimport
import time
import os
import json
from requests_oauthlib import OAuth1Session
from dotenv import find_dotenv, load_dotenv
# グーグルスプレッドシートを操作する為にimport
import gspread

# グーグルスプレッドシートの認証情報設定の為にimport
from google.oauth2.service_account import Credentials

# 現在のパスを指定
PWD = os.getcwd()

env_file = find_dotenv()
load_dotenv(env_file)  # .envファイルを探して読み込む

# スプレッドシートキーを取得
SPREADSHEET_KEY = os.environ.get('SPREADSHEET_KEY')

# 認証情報設定

# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
#※Pythonファイルと同じ位置にjsonファイルを置く
credentials = Credentials.from_service_account_file(
    'spreadsheet-test.json',
    scopes=scopes
)
# OAuth2の資格情報を使用してGoogleAPIにログイン
gc = gspread.authorize(credentials)

#共有設定したスプレッドシートのワークブックを開く
workbook = gc.open_by_key(SPREADSHEET_KEY)

# ワークシートを開く
worksheet = workbook.worksheet('キーワードリスト')

#セルの値を行で取得
keyword_list = worksheet.col_values(2)[1:]
print(keyword_list)

# クロームオプションの設定
options = webdriver.ChromeOptions()

# seleniumで自動操作するブラウザはGoogleChrome
# Optionsオブジェクトを作成
options = Options()
# ヘッドレスモードを有効にする
options.add_argument('--headless')

for i in range(len(keyword_list)):
    # keyword
    keyword = keyword_list[i]
    file_make = f'{PWD}\{keyword}' #ファイルを作成
    if not os.path.exists(file_make):
        os.mkdir(file_make)
        
    # Seleniumでダウンロードするデフォルトディレクトリ
    download_directory = file_make
    # デフォルトのダウンロードディレクトリの指定
    prefs = {"download.default_directory" : download_directory}  

    # オプションを指定してクロームドライバーの起動
    options.add_experimental_option("prefs", prefs)

    
    # ChromeのWebDriverオブジェクトを作成
    # driver = webdriver.Chrome(options=Options)
    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")


    # 関連キーワード（ラックキーワード）
    URL_related = f'https://related-keywords.com/result/suggest?q={keyword_list[i]}'
    URL_news = f'https://related-keywords.com/result/news?q={keyword_list[i]}'
    URL_googletrend = f'https://related-keywords.com/result/trend?q={keyword_list[i]}'
    URL_cooccurrence = f'https://related-keywords.com/result/cooccurrence?q={keyword_list[i]}'
    URL_similarity = f'https://related-keywords.com/result/similarityAndAssociation?q={keyword_list[i]}'
    URL_synonym = f'https://related-keywords.com/result/synonym?q={keyword_list[i]}'

    # URLの辞書を作成
    URL_dct = {
        'URL_related' : URL_related,
        'URL_news' : URL_news,
        'URL_cooccurrence' : URL_cooccurrence,
        'URL_similarity' :URL_similarity,
        'URL_synonym' : URL_synonym,
    }

# url1 = URL_list['URL_news']

    for url in URL_dct.items():
        # 関連キーワード（ラックキーワード）
        # 2秒待機（読み込みのため）
        driver.get(url[1])
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
    print(f'{keyword_list[i]}は終了')
    
print('='*10, 'ファイルまとめ作成','='*10)
# キーワードをまとめる
import pandas as pd
import glob

for keyword in keyword_list:
    # csvファイルのリスト
    csvfules_list = glob.glob(rf"./{keyword}/*.csv", recursive=False)
    with pd.ExcelWriter(fr'./{keyword}/000_{keyword}_matome.xlsx') as writer:
        for i, csv_file in enumerate(csvfules_list):
            df = pd.read_csv(fr'./{csv_file}', encoding='UTF16', sep='\t')
            df.to_excel(writer, sheet_name=f'{keyword}{i}')
print('='*10, '終了','='*10)