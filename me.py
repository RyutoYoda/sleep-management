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

show_sleep_info = st.checkbox('自身の必要睡眠量を知る方法について')
if show_sleep_info:
    st.write('ステップ1')
    st.write('4日間連続で朝自然に起床するまで眠ります。')
    st.write('ステップ2')
    st.write('4日目に計測した睡眠時間が必要睡眠量となります。')
    st.write('※個人差はありますが6～8時間が適切な睡眠時間とされています。')
    

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
           CASE WHEN strftime('%s', wake_time) < strftime('%s', sleep_time)
                THEN strftime('%s', wake_time, '+1 day') - strftime('%s', sleep_time)
                ELSE strftime('%s', wake_time) - strftime('%s', sleep_time)
           END AS sleep_duration
    FROM sleep_data
    WHERE date BETWEEN '{start_date}' AND '{end_date}'
''', conn)


# 統計情報を表示する
if not df.empty:
    st.header('過去1か月間の睡眠時間の統計情報')
    
    # sleep_durationを時間に変換（小数）
    df['hours'] = df['sleep_duration'] / 3600
    
    # hours列を小数点第1位まで表示
    df['hours'] = df['hours'].round(1)
    
    st.write(df[['date', 'sleep_time', 'wake_time', 'hours']])
    
    avg_hours = df['hours'].mean()
    
    st.write(f'平均睡眠時間: {avg_hours:.1f} 時間')
    
    total_minutes = df['sleep_duration'].sum() // 60
    st.write(f'合計睡眠時間: {total_minutes}分')
    
    if avg_hours < 6:
        st.warning('平均睡眠時間が短いです。改善のためには睡眠時間を延ばすように心がけましょう。')
    elif avg_hours > 8:
        st.warning('平均睡眠時間が長すぎます。改善のためには早寝早起きを心がけましょう。')
    else:
        st.success('適切な睡眠時間です。')


        
    # 睡眠時間の推移を折れ線グラフで表示する
    df['date'] = pd.to_datetime(df['date']) # 日付をdatetime型に変換
    df = df.set_index('date') # 日付をインデックスに設定
    st.line_chart(df['sleep_duration'] / 3600) #
