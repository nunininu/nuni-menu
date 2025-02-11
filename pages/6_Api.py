import streamlit as st
import requests
import nuni_menu.constraints as const
import datatime

st.set_page_config(page_title="API", page_icon="🍽️")

st.markdown("# 🍽️ API")
st.sidebar.header("나이계산기")

dt = st.date_input("생일입력", min_value=datatime.date(1900,1,1))
if st.button("결과 보기"):
    headers = {
        'accept': 'appliication/json'
    }
    r = requests.get(f'{const.API_AGE}/{dt}', headers = headers)
    
    if r.status_code == 200:
        data = r.json()
        age = data['age']
        st.success(f"{dt}당신의 나이는{age} 입니다.")
    else: 
        st.error(f"문제가 발생하였습니다. 관리자 문의{r.status_code}")    

