import os, gspread

from oauth2client.service_account import ServiceAccountCredentials
from google.cloud import bigquery
from datetime import datetime

client = bigquery.Client(location="asia-northeast1")
project_id = os.environ.get("PROJECT_ID")
dataset = os.environ.get("DATASET")
table = os.environ.get("TABLE")
table_id = '{}.{}.{}'.format(project_id, dataset, table)

query = """
    SELECT keyword, query, value, datetime
    FROM `{}`
    WHERE type = 'rising'
    ORDER BY datetime, value DESC
    LIMIT 25
""".format(table_id)
print(query)

query_job = client.query(query)  # Make an API request.

# print("The query data:")
# for row in query_job:
#     # Row values can be accessed by field name or index.
#     print("keyword={}, query={}, value={}, datetime={}".format(row[0], row[1], row[2], row[3]))

# 以下、Sheets への書き出し example
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
date_str = datetime.now().strftime("%Y%m%d%H%M%S")
file_name = "demo_pytrends_data_" + date_str
folder_id = os.getenv("FOLDER_ID", None)
client.create(title=file_name, folder_id=folder_id)

# Google Sheetsを開く
sample_sheet = client.open(file_name).add_worksheet(title="SAMPLE", rows=0, cols=0)

# Google Sheetsに出力
for row in query_job:
    sample_sheet.add_rows(row)
