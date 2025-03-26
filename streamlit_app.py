import streamlit as st
import pandas as pd
from streamlit_qrcode_scanner import qrcode_scanner
st.title("🎈 My QR app")


qrcode = qrcode_scanner()
st.markdown(f"# {qrcode}")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['QR codes'])


def add_qr_code(code):
    st.session_state.df.loc[len(st.session_state.df)] = [code]
    st.session_state.last_qr = code

def delete_last():
    if "last_qr" in st.session_state:
        # Remove all rows where "QR codes" match the last QR code
        st.session_state.df = st.session_state.df[st.session_state.df["QR codes"] != st.session_state.last_qr]
        del st.session_state.last_qr  # Clean up after deletion

def delete_all():
    st.session_state.df = pd.DataFrame(columns=["QR codes"])
    st.session_state.pop("last_qr", None)  # Clear the last QR if it exists





left, middle, right = st.columns(3, gap='small', border=True)

with left:
    if st.button("Add QR code"):
        add_qr_code(qrcode)
        st.success(f"Added: {qrcode}")

with middle:
    if st.button("Delete last"):
        delete_last()

with right:
    if st.button("Delete all"):
        delete_all()





st.dataframe(st.session_state.df, use_container_width=True)
