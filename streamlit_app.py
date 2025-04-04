import streamlit as st
from streamlit_gsheets import GSheetsConnection


st.title("🔋 Battery Scanner")

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=0,usecols=[0, 1]).astype(str)

# Create a selectbox for the user to select a unit
all_units = df["unit"].unique().tolist()
selected_row = st.selectbox("Select a Unit", all_units)


if 'qrcode' not in st.session_state:
    st.session_state.qrcode = ""

qrcode = st.session_state.qrcode

def add_qr_code(code):
    df = conn.read(ttl=0,usecols=[0, 1]).astype(str)
    df.loc[df["unit"] == selected_row, "battery"] = code
    conn.update(data=df)
    st.success("QR code added successfully.")
    

# Display the selected row
st.dataframe(
    df.loc[df["unit"] == selected_row],
    use_container_width=True,
    hide_index=True
    )

st.page_link("1_scanner.py", label="Scan QR code", icon="📸", help="Scan QR code")

# pg = st.navigation([st.Page("page1.py", title="First page")])







st.markdown(f"{qrcode}")
st.button("Add QR code", on_click=add_qr_code, args=(qrcode,))