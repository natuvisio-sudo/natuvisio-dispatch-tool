
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
CSV_DISPATCH = "dispatch_history.csv"
CSV_FINANCE = "financial_ledger.csv" # NEW: Tracks money
CSV_PAYOUTS = "payout_history.csv"   # NEW: Tracks payments to brands

# Design Constants
PHI = 1.618
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

# BRAND CONTRACTS (The "Deal")
# Commission Rate: 0.15 = 15%
BRAND_CONTRACTS = {
    "HAKI HEAL": {"commission": 0.15, "phone": "601158976276", "color": "#4ECDC4"},
    "AURORACO": {"commission": 0.20, "phone": "601158976276", "color": "#FF6B6B"},
    "LONGEVICALS": {"commission": 0.12, "phone": "601158976276", "color": "#95E1D3"}
}

# Data Map
DISPATCH_MAP = {
# Product Database
PRODUCT_DB = {
"HAKI HEAL": {
        "phone": "601158976276",
        "color": "#4ECDC4",
        "products": {
            "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM-01", "price": 450},
            "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY-01", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP-01", "price": 120}
        }
        "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM", "price": 450},
        "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY", "price": 380},
        "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP", "price": 120}
},
"AURORACO": {
        "phone": "601158976276",
        "color": "#FF6B6B",
        "products": {
            "AURORACO MATCHA EZMESI": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO KAKAO EZMESI": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SUPER GIDA": {"sku": "SKU-AUR-SUPER", "price": 800}
        }
        "AURORACO MATCHA": {"sku": "SKU-AUR-MATCHA", "price": 650},
        "AURORACO CACAO": {"sku": "SKU-AUR-CACAO", "price": 550},
        "AURORACO SUPER": {"sku": "SKU-AUR-SUPER", "price": 800}
},
"LONGEVICALS": {
        "phone": "601158976276",
        "color": "#95E1D3",
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
        "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
        "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
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
# 2. DESIGN SYSTEM
# ============================================================================

st.markdown(f"""
<style>
   @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* BACKGROUND */
   .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.6), rgba(15, 23, 42, 0.7)), 
        background-image: linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.95)), 
                         url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
       background-size: cover;
       background-attachment: fixed;
       font-family: 'Inter', sans-serif;
   }}

    /* GLASS CARD */
   .glass-card {{
        background: rgba(255, 255, 255, 0.05);
        background: rgba(255, 255, 255, 0.03);
       backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.08);
       border-radius: 16px;
       padding: {FIBO['md']}px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
       margin-bottom: {FIBO['sm']}px;
   }}

    /* TYPOGRAPHY */
    h1, h2, h3 {{
    h1, h2, h3, h4 {{
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
    .metric-value {{ font-family: 'Space Grotesk'; font-size: 24px; font-weight: 700; color: #fff; }}
    .metric-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.5); }}
   
    /* BUTTONS */
    .status-paid {{ color: #4ECDC4; font-weight: bold; }}
    .status-pending {{ color: #FF6B6B; font-weight: bold; }}

    /* BUTTONS & INPUTS */
   div.stButton > button {{
       background: linear-gradient(135deg, #4ECDC4 0%, #2980B9 100%) !important;
       color: white !important;
       border: none !important;
        padding: 12px 24px !important;
        border-radius: 8px !important;
        border-radius: 6px !important;
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
    .stTextInput>div>div>input {{ background: rgba(255,255,255,0.05) !important; color: white !important; border: 1px solid rgba(255,255,255,0.1) !important; }}
    
   #MainMenu, header, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 4. DATABASE & STATE
# 3. DATABASE ENGINE
# ============================================================================

if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state: st.session_state.selected_brand_lock = None
def get_db(file, columns):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame(columns=columns)

def save_db(file, df, new_row=None):
    if new_row is not None:
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(file, index=False)
    return df

def load_history():
    if os.path.exists(CSV_FILE): return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status", "Tracking_Num"])
# Initialize DBs if missing
if not os.path.exists(CSV_DISPATCH):
    save_db(CSV_DISPATCH, pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status", "Tracking_Num"]))

def save_to_history(new_entry):
    df = load_history()
    new_df = pd.DataFrame([new_entry])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
if not os.path.exists(CSV_FINANCE):
    save_db(CSV_FINANCE, pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate", "Commission_Amt", "Payable_To_Brand", "Status"]))

if not os.path.exists(CSV_PAYOUTS):
    save_db(CSV_PAYOUTS, pd.DataFrame(columns=["Payout_ID", "Time", "Brand", "Amount", "Method", "Notes"]))

# ============================================================================
# 5. AUTHENTICATION VIEW
# 4. AUTHENTICATION
# ============================================================================

if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False

def login_screen():
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 20vh'></div>", unsafe_allow_html=True)
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
        st.markdown('<div class="glass-card" style="text-align:center;"><h3>🏔️ NATUVISIO ADMIN</h3><p>Financial & Logistics OS</p></div>', unsafe_allow_html=True)
        pwd = st.text_input("Access Key", type="password")
        if st.button("UNLOCK", use_container_width=True):
            if pwd == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Access Denied")
        if st.button("EXIT"): st.switch_page("streamlit_app.py")

# ============================================================================
# 6. DASHBOARD VIEW
# 5. CORE LOGIC BLOCKS
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
    c1, c2 = st.columns([6,1])
    with c1: st.markdown("## 🏔️ COMMAND CENTER")
    with c2: 
if st.button("LOGOUT"):
st.session_state.admin_logged_in = False
st.switch_page("streamlit_app.py")

    st.markdown(f"<div style='height: {FIBO['sm']}px'></div>", unsafe_allow_html=True)
    
    if st.button("⬅️ Main Menu"): st.switch_page("streamlit_app.py")
    st.markdown("---")

# --- TABS ---
    tab_dispatch, tab_orders, tab_analytics = st.tabs(["🚀 NEW DISPATCH", "📦 ACTIVE ORDERS", "📈 ANALYTICS"])

    # --- TAB 1: DISPATCH (WITH CART) ---
    with tab_dispatch:
        col_L, col_R = st.columns([1.618, 1]) # Golden Ratio Columns
    tabs = st.tabs([
        "🚀 DISPATCH & ORDERS", 
        "💰 FINANCIALS", 
        "🏦 VENDOR PAYOUTS", 
        "🧾 INVOICING",
        "📊 REPORTS"
    ])

    # ------------------------------------------------------------------------
    # TAB 1: DISPATCH & ORDERS (The Physical Flow)
    # ------------------------------------------------------------------------
    with tabs[0]:
        col_L, col_R = st.columns([1.5, 1])

        # --- NEW ORDER FORM ---
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
            st.markdown('<div class="glass-card"><h4>📝 New Order Entry</h4>', unsafe_allow_html=True)

            # Brand Lock Logic
            if st.session_state.cart:
                st.info(f"🔒 Locked to: {st.session_state.selected_brand_lock}")
                active_brand = st.session_state.selected_brand_lock
            else:
                active_brand = st.selectbox("Select Partner", list(DISPATCH_MAP.keys()))

            brand_data = DISPATCH_MAP[active_brand]
            if 'cart' not in st.session_state: st.session_state.cart = []

            cp, cq = st.columns([3, 1])
            with cp: prod = st.selectbox("Product", list(brand_data["products"].keys()))
            with cq: qty = st.number_input("Qty", 1, value=1)
            # 1. Customer
            c_name = st.text_input("Customer Name")
            c_phone = st.text_input("Phone (905...)")
            c_addr = st.text_area("Address", height=60)

            details = brand_data["products"][prod]
            # 2. Cart
            st.markdown("---")
            sel_brand = st.selectbox("Brand Partner", list(BRAND_CONTRACTS.keys()))
            sel_prod = st.selectbox("Product", list(PRODUCT_DB[sel_brand].keys()))
            qty = st.number_input("Qty", 1, value=1)

            if st.button("➕ ADD TO CART", use_container_width=True):
            # Add to Cart Logic
            if st.button("➕ Add Line Item"):
                prod_data = PRODUCT_DB[sel_brand][sel_prod]
                line_total = prod_data['price'] * qty
                
                # COMMISSION LOGIC HAPPENS HERE
                comm_rate = BRAND_CONTRACTS[sel_brand]["commission"]
                comm_amt = line_total * comm_rate
                payable = line_total - comm_amt
                
st.session_state.cart.append({
                    "brand": active_brand,
                    "product": prod,
                    "sku": details['sku'],
                    "qty": qty,
                    "subtotal": details['price'] * qty
                    "Brand": sel_brand,
                    "Product": sel_prod,
                    "SKU": prod_data['sku'],
                    "Qty": qty,
                    "Price": prod_data['price'],
                    "Total": line_total,
                    "Comm_Rate": comm_rate,
                    "Comm_Amt": comm_amt,
                    "Payable": payable
})
                st.session_state.selected_brand_lock = active_brand
st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

        # --- CART REVIEW & SUBMIT ---
with col_R:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📦 Shipment Manifest")
            st.markdown('<div class="glass-card"><h4>📦 Active Cart</h4>', unsafe_allow_html=True)

if st.session_state.cart:
                df_cart = pd.DataFrame(st.session_state.cart)
                st.dataframe(df_cart[["product", "qty", "subtotal"]], use_container_width=True, hide_index=True)
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df[["Product", "Qty", "Total"]], hide_index=True, use_container_width=True)
                
                grand_total = cart_df['Total'].sum()
                total_comm = cart_df['Comm_Amt'].sum()
                total_payable = cart_df['Payable'].sum()

                total = df_cart['subtotal'].sum()
                st.markdown(f"<div class='metric-value' style='text-align: right;'>{total:,.0f} ₺</div>", unsafe_allow_html=True)
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.1); padding:10px; border-radius:8px;'>
                    <div style='display:flex; justify-content:space-between;'><span>Order Total:</span><strong>{grand_total:,.2f} ₺</strong></div>
                    <div style='display:flex; justify-content:space-between; color:#4ECDC4;'><span>NATUVISIO Income:</span><strong>{total_comm:,.2f} ₺</strong></div>
                    <div style='display:flex; justify-content:space-between; color:#FF6B6B;'><span>Owed to Vendor:</span><strong>{total_payable:,.2f} ₺</strong></div>
                </div>
                """, unsafe_allow_html=True)

                priority = st.selectbox("Priority Level", ["Standard", "🚨 URGENT", "🧊 Cold Chain"])
                st.markdown("<br>", unsafe_allow_html=True)

                if st.button("⚡ FLASH DISPATCH", type="primary", use_container_width=True):
                    if cust_name and cust_phone:
                if st.button("⚡ CONFIRM ORDER & LOG FINANCE"):
                    if c_name and c_phone:
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
                        # 1. Save Dispatch Log
                        items_str = ", ".join([f"{x['Product']}(x{x['Qty']})" for x in st.session_state.cart])
                        dispatch_df = get_db(CSV_DISPATCH, [])
                        save_db(CSV_DISPATCH, dispatch_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": cart_df['Brand'].iloc[0], # Assuming single brand per cart for MVP
                            "Customer": c_name, "Items": items_str, "Total_Value": grand_total, 
                            "Status": "Pending", "Tracking_Num": ""
})

                        # WhatsApp Link
                        clean_phone = brand_data['phone'].replace("+", "").replace(" ", "")
                        msg = f"*{priority} DISPATCH*\n🆔 {oid}\n👤 {cust_name}\n📞 {cust_phone}\n🏠 {cust_addr}\n\n📦 CONTENTS:\n{items_txt}\n\n⚠️ Please confirm tracking."
                        url = f"https://wa.me/{clean_phone}?text={urllib.parse.quote(msg)}"
                        # 2. Save Financial Ledger (One row per brand per order)
                        finance_df = get_db(CSV_FINANCE, [])
                        # Group by brand if mixed cart (Advanced) - for now assuming single brand cart logic
                        save_db(CSV_FINANCE, finance_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": cart_df['Brand'].iloc[0],
                            "Total_Sale": grand_total, "Commission_Rate": cart_df['Comm_Rate'].iloc[0],
                            "Commission_Amt": total_comm, "Payable_To_Brand": total_payable,
                            "Status": "Unpaid"
                        })

                        st.success("✅ Order Logged!")
                        st.markdown(f"""
                        <a href="{url}" target="_blank" style="text-decoration:none;">
                            <div style="background:#25D366;color:white;padding:15px;border-radius:8px;text-align:center;font-weight:bold;">
                                📲 OPEN WHATSAPP
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                        # 3. Generate WhatsApp
                        brand_info = BRAND_CONTRACTS[cart_df['Brand'].iloc[0]]
                        phone_clean = brand_info['phone'].replace(" ","")
                        msg = f"*NEW ORDER {oid}*\nCust: {c_name}\nItems: {items_str}\nShip to: {c_addr}"
                        url = f"https://wa.me/{phone_clean}?text={urllib.parse.quote(msg)}"

                        st.success("✅ Order Logged to Dispatch & Finance Ledgers!")
                        st.markdown(f"[📲 Open WhatsApp]({url})")
st.session_state.cart = []
                        st.session_state.selected_brand_lock = None
else:
st.error("Missing Customer Details")
                
                if st.button("🗑️ Clear Cart"):
                        
                if st.button("Clear Cart"):
st.session_state.cart = []
                    st.session_state.selected_brand_lock = None
st.rerun()
else:
                st.info("Cart is empty.")
                st.info("Cart Empty")
st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: ACTIVE ORDERS ---
    with tab_orders:
        df = load_history()
        if not df.empty:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.dataframe(df.sort_values("Time", ascending=False), use_container_width=True, hide_index=True)
            st.markdown('</div>', unsafe_allow_html=True)
        # --- RECENT ORDERS TABLE ---
        st.markdown("### 🗂️ Recent Dispatch Log")
        hist = get_db(CSV_DISPATCH, [])
        if not hist.empty:
            st.dataframe(hist.sort_index(ascending=False).head(5), use_container_width=True)

    # ------------------------------------------------------------------------
    # TAB 2: FINANCIALS (The Commission Engine)
    # ------------------------------------------------------------------------
    with tabs[1]:
        st.markdown("### 💰 Financial Ledger")
        fin_df = get_db(CSV_FINANCE, ["Order_ID", "Brand", "Total_Sale", "Commission_Amt", "Payable_To_Brand"])
        
        if not fin_df.empty:
            # Metrics
            m1, m2, m3, m4 = st.columns(4)
            total_gmv = fin_df['Total_Sale'].sum()
            total_rev = fin_df['Commission_Amt'].sum()
            total_payable = fin_df['Payable_To_Brand'].sum()
            
            m1.metric("Total GMV", f"{total_gmv:,.0f} ₺")
            m2.metric("NATUVISIO Revenue", f"{total_rev:,.0f} ₺")
            m3.metric("Vendor Payables", f"{total_payable:,.0f} ₺")
            m4.metric("Margin", f"{(total_rev/total_gmv)*100:.1f}%")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Ledger Table
            st.dataframe(fin_df.sort_index(ascending=False), use_container_width=True)
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
            st.info("No financial records yet.")

    # ------------------------------------------------------------------------
    # TAB 3: VENDOR PAYOUTS (The Wallet)
    # ------------------------------------------------------------------------
    with tabs[2]:
        col_pay_L, col_pay_R = st.columns([1, 2])
        
        fin_df = get_db(CSV_FINANCE, [])
        payouts_df = get_db(CSV_PAYOUTS, [])
        
        with col_pay_L:
            st.markdown('<div class="glass-card"><h4>🏦 Make a Payout</h4>', unsafe_allow_html=True)
            
            pay_brand = st.selectbox("Select Vendor", list(BRAND_CONTRACTS.keys()))
            
            # Calculate Balance
            if not fin_df.empty:
                brand_sales = fin_df[fin_df['Brand'] == pay_brand]['Payable_To_Brand'].sum()
                brand_paid = payouts_df[payouts_df['Brand'] == pay_brand]['Amount'].sum() if not payouts_df.empty else 0
                balance = brand_sales - brand_paid
            else:
                balance = 0
            
            st.metric(f"Current Balance: {pay_brand}", f"{balance:,.2f} ₺")

            st.bar_chart(df['Brand'].value_counts())
            pay_amt = st.number_input("Payout Amount", min_value=0.0, max_value=float(balance), value=0.0)
            pay_method = st.selectbox("Method", ["Bank Transfer", "Cash", "Crypto"])
            pay_note = st.text_input("Reference / Note")
            
            if st.button("💸 Record Payout"):
                if pay_amt > 0:
                    pid = f"PAY-{datetime.now().strftime('%m%d%H%M')}"
                    save_db(CSV_PAYOUTS, payouts_df, {
                        "Payout_ID": pid, "Time": datetime.now(),
                        "Brand": pay_brand, "Amount": pay_amt,
                        "Method": pay_method, "Notes": pay_note
                    })
                    st.success("Payout Recorded!")
                    st.rerun()
                else:
                    st.error("Invalid Amount")
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_pay_R:
            st.markdown("### 📜 Payout History")
            if not payouts_df.empty:
                st.dataframe(payouts_df.sort_index(ascending=False), use_container_width=True)
            else:
                st.caption("No payouts recorded yet.")

    # ------------------------------------------------------------------------
    # TAB 4: INVOICING (Fatura)
    # ------------------------------------------------------------------------
    with tabs[3]:
        st.markdown("### 🧾 Commission Invoice Generator")
        st.caption("Use this data to issue official e-Fatura to your partners for your commission services.")
        
        sel_inv_brand = st.selectbox("Filter Brand", ["All"] + list(BRAND_CONTRACTS.keys()))
        
        if not fin_df.empty:
            filtered = fin_df if sel_inv_brand == "All" else fin_df[fin_df['Brand'] == sel_inv_brand]
            
            # Monthly Aggregation
            if not filtered.empty:
                filtered['Time'] = pd.to_datetime(filtered['Time'])
                filtered['Month'] = filtered['Time'].dt.strftime('%Y-%m')
                
                invoice_data = filtered.groupby(['Brand', 'Month'])['Commission_Amt'].sum().reset_index()
                invoice_data['KDV (20%)'] = invoice_data['Commission_Amt'] * 0.20
                invoice_data['Total Invoice'] = invoice_data['Commission_Amt'] * 1.20
                
                st.dataframe(invoice_data, use_container_width=True)
                
                st.download_button(
                    "📥 Download Invoice Data (CSV)",
                    invoice_data.to_csv(index=False),
                    "invoice_data.csv",
                    "text/csv"
                )
            else:
                st.info("No data for selected brand.")

    # ------------------------------------------------------------------------
    # TAB 5: REPORTS & TAXES
    # ------------------------------------------------------------------------
    with tabs[4]:
        st.markdown("### 📊 Executive Summary")
        
        if not fin_df.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="glass-card"><h5>Sales by Brand</h5>', unsafe_allow_html=True)
                st.bar_chart(fin_df.groupby("Brand")["Total_Sale"].sum())
                st.markdown('</div>', unsafe_allow_html=True)
                
            with c2:
                st.markdown('<div class="glass-card"><h5>Commissions Earned</h5>', unsafe_allow_html=True)
                st.bar_chart(fin_df.groupby("Brand")["Commission_Amt"].sum())
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("Gathering data...")

# ============================================================================
# 7. MAIN EXECUTION
# 6. EXECUTION
# ============================================================================

if not st.session_state.admin_logged_in:
