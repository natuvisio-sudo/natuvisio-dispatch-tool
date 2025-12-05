import os
from datetime import datetime, timedelta
import urllib.parse
import time

# ============================================================================
# 1. CONFIGURATION & SETUP
# 1. CONFIGURATION & ARCHITECTURE
# ============================================================================

st.set_page_config(
@@ -18,22 +19,44 @@
# Constants
ADMIN_PASS = "admin2025"
CSV_DISPATCH = "dispatch_history.csv"
CSV_FINANCE = "financial_ledger.csv" # NEW: Tracks money
CSV_PAYOUTS = "payout_history.csv"   # NEW: Tracks payments to brands
CSV_FINANCE = "financial_ledger.csv"
CSV_INVOICES = "invoice_registry.csv"  # NEW: Tracks generated invoices
CSV_PAYOUTS = "payout_history.csv"

# Design Constants
# Design Constants (Golden Ratio)
PHI = 1.618
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

# ----------------------------------------------------------------------------
# DATA MODELS
# ----------------------------------------------------------------------------

# BRAND CONTRACTS (The "Deal")
# Commission Rate: 0.15 = 15%
BRAND_CONTRACTS = {
    "HAKI HEAL": {"commission": 0.15, "phone": "601158976276", "color": "#4ECDC4"},
    "AURORACO": {"commission": 0.20, "phone": "601158976276", "color": "#FF6B6B"},
    "LONGEVICALS": {"commission": 0.12, "phone": "601158976276", "color": "#95E1D3"}
    "HAKI HEAL": {
        "commission": 0.15,
        "phone": "601158976276",
        "color": "#4ECDC4",
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "email": "finance@hakiheal.com"
    },
    "AURORACO": {
        "commission": 0.20,
        "phone": "601158976276",
        "color": "#FF6B6B",
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "email": "ops@auroraco.com"
    },
    "LONGEVICALS": {
        "commission": 0.12,
        "phone": "601158976276",
        "color": "#95E1D3",
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "email": "accounting@longevicals.com"
    }
}

# Product Database
# PRODUCT CATALOG
PRODUCT_DB = {
"HAKI HEAL": {
"HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM", "price": 450},
@@ -52,58 +75,113 @@
}

# ============================================================================
# 2. DESIGN SYSTEM
# 2. PREMIUM CSS & ANIMATION SYSTEM
# ============================================================================

st.markdown(f"""
<style>
   @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* BASE THEME */
   .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.95)), 
        background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), 
                         url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
       background-size: cover;
       background-attachment: fixed;
       font-family: 'Inter', sans-serif;
   }}

    /* GLASS CARDS */
   .glass-card {{
        background: rgba(255, 255, 255, 0.03);
        background: rgba(255, 255, 255, 0.04);
       backdrop-filter: blur(16px);
       border: 1px solid rgba(255, 255, 255, 0.08);
       border-radius: 16px;
       padding: {FIBO['md']}px;
       margin-bottom: {FIBO['sm']}px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
   }}

    /* TYPOGRAPHY */
   h1, h2, h3, h4 {{
       font-family: 'Space Grotesk', sans-serif !important;
       color: white !important;
       letter-spacing: -0.02em;
   }}
   
    .metric-value {{ font-family: 'Space Grotesk'; font-size: 24px; font-weight: 700; color: #fff; }}
    .metric-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.5); }}
    /* ANIMATIONS & ALERTS */
    @keyframes pulse-red {{
        0% {{ box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4); }}
        70% {{ box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }}
    }}
    
    .status-alert-red {{
        border-left: 4px solid #FF6B6B !important;
        animation: pulse-red 2s infinite;
    }}
   
    .status-paid {{ color: #4ECDC4; font-weight: bold; }}
    .status-pending {{ color: #FF6B6B; font-weight: bold; }}
    .status-alert-green {{
        border-left: 4px solid #4ECDC4 !important;
        transition: all 0.5s ease;
    }}

    /* BUTTONS & INPUTS */
    /* TIMELINE STEPS */
    .timeline-container {{
        display: flex;
        justify-content: space-between;
        margin: 20px 0;
        position: relative;
    }}
    .timeline-step {{
        text-align: center;
        font-size: 10px;
        color: rgba(255,255,255,0.5);
        position: relative;
        z-index: 2;
    }}
    .timeline-step.active {{
        color: #4ECDC4;
        font-weight: bold;
    }}
    .step-dot {{
        width: 12px;
        height: 12px;
        background: rgba(255,255,255,0.2);
        border-radius: 50%;
        margin: 0 auto 5px auto;
        border: 2px solid transparent;
    }}
    .timeline-step.active .step-dot {{
        background: #4ECDC4;
        box-shadow: 0 0 10px #4ECDC4;
    }}
    .timeline-line {{
        position: absolute;
        top: 6px;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(255,255,255,0.1);
        z-index: 1;
    }}

    /* CUSTOM INPUTS */
    .stTextInput>div>div>input {{ background: rgba(0,0,0,0.3) !important; color: white !important; border: 1px solid rgba(255,255,255,0.1) !important; }}
   div.stButton > button {{
       background: linear-gradient(135deg, #4ECDC4 0%, #2980B9 100%) !important;
       color: white !important;
       border: none !important;
       border-radius: 6px !important;
       font-weight: 600 !important;
   }}
    .stTextInput>div>div>input {{ background: rgba(255,255,255,0.05) !important; color: white !important; border: 1px solid rgba(255,255,255,0.1) !important; }}
   
   #MainMenu, header, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 3. DATABASE ENGINE
# 3. DATABASE ENGINE (UPDATED SCHEMAS)
# ============================================================================

def get_db(file, columns):
@@ -117,18 +195,31 @@
df.to_csv(file, index=False)
return df

# Initialize DBs if missing
if not os.path.exists(CSV_DISPATCH):
    save_db(CSV_DISPATCH, pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status", "Tracking_Num"]))

if not os.path.exists(CSV_FINANCE):
    save_db(CSV_FINANCE, pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate", "Commission_Amt", "Payable_To_Brand", "Status"]))
def update_db(file, df):
    df.to_csv(file, index=False)

if not os.path.exists(CSV_PAYOUTS):
    save_db(CSV_PAYOUTS, pd.DataFrame(columns=["Payout_ID", "Time", "Brand", "Amount", "Method", "Notes"]))
# INITIALIZE DATABASES WITH NEW COLUMNS
cols_dispatch = [
    "Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", 
    "Status", "Tracking_Num", "Notified", "Notified_Method"
]
cols_finance = [
    "Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate", 
    "Commission_Amt", "Payable_To_Brand", "Invoice_Ref", "Payment_Status"
]
cols_invoices = [
    "Invoice_Ref", "Date", "Brand", "Total_Commission", "KDV", "Total_Due", 
    "Sent_Status", "Paid_Status"
]
cols_payouts = ["Payout_ID", "Time", "Brand", "Amount", "Method", "Notes"]

if not os.path.exists(CSV_DISPATCH): save_db(CSV_DISPATCH, pd.DataFrame(columns=cols_dispatch))
if not os.path.exists(CSV_FINANCE): save_db(CSV_FINANCE, pd.DataFrame(columns=cols_finance))
if not os.path.exists(CSV_INVOICES): save_db(CSV_INVOICES, pd.DataFrame(columns=cols_invoices))
if not os.path.exists(CSV_PAYOUTS): save_db(CSV_PAYOUTS, pd.DataFrame(columns=cols_payouts))

# ============================================================================
# 4. AUTHENTICATION
# 4. AUTHENTICATION & LOGIN
# ============================================================================

if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False
@@ -137,18 +228,22 @@
st.markdown("<div style='height: 20vh'></div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
        st.markdown('<div class="glass-card" style="text-align:center;"><h3>🏔️ NATUVISIO ADMIN</h3><p>Financial & Logistics OS</p></div>', unsafe_allow_html=True)
        pwd = st.text_input("Access Key", type="password")
        if st.button("UNLOCK", use_container_width=True):
            if pwd == ADMIN_PASS:
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Access Denied")
        if st.button("EXIT"): st.switch_page("streamlit_app.py")
        st.markdown('<div class="glass-card" style="text-align:center;"><h3>🏔️ NATUVISIO ADMIN</h3><p>Secure Operations OS</p></div>', unsafe_allow_html=True)
        pwd = st.text_input("Admin Access Key", type="password")
        
        c_a, c_b = st.columns(2)
        with c_a:
            if st.button("UNLOCK SYSTEM", use_container_width=True):
                if pwd == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("Access Denied")
        with c_b:
            if st.button("EXIT", use_container_width=True): st.switch_page("streamlit_app.py")

# ============================================================================
# 5. CORE LOGIC BLOCKS
# 5. CORE SYSTEM LOGIC
# ============================================================================

def dashboard_screen():
@@ -163,264 +258,298 @@
if st.button("⬅️ Main Menu"): st.switch_page("streamlit_app.py")
st.markdown("---")

    # --- TABS ---
    tabs = st.tabs([
        "🚀 DISPATCH & ORDERS", 
        "💰 FINANCIALS", 
        "🏦 VENDOR PAYOUTS", 
        "🧾 INVOICING",
        "📊 REPORTS"
    ])
    tabs = st.tabs(["🚀 LOGISTICS & OPS", "🧾 INVOICING & COMMISSIONS", "🏦 PAYOUTS & AUDIT", "⚙️ CONTRACTS"])

# ------------------------------------------------------------------------
    # TAB 1: DISPATCH & ORDERS (The Physical Flow)
    # TAB 1: LOGISTICS & OPERATIONS (ORDER FLOW)
# ------------------------------------------------------------------------
with tabs[0]:
        col_L, col_R = st.columns([1.5, 1])
        st.markdown("### 📝 New Order Entry")

        # --- NEW ORDER FORM ---
        with col_L:
            st.markdown('<div class="glass-card"><h4>📝 New Order Entry</h4>', unsafe_allow_html=True)
            
        # --- NEW ORDER LOGIC ---
        with st.expander("➕ Create New Order", expanded=True):
            cL, cR = st.columns([1, 1])
if 'cart' not in st.session_state: st.session_state.cart = []

            # 1. Customer
            c_name = st.text_input("Customer Name")
            c_phone = st.text_input("Phone (905...)")
            c_addr = st.text_area("Address", height=60)
            with cL:
                c_name = st.text_input("Customer Name")
                c_phone = st.text_input("Phone")
                c_addr = st.text_area("Address", height=60)

            # 2. Cart
            st.markdown("---")
            sel_brand = st.selectbox("Brand Partner", list(BRAND_CONTRACTS.keys()))
            sel_prod = st.selectbox("Product", list(PRODUCT_DB[sel_brand].keys()))
            qty = st.number_input("Qty", 1, value=1)
            
            # Add to Cart Logic
            if st.button("➕ Add Line Item"):
                prod_data = PRODUCT_DB[sel_brand][sel_prod]
                line_total = prod_data['price'] * qty
                
                # COMMISSION LOGIC HAPPENS HERE
                comm_rate = BRAND_CONTRACTS[sel_brand]["commission"]
                comm_amt = line_total * comm_rate
                payable = line_total - comm_amt
            with cR:
                sel_brand = st.selectbox("Brand", list(BRAND_CONTRACTS.keys()))
                sel_prod = st.selectbox("Product", list(PRODUCT_DB[sel_brand].keys()))
                qty = st.number_input("Qty", 1, value=1)

                st.session_state.cart.append({
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
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # --- CART REVIEW & SUBMIT ---
        with col_R:
            st.markdown('<div class="glass-card"><h4>📦 Active Cart</h4>', unsafe_allow_html=True)
                if st.button("Add to Order"):
                    p_data = PRODUCT_DB[sel_brand][sel_prod]
                    rate = BRAND_CONTRACTS[sel_brand]["commission"]
                    total = p_data['price'] * qty
                    comm = total * rate
                    
                    st.session_state.cart.append({
                        "Brand": sel_brand, "Product": sel_prod, "Qty": qty,
                        "Total": total, "Comm": comm, "Payable": total - comm
                    })
                    st.rerun()

            # Cart Review
if st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df[["Product", "Qty", "Total"]], hide_index=True, use_container_width=True)
                
                grand_total = cart_df['Total'].sum()
                total_comm = cart_df['Comm_Amt'].sum()
                total_payable = cart_df['Payable'].sum()
                
                st.markdown(f"""
                <div style='background:rgba(255,255,255,0.1); padding:10px; border-radius:8px;'>
                    <div style='display:flex; justify-content:space-between;'><span>Order Total:</span><strong>{grand_total:,.2f} ₺</strong></div>
                    <div style='display:flex; justify-content:space-between; color:#4ECDC4;'><span>NATUVISIO Income:</span><strong>{total_comm:,.2f} ₺</strong></div>
                    <div style='display:flex; justify-content:space-between; color:#FF6B6B;'><span>Owed to Vendor:</span><strong>{total_payable:,.2f} ₺</strong></div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("⚡ CONFIRM ORDER & LOG FINANCE"):
                    if c_name and c_phone:
                        oid = f"NV-{datetime.now().strftime('%m%d%H%M')}"
                        
                        # 1. Save Dispatch Log
                        items_str = ", ".join([f"{x['Product']}(x{x['Qty']})" for x in st.session_state.cart])
                        dispatch_df = get_db(CSV_DISPATCH, [])
                        save_db(CSV_DISPATCH, dispatch_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": cart_df['Brand'].iloc[0], # Assuming single brand per cart for MVP
                            "Customer": c_name, "Items": items_str, "Total_Value": grand_total, 
                            "Status": "Pending", "Tracking_Num": ""
                        })
                        
                        # 2. Save Financial Ledger (One row per brand per order)
                        finance_df = get_db(CSV_FINANCE, [])
                        # Group by brand if mixed cart (Advanced) - for now assuming single brand cart logic
                        save_db(CSV_FINANCE, finance_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": cart_df['Brand'].iloc[0],
                            "Total_Sale": grand_total, "Commission_Rate": cart_df['Comm_Rate'].iloc[0],
                            "Commission_Amt": total_comm, "Payable_To_Brand": total_payable,
                            "Status": "Unpaid"
                        })
                        
                        # 3. Generate WhatsApp
                        brand_info = BRAND_CONTRACTS[cart_df['Brand'].iloc[0]]
                        phone_clean = brand_info['phone'].replace(" ","")
                        msg = f"*NEW ORDER {oid}*\nCust: {c_name}\nItems: {items_str}\nShip to: {c_addr}"
                        url = f"https://wa.me/{phone_clean}?text={urllib.parse.quote(msg)}"
                        
                        st.success("✅ Order Logged to Dispatch & Finance Ledgers!")
                        st.markdown(f"[📲 Open WhatsApp]({url})")
                        st.session_state.cart = []
                    else:
                        st.error("Missing Customer Details")
                        
                if st.button("Clear Cart"):
                st.dataframe(pd.DataFrame(st.session_state.cart))
                if st.button("⚡ CONFIRM ORDER & LOG"):
                    oid = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                    items = ", ".join([f"{x['Product']}(x{x['Qty']})" for x in st.session_state.cart])
                    brand_main = st.session_state.cart[0]['Brand'] # MVP: Single brand carts
                    totals = pd.DataFrame(st.session_state.cart).sum()
                    
                    # 1. Log Dispatch
                    d_df = get_db(CSV_DISPATCH, cols_dispatch)
                    d_new = {
                        "Order_ID": oid, "Time": datetime.now(), "Brand": brand_main,
                        "Customer": c_name, "Items": items, "Total_Value": totals['Total'],
                        "Status": "Order Received", "Tracking_Num": "", "Notified": "NO", "Notified_Method": ""
                    }
                    save_db(CSV_DISPATCH, d_df, d_new)
                    
                    # 2. Log Finance
                    f_df = get_db(CSV_FINANCE, cols_finance)
                    f_new = {
                        "Order_ID": oid, "Time": datetime.now(), "Brand": brand_main,
                        "Total_Sale": totals['Total'], "Commission_Rate": BRAND_CONTRACTS[brand_main]['commission'],
                        "Commission_Amt": totals['Comm'], "Payable_To_Brand": totals['Payable'],
                        "Invoice_Ref": "", "Payment_Status": "Pending"
                    }
                    save_db(CSV_FINANCE, f_df, f_new)
                    
                    st.success(f"Order {oid} Logged Successfully!")
