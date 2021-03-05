import pandas as pd
import glob
import os

class DirMake:
    def __init__(self, keyword_list):
        self.keyword_list = keyword_list

    def make_dir(self):
        # 現在のパスを指定
        PWD = os.getcwd()
        CSV_DIR = rf'{PWD}\CSV'
        if not os.path.exists(CSV_DIR):
            os.mkdir(CSV_DIR)

        keyword_list_path = list(map(lambda keyword: rf'{CSV_DIR}\{keyword}', self.keyword_list)) # フォルダの絶対パスを作成
        for i in range(len(self.keyword_list)):
            # keyword
            keyword = self.keyword_list[i]
            dir_make = rf'{CSV_DIR}\{keyword}' # フォルダを作成
            if not os.path.exists(dir_make):
                os.mkdir(dir_make)
            print(f'{dir_make} フォルダ作成')
        return keyword_list_path