import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse
import time

# ============================================================================
# 1. CONFIGURATION & ARCHITECTURE
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Admin OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Constants
ADMIN_PASS = "admin2025"
CSV_DISPATCH = "dispatch_history.csv"
CSV_FINANCE = "financial_ledger.csv"
CSV_INVOICES = "invoice_registry.csv"  # NEW: Tracks generated invoices
CSV_PAYOUTS = "payout_history.csv"

# Design Constants (Golden Ratio)
PHI = 1.618
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

# ----------------------------------------------------------------------------
# DATA MODELS
# ----------------------------------------------------------------------------

# BRAND CONTRACTS (The "Deal")
BRAND_CONTRACTS = {
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

# PRODUCT CATALOG
PRODUCT_DB = {
    "HAKI HEAL": {
        "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM", "price": 450},
        "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY", "price": 380},
        "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP", "price": 120}
    },
    "AURORACO": {
        "AURORACO MATCHA": {"sku": "SKU-AUR-MATCHA", "price": 650},
        "AURORACO CACAO": {"sku": "SKU-AUR-CACAO", "price": 550},
        "AURORACO SUPER": {"sku": "SKU-AUR-SUPER", "price": 800}
    },
    "LONGEVICALS": {
        "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
        "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
    }
}

# ============================================================================
# 2. PREMIUM CSS & ANIMATION SYSTEM
# ============================================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');

    /* BASE THEME */
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.85), rgba(15, 23, 42, 0.95)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }}

    /* GLASS CARDS */
    .glass-card {{
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
    
    .status-alert-green {{
        border-left: 4px solid #4ECDC4 !important;
        transition: all 0.5s ease;
    }}

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
    
    #MainMenu, header, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 3. DATABASE ENGINE (UPDATED SCHEMAS)
# ============================================================================

def get_db(file, columns):
    if os.path.exists(file): return pd.read_csv(file)
    return pd.DataFrame(columns=columns)

def save_db(file, df, new_row=None):
    if new_row is not None:
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(file, index=False)
    return df

def update_db(file, df):
    df.to_csv(file, index=False)

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
# 4. AUTHENTICATION & LOGIN
# ============================================================================

if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False

def login_screen():
    st.markdown("<div style='height: 20vh'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
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
# 5. CORE SYSTEM LOGIC
# ============================================================================

def dashboard_screen():
    # --- HEADER ---
    c1, c2 = st.columns([6,1])
    with c1: st.markdown("## 🏔️ COMMAND CENTER")
    with c2: 
        if st.button("LOGOUT"):
            st.session_state.admin_logged_in = False
            st.switch_page("streamlit_app.py")
    
    if st.button("⬅️ Main Menu"): st.switch_page("streamlit_app.py")
    st.markdown("---")

    tabs = st.tabs(["🚀 LOGISTICS & OPS", "🧾 INVOICING & COMMISSIONS", "🏦 PAYOUTS & AUDIT", "⚙️ CONTRACTS"])

    # ------------------------------------------------------------------------
    # TAB 1: LOGISTICS & OPERATIONS (ORDER FLOW)
    # ------------------------------------------------------------------------
    with tabs[0]:
        st.markdown("### 📝 New Order Entry")
        
        # --- NEW ORDER LOGIC ---
        with st.expander("➕ Create New Order", expanded=True):
            cL, cR = st.columns([1, 1])
            if 'cart' not in st.session_state: st.session_state.cart = []
            
            with cL:
                c_name = st.text_input("Customer Name")
                c_phone = st.text_input("Phone")
                c_addr = st.text_area("Address", height=60)
            
            with cR:
                sel_brand = st.selectbox("Brand", list(BRAND_CONTRACTS.keys()))
                sel_prod = st.selectbox("Product", list(PRODUCT_DB[sel_brand].keys()))
                qty = st.number_input("Qty", 1, value=1)
                
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
    # TAB 2: INVOICING & COMMISSIONS
    # ------------------------------------------------------------------------
    with tabs[1]:
        st.markdown("### 🧾 Unified Invoice Engine")
        
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
    # TAB 3: PAYOUTS & AUDIT
    # ------------------------------------------------------------------------
    with tabs[2]:
        col_pay_L, col_pay_R = st.columns([1, 2])
        fin_df = get_db(CSV_FINANCE, cols_finance)
        pay_df = get_db(CSV_PAYOUTS, cols_payouts)
        
        with col_pay_L:
            st.markdown('<div class="glass-card"><h4>🏦 Vendor Payout Wallet</h4>', unsafe_allow_html=True)
            p_brand = st.selectbox("Vendor Wallet", list(BRAND_CONTRACTS.keys()))
            
            # Calculate Wallet Balance
            total_sales = fin_df[fin_df['Brand'] == p_brand]['Payable_To_Brand'].sum()
            total_paid = pay_df[pay_df['Brand'] == p_brand]['Amount'].sum()
            balance = total_sales - total_paid
            
            st.metric("Current Balance Owed", f"{balance:,.2f} TL")
            st.caption(f"Lifetime Sales: {total_sales:,.0f} TL | Paid: {total_paid:,.0f} TL")
            
            amt = st.number_input("Payout Amount", min_value=0.0, max_value=float(balance) if balance > 0 else 0.0)
            method = st.selectbox("Method", ["Bank Transfer", "Crypto", "Cash"])
            ref = st.text_input("Reference Note")
            
            if st.button("💸 Record Payout"):
                if amt > 0:
                    pid = f"PAY-{datetime.now().strftime('%m%d%H%M')}"
                    save_db(CSV_PAYOUTS, pay_df, {
                        "Payout_ID": pid, "Time": datetime.now(), "Brand": p_brand,
                        "Amount": amt, "Method": method, "Notes": ref
                    })
                    st.success("Payout Recorded!")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with col_pay_R:
            st.markdown("### 📜 Payout Audit Log")
            st.dataframe(pay_df.sort_values("Time", ascending=False), use_container_width=True)

    # ------------------------------------------------------------------------
    # TAB 4: CONTRACTS & SETTINGS
    # ------------------------------------------------------------------------
    with tabs[3]:
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
