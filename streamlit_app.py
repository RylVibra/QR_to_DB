import streamlit as st
import pandas as pd
from streamlit_qrcode_scanner import qrcode_scanner
from streamlit_gsheets import GSheetsConnection

st.title("🎈 QR to Battery DB")

def add_qr_code(code):
    if code in df["battery"].values:
        st.warning("This QR code already exists in the database.")
    else:
        df.loc[df["unit"] == selected_row, "battery"] = code
        conn.update(data=df)
        st.success("QR code added successfully.")
    
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=0,usecols=[0, 1]).astype(str)
all_units = df["unit"].unique().tolist()
selected_row = st.selectbox("Select a Unit", all_units)

# Display the selected row
st.dataframe(
    df.loc[df["unit"] == selected_row], 
    use_container_width=True, 
    hide_index=True
    )

qrcode = qrcode_scanner()
last_qr = None

# if not last_qr and qrcode!=last_qr:
    # st.toast("New code added!", icon="📷")
    # last_qr = qrcode
    
st.markdown(f"{qrcode}")
# st.write(df.dtypes)
st.button("Add QR code", on_click=add_qr_code, args=(qrcode,))