import os, gspread, pytz, pandas

from pytrends.request import TrendReq
from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import bigquery
from datetime import datetime

# pytrendsを初期化
pytrends = TrendReq(hl='ja-JP', tz=360)

# トレンドを取得したいキーワードを設定
keywords = os.getenv("KEYWORDS", "Google").split(",")

# Googleトレンドデータを取得
pytrends.build_payload(keywords, timeframe='now 7-d')

# 関連クエリを取得
related_queries = pytrends.related_queries()

# 以下、BigQuery へ insert
#-------------------------
client = bigquery.Client()
project_id = os.environ.get("PROJECT_ID")
dataset = os.environ.get("DATASET")
table = os.environ.get("TABLE")
table_id = '{}.{}.{}'.format(project_id, dataset, table)

now = datetime.now(pytz.timezone("Asia/Tokyo")).strftime("%Y-%m-%dT%H:%M:%S")
#now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ") # TIMESTAMP 型の場合
rows_to_insert = []

for keyword, data in related_queries.items():
    result_dict = {
        "keyword": keyword,
        "top": [],
        "rising": []
    }

    top_data = data['top'].to_dict()
    rising_data = data['rising'].to_dict()

    # Top queries (key = query or value)
    tmp_array = {}
    for key, values in top_data.items():
        for i, val in values.items():
            tmp_array.setdefault(i, {"type": "top"})
            tmp_array[i].update({key: val})

    for _, d in tmp_array.items():
        rows_to_insert.append({
            "keyword": keyword,
            "type": d["type"],
            "query": d["query"],
            "value": d["value"],
            "datetime": now
        })

    # Rising queries (key = query or value)
    tmp_array = {}
    for key, values in rising_data.items():
        for i, val in values.items():
            tmp_array.setdefault(i, {"type": "rising"})
            tmp_array[i].update({key: val})

    for _, d in tmp_array.items():
        rows_to_insert.append({
            "keyword": keyword,
            "type": d["type"],
            "query": d["query"],
            "value": d["value"],
            "datetime": now
        })

errors = client.insert_rows_json(table_id, rows_to_insert)
if errors == []:
    print("New rows have been added to BigQuery. {}".format(rows_to_insert))
else:
    print(errors)
    exit(1)


# # 以下、Sheets への書き出し example
# #-------------------------

# # Google Sheets APIの認証情報を設定
# scope = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/drive'
# ]
# client_secret_path = os.getenv("SECRET_DIR", ".")
# creds = ServiceAccountCredentials.from_json_keyfile_name(client_secret_path + '/client_secret.json', scope)
# client = gspread.authorize(creds)

# # ファイルを作成
# date_str = datetime.now().strftime("%Y%m%d%H%M%S")
# file_name = "demo_pytrends_data_" + date_str
# folder_id = os.getenv("FOLDER_ID", None)
# client.create(title=file_name, folder_id=folder_id)

# # Google Sheetsを開く
# top_sheet = client.open(file_name).add_worksheet(title="TOP", rows=0, cols=0)
# rising_sheet = client.open(file_name).add_worksheet(title="RISING", rows=0, cols=0)

# # Google Sheetsに出力
# for i, row in top_queries.iterrows():
#     top_sheet.append_row(row.tolist())
# for i, row in rising_queries.iterrows():
#     rising_sheet.append_row(row.tolist())

