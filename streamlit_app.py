import streamlit as st
import urllib.parse
import pandas as pd
import os
from datetime import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="NATUVISIO Dispatch", page_icon="🚀", layout="wide")

# --- 2. SETTINGS ---
CSV_FILE = "dispatch_history.csv"

# --- 3. DATA CONFIGURATION (The "Bridge" Map) ---
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

# --- 4. PREMIUM STYLING ---
st.markdown("""
    <style>
    /* BACKGROUND */
    .stApp {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
    }
    /* CONTAINERS */
    .stMarkdown, .stDataFrame, div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 12px;
        padding: 20px;
        color: #333;
    }
    /* HEADERS */
    h1, h2, h3 { color: white !important; text-shadow: 0 2px 4px rgba(0,0,0,0.3); }
    /* BUTTONS */
    div.stButton > button {
        background: #25D366; 
        color: white; 
        border: none;
        font-weight: bold;
        padding: 10px 20px;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 5. HELPER FUNCTIONS ---
def load_history():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status"])

def save_to_history(new_entry):
    df = load_history()
    new_df = pd.DataFrame([new_entry])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# --- 6. SESSION STATE (Cart) ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state:
    st.session_state.selected_brand_lock = None

# --- 7. MAIN APP LAYOUT ---
st.title("🚀 NATUVISIO Logistics Hub")
st.markdown("##### *Single-View Dispatch System*")
st.divider()

col_L, col_R = st.columns([1.5, 1])

# --- LEFT COLUMN: BUILDER ---
with col_L:
    st.markdown("### 👤 1. Customer")
    c1, c2 = st.columns(2)
    with c1: cust_name = st.text_input("Name", placeholder="Full Name")
    with c2: cust_phone = st.text_input("Phone", placeholder="+90...")
    cust_addr = st.text_area("Address", height=70)
    
    st.markdown("---")
    st.markdown("### 🛒 2. Build Shipment")
    
    # Brand Lock Logic
    if st.session_state.cart:
        st.info(f"🔒 Locked to: **{st.session_state.selected_brand_lock}**")
        active_brand = st.session_state.selected_brand_lock
    else:
        active_brand = st.selectbox("Select Brand", list(DISPATCH_MAP.keys()))

    brand_data = DISPATCH_MAP[active_brand]
    
    # Product Adder
    cp, cq = st.columns([3, 1])
    with cp: 
        selected_prod = st.selectbox("Product", list(brand_data["products"].keys()))
    with cq: 
        qty = st.number_input("Qty", min_value=1, value=1)
        
    prod_details = brand_data["products"][selected_prod]
    
    if st.button("➕ Add to Cart"):
        st.session_state.cart.append({
            "brand": active_brand,
            "product": selected_prod,
            "sku": prod_details['sku'],
            "qty": qty,
            "subtotal": prod_details['price'] * qty
        })
        st.session_state.selected_brand_lock = active_brand
        st.rerun()

# --- RIGHT COLUMN: REVIEW & SEND ---
with col_R:
    st.markdown("### 📦 3. Review")
    
    if st.session_state.cart:
        # Show Table
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df[["product", "qty", "subtotal"]], use_container_width=True, hide_index=True)
        
        total = cart_df["subtotal"].sum()
        st.markdown(f"#### Total Value: `{total} TL`")
        
        priority = st.selectbox("Priority", ["Standard", "🚨 URGENT", "🧊 Cold Chain"])
        
        if st.button("⚡ LOG & GENERATE LINK"):
            if cust_name and cust_phone:
                # 1. Prepare Data
                oid = f"ORD-{datetime.now().strftime('%m%d%H%M%S')}"
                items_str = ", ".join([f"{i['product']}(x{i['qty']})" for i in st.session_state.cart])
                
                # 2. Save Log
                save_to_history({
                    "Order_ID": oid,
                    "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Brand": active_brand,
                    "Customer": cust_name,
                    "Items": items_str,
                    "Total_Value": total,
                    "Status": "Generated"
                })
                
                # 3. Create WhatsApp Link
                safe_addr = cust_addr.replace("\n", ", ")
                target_phone = brand_data['phone'].replace("+", "").replace(" ", "")
                
                msg = (
                    f"*{priority} DISPATCH REQUEST*\n"
                    f"🆔 {oid}\n"
                    f"--------------------------------\n"
                    f"👤 {cust_name}\n"
                    f"📞 {cust_phone}\n"
                    f"🏠 {safe_addr}\n"
                    f"--------------------------------\n"
                    f"📦 ITEMS:\n"
                )
                for item in st.session_state.cart:
                    msg += f"- {item['product']} (x{item['qty']})\n"
                msg += "Please Confirm Tracking."
                
                url = f"https://wa.me/{target_phone}?text={urllib.parse.quote(msg)}"
                
                st.success("✅ Order Logged!")
                st.markdown(f"""
                <a href="{url}" target="_blank" style="text-decoration:none;">
                    <div style="background:#25D366;color:white;padding:15px;text-align:center;border-radius:10px;font-weight:bold;font-size:20px;">
                        📲 OPEN WHATSAPP
                    </div>
                </a>
                """, unsafe_allow_html=True)
                
                # Cleanup
                st.session_state.cart = []
                st.session_state.selected_brand_lock = None
            else:
                st.error("Missing Name/Phone!")
                
        if st.button("Clear Cart"):
            st.session_state.cart = []
            st.session_state.selected_brand_lock = None
            st.rerun()
    else:
        st.info("Cart is empty.")

# --- 8. LOGS ---
st.divider()
st.subheader("🗃️ Dispatch History")
df = load_history()
if not df.empty:
    st.dataframe(df.sort_values(by="Time", ascending=False), use_container_width=True)
else:
    st.caption("No records found.")
