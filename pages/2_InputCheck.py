import streamlit as st
import os
import pandas as pd

st.subheader("입력안한사람잡아내기")
checkPress = st.button ("입력 안 한 사람은?")
if checkPress:
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(queryy,(cdt,))
        rowss = cursor.fetchall()

        fdf=pd.DataFrame(rows,columns=['name','count'])
        team_member=fdf['name'].tolist()
        if len(team_member) >=1:
            #st.text(",  ".join(teamember))
            cursor.close()
            conn.close()
            st.success(",  ".join(team_member))
        else:
            cursor.close()
            conn.close()
            st.warning("모든 요원 입력 완료!")
    except Exception as e:
        st.warning(f"조회 중 오류가 발생했습니다")
        print(f"Exception: {e}")
