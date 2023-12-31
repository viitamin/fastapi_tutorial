import streamlit as st
import requests

st.title("사용자 관리 시스템")
st.header("사용자 정보 입력")

with st.form("my_form"):
    username = st.text_input("사용자 이름")
    email = st.text_input("이메일")
    password = st.text_input("비밀번호", type = "password")
    is_active = st.checkbox("활성 등록")
    submit_button = st.form_submit_button(label = "사용자 등록")

if submit_button:
    response = requests.post("http://localhost:8000/users/",
                            json = {
                                'name': username,
                                'email': email,
                                'password': password,
                                'is_active': is_active
                            })
    
    if response.status_code == 200:
        st.success("등록완료: {}".format(response.json()["name"]))
    else:
        st.error("에러: {}".format(response.text))
        