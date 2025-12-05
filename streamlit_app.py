import streamlit as st
from twilio.rest import Client

# --- CRITICAL: HOW TO SAVE ---
# After editing this file, you must click the "Source Control" icon (branch icon) on the left.
# Then type a message (e.g., "Updated logic") and click "Commit & Push".
# Only then will your changes go live on the web app.

# --- CONFIGURATION (Secrets) ---
# We will set these in the Streamlit Dashboard later, not here!
try:
    TWILIO_SID = st.secrets["TWILIO_SID"]
    TWILIO_TOKEN = st.secrets["TWILIO_TOKEN"]
    FROM_NUMBER = st.secrets["FROM_NUMBER"]
except:
    st.error("⚠️ Secrets not found! Please set them in Streamlit Cloud.")
    st.stop()

# --- THE DATABASE ---
DISPATCH_MAP = {
    "HAKI HEAL": {
        "sku": "SKU-HAKI-001",
        "name": "Recovery Oil (50ml)",
        "phone": "+60 11-5897 6276" # Replace with real partner number
    },
    "AURORACO": {
        "sku": "SKU-AUR-088",
        "name": "Ceremonial Matcha",
        "phone": "+60 11-5897 6276" # Replace with real partner number
    },
    "LONGEVICALS": {
        "sku": "SKU-LONG-999",
        "name": "NMN Cold Pack",
        "phone": "+60 11-5897 6276" # Replace with real partner number
    }
}

# --- THE APP INTERFACE ---
st.title("🚀 NATUVISIO Dispatcher")
st.write("Select a partner to trigger an instant fulfillment request.")

# Dropdown Selection
brand = st.selectbox("Select Brand Partner", list(DISPATCH_MAP.keys()))

# Show Details
item = DISPATCH_MAP[brand]
st.info(f"📦 **Ready to Dispatch:** {item['name']} ({item['sku']})")

# The "Big Red Button"
if st.button(f"⚡ SEND ORDER TO {brand}"):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    
    msg_body = (
        f"🚨 *NATUVISIO ALERT*\n"
        f"Please ship immediately:\n"
        f"Item: {item['name']}\n"
        f"SKU: {item['sku']}\n"
        f"Confirm when shipped."
    )
    
    try:
        message = client.messages.create(
            body=msg_body,
            from_=FROM_NUMBER,
            to=f"whatsapp:{item['phone']}"
        )
        st.success(f"✅ Message sent! ID: {message.sid}")
    except Exception as e:

        st.error(f"❌ Failed: {e}")

