import streamlit as st
import urllib.parse
import pandas as pd
import os
from datetime import datetime

# --- CONFIGURATION & DATA ---
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

CSV_FILE = "dispatch_history.csv"

# --- PAGE CONFIG & STYLING ---
st.set_page_config(page_title="NATUVISIO Dispatch", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to right, #ece9e6, #ffffff);
        color: #333;
    }
    .main-header {
        font-family: 'Helvetica Neue', sans-serif;
        color: #1e3c72;
    }
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state:
    st.session_state.selected_brand_lock = None

# --- HELPER FUNCTIONS ---
def load_history():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Time", "Brand", "Customer", "Items", "Total_Value"])

def save_to_history(new_entry):
    df = load_history()
    # Create a DataFrame for the new entry
    new_df = pd.DataFrame([new_entry])
    # Concatenate appropriately
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# --- APP HEADER ---
st.title("🚀 NATUVISIO Logistics Hub")
st.markdown("##### *Centralized Dispatch Bridge*")
st.divider()

# --- SECTION 1: CUSTOMER INFO (Top Level for Stability) ---
st.markdown("### 👤 Step 1: Customer Information")
c1, c2, c3 = st.columns(3)
with c1:
    cust_name = st.text_input("Customer Name", placeholder="Full Name")
with c2:
    cust_phone = st.text_input("Customer Phone", placeholder="+90...")
with c3:
    cust_email = st.text_input("Customer Email", placeholder="optional")

# Debugging note: Address is now full width to prevent cutting off
cust_address = st.text_area("Full Delivery Address", height=80, placeholder="Street, Apt, City, Zip Code...")

st.divider()

# --- SECTION 2: BUILD SHIPMENT (Cart System) ---
st.markdown("### 📦 Step 2: Build Shipment Package")

col_build_1, col_build_2 = st.columns([1, 2])

with col_build_1:
    # Brand Logic: If cart has items, lock the brand so we don't mix brands in one WhatsApp msg
    if st.session_state.cart:
        st.info(f"🔒 Locked to: **{st.session_state.selected_brand_lock}**")
        active_brand = st.session_state.selected_brand_lock
    else:
        active_brand = st.selectbox("Select Partner Brand", list(DISPATCH_MAP.keys()))

    # Product Selection based on active brand
    brand_data = DISPATCH_MAP[active_brand]
    product_options = list(brand_data["products"].keys())
    
    selected_prod = st.selectbox("Product", product_options)
    prod_details = brand_data["products"][selected_prod]
    
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        qty = st.number_input("Qty", min_value=1, value=1)
    with col_q2:
        st.markdown(f"<br><b>{prod_details['price']} TL</b> / unit", unsafe_allow_html=True)

    if st.button("➕ Add to Package"):
        # Add to session cart
        item_entry = {
            "brand": active_brand,
            "product": selected_prod,
            "sku": prod_details['sku'],
            "qty": qty,
            "price": prod_details['price'],
            "subtotal": prod_details['price'] * qty
        }
        st.session_state.cart.append(item_entry)
        st.session_state.selected_brand_lock = active_brand # Lock brand
        st.rerun()

with col_build_2:
    st.markdown("#### Current Package Items")
    if st.session_state.cart:
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(
            cart_df[["product", "qty", "sku", "subtotal"]], 
            use_container_width=True,
            hide_index=True
        )
        
        total_val = cart_df["subtotal"].sum()
        st.markdown(f"**Total Shipment Value:** `{total_val} TL`")
        
        if st.button("🗑️ Clear Package"):
            st.session_state.cart = []
            st.session_state.selected_brand_lock = None
            st.rerun()
    else:
        st.caption("Package is empty. Add items from the left.")

st.divider()

# --- SECTION 3: DISPATCH ACTION ---
st.markdown("### 🚀 Step 3: Dispatch & Log")

priority = st.selectbox("Priority Level", ["Standard", "🚨 URGENT", "🧊 Cold Chain"])
special_note = st.text_input("Internal Note for Warehouse", placeholder="e.g. Gift wrap required")

if st.button("✅ GENERATE DISPATCH LINK", type="primary", use_container_width=True):
    if not st.session_state.cart:
        st.error("❌ Package is empty!")
    elif not cust_name or not cust_phone or not cust_address:
        st.error("❌ Missing Customer Name, Phone, or Address!")
    else:
        # 1. Prepare Data
        brand_info = DISPATCH_MAP[st.session_state.selected_brand_lock]
        target_phone = brand_info['phone'].replace("+", "").replace(" ", "")
        
        # 2. Format Items List for WhatsApp
        items_text = ""
        items_summary_for_log = []
        total_shipment_value = 0
        
        for item in st.session_state.cart:
            items_text += f"📦 {item['product']} (x{item['qty']}) - {item['sku']}\n"
            items_summary_for_log.append(f"{item['product']}(x{item['qty']})")
            total_shipment_value += item['subtotal']
            
        # 3. Build Message
        # Fix address formatting (newlines can break links)
        safe_address = cust_address.replace("\n", ", ")
        
        msg_body = (
            f"*{priority} DISPATCH REQUEST*\n"
            f"--------------------------------\n"
            f"👤 *Cust:* {cust_name}\n"
            f"📞 *Tel:* {cust_phone}\n"
            f"🏠 *Addr:* {safe_address}\n"
            f"📧 *Email:* {cust_email}\n"
            f"--------------------------------\n"
            f"{items_text}"
            f"--------------------------------\n"
            f"📝 *Note:* {special_note}\n"
            f"💰 *Val:* {total_shipment_value} TL\n"
            f"PLEASE CONFIRM TRACKING."
        )
        
        encoded_msg = urllib.parse.quote(msg_body)
        whatsapp_url = f"https://wa.me/{target_phone}?text={encoded_msg}"
        
        # 4. Save to Unified Log (CSV)
        log_entry = {
            "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Brand": st.session_state.selected_brand_lock,
            "Customer": cust_name,
            "Items": ", ".join(items_summary_for_log),
            "Total_Value": total_shipment_value
        }
        save_to_history(log_entry)
        
        # 5. Show Success & Link
        st.success("✅ Order Logged to Database! Click below to send.")
        st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
            <div style="
                background-color: #25D366; 
                color: white; 
                padding: 20px; 
                border-radius: 12px; 
                text-align: center; 
                font-weight: bold; 
                font-size: 22px; 
                box-shadow: 0 4px 10px rgba(37, 211, 102, 0.4);">
                📲 OPEN WHATSAPP TO SEND
            </div>
        </a>
        """, unsafe_allow_html=True)

# --- SECTION 4: UNIFIED DISPATCH LOG ---
st.divider()
st.markdown("### 🗃️ Unified Dispatch History")

history_df = load_history()

if not history_df.empty:
    # Analytics
    col_m1, col_m2, col_m3 = st.columns(3)
    total_revenue = history_df["Total_Value"].sum()
    total_orders = len(history_df)
    top_brand = history_df["Brand"].mode()[0] if not history_df.empty else "N/A"
    
    col_m1.metric("Total Dispatched Value", f"{total_revenue:,.0f} TL")
    col_m2.metric("Total Shipments", total_orders)
    col_m3.metric("Top Partner", top_brand)
    
    # Sort by time desc
    if "Time" in history_df.columns:
        history_df = history_df.sort_values(by="Time", ascending=False)
        
    st.dataframe(history_df, use_container_width=True, hide_index=True)
else:
    st.info("No dispatch history found yet.")
