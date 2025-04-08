import streamlit as st
from streamlit_gsheets import GSheetsConnection
from streamlit_qrcode_scanner import qrcode_scanner
from datetime import date

# st.title("🔋 Battery Scanner")

# Constants
gsheet = "gsheets"
wksheet = "Sheet2"
timestamp_pattern = "%Y-%m-%d"
color = "red"
# Create a connection object.
conn = st.connection(gsheet, type=GSheetsConnection)

def read_db():
    # Read the data from the Google Sheet
    return conn.read(worksheet=wksheet,ttl=0, usecols=[0,1,2]).astype(str)


def get_row_data(df, selected_row):
    return df.loc[df['unit'] == selected_row]

# Function to add QR code to the selected unit
def add_qr_code(code):
    local_df = read_db()
    print(code)
    if not code:
        st.error("Please scan a QR code.")
        return
    if code in local_df['battery'].values:
        existing_unit = local_df.loc[local_df['battery'] == code, 'unit'].values[0]
        if existing_unit==selected_row:
            st.error(f"Battery code already exists in unit {existing_unit}.")
            return
        st.error(f"Battery code already exists. Force removed from unit {existing_unit}.")
        local_df.loc[local_df['battery'] == code, 'battery'] = f"forced-removal-{code}"
    local_df.loc[local_df['unit'] == selected_row, 'battery'] = code
    local_df.loc[local_df['unit'] == selected_row, 'timestamp'] = date.today().strftime(timestamp_pattern)
    conn.update(data=local_df)
    
    
    
# Initialize session state for QR code storage
if 'qrcode' not in st.session_state:
    st.session_state.qrcode = ""


df = read_db()
# st.dataframe(df, use_container_width=True)


# Create a selectbox for the user to select a unit
selected_row = st.selectbox(
    label="Select a Unit", 
    options=df['unit'].unique().tolist(),
    help="Select a unit to scan its battery code."
    )

if 'selected_row' not in st.session_state:
    st.session_state.selected_row =  selected_row

# Display the selected row
table_data = get_row_data(df, selected_row)
unit = table_data['unit'].values[0]
battery = table_data['battery'].values[0]
if battery!= "nan":
    battery_SL = '-'.join(battery.split("-")[5:])
    st.write(f"SL: {battery_SL}")
else:
    st.write("No battery code attached.")
timestamp = table_data['timestamp'].values[0]
st.write(f"Last update: {timestamp}")


# QR code scanner
qrcode = qrcode_scanner()

# Get stored QR code from session state
stored_qr_code = st.session_state.get("qrcode", "")

# Check if a new QR code was scanned
if qrcode and qrcode!=stored_qr_code:
    # Set the new QR code in session state
    st.session_state.qrcode = qrcode
    stored_qr_code = st.session_state.get("qrcode", "")
    st.toast(body="New Code Scanned!", icon="✅")


if stored_qr_code:
    qr_data = stored_qr_code.split("-")
    if len(qr_data) > 6:
        company, amphr, m, d, yr, *serial = qr_data
        serial = '-'.join(serial)
        qr_data = {
            'Company': company, 
            'Capacity': amphr, 
            'Date': f"{m}-{d}-{yr}"
            }
        color = "green" if stored_qr_code==battery else "orange"
        # st.write(f"{stored_qr_code=} : {battery=}")
        st.markdown(f"##### SL: :{color}[{serial}]")
        st.table(data=qr_data)
    else:
        st.error("Invalid QR code format.")


st.button(
    label="Add Battery code", 
    icon="📌", 
    help="Attach code to unit", 
    on_click=add_qr_code,
    args=(stored_qr_code,), 
    use_container_width=True
    )