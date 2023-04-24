# sleep-management
は、毎日の睡眠時間を記録し、過去1か月間の睡眠時間の統計情報を表示するためのアプリケーションです。以下は、このアプリケーションの使い方と機能についての説明です。

# 機能
毎日の睡眠時間を記録することができます。
過去1か月間の睡眠時間の統計情報を表示することができます。
データをリセットすることができます。

# 使い方
「睡眠時間の記録」のセクションで、記録したい日付、就寝時間、起床時間を入力してください。
「保存」ボタンをクリックすると、入力されたデータがSQLiteに保存されます。
「過去1か月間の睡眠時間の統計情報」のセクションで、過去1か月間の睡眠時間の統計情報が表示されます。
「データのリセット」ボタンをクリックすると、保存されたデータがすべて削除されます。この操作は取り消せないので、注意してください。
#動作環境
このアプリケーションは、Python 3.7以降と、以下のPythonライブラリが必要です。

・streamlit
・pandas
・sqlite3

# インストール方法
Python 3.7以降をインストールしてください。

# 以下のコマンドを実行して、必要なライブラリをインストールしてください。
'pip install streamlit pandas sqlite3'

# 以下のコマンドを実行して、Sleep Loggerを起動してください。
'streamlit run sleep_logger.py'


