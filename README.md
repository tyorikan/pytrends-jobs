# pytrends-jobs

## Quickstart: ローカル環境で実行するまで

1. Sheets API と Drive API の有効化  
https://console.cloud.google.com/apis/library/sheets.googleapis.com  
https://console.cloud.google.com/apis/library/drive.googleapis.com

2. API 同意画面で権限追加  
https://console.cloud.google.com/apis/credentials/consent  
* 機密性の高いスコープ  
Google スプレッドシートのすべてのスプレッドシートの参照、編集、作成、削除  
* 制限付きのスコープ  
Google ドライブのすべてのファイルの表示、編集、作成、削除

3. サービスアカウントを作成し、client_secret.json をダウンロード（TODO: デフォルト認証情報取得する方法があるかも）  

4. Drive にフォルダを作成し、作成したサービスアカウントが編集できるようアクセス権追加

5. 環境変数 FOLDER_ID にフォルダ ID を指定し、実行
```
export FOLDER_ID=xxxxxxxx
python3 main.py
```
