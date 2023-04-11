import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime, timedelta



# SQLiteに接続する
conn = sqlite3.connect('sleep_data.db')

# テーブルを作成する
conn.execute('''
CREATE TABLE IF NOT EXISTS sleep_data (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    sleep_time TEXT NOT NULL,
    wake_time TEXT NOT NULL
)
''')

# ユーザーからの入力を受け付ける
st.header('睡眠時間の記録')
date = st.date_input('日付を選択してください')
sleep_time = st.time_input('就寝時間を選択してください')
wake_time = st.time_input('起床時間を選択してください')

# 入力されたデータをSQLiteに保存する
if st.button('保存'):
    date_str = date.strftime('%Y-%m-%d')
    sleep_time_str = sleep_time.strftime('%H:%M:%S')
    wake_time_str = wake_time.strftime('%H:%M:%S')
    conn.execute(f'''
        INSERT INTO sleep_data (date, sleep_time, wake_time)
        VALUES ('{date_str}', '{sleep_time_str}', '{wake_time_str}')
    ''')
    conn.commit()

# データのリセットボタンを表示する
if st.button('データのリセット'):
    # 確認メッセージを表示する
    if st.warning('本当にデータをリセットしますか？この操作は取り消せません。'):
        # テーブルを削除して再作成する
        conn.execute('DROP TABLE IF EXISTS sleep_data')
        conn.execute('''
            CREATE TABLE sleep_data (
                id INTEGER PRIMARY KEY,
                date TEXT NOT NULL,
                sleep_time TEXT NOT NULL,
                wake_time TEXT NOT NULL
            )
        ''')
        conn.commit()
        st.success('データをリセットしました。ページをリロードしてください。')



# 一か月ごとの睡眠時間の統計情報を取得する
end_date = datetime.today().date()
start_date = end_date - timedelta(days=30)
df = pd.read_sql_query(f'''
    SELECT date, sleep_time, wake_time,
           strftime('%s', wake_time) - strftime('%s', sleep_time) AS sleep_duration
    FROM sleep_data
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
''', conn)

# 統計情報を表示する
if not df.empty:
    st.header('過去1か月間の睡眠時間の統計情報')
    st.write(df)
    avg_duration = df['sleep_duration'].mean() / 3600
    st.write(f'平均睡眠時間: {avg_duration:.1f} 時間')
    if avg_duration < 7:
        st.warning('平均睡眠時間が短いです。改善のためには睡眠時間を延ばすように心がけましょう。')
    elif avg_duration > 9:
        st.warning('平均睡眠時間が長いです。改善のためには早寝早起きを心がけましょう。')
        
    # 睡眠時間の推移を折れ線グラフで表示する
    df['date'] = pd.to_datetime(df['date']) # 日付をdatetime型に変換
    df = df.set_index('date') # 日付をインデックスに設定
    st.line_chart(df['sleep_duration'] / 3600) #
