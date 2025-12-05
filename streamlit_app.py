import streamlit as st
import urllib.parse
import pandas as pd
from datetime import datetime

# --- CONFIGURATION & DATA ---
# Added 'price' to the data structure
DISPATCH_MAP = {
    "HAKI HEAL": {
        "phone": "601158976276", 
        "products": {
            "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM-01", "price": 450},
            "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY-01", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP-01", "price": 120}
        }
    },
    "AURORACO": {
        "phone": "601158976276", 
        "products": {
            "AURORACO MATCHA EZMESI": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO KAKAO EZMESI": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SUPER GIDA": {"sku": "SKU-AUR-SUPER", "price": 800}
        }
    },
    "LONGEVICALS": {
        "phone": "601158976276", 
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
    }
}

# --- PAGE CONFIG & STYLING ---
st.set_page_config(page_title="NATUVISIO Dispatch", page_icon="🚀", layout="wide")

# Custom CSS for "Beautiful" Visuals
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    /* Cards/Containers */
    .css-1r6slb0, .css-12oz5g7 {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #333;
    }
    /* Input Fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 10px;
    }
    /* Headers */
    h1, h2, h3 {
        color: #ffffff !important;
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    .stDataFrame {
        background-color: white; 
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE (For Logging) ---
if 'order_history' not in st.session_state:
    st.session_state.order_history = []

# --- APP HEADER ---
st.title("🚀 NATUVISIO Logistics Hub")
st.markdown("##### *Bridge Operations Dashboard*")
st.divider()

# --- MAIN FORM ---
col_main_1, col_main_2 = st.columns([1, 1])

with col_main_1:
    st.markdown("### 👤 Customer Details")
    customer_name = st.text_input("Full Name", placeholder="e.g. Ahmet Yilmaz")
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        customer_phone = st.text_input("Phone", placeholder="0532...")
    with col_c2:
        customer_email = st.text_input("Email", placeholder="email@example.com")
    customer_address = st.text_area("Delivery Address")

with col_main_2:
    st.markdown("### 📦 Shipment Details")
    
    # Brand Selection
    selected_brand = st.selectbox("Select Partner Brand", list(DISPATCH_MAP.keys()))
    brand_data = DISPATCH_MAP[selected_brand]
    
    # Product Selection
    product_list = list(brand_data["products"].keys())
    selected_product_name = st.selectbox("Select Product", product_list)
    
    # Get Details
    product_details = brand_data["products"][selected_product_name]
    sku = product_details['sku']
    unit_price = product_details['price']
    
    # Quantity & Priority
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        quantity = st.number_input("Quantity", min_value=1, value=1)
    with col_p2:
        priority = st.selectbox("Priority", ["Standard", "🚨 URGENT", "🧊 Cold Chain"])
        
    # Total
    total_price = unit_price * quantity
    st.info(f"💰 **Total Value:** {total_price} TL ({unit_price} TL x {quantity})")

    custom_note = st.text_input("Internal Note", placeholder="Optional...")

st.divider()

# --- ACTION SECTION ---
# Logic: We use a button to 'Log' the order, which then reveals the WhatsApp link.
# This ensures we capture the data before they leave the app.

if st.button("✅ Confirm & Prepare Order"):
    if customer_name and customer_phone:
        # 1. Add to History
        new_order = {
            "Time": datetime.now().strftime("%H:%M:%S"),
            "Brand": selected_brand,
            "Product": selected_product_name,
            "Qty": quantity,
            "Total (TL)": total_price,
            "Customer": customer_name,
            "Status": "Generated"
        }
        st.session_state.order_history.append(new_order)
        st.success("Order Logged Successfully! Click below to dispatch.")
        
        # 2. Generate WhatsApp Link
        clean_phone = brand_data['phone'].replace("+", "").replace(" ", "")
        
        msg_body = (
            f"*{priority} DISPATCH REQUEST*\n"
            f"--------------------------------\n"
            f"👤 *Cust:* {customer_name}\n"
            f"📞 *Tel:* {customer_phone}\n"
            f"🏠 *Addr:* {customer_address}\n"
            f"--------------------------------\n"
            f"📦 *Item:* {selected_product_name}\n"
            f"🔢 *Qty:* {quantity}\n"
            f"🆔 *SKU:* {sku}\n"
            f"📝 *Note:* {custom_note}\n"
            f"--------------------------------\n"
            f"CONFIRM TRACKING."
        )
        
        encoded_msg = urllib.parse.quote(msg_body)
        whatsapp_url = f"https://wa.me/{clean_phone}?text={encoded_msg}"
        
        # 3. Show Big Green Button
        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 20px;">
                📲 OPEN WHATSAPP NOW
            </div>
        </a>
        """, unsafe_allow_html=True)
        
    else:
        st.error("Please fill in Customer Name and Phone to proceed.")

# --- HISTORY LOG ---
st.divider()
st.markdown("### 📋 Session Dispatch Log")

if len(st.session_state.order_history) > 0:
    df = pd.DataFrame(st.session_state.order_history)
    st.dataframe(df, use_container_width=True)
    
    # Metrics
    total_sales = sum(item['Total (TL)'] for item in st.session_state.order_history)
    st.metric("Total Session Value", f"{total_sales} TL")
else:
    st.caption("No orders dispatched in this session yet.")
