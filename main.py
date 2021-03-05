from Tools import  SpredKeywod, Chromdriver, DirMake, Scrap, CsvFileAll

def main():
    # 関連キーワード（ラッコキーワード）
    URL_related = f'https://related-keywords.com/result/suggest?q='
    URL_news = f'https://related-keywords.com/result/news?q='
    URL_googletrend = f'https://related-keywords.com/result/trend?q='
    URL_cooccurrence = f'https://related-keywords.com/result/cooccurrence?q='
    URL_similarity = f'https://related-keywords.com/result/similarityAndAssociation?q='
    URL_synonym = f'https://related-keywords.com/result/synonym?q='

    # URLの辞書を作成
    URL_dct = {
        'URL_related' : URL_related,
        'URL_news' : URL_news,
        'URL_cooccurrence' : URL_cooccurrence,
        'URL_similarity' :URL_similarity,
        'URL_synonym' : URL_synonym,
    }

    # スプレッドシートのキーワード読み取り
    keyword_list = SpredKeywod.SpredKeywod('spreadsheet-test.json','キーワードリスト','SPREADSHEET_KEY').spred_keyword_list()
    # キーワードフォルダのパスの指定
    print(keyword_list)
    keyword_list_path = DirMake.DirMake(keyword_list).make_dir()

    for i in range(len(keyword_list)):
        keyword_path = keyword_list_path[i]                                     # キーワードのフォルダのパス
        driver = Chromdriver.Chromdriver(keyword_path).openDriver(False)        # driverのオプション設定(True:Background実行)
        keyword = keyword_list[i]                                               # キーワード
        scrap = Scrap.Scrap().srape(keyword, URL_dct, driver)                   # キーワードでスクレイピング
        csvfile_all = CsvFileAll.CsvFileAll(keyword).file_all()                 # csvファイルをひとつにまとめる
        
    print('='*10, '終了','='*10)

if __name__ == '__main__':
    main()