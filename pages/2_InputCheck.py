import streamlit as st
from nuni_menu.db import select_members_without_lunch

st.subheader("입력 안 한 사람 잡아내기")
checkPress = st.button ("입력 안 한 사람은?")

if checkPress:
    try:
        df = select_members_without_lunch()
        st.dataframe(df, use_container_width=True)
    except Exception as e:
        st.warning(f"조회 중 오류가 발생했습니다")
        print(f"Exception: {e}")
