import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
# TEST MODE: All brands routed to +601158976276
# FORMAT: Country Code + Number (No '+' sign, no spaces).

DISPATCH_MAP = {
    "HAKI HEAL": {
        "phone": "601158976276", # TEST NUMBER
        "products": {
            "HAKI HEAL CREAM": "SKU-HAKI-CRM-01",
            "HAKI HEAL VUCUT LOSYONU": "SKU-HAKI-BODY-01",
            "HAKI HEAL SABUN": "SKU-HAKI-SOAP-01"
        }
    },
    "AURORACO": {
        "phone": "601158976276", # TEST NUMBER
        "products": {
            "AURORACO MATCHA EZMESI": "SKU-AUR-MATCHA",
            "AURORACO KAKAO EZMESI": "SKU-AUR-CACAO",
            "AURORACO SUPER GIDA": "SKU-AUR-SUPER"
        }
    },
    "LONGEVICALS": {
        "phone": "601158976276", # TEST NUMBER
        "products": {
            "LONGEVICALS DHA": "SKU-LONG-DHA",
            "LONGEVICALS EPA": "SKU-LONG-EPA"
        }
    }
}

# --- APP HEADER ---
st.set_page_config(page_title="NATUVISIO Dispatch", page_icon="🚀")
st.title("🚀 NATUVISIO Dispatcher")
st.markdown("### Internal Logistics Hub (Free Mode)")
st.divider()

# --- SECTION 1: CUSTOMER DETAILS ---
st.subheader("👤 Customer Information")
col_c1, col_c2 = st.columns(2)

with col_c1:
    customer_name = st.text_input("Name Surname", placeholder="e.g. Ahmet Yilmaz")
    customer_phone = st.text_input("Customer Phone", placeholder="e.g. 0532 555 55 55")

with col_c2:
    customer_email = st.text_input("Email Address", placeholder="e.g. ahmet@example.com")

customer_address = st.text_area("Full Delivery Address", placeholder="Street, Building, Apt, City...")

st.divider()

# --- SECTION 2: ORDER DETAILS ---
st.subheader("📦 Order Routing")
col1, col2 = st.columns(2)

with col1:
    # Step 1: Select Brand
    selected_brand = st.selectbox("Select Partner", list(DISPATCH_MAP.keys()))
    
with col2:
    priority = st.selectbox("Priority Level", ["Standard", "🚨 URGENT", "🧊 Cold Chain"])

# Get Brand Data
brand_data = DISPATCH_MAP[selected_brand]

# Step 2: Select Product (Dynamic based on Brand)
product_list = list(brand_data["products"].keys())
selected_product_name = st.selectbox("Select Product", product_list)

# Get SKU for the selected product
selected_sku = brand_data["products"][selected_product_name]

# Optional Notes
custom_note = st.text_input("Special Instructions (Optional)", placeholder="e.g. Include gift note...")

# --- MESSAGE GENERATION ---
# Clean the phone number just in case
clean_phone = brand_data['phone'].replace("+", "").replace(" ", "")

# Build the text
msg_body = (
    f"*{priority} DISPATCH REQUEST*\n"
    f"--------------------------------\n"
    f"👤 *Customer:* {customer_name}\n"
    f"📞 *Phone:* {customer_phone}\n"
    f"📧 *Email:* {customer_email}\n"
    f"🏠 *Address:* {customer_address}\n"
    f"--------------------------------\n"
    f"📦 *Item:* {selected_product_name}\n"
    f"🆔 *SKU:* {selected_sku}\n"
    f"📝 *Note:* {custom_note if custom_note else 'None'}\n"
    f"--------------------------------\n"
    f"Please confirm tracking number."
)

# Encode for URL
encoded_msg = urllib.parse.quote(msg_body)
whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"

# --- PREVIEW & SEND ---
st.info(f"**Target:** {selected_brand} ({clean_phone})")
st.text_area("Message Preview:", value=msg_body, height=300, disabled=True)

# The "Big Green Button"
st.markdown(f"""
    <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
        <div style="
            background-color: #25D366; 
            color: white; 
            padding: 15px 20px; 
            text-align: center; 
            border-radius: 10px; 
            font-size: 18px; 
            font-weight: bold; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s;">
            📲 OPEN WHATSAPP TO SEND
        </div>
    </a>
    """, unsafe_allow_html=True)

st.caption("ℹ️ Clicking this opens WhatsApp Web/App with the message ready to send.")
