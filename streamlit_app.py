import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 1. CONFIGURATION & SETUP
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Admin OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
ADMIN_PASS = "admin2025"
CSV_FILE = "dispatch_history.csv"
PHI = 1.618  # Golden Ratio for spacing

# Spacing System (Fibonacci)
FIBO = {
    'xs': 8,
    'sm': 13,
    'md': 21,
    'lg': 34,
    'xl': 55
}

# Data Map
DISPATCH_MAP = {
    "HAKI HEAL": {
        "phone": "601158976276",
        "color": "#4ECDC4",
        "products": {
            "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM-01", "price": 450},
            "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY-01", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP-01", "price": 120}
        }
    },
    "AURORACO": {
        "phone": "601158976276",
        "color": "#FF6B6B",
        "products": {
            "AURORACO MATCHA EZMESI": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO KAKAO EZMESI": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SUPER GIDA": {"sku": "SKU-AUR-SUPER", "price": 800}
        }
    },
    "LONGEVICALS": {
        "phone": "601158976276",
        "color": "#95E1D3",
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
    }
}

# ============================================================================
# 2. PREMIUM ASSETS (SVG Icons)
# ============================================================================

def get_icon(name, color="#ffffff"):
    icons = {
        "mountain": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 20L9 8L12 14L15 6L21 20H3Z"/><path d="M9 8L7 12"/></svg>',
        "box": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
        "truck": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>',
        "chart": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "whatsapp": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
    }
    return icons.get(name, "")

# ============================================================================
# 3. DESIGN SYSTEM (CSS)
# ============================================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* BACKGROUND */
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.6), rgba(15, 23, 42, 0.7)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }}

    /* GLASS CARD */
    .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: {FIBO['md']}px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        margin-bottom: {FIBO['sm']}px;
    }}

    /* TYPOGRAPHY */
    h1, h2, h3 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: white !important;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}
    
    .metric-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: 28px;
        font-weight: 700;
        color: #fff;
    }}
    .metric-label {{
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: rgba(255,255,255,0.6);
    }}

    /* INPUTS */
    .stTextInput > div > div > input, .stSelectbox > div > div > select, .stNumberInput > div > div > input {{
        background: rgba(0,0,0,0.2) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 8px !important;
    }}
    
    /* BUTTONS */
    div.stButton > button {{
        background: linear-gradient(135deg, #4ECDC4 0%, #2980B9 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        transition: all 0.3s ease !important;
    }}
    div.stButton > button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
    }}

    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu, header, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 4. DATABASE & STATE
# ============================================================================

if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state: st.session_state.selected_brand_lock = None

def load_history():
    if os.path.exists(CSV_FILE): return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status", "Tracking_Num"])

def save_to_history(new_entry):
    df = load_history()
    new_df = pd.DataFrame([new_entry])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

# ============================================================================
# 5. AUTHENTICATION VIEW
# ============================================================================

def login_screen():
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="margin-bottom: 20px;">{get_icon('mountain', '#4ECDC4')}</div>
            <h3>NATUVISIO ADMIN</h3>
            <p style="color: rgba(255,255,255,0.6); font-size: 12px;">SECURE LOGISTICS OS</p>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("Enter Access Key", type="password", label_visibility="collapsed")
        
        b1, b2 = st.columns(2)
        with b1:
            if st.button("UNLOCK SYSTEM", use_container_width=True):
                if pwd == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
        with b2:
            if st.button("EXIT", use_container_width=True):
                st.switch_page("streamlit_app.py")

# ============================================================================
# 6. DASHBOARD VIEW
# ============================================================================

