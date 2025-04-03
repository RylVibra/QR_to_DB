import streamlit as st
import pandas as pd
from streamlit_qrcode_scanner import qrcode_scanner
from streamlit_gsheets import GSheetsConnection
st.title("🎈 My QR app")


# qrcode = qrcode_scanner()
qrcode = "test"
st.markdown(f"# {qrcode}")

if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=['QR codes'])


def add_qr_code(code):
    if code in st.session_state.df["QR codes"].values:
        st.warning("This QR code already exists in the list.")
        return
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

left, middle, right = st.columns(3, border=True, )

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


# st.dataframe(st.session_state.df, use_container_width=True)




# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read(
    worksheet="Sheet2",
    ttl="10m",
    usecols=[0, 1],
    nrows=3,
)

# Print results.
for row in df.itertuples():
    st.write(f"{row.name} has a :{row.pet}:")
