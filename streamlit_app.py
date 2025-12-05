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
CSV_INVOICES = "invoice_registry.csv"
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

def get_icon(name, color="#ffffff"):
    icons = {
        "mountain": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 20L9 8L12 14L15 6L21 20H3Z"/><path d="M9 8L7 12"/></svg>',
        "box": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
        "truck": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>',
        "chart": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "whatsapp": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>'
    }
    return icons.get(name, "")

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
    h1, h2, h3, h4, h5 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: white !important;
        letter-spacing: -0.02em;
    }}
    
    .metric-value {{ font-family: 'Space Grotesk'; font-size: 24px; font-weight: 700; color: #fff; }}
    .metric-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.5); }}
    
    /* ANIMATIONS */
    @keyframes pulse-red {{
        0% {{ box-shadow: 0 0 0 0 rgba(255, 107, 107, 0.4); }}
        70% {{ box-shadow: 0 0 0 10px rgba(255, 107, 107, 0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(255, 107, 107, 0); }}
    }}
    .status-alert-red {{ border-left: 4px solid #FF6B6B !important; animation: pulse-red 2s infinite; }}
    .status-alert-green {{ border-left: 4px solid #4ECDC4 !important; }}

    /* TIMELINE */
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
        flex: 1;
    }}
    .timeline-step.active {{ color: #4ECDC4; font-weight: bold; }}
    .step-dot {{
        width: 12px; height: 12px; background: rgba(255,255,255,0.2);
        border-radius: 50%; margin: 0 auto 5px auto; border: 2px solid transparent;
    }}
    .timeline-step.active .step-dot {{ background: #4ECDC4; box-shadow: 0 0 10px #4ECDC4; }}
    .timeline-line {{
        position: absolute; top: 6px; left: 0; width: 100%; height: 2px; background: rgba(255,255,255,0.1); z-index: 1;
    }}

    /* INPUTS & BUTTONS */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stNumberInput>div>div>input {{ 
        background: rgba(0,0,0,0.3) !important; 
        color: white !important; 
        border: 1px solid rgba(255,255,255,0.1) !important; 
        border-radius: 8px !important;
    }}
    div.stButton > button {{
        background: linear-gradient(135deg, #4ECDC4 0%, #2980B9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    #MainMenu, header, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 3. DATABASE ENGINE
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

# INITIALIZE DATABASES
cols_dispatch = ["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status", "Tracking_Num", "Notified", "Notified_Method"]
cols_finance = ["Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate", "Commission_Amt", "Payable_To_Brand", "Invoice_Ref", "Payment_Status"]
cols_invoices = ["Invoice_Ref", "Date", "Brand", "Total_Commission", "KDV", "Total_Due", "Sent_Status", "Paid_Status"]
cols_payouts = ["Payout_ID", "Time", "Brand", "Amount", "Method", "Notes"]

if not os.path.exists(CSV_DISPATCH): save_db(CSV_DISPATCH, pd.DataFrame(columns=cols_dispatch))
if not os.path.exists(CSV_FINANCE): save_db(CSV_FINANCE, pd.DataFrame(columns=cols_finance))
if not os.path.exists(CSV_INVOICES): save_db(CSV_INVOICES, pd.DataFrame(columns=cols_invoices))
if not os.path.exists(CSV_PAYOUTS): save_db(CSV_PAYOUTS, pd.DataFrame(columns=cols_payouts))

# ============================================================================
# 4. AUTHENTICATION
# ============================================================================

if 'admin_logged_in' not in st.session_state: st.session_state.admin_logged_in = False

def login_screen():
    st.markdown("<div style='height: 20vh'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        st.markdown(f"""
        <div class="glass-card" style="text-align:center;">
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
            if st.button("EXIT", use_container_width=True): st.switch_page("streamlit_app.py")

# ============================================================================
# 5. CORE SYSTEM LOGIC
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
    tabs = st.tabs(["🚀 LOGISTICS & OPS", "🧾 FINANCIALS", "🏦 PAYOUTS", "⚙️ SETTINGS"])

    # ------------------------------------------------------------------------
    # TAB 1: LOGISTICS (Original Dispatch + Cart Logic)
    # ------------------------------------------------------------------------
    with tabs[0]:
        col_L, col_R = st.columns([1.618, 1])
        
        with col_L:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 👤 Customer Identity")
            if 'cart' not in st.session_state: st.session_state.cart = []
            if 'selected_brand_lock' not in st.session_state: st.session_state.selected_brand_lock = None
            
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
                active_brand = st.selectbox("Select Partner", list(BRAND_CONTRACTS.keys()))

            # Use Combined Logic for Products
            if active_brand in PRODUCT_DB:
                prod_list = list(PRODUCT_DB[active_brand].keys())
                
                cp, cq = st.columns([3, 1])
                with cp: prod = st.selectbox("Product", prod_list)
                with cq: qty = st.number_input("Qty", 1, value=1)
                
                p_data = PRODUCT_DB[active_brand][prod]
                
                if st.button("➕ ADD TO CART", use_container_width=True):
                    # Calculate Commissions Here
                    comm_rate = BRAND_CONTRACTS[active_brand]["commission"]
                    line_total = p_data['price'] * qty
                    comm_amt = line_total * comm_rate
                    
                    st.session_state.cart.append({
                        "brand": active_brand,
                        "product": prod,
                        "sku": p_data['sku'],
                        "qty": qty,
                        "subtotal": line_total,
                        "comm_amt": comm_amt,
                        "payable": line_total - comm_amt
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
                        
                        # 1. Save Dispatch
                        d_df = get_db(CSV_DISPATCH, cols_dispatch)
                        d_new = {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": active_brand,
                            "Customer": cust_name, "Items": items_txt.replace("\n", ", "),
                            "Total_Value": total, "Status": "Pending", "Tracking_Num": "",
                            "Notified": "NO", "Notified_Method": ""
                        }
                        save_db(CSV_DISPATCH, d_df, d_new)
                        
                        # 2. Save Finance
                        f_df = get_db(CSV_FINANCE, cols_finance)
                        total_comm = df_cart['comm_amt'].sum()
                        total_pay = df_cart['payable'].sum()
                        f_new = {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": active_brand,
                            "Total_Sale": total, "Commission_Rate": BRAND_CONTRACTS[active_brand]['commission'],
                            "Commission_Amt": total_comm, "Payable_To_Brand": total_pay,
                            "Invoice_Ref": "", "Payment_Status": "Unpaid"
                        }
                        save_db(CSV_FINANCE, f_df, f_new)
                        
                        # WhatsApp Link
                        clean_phone = BRAND_CONTRACTS[active_brand]['phone'].replace("+", "").replace(" ", "")
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
                    
                    # TIMELINE VISUALIZATION
                    steps = ["Pending", "Brand Notified", "Dispatched", "Completed"]
                    current_step = row['Status'] if row['Status'] in steps else "Pending"
                    
                    timeline_html = '<div class="timeline-container"><div class="timeline-line"></div>'
                    for step in steps:
                        # Determine active state
                        is_active = False
                        if step == current_step:
                            is_active = True
                        elif current_step in steps and steps.index(step) < steps.index(current_step):
                            is_active = True
                            
                        active_class = "active" if is_active else ""
                        timeline_html += f'<div class="timeline-step {active_class}"><div class="step-dot"></div>{step}</div>'
                    timeline_html += '</div>'
                    st.markdown(timeline_html, unsafe_allow_html=True)
                    
                    # ACTION CONTROLS
                    c1, c2 = st.columns(2)
                    
                    with c1:
                        if row['Notified'] == "NO":
                            if st.button("Mark Notified", key=f"ntf_{idx}"):
                                ops_df.at[idx, 'Notified'] = "YES"
                                ops_df.at[idx, 'Notified_Method'] = "WhatsApp"
                                ops_df.at[idx, 'Status'] = "Brand Notified"
                                update_db(CSV_DISPATCH, ops_df)
                                st.rerun()
                        elif row['Status'] == "Brand Notified":
                            track_code = st.text_input("Tracking #", key=f"trk_{idx}")
                            if st.button("Confirm Dispatch", key=f"cfd_{idx}"):
                                ops_df.at[idx, 'Tracking_Num'] = track_code
                                ops_df.at[idx, 'Status'] = "Dispatched"
                                update_db(CSV_DISPATCH, ops_df)
                                st.rerun()
                    
                    with c2:
                        if row['Status'] == "Dispatched":
                            if st.button("Mark Completed", key=f"dlv_{idx}"):
                                ops_df.at[idx, 'Status'] = "Completed"
                                update_db(CSV_DISPATCH, ops_df)
                                st.rerun()
                    
                    st.markdown("</div>", unsafe_allow_html=True)

    # ------------------------------------------------------------------------
    # TAB 2: FINANCIALS (Commissions & Invoicing)
    # ------------------------------------------------------------------------
    with tabs[1]:
        st.markdown("### 🧾 Unified Invoice Engine")
        
        fin_df = get_db(CSV_FINANCE, cols_finance)
        
        # A. Uninvoiced Orders (Ready to Bill)
        st.markdown("#### 1. Pending Commissions (Uninvoiced)")
        pending_inv = fin_df[fin_df['Invoice_Ref'].isna() | (fin_df['Invoice_Ref'] == "")]
        
        if not pending_inv.empty:
            st.dataframe(pending_inv, use_container_width=True)
            
            c1, c2 = st.columns(2)
            with c1: target_brand = st.selectbox("Generate Invoice for:", list(BRAND_CONTRACTS.keys()))
            with c2: 
                if st.button("📄 GENERATE INVOICE"):
                    brand_items = pending_inv[pending_inv['Brand'] == target_brand]
                    if not brand_items.empty:
                        inv_ref = f"INV-{datetime.now().strftime('%Y%m')}-{target_brand[:3]}"
                        total = brand_items['Commission_Amt'].sum()
                        kdv = total * 0.20
                        
                        inv_df = get_db(CSV_INVOICES, cols_invoices)
                        save_db(CSV_INVOICES, inv_df, {
                            "Invoice_Ref": inv_ref, "Date": datetime.now().date(), "Brand": target_brand,
                            "Total_Commission": total, "KDV": kdv, "Total_Due": total + kdv,
                            "Sent_Status": "Pending", "Paid_Status": "Unpaid"
                        })
                        
                        for i in brand_items.index: fin_df.at[i, 'Invoice_Ref'] = inv_ref
                        update_db(CSV_FINANCE, fin_df)
                        
                        st.success(f"Invoice {inv_ref} Generated!")
                        st.rerun()
        else:
            st.info("No pending commissions to invoice.")

        st.markdown("---")
        
        # B. Invoice Registry
        st.markdown("#### 2. Invoice Registry")
        inv_reg = get_db(CSV_INVOICES, cols_invoices)
        if not inv_reg.empty:
            st.dataframe(inv_reg, use_container_width=True)

    # ------------------------------------------------------------------------
    # TAB 3: PAYOUTS
    # ------------------------------------------------------------------------
    with tabs[2]:
        cL, cR = st.columns([1, 2])
        fin_df = get_db(CSV_FINANCE, cols_finance)
        pay_df = get_db(CSV_PAYOUTS, cols_payouts)
        
        with cL:
            st.markdown('<div class="glass-card"><h4>🏦 Vendor Payouts</h4>', unsafe_allow_html=True)
            p_brand = st.selectbox("Vendor", list(BRAND_CONTRACTS.keys()))
            
            total_sales = fin_df[fin_df['Brand'] == p_brand]['Payable_To_Brand'].sum()
            total_paid = pay_df[pay_df['Brand'] == p_brand]['Amount'].sum()
            bal = total_sales - total_paid
            
            st.metric("Balance Owed", f"{bal:,.2f} TL")
            
            amt = st.number_input("Payout Amount", 0.0, float(bal) if bal>0 else 0.0)
            if st.button("Record Payout"):
                if amt > 0:
                    pid = f"PAY-{datetime.now().strftime('%m%d%H%M')}"
                    save_db(CSV_PAYOUTS, pay_df, {
                        "Payout_ID": pid, "Time": datetime.now(), "Brand": p_brand,
                        "Amount": amt, "Method": "Bank", "Notes": "Standard Payout"
                    })
                    st.success("Recorded")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with cR:
            st.markdown("### 📜 Payout Log")
            st.dataframe(pay_df, use_container_width=True)

    # ------------------------------------------------------------------------
    # TAB 4: SETTINGS
    # ------------------------------------------------------------------------
    with tabs[3]:
        st.markdown("### ⚙️ Partner Configurations")
        for b, d in BRAND_CONTRACTS.items():
            with st.expander(f"🔐 {b}"): st.json(d)

# ============================================================================
# 6. MAIN EXECUTION
# ============================================================================

if not st.session_state.admin_logged_in:
    login_screen()
else:
    dashboard_screen()
