import requests  # pip install requests
import streamlit as st
from streamlit_lottie import st_lottie
from PIL import Image


def app():
    def load_lottieurl(url: str):
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()

    lottie_h1 = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_vktpsg4v.json")
    st.markdown("# Easy trading with minimal effort")
    st_lottie(lottie_h1, key=1)

    lottie_h2 = load_lottieurl("https://assets7.lottiefiles.com/private_files/lf30_F3v2Nj.json")
    st.markdown("# Easy Access to Multiple Stocks")
    st_lottie(lottie_h2,key=2)

    lottie_h3 = load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_i2eyukor.json")
    st.markdown("# Simple to understand Indicators")
    st_lottie(lottie_h3, key=3)

    lottie_h4 = load_lottieurl("https://assets7.lottiefiles.com/packages/lf20_7vtbqi1v.json")
    st.markdown("# Start Trading , Start Earning")
    st_lottie(lottie_h4, key=4)