st.session_state.cart = []
st.rerun()
            else:
                st.info("Cart Empty")
            st.markdown('</div>', unsafe_allow_html=True)

        # --- RECENT ORDERS TABLE ---
        st.markdown("### 🗂️ Recent Dispatch Log")
        hist = get_db(CSV_DISPATCH, [])
        if not hist.empty:
            st.dataframe(hist.sort_index(ascending=False).head(5), use_container_width=True)
        # --- LIVE OPS CONSOLE ---
        st.markdown("### 📡 Live Operations Console")
        ops_df = get_db(CSV_DISPATCH, cols_dispatch)
        
        if not ops_df.empty:
            ops_df = ops_df.sort_values("Time", ascending=False)
            
            for idx, row in ops_df.iterrows():
                # Define Glow Class based on status
                glow_class = "status-alert-red" if row['Notified'] == "NO" else "status-alert-green"
                
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card {glow_class}">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <h4 style="margin:0; color:#fff;">{row['Order_ID']} | {row['Brand']}</h4>
                                <small style="color:rgba(255,255,255,0.6)">{row['Customer']} • {row['Items']}</small>
                            </div>
                            <div style="text-align:right;">
                                <h4 style="margin:0;">{row['Total_Value']} TL</h4>
                                <small>{row['Time']}</small>
                            </div>
                        </div>
                        <hr style="border-color:rgba(255,255,255,0.1);">
                    """, unsafe_allow_html=True)
                    
                    # STATUS TIMELINE VISUALIZATION
                    steps = ["Order Received", "Brand Notified", "Dispatched", "Completed"]
                    current_step = row['Status']
                    
                    timeline_html = '<div class="timeline-container"><div class="timeline-line"></div>'
                    for step in steps:
                        active = "active" if step == current_step or steps.index(step) < steps.index(current_step) if current_step in steps else ""
                        timeline_html += f'<div class="timeline-step {active}"><div class="step-dot"></div>{step}</div>'
                    timeline_html += '</div>'
                    st.markdown(timeline_html, unsafe_allow_html=True)
                    
                    # ACTION CONTROLS
                    c1, c2, c3 = st.columns([1, 1, 2])
                    
                    # 1. Notification Tracker
                    with c1:
                        if row['Notified'] == "NO":
                            st.error("⚠️ BRAND NOT NOTIFIED")
                            if st.button("Mark Notified via WhatsApp", key=f"ntf_{idx}"):
                                ops_df.at[idx, 'Notified'] = "YES"
                                ops_df.at[idx, 'Notified_Method'] = "WhatsApp"
                                ops_df.at[idx, 'Status'] = "Brand Notified"
                                update_db(CSV_DISPATCH, ops_df)
                                st.rerun()
                        else:
                            st.success(f"✅ Notified ({row['Notified_Method']})")
                            
                    # 2. Dispatch Tracker
                    with c2:
                        if row['Status'] == "Brand Notified":
                            track_code = st.text_input("Tracking #", key=f"trk_{idx}")
                            if st.button("Confirm Dispatch", key=f"cfd_{idx}"):
                                ops_df.at[idx, 'Tracking_Num'] = track_code
                                ops_df.at[idx, 'Status'] = "Dispatched"
                                update_db(CSV_DISPATCH, ops_df)
                                st.rerun()
                        elif row['Status'] == "Dispatched":
                            st.info(f"🚚 Tracking: {row['Tracking_Num']}")
                            if st.button("Mark Delivered", key=f"dlv_{idx}"):
                                ops_df.at[idx, 'Status'] = "Completed"
                                update_db(CSV_DISPATCH, ops_df)
                                st.rerun()
                    
                    # 3. WhatsApp Deep Link
                    with c3:
                        phone = BRAND_CONTRACTS[row['Brand']]['phone']
                        msg = f"ORDER {row['Order_ID']}\nCust: {row['Customer']}\nItems: {row['Items']}\nShip to address provided."
                        link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                        st.markdown(f'<a href="{link}" target="_blank"><button style="width:100%; padding:10px; background:#25D366; border:none; border-radius:6px; color:white; font-weight:bold;">📲 Open WhatsApp</button></a>', unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------------------------------------
    # TAB 2: FINANCIALS (The Commission Engine)
    # TAB 2: INVOICING & COMMISSIONS
# ------------------------------------------------------------------------
with tabs[1]:
        st.markdown("### 💰 Financial Ledger")
        fin_df = get_db(CSV_FINANCE, ["Order_ID", "Brand", "Total_Sale", "Commission_Amt", "Payable_To_Brand"])
        st.markdown("### 🧾 Unified Invoice Engine")

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
        fin_df = get_db(CSV_FINANCE, cols_finance)
        
        # A. Uninvoiced Orders (Ready to Bill)
        st.markdown("#### 1. Pending Commissions (Uninvoiced)")
        pending_inv = fin_df[fin_df['Invoice_Ref'].isna() | (fin_df['Invoice_Ref'] == "")]
        
        if not pending_inv.empty:
            edited_inv = st.data_editor(
                pending_inv,
                column_config={
                    "Generate?": st.column_config.CheckboxColumn("Select", default=False)
                },
                disabled=["Order_ID", "Brand", "Commission_Amt"],
                hide_index=True,
                key="editor_inv"
            )

            # Ledger Table
            st.dataframe(fin_df.sort_index(ascending=False), use_container_width=True)
            # Invoice Generation Logic
            c_gen1, c_gen2 = st.columns(2)
            with c_gen1:
                target_brand = st.selectbox("Generate Invoice for:", list(BRAND_CONTRACTS.keys()))
            with c_gen2:
                if st.button("📄 GENERATE COMMISSION INVOICE"):
                    # Filter for selected brand and calculate
                    brand_items = pending_inv[pending_inv['Brand'] == target_brand]
                    if not brand_items.empty:
                        inv_ref = f"INV-{datetime.now().strftime('%Y%m')}-{target_brand[:3]}"
                        total_comm = brand_items['Commission_Amt'].sum()
                        kdv = total_comm * 0.20
                        
                        # 1. Create Invoice Record
                        inv_df = get_db(CSV_INVOICES, cols_invoices)
                        save_db(CSV_INVOICES, inv_df, {
                            "Invoice_Ref": inv_ref, "Date": datetime.now().date(),
                            "Brand": target_brand, "Total_Commission": total_comm,
                            "KDV": kdv, "Total_Due": total_comm + kdv,
                            "Sent_Status": "Pending", "Paid_Status": "Unpaid"
                        })
                        
                        # 2. Update Ledger
                        for idx in brand_items.index:
                            fin_df.at[idx, 'Invoice_Ref'] = inv_ref
                        update_db(CSV_FINANCE, fin_df)
                        
                        st.success(f"✅ Invoice {inv_ref} Generated for {total_comm:,.2f} TL")
                        st.rerun()
                    else:
                        st.warning("No pending items for this brand.")
else:
            st.info("No financial records yet.")
            st.info("All orders have been invoiced.")

        st.markdown("---")
        
        # B. Invoice Registry (Cross-Check)
        st.markdown("#### 2. Invoice Registry & Actions")
        inv_reg = get_db(CSV_INVOICES, cols_invoices)
        
        if not inv_reg.empty:
            for i, inv in inv_reg.iterrows():
                # Dynamic Coloring
                status_color = "#4ECDC4" if inv['Paid_Status'] == "Paid" else "#FF6B6B"
                
                with st.expander(f"📄 {inv['Invoice_Ref']} | {inv['Brand']} | {inv['Total_Due']:.2f} TL", expanded=False):
                    c1, c2, c3, c4 = st.columns(4)
                    c1.write(f"**Date:** {inv['Date']}")
                    c2.write(f"**Comm:** {inv['Total_Commission']:.2f}")
                    c3.write(f"**KDV:** {inv['KDV']:.2f}")
                    c4.markdown(f"<span style='color:{status_color}; font-weight:bold;'>{inv['Paid_Status']}</span>", unsafe_allow_html=True)
                    
                    # Action Buttons
                    a1, a2 = st.columns(2)
                    with a1:
                        if inv['Sent_Status'] == "Pending":
                            if st.button("📧 Mark Sent", key=f"sent_{i}"):
                                inv_reg.at[i, 'Sent_Status'] = "Sent"
                                update_db(CSV_INVOICES, inv_reg)
                                st.rerun()
                        else:
                            st.success("✅ Invoice Sent")
                            
                    with a2:
                        if inv['Paid_Status'] == "Unpaid":
                            if st.button("💰 Mark Paid", key=f"paid_{i}"):
                                inv_reg.at[i, 'Paid_Status'] = "Paid"
                                update_db(CSV_INVOICES, inv_reg)
                                st.rerun()

# ------------------------------------------------------------------------
    # TAB 3: VENDOR PAYOUTS (The Wallet)
    # TAB 3: PAYOUTS & AUDIT
# ------------------------------------------------------------------------
with tabs[2]:
col_pay_L, col_pay_R = st.columns([1, 2])
        
        fin_df = get_db(CSV_FINANCE, [])
        payouts_df = get_db(CSV_PAYOUTS, [])
        fin_df = get_db(CSV_FINANCE, cols_finance)
        pay_df = get_db(CSV_PAYOUTS, cols_payouts)

with col_pay_L:
            st.markdown('<div class="glass-card"><h4>🏦 Make a Payout</h4>', unsafe_allow_html=True)
            
            pay_brand = st.selectbox("Select Vendor", list(BRAND_CONTRACTS.keys()))
            st.markdown('<div class="glass-card"><h4>🏦 Vendor Payout Wallet</h4>', unsafe_allow_html=True)
            p_brand = st.selectbox("Vendor Wallet", list(BRAND_CONTRACTS.keys()))

            # Calculate Balance
            if not fin_df.empty:
                brand_sales = fin_df[fin_df['Brand'] == pay_brand]['Payable_To_Brand'].sum()
                brand_paid = payouts_df[payouts_df['Brand'] == pay_brand]['Amount'].sum() if not payouts_df.empty else 0
                balance = brand_sales - brand_paid
            else:
                balance = 0
            # Calculate Wallet Balance
            total_sales = fin_df[fin_df['Brand'] == p_brand]['Payable_To_Brand'].sum()
            total_paid = pay_df[pay_df['Brand'] == p_brand]['Amount'].sum()
            balance = total_sales - total_paid

            st.metric(f"Current Balance: {pay_brand}", f"{balance:,.2f} ₺")
            st.metric("Current Balance Owed", f"{balance:,.2f} TL")
            st.caption(f"Lifetime Sales: {total_sales:,.0f} TL | Paid: {total_paid:,.0f} TL")

            pay_amt = st.number_input("Payout Amount", min_value=0.0, max_value=float(balance), value=0.0)
            pay_method = st.selectbox("Method", ["Bank Transfer", "Cash", "Crypto"])
            pay_note = st.text_input("Reference / Note")
            amt = st.number_input("Payout Amount", min_value=0.0, max_value=float(balance) if balance > 0 else 0.0)
            method = st.selectbox("Method", ["Bank Transfer", "Crypto", "Cash"])
            ref = st.text_input("Reference Note")

if st.button("💸 Record Payout"):
                if pay_amt > 0:
                if amt > 0:
pid = f"PAY-{datetime.now().strftime('%m%d%H%M')}"
                    save_db(CSV_PAYOUTS, payouts_df, {
                        "Payout_ID": pid, "Time": datetime.now(),
                        "Brand": pay_brand, "Amount": pay_amt,
                        "Method": pay_method, "Notes": pay_note
                    save_db(CSV_PAYOUTS, pay_df, {
                        "Payout_ID": pid, "Time": datetime.now(), "Brand": p_brand,
                        "Amount": amt, "Method": method, "Notes": ref
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
            st.markdown("### 📜 Payout Audit Log")
            st.dataframe(pay_df.sort_values("Time", ascending=False), use_container_width=True)

# ------------------------------------------------------------------------
    # TAB 4: INVOICING (Fatura)
    # TAB 4: CONTRACTS & SETTINGS
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
        st.markdown("### ⚙️ Partner Configurations")
        for brand, data in BRAND_CONTRACTS.items():
            with st.expander(f"🔐 {brand} Contract Details"):
                st.json(data)

# ============================================================================
# 6. EXECUTION
# ============================================================================

if not st.session_state.admin_logged_in:
login_screen()
else:
dashboard_screen()
