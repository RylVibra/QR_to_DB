import streamlit as st
import pandas as pd
from streamlit_qrcode_scanner import qrcode_scanner
from streamlit_gsheets import GSheetsConnection

st.title("🎈 My QR app")

def add_qr_code(code):
    df.loc[df["unit"] == selected_row, "battery"] = code
    conn.update(data=df)
    st.session_state.code = ""

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=0,usecols=[0, 1])
all_units = df["unit"].unique().tolist()
selected_row = st.sidebar.selectbox("Select a Unit", all_units)

st.dataframe(
    df.loc[df["unit"] == selected_row], 
    use_container_width=True, 
    hide_index=True
    )


if 'code' not in st.session_state:
    st.session_state.code = ""

qrcode = qrcode_scanner()
# qrcode = "test"
if qrcode:
    st.session_state.code = qrcode
st.markdown(f"{st.session_state.code}")
    
st.button("Add QR code", on_click=add_qr_code, args=(st.session_state.code,))