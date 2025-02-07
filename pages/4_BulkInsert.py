import streamlit as st
from nuni_menu.db import insert_menu
import pandas as pd

st.set_page_config(page_title="BulkInsert", page_icon="📈")
st.markdown("# BulkInsert")
st.sidebar.header("BulkInsert Page")

st.subheader("벌크 인서트")
if st.button("한방에 인서트"):
    df = pd.read_csv('note/lunch_menu.csv')
    start_idx = df.columns.get_loc('2025-01-07')
    melted_df = df.melt(id_vars=['ename'], value_vars=df.columns[start_idx:-2],
                     var_name='dt', value_name='menu')

    not_na_df = melted_df[~melted_df['menu'].isin(['-','x','<결석>'])]

    total_count = len(not_na_df)
    success_count = 0
    fail_count = 0
    fail_messages = []

    for _, row in not_na_df.iterrows():
        m_id = members[row['ename']] ## 50line에서 가져옴
        r = insert_menu(row['menu'], m_id, row['dt'])
        if r:
            success_count = success_count + 1
        else:
            fail_count = fail_count + 1

    if fail_count == 0:
        st.success(f"총 {total_count}건 벌크인서트 성공")
    else:
        st.error(f"총 {total_count}건 중 {fail_count}건 실패")
