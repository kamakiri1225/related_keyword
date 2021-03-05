import pandas as pd
import glob

class CsvFileAll: # キーワードをまとめる    
    def __init__(self, keyword):
        self.keyword = keyword
        print('='*10, f'{self.keyword}:ファイルまとめ作成','='*10)

    def file_all(self):
        # csvファイルのリスト
        csvfules_list = glob.glob(rf"./CSV/{self.keyword}/*.csv", recursive=False)
        with pd.ExcelWriter(rf'./CSV/{self.keyword}/000_{self.keyword}_matome.xlsx') as writer:
            for i, csv_file in enumerate(csvfules_list):
                df = pd.read_csv(rf'./{csv_file}', encoding='UTF16', sep='\t')
                df.to_excel(writer, sheet_name=f'{self.keyword}{i}')