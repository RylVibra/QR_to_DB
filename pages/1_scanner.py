
import streamlit as st
from streamlit_qrcode_scanner import qrcode_scanner

last_qr = None

qrcode = qrcode_scanner()

if qrcode!=last_qr:
    st.toast("New code added!", icon="📷")
    last_qr = qrcode