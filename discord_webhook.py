import requests

import streamlit as st


def sendMsg(url, token, msg):
    try:
        payload = {"content": msg}
        header = {"authorization": token}
        r = requests.post(url, data=payload, headers=header)
    except :
        st.toast("Connection Problem ⚠️")