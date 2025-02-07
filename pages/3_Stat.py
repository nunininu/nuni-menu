import streamlit as st
from nuni_menu.db import select_table
import matplotlib.pyplot as plt

st.set_page_config(page_title="Stat", page_icon="📊")
st.markdown("# Stat")
st.sidebar.header("Stat Page")

st.subheader("통계")
select_df = select_table()
gdf = select_df.groupby('ename')['menu'].count().reset_index()

# 📊 Matplotlib로 바 차트 그리기
# https://docs.streamlit.io/develop/api-reference/charts/st.pyplot
try:
    fig, ax = plt.subplots()
    gdf.plot(x="ename", y="menu", kind="bar", ax=ax)
    st.pyplot(fig)
except Exception as e:
    st.warning(f"차트를 그리기에 충분한 데이터가 없습니다")
    print(f"Exception:{e}")
