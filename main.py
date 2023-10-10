import os
import datetime
import gspread

from pytrends.request import TrendReq
from oauth2client.service_account import ServiceAccountCredentials

# pytrendsを初期化
pytrends = TrendReq(hl='ja-JP', tz=360)

# トレンドを取得したいキーワードを設定
keywords = os.getenv("KEYWORDS", "Google").split(",")

# Googleトレンドデータを取得
pytrends.build_payload(keywords, timeframe='now 7-d')

# 関連クエリを取得
related_queries = pytrends.related_queries()
top_queries = related_queries[keywords[0]]['top']
rising_queries = related_queries[keywords[0]]['rising']

# 表示
print(top_queries)
print(rising_queries)

# 以下、Sheets への書き出し
#-------------------------

# Google Sheets APIの認証情報を設定
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
client_secret_path = os.getenv("SECRET_DIR", ".")
creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_path + '/client_secret.json', scope)
client = gspread.authorize(creds)

# ファイルを作成
date_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
file_name = "demo_pytrends_data_" + date_str
folder_id = os.getenv("FOLDER_ID", None)
client.create(title=file_name, folder_id=folder_id)

# Google Sheetsを開く
top_sheet = client.open(file_name).add_worksheet(title="TOP", rows=0, cols=0)
rising_sheet = client.open(file_name).add_worksheet(title="RISING", rows=0, cols=0)

# Google Sheetsに出力
for i, row in top_queries.iterrows():
    top_sheet.append_row(row.tolist())
for i, row in rising_queries.iterrows():
    rising_sheet.append_row(row.tolist())