def dashboard_screen():
    # --- HEADER ---
    h1, h2 = st.columns([6, 1])
    with h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 15px;">
            {get_icon('mountain', '#4ECDC4')}
            <div>
                <h2 style="margin:0;">ADMIN HQ</h2>
                <span style="font-size: 12px; color: rgba(255,255,255,0.5); letter-spacing: 1px;">LOGISTICS COMMAND CENTER</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with h2:
        if st.button("LOGOUT"):
            st.session_state.admin_logged_in = False
            st.switch_page("streamlit_app.py")

    st.markdown(f"<div style='height: {FIBO['sm']}px'></div>", unsafe_allow_html=True)

    # --- TABS ---
    tab_dispatch, tab_orders, tab_analytics = st.tabs(["🚀 NEW DISPATCH", "📦 ACTIVE ORDERS", "📈 ANALYTICS"])

    # --- TAB 1: DISPATCH (WITH CART) ---
    with tab_dispatch:
        col_L, col_R = st.columns([1.618, 1]) # Golden Ratio Columns
        
        with col_L:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 👤 Customer Identity")
            c_name, c_phone = st.columns(2)
            with c_name: cust_name = st.text_input("Full Name")
            with c_phone: cust_phone = st.text_input("Phone (905...)")
            cust_addr = st.text_area("Delivery Address")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🛒 Inventory Selection")
            
            # Brand Lock Logic
            if st.session_state.cart:
                st.info(f"🔒 Locked to: {st.session_state.selected_brand_lock}")
                active_brand = st.session_state.selected_brand_lock
            else:
                active_brand = st.selectbox("Select Partner", list(DISPATCH_MAP.keys()))

            brand_data = DISPATCH_MAP[active_brand]
            
            cp, cq = st.columns([3, 1])
            with cp: prod = st.selectbox("Product", list(brand_data["products"].keys()))
            with cq: qty = st.number_input("Qty", 1, value=1)
            
            details = brand_data["products"][prod]
            
            if st.button("➕ ADD TO CART", use_container_width=True):
                st.session_state.cart.append({
                    "brand": active_brand,
                    "product": prod,
                    "sku": details['sku'],
                    "qty": qty,
                    "subtotal": details['price'] * qty
                })
                st.session_state.selected_brand_lock = active_brand
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_R:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📦 Shipment Manifest")
            
            if st.session_state.cart:
                df_cart = pd.DataFrame(st.session_state.cart)
                st.dataframe(df_cart[["product", "qty", "subtotal"]], use_container_width=True, hide_index=True)
                
                total = df_cart['subtotal'].sum()
                st.markdown(f"<div class='metric-value' style='text-align: right;'>{total:,.0f} ₺</div>", unsafe_allow_html=True)
                
                priority = st.selectbox("Priority Level", ["Standard", "🚨 URGENT", "🧊 Cold Chain"])
                
                if st.button("⚡ FLASH DISPATCH", type="primary", use_container_width=True):
                    if cust_name and cust_phone:
                        oid = f"NV-{datetime.now().strftime('%m%d%H%M')}"
                        items_txt = "\n".join([f"• {i['product']} (x{i['qty']})" for i in st.session_state.cart])
                        
                        # Save
                        save_to_history({
                            "Order_ID": oid,
                            "Time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                            "Brand": active_brand,
                            "Customer": cust_name,
                            "Items": items_txt.replace("\n", ", "),
                            "Total_Value": total,
                            "Status": "Pending",
                            "Tracking_Num": ""
                        })
                        
                        # WhatsApp Link
                        clean_phone = brand_data['phone'].replace("+", "").replace(" ", "")
                        msg = f"*{priority} DISPATCH*\n🆔 {oid}\n👤 {cust_name}\n📞 {cust_phone}\n🏠 {cust_addr}\n\n📦 CONTENTS:\n{items_txt}\n\n⚠️ Please confirm tracking."
                        url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(msg)}"
                        
                        st.success("✅ Order Logged!")
                        st.markdown(f"""
                        <a href="{url}" target="_blank" style="text-decoration:none;">
                            <div style="background:#25D366;color:white;padding:15px;border-radius:8px;text-align:center;font-weight:bold;">
                                📲 OPEN WHATSAPP
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                        
                        st.session_state.cart = []
                        st.session_state.selected_brand_lock = None
                    else:
                        st.error("Missing Customer Details")
                
                if st.button("🗑️ Clear Cart"):
                    st.session_state.cart = []
                    st.session_state.selected_brand_lock = None
                    st.rerun()
            else:
                st.info("Cart is empty.")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: ACTIVE ORDERS ---
    with tab_orders:
        df = load_history()
        if not df.empty:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.dataframe(df.sort_values("Time", ascending=False), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No dispatch history found.")

    # --- TAB 3: ANALYTICS ---
    with tab_analytics:
        df = load_history()
        if not df.empty:
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f"""<div class="glass-card"><div class="metric-value">{len(df)}</div><div class="metric-label">TOTAL ORDERS</div></div>""", unsafe_allow_html=True)
            with m2:
                rev = df['Total_Value'].sum()
                st.markdown(f"""<div class="glass-card"><div class="metric-value">{rev:,.0f} ₺</div><div class="metric-label">REVENUE</div></div>""", unsafe_allow_html=True)
            with m3:
                pending = len(df[df['Status']=='Pending'])
                st.markdown(f"""<div class="glass-card"><div class="metric-value">{pending}</div><div class="metric-label">PENDING</div></div>""", unsafe_allow_html=True)
            
            st.bar_chart(df['Brand'].value_counts())

# ============================================================================
# 7. MAIN EXECUTION
# ============================================================================

if not st.session_state.admin_logged_in:
    login_screen()
else:
    dashboard_screen()

