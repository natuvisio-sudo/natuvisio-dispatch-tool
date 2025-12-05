import streamlit as st
import urllib.parse
import pandas as pd
import os
from datetime import datetime

# --- 1. PAGE CONFIGURATION (MUST BE FIRST) ---
st.set_page_config(page_title="Admin HQ", page_icon="🏢", layout="wide")

# --- 2. SECURITY & SETTINGS ---
ADMIN_PASS = "admin2025"
CSV_FILE = "dispatch_history.csv"

# --- 3. DATA & PRODUCTS ---
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

# --- 4. ROBUST DATABASE FUNCTIONS ---
def load_history():
    """Safely loads the CSV history, creating it if missing."""
    try:
        if os.path.exists(CSV_FILE):
            return pd.read_csv(CSV_FILE)
    except Exception as e:
        st.error(f"Database Error: {e}")
    
    # Return empty structure if file missing or corrupt
    return pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status", "Tracking_Num"])

def save_to_history(new_entry):
    """Safely appends a new order to the CSV."""
    try:
        df = load_history()
        new_df = pd.DataFrame([new_entry])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Failed to save order: {e}")
        return False

# --- 5. PREMIUM STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.5)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-attachment: fixed;
    }
    .stMarkdown, .stDataFrame, div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(12px);
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }
    h1, h2, h3 { color: white !important; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }
    
    div.stButton > button {
        background: linear-gradient(135deg, #7C9A86 0%, #31462f 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 8px;
        text-transform: uppercase;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #A0E8AF 0%, #7C9A86 100%);
        color: #1a1a1a;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# --- 6. AUTHENTICATION LOGIC ---
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False

if not st.session_state.admin_logged_in:
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.title("🏢 NATUVISIO HQ")
        st.write("Secure Access Required")
        
        pwd = st.text_input("Admin Key", type="password")
        
        col_login, col_back = st.columns(2)
        with col_login:
            if st.button("Unlock Dashboard", type="primary", use_container_width=True):
                if pwd == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("⛔ Access Denied")
        with col_back:
            if st.button("⬅️ Main Menu", use_container_width=True):
                st.switch_page("streamlit_app.py")
    st.stop() # Stop here if not logged in

# --- 7. MAIN DASHBOARD ---
# Initialize Cart
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state: st.session_state.selected_brand_lock = None

# Header
c_head, c_logout = st.columns([6, 1])
with c_head:
    st.title("🏢 Admin Command Center")
with c_logout:
    if st.button("Logout"):
        st.session_state.admin_logged_in = False
        st.switch_page("streamlit_app.py")

if st.button("⬅️ Back to Main Menu"):
    st.switch_page("streamlit_app.py")

st.divider()

# --- 8. METRICS ---
df = load_history()
if not df.empty:
    m1, m2, m3, m4 = st.columns(4)
    total_val = df["Total_Value"].sum() if "Total_Value" in df.columns else 0
    shipped = len(df[df['Status'] == 'Shipped']) if "Status" in df.columns else 0
    pending = len(df[df['Status'] == 'Pending']) if "Status" in df.columns else 0
    
    m1.metric("Total Volume", f"{total_val:,.0f} TL")
    m2.metric("Total Orders", len(df))
    m3.metric("Shipped", shipped)
    m4.metric("Pending", pending)

st.divider()

# --- 9. DISPATCH WORKFLOW ---
col_L, col_R = st.columns([1.5, 1])

with col_L:
    st.markdown("### 👤 1. Customer Details")
    cc1, cc2 = st.columns(2)
    with cc1: cust_name = st.text_input("Full Name")
    with cc2: cust_phone = st.text_input("Phone Number")
    cust_address = st.text_area("Delivery Address", height=70)
    
    st.markdown("---")
    st.markdown("### 🛒 2. Build Shipment")
    
    # Brand Locking Logic
    if st.session_state.cart:
        st.info(f"🔒 Locked to: **{st.session_state.selected_brand_lock}**")
        active_brand = st.session_state.selected_brand_lock
    else:
        active_brand = st.selectbox("Select Brand Partner", list(DISPATCH_MAP.keys()))

    brand_data = DISPATCH_MAP[active_brand]
    
    # Product Adder
    c_prod, c_qty = st.columns([3, 1])
    with c_prod:
        selected_prod = st.selectbox("Select Product", list(brand_data["products"].keys()))
    with c_qty:
        qty = st.number_input("Qty", min_value=1, value=1)
        
    prod_details = brand_data["products"][selected_prod]
    
    if st.button("➕ Add to Cart"):
        item_entry = {
            "brand": active_brand,
            "product": selected_prod,
            "sku": prod_details['sku'],
            "qty": qty,
            "subtotal": prod_details['price'] * qty
        }
        st.session_state.cart.append(item_entry)
        st.session_state.selected_brand_lock = active_brand
        st.rerun()

with col_R:
    st.markdown("### 📦 3. Review & Dispatch")
    
    if st.session_state.cart:
        cart_df = pd.DataFrame(st.session_state.cart)
        st.dataframe(cart_df[["product", "qty", "subtotal"]], use_container_width=True, hide_index=True)
        
        total_order = cart_df["subtotal"].sum()
        st.markdown(f"#### Total Value: `{total_order} TL`")
        
        priority = st.selectbox("Priority", ["Standard", "🚨 URGENT", "🧊 Cold Chain"])
        
        if st.button("⚡ CONFIRM & DISPATCH", type="primary", use_container_width=True):
            if cust_name and cust_phone:
                # Generate ID
                order_id = f"ORD-{datetime.now().strftime('%m%d%H%M%S')}"
                items_str = ", ".join([f"{i['product']}(x{i['qty']})" for i in st.session_state.cart])
                
                # Save to DB
                new_entry = {
                    "Order_ID": order_id,
                    "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "Brand": active_brand,
                    "Customer": cust_name,
                    "Items": items_str,
                    "Total_Value": total_order,
                    "Status": "Pending",
                    "Tracking_Num": ""
                }
                
                if save_to_history(new_entry):
                    # WhatsApp Link Generation
                    safe_addr = cust_address.replace("\n", ", ")
                    target_phone = brand_data['phone'].replace("+", "").replace(" ", "")
                    
                    msg_body = (
                        f"*{priority} DISPATCH REQUEST*\n"
                        f"🆔 Order: {order_id}\n"
                        f"--------------------------------\n"
                        f"👤 *Cust:* {cust_name}\n"
                        f"📞 *Tel:* {cust_phone}\n"
                        f"🏠 *Addr:* {safe_addr}\n"
                        f"--------------------------------\n"
                        f"📦 ITEMS:\n"
                    )
                    for item in st.session_state.cart:
                        msg_body += f"- {item['product']} (x{item['qty']})\n"
                    
                    msg_body += f"--------------------------------\nPLEASE CONFIRM TRACKING."
                    
                    encoded_msg = urllib.parse.quote(msg_body)
                    whatsapp_url = f"https://wa.me/{target_phone}?text={encoded_msg}"
                    
                    st.success("✅ Order Logged Successfully!")
                    st.markdown(f"""
                    <a href="{whatsapp_url}" target="_blank" style="text-decoration: none;">
                        <div style="background: #25D366; color: white; padding: 15px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 18px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);">
                            📲 CLICK TO SEND WHATSAPP
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    # Clear Cart
                    st.session_state.cart = []
                    st.session_state.selected_brand_lock = None
            else:
                st.error("⚠️ Missing Customer Name or Phone Number")
                
        if st.button("🗑️ Clear Cart"):
            st.session_state.cart = []
            st.session_state.selected_brand_lock = None
            st.rerun()
    else:
        st.info("Cart is empty.")

st.divider()

# --- 10. LIVE AUDIT LOG ---
st.subheader("🔍 Live Fulfillment Log")
if not df.empty:
    st.dataframe(
        df.sort_values(by="Time", ascending=False), 
        use_container_width=True, 
        hide_index=True
    )
else:
    st.caption("No dispatch history found.")
