from requests_oauthlib import OAuth1Session
from dotenv import find_dotenv, load_dotenv
import gspread # グーグルスプレッドシートを操作する為にimport
from google.oauth2.service_account import Credentials # グーグルスプレッドシートの認証情報設定の為にimport
import os

class SpredKeywod:
    # スプレッドシートのキーワードを取得
    '''
    スプレッドシートの指定
    キーワードの取得
    '''
    def __init__(self, JSON_FILE, SPRED_SHEET_NAME, SPREADSHEET_KEY):
        self.JSON_FILE = JSON_FILE
        self.SPRED_SHEET_NAME = SPRED_SHEET_NAME
        self.SPREADSHEET_KEY = SPREADSHEET_KEY
        
    def env_file(self):
        # .envファイルを探して読み込む
        env_file = find_dotenv()
        load_dotenv(env_file)  

        # スプレッドシートキーを取得
        SPREADSHEET_KEY = os.environ.get(self.SPREADSHEET_KEY) # SPREADSHEET_KEY='SPREADSHEET_KEY'
        return SPREADSHEET_KEY
    
    def spred_auth(self):
        # 認証情報設定
        # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]

        # ダウンロードしたjsonファイル名をクレデンシャル変数に設定（秘密鍵、Pythonファイルから読み込みしやすい位置に置く）
        #※Pythonファイルと同じ位置にjsonファイルを置く
        credentials = Credentials.from_service_account_file(
            self.JSON_FILE, #spreadsheet-test.json
            scopes=scopes
        )
        # OAuth2の資格情報を使用してGoogleAPIにログイン
        gc = gspread.authorize(credentials)
        return gc
    
    def spred_keyword_list(self):
        #共有設定したスプレッドシートのワークブックを開く
        SPREADSHEET_KEY = self.env_file()
        gc = self.spred_auth()
        workbook = gc.open_by_key(SPREADSHEET_KEY)

        # ワークシートを開く
        worksheet = workbook.worksheet('キーワードリスト')

        #セルの値を行で取得
        keyword_list = worksheet.col_values(2)[1:]
        return keyword_list