import streamlit as st
from nuni_menu.db import select_table

st.set_page_config(page_title="Select", page_icon="📊")
st.markdown("# Select")
st.sidebar.header("Select Page")

st.subheader("조회")
select_df = select_table()
select_df
