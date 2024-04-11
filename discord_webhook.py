import requests

import streamlit as st


def sendMsg(url, token, msg):
    try:
        # print(url)
        payload = {"content": msg}
        header = {"authorization": token}
        r = requests.post(url, data=payload, headers=header)
        print("Msg Sent to Discord")

    except Exception as e:
        
        print("Network Error:"+ str(e))
  
        st.toast("Connection Problem ⚠️")