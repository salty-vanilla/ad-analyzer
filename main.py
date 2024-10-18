import pandas as pd
import streamlit as st
from collections import Counter
import altair as alt

COLUMN_MAP = {
    'status': 'ステータス',
    'assigned': '担当者',
    'paper_name': '論文名',
    'link': 'リンク',
    'published_date': '日付（最初の公知日）',
    'conference': '学会名',
    'task': 'タスク',
    'method_type': '手法タイプ',
    'model_type': 'モデルタイプ',
    'multi_class': 'マルチクラス',
    'language': '言語情報',
    'comparison_methods': '比較手法',
    'dataset': 'データセット',
    'other_domains': '他ドメイン',
}

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    # True/Falseのマッピングを行う
    df[COLUMN_MAP['multi_class']] = df[COLUMN_MAP['multi_class']].map({'Yes': True, 'No': False})
    df[COLUMN_MAP['language']] = df[COLUMN_MAP['language']].map({'Yes': True, 'No': False})
    
    # リストに変換しつつ、空の要素がある場合はそれを除去する処理
    for column in ['comparison_methods', 'dataset', 'other_domains', 'method_type', 'model_type', 'task']:
        df[COLUMN_MAP[column]] = df[COLUMN_MAP[column]].apply(lambda x: [i.strip() for i in str(x).split(',') if i.strip()])

    return df

def get_ranking(df: pd.DataFrame, column: str):
    items = df.explode(COLUMN_MAP[column])[COLUMN_MAP[column]].dropna()
    items = items[items != '']  # 空の文字列を除外
    counter = Counter(items)
    del counter['nan']
    ranking = pd.DataFrame(counter.items(), columns=[COLUMN_MAP[column], '出現回数']).sort_values(by='出現回数', ascending=False)
    return ranking

def get_boolean_ranking(df: pd.DataFrame, column: str):
    # True/Falseのカウントを取るための処理
    ranking = df[column].value_counts().reset_index()
    ranking.columns = [column, '出現回数']
    return ranking

def plot_altair_chart(ranking: pd.DataFrame, column: str):
    # Altairを使って降順の棒グラフを表示
    chart = alt.Chart(ranking).mark_bar().encode(
        x=alt.X(f'{column}:N', sort='-y', title=column),
        y=alt.Y('出現回数:Q', title='出現回数')
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(chart, use_container_width=True)

def main():
    st.title('論文サーベイ分析')
    
    # CSVの読み込み
    df = pd.read_csv('data/paper_db.csv')
    df = preprocess(df)
    
    # データフレームの表示と編集
    st.write("### サーベイ結果")
    st.dataframe(df)

    # マルチクラスと言語情報の集計とグラフ表示
    for boolean_column in ['multi_class', 'language']:
        with st.expander(f"{COLUMN_MAP[boolean_column]}の集計"):
            ranking = get_boolean_ranking(df, COLUMN_MAP[boolean_column])
            st.table(ranking)  # ランキングをテーブルとして表示
            plot_altair_chart(ranking, COLUMN_MAP[boolean_column])

    # 複数カラムのランキング表示とグラフ描画
    for column_key in ['comparison_methods', 'dataset', 'other_domains', 'method_type', 'model_type', 'task']:
        with st.expander(f"{COLUMN_MAP[column_key]}ランキングを表示"):
            ranking = get_ranking(df, column_key)
            st.table(ranking)  # ランキングをテーブルとして表示
            plot_altair_chart(ranking, COLUMN_MAP[column_key])

if __name__ == "__main__":
    main()
