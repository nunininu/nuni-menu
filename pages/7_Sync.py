import streamlit as st
import pandas as pd
import requests

from nuni_menu.constraints import EP
from nuni_menu.db import insert_menu, select_table, members

st.set_page_config(
    page_title="SYNC",
    page_icon="🔁",
)

st.markdown("# 🔁 SYNC")
st.sidebar.header("모두의 점심 데이터 비교 합치기")

def get_df_from_api(api_url):
    res = requests.get(api_url)
    data = res.json()
    df = pd.DataFrame(data)
    return df


if st.button("데이터 동기화"):
    res = requests.get(EP)
    data = res.json()
    endpoints = data['endpoints']
    
    ## endpoints 중에 내것을 빼기
    for i, e in enumerate(endpoints):
        if e['name'] == "nuni":
            del endpoints[i]
            
        if e['name'] == "cho":
            del endpoints[i]
            
    for p in endpoints:
        st.success(f'{p["name"]}, {p["url"]}')
        my_df = select_table()
        api_url = p["url"]
        api_df = get_df_from_api(api_url)
        
        merge_df = pd.merge(my_df, api_df, how='right', indicator=True)
        diff_df = merge_df[merge_df['_merge'] == 'right_only'].drop('_merge', axis=1)
        
        for _, row in diff_df.iterrows():
            menu_name = row['menu_name']
            name = row['name']
            member_id = members[name]
            dt = row['dt']
            insert_menu(menu_name, member_id, dt)
        
        
    
    
    # res = requests.get("https://jacob0503.vercel.app/api/py/select_table")
    # data = res.json()
    # df_jacob = pd.DataFrame(data)
    
    # df_jacob
        
    # new_rows = []

    # for _, row_2 in df2.iterrows():
    #     is_match_row = False
    #     for _, row_1 in df1.iterrows():
    #         is_match_columns = True
    #         for c_name in df1.columns:
    #             if row_2[c_name] != row_1[c_name]:
    #                 is_match_columns = False
    #                 break
            
    #         if is_match_columns: 
    #             is_match_row = True
    
    #     if not is_match_row:
    #         new_rows.append(row_2)

    # df_new = pd.DataFrame(new_rows)
    
    # print(df_new)
    
    
    
    # API 목록 갖고 오고
    # 그 중 내것을 빼고
    # 목록을 순회하면서 나의 df랑 비교해서 없는 것 => 데이터프레임으로 만들고
    # 데이터 프레임을 순회하면서 insert한다
    st.success(f"작업완료 - 새로운 원천 00 곳에서 총 00 건을 새로 추가하였습니다.")