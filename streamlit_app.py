import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse
import time

# ============================================================================
# 1. GLOBAL CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Bridge OS",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CONSTANTS & CREDENTIALS ---
ADMIN_PASS = "admin2025"
BRAND_CREDENTIALS = {
    "HAKI HEAL": "haki123",
    "AURORACO": "aurora2025",
    "LONGEVICALS": "longsci"
}

# --- DATABASE FILES ---
CSV_DISPATCH = "dispatch_history.csv"
CSV_FINANCE = "financial_ledger.csv"
CSV_INVOICES = "invoice_registry.csv"
CSV_PAYOUTS = "payout_history.csv"

# --- DESIGN CONSTANTS ---
PHI = 1.618
FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

# --- BUSINESS LOGIC MODELS ---
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
# 2. PREMIUM DESIGN SYSTEM (CSS)
# ============================================================================

def load_css():
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
            color: #ffffff;
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
        
        .metric-value {{ font-family: 'Space Grotesk'; font-size: 24px; font-weight: 700; color: #fff; }}
        .metric-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.5); }}
        
        /* ALERTS */
        @keyframes pulse-red {{
            0% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); }}
            70% {{ box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }}
        }}
        .status-alert-red {{ border-left: 4px solid #EF4444 !important; animation: pulse-red 2s infinite; }}
        .status-alert-green {{ border-left: 4px solid #10B981 !important; }}

        /* TIMELINE */
        .timeline-container {{ display: flex; justify-content: space-between; margin: 20px 0; position: relative; }}
        .timeline-line {{ position: absolute; top: 6px; left: 0; width: 100%; height: 2px; background: rgba(255,255,255,0.1); z-index: 0; }}
        .timeline-step {{ position: relative; z-index: 1; text-align: center; flex: 1; color: rgba(255,255,255,0.4); font-size: 10px; text-transform: uppercase; }}
        .timeline-dot {{ width: 12px; height: 12px; background: rgba(255,255,255,0.2); border-radius: 50%; margin: 0 auto 5px; border: 2px solid transparent; }}
        .timeline-step.active {{ color: #4ECDC4; font-weight: bold; }}
        .timeline-step.active .timeline-dot {{ background: #4ECDC4; box-shadow: 0 0 10px #4ECDC4; }}

        /* INPUTS & BUTTONS */
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

def get_icon(name, color="#ffffff"):
    icons = {
        "mountain": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 20L9 8L12 14L15 6L21 20H3Z"/><path d="M9 8L7 12"/></svg>',
        "box": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
        "truck": f'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="1" y="3" width="15" height="13"></rect><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"></polygon><circle cx="5.5" cy="18.5" r="2.5"></circle><circle cx="18.5" cy="18.5" r="2.5"></circle></svg>'
    }
    return icons.get(name, "")

# ============================================================================
# 3. DATABASE ENGINE (Unified)
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

# INITIALIZE LEDGERS
cols_dispatch = ["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status", "Tracking_Num", "Notified", "Notified_Method"]
cols_finance = ["Order_ID", "Time", "Brand", "Total_Sale", "Commission_Rate", "Commission_Amt", "Payable_To_Brand", "Invoice_Ref", "Payment_Status"]
cols_invoices = ["Invoice_Ref", "Date", "Brand", "Total_Commission", "KDV", "Total_Due", "Sent_Status", "Paid_Status"]
cols_payouts = ["Payout_ID", "Time", "Brand", "Amount", "Method", "Notes"]

for f, c in [(CSV_DISPATCH, cols_dispatch), (CSV_FINANCE, cols_finance), (CSV_INVOICES, cols_invoices), (CSV_PAYOUTS, cols_payouts)]:
    if not os.path.exists(f): save_db(f, pd.DataFrame(columns=c))

# ============================================================================
# 4. SESSION STATE MANAGEMENT
# ============================================================================

if 'page' not in st.session_state: st.session_state.page = 'login'
if 'user_role' not in st.session_state: st.session_state.user_role = None
if 'logged_brand' not in st.session_state: st.session_state.logged_brand = None
if 'cart' not in st.session_state: st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state: st.session_state.selected_brand_lock = None

# ============================================================================
# 5. VIEW: LOGIN SCREEN
# ============================================================================

def login_view():
    load_css()
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 40px; margin-bottom: 20px;">{get_icon('mountain', '#4ECDC4')}</div>
            <h2 style="margin-bottom: 10px;">NATUVISIO BRIDGE</h2>
            <p style="color: rgba(255,255,255,0.6); font-size: 12px; margin-bottom: 30px;">SECURE LOGISTICS OPERATING SYSTEM</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login Form
        role = st.selectbox("Select Role", ["Admin HQ", "Brand Partner"])
        
        if role == "Brand Partner":
            brand_user = st.selectbox("Select Brand", list(BRAND_CREDENTIALS.keys()))
        
        pwd = st.text_input("Access Key", type="password")
        
        if st.button("AUTHENTICATE", use_container_width=True):
            if role == "Admin HQ":
                if pwd == ADMIN_PASS:
                    st.session_state.user_role = 'ADMIN'
                    st.session_state.page = 'admin_dashboard'
                    st.rerun()
                else:
                    st.error("Invalid Admin Key")
            
            elif role == "Brand Partner":
                if pwd == BRAND_CREDENTIALS.get(brand_user):
                    st.session_state.user_role = 'PARTNER'
                    st.session_state.logged_brand = brand_user
                    st.session_state.page = 'partner_dashboard'
                    st.rerun()
                else:
                    st.error("Invalid Brand Key")

# ============================================================================
# 6. VIEW: ADMIN DASHBOARD
# ============================================================================

def admin_dashboard():
    load_css()
    
    # Header
    c1, c2 = st.columns([6,1])
    with c1: 
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:15px;">
            {get_icon('mountain', '#4ECDC4')}
            <div><h2 style="margin:0">ADMIN HQ</h2><span style="font-size:12px; opacity:0.7">COMMAND CENTER</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button("LOGOUT"):
            st.session_state.page = 'login'
            st.session_state.user_role = None
            st.rerun()
    
    st.markdown("---")
    
    # TABS
    tabs = st.tabs(["🚀 LOGISTICS", "🧾 INVOICING", "🏦 PAYOUTS", "📊 REPORTING"])

    # --- TAB 1: LOGISTICS ---
    with tabs[0]:
        cL, cR = st.columns([1.6, 1])
        
        # DISPATCH BUILDER
        with cL:
            st.markdown('<div class="glass-card"><h4>📝 New Order</h4>', unsafe_allow_html=True)
            cust_name = st.text_input("Customer Name")
            cust_phone = st.text_input("Phone (905...)")
            cust_addr = st.text_area("Address", height=60)
            st.markdown("---")
            
            if st.session_state.cart:
                act_brand = st.session_state.cart[0]['Brand']
                st.info(f"Locked to {act_brand}")
            else:
                act_brand = st.selectbox("Brand", list(BRAND_CONTRACTS.keys()))
            
            cp, cq = st.columns([3, 1])
            with cp: prod = st.selectbox("Product", list(PRODUCT_DB[act_brand].keys()))
            with cq: qty = st.number_input("Qty", 1, value=1)
            
            if st.button("➕ Add Item"):
                p_data = PRODUCT_DB[act_brand][prod]
                rate = BRAND_CONTRACTS[act_brand]["commission"]
                tot = p_data['price'] * qty
                comm = tot * rate
                st.session_state.cart.append({
                    "Brand": act_brand, "Product": prod, "Qty": qty, 
                    "Total": tot, "Comm": comm, "Payable": tot - comm
                })
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # MANIFEST
        with cR:
            st.markdown('<div class="glass-card"><h4>📦 Manifest</h4>', unsafe_allow_html=True)
            if st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df[["Product", "Qty", "Total"]], hide_index=True)
                
                total_val = cart_df['Total'].sum()
                total_comm = cart_df['Comm'].sum()
                
                st.markdown(f"<h2 style='text-align:right'>{total_val:,.0f} TL</h2>", unsafe_allow_html=True)
                st.caption(f"Commission: {total_comm:,.2f} TL")
                
                if st.button("⚡ FLASH DISPATCH"):
                    if cust_name and cust_phone:
                        oid = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                        items = ", ".join([f"{x['Product']} (x{x['Qty']})" for x in st.session_state.cart])
                        
                        # Save Physical
                        d_df = get_db(CSV_DISPATCH, cols_dispatch)
                        save_db(CSV_DISPATCH, d_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": act_brand,
                            "Customer": cust_name, "Items": items, "Total_Value": total_val,
                            "Status": "Order Received", "Tracking_Num": "", "Notified": "NO", "Notified_Method": ""
                        })
                        
                        # Save Financial
                        f_df = get_db(CSV_FINANCE, cols_finance)
                        save_db(CSV_FINANCE, f_df, {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": act_brand,
                            "Total_Sale": total_val, "Commission_Rate": BRAND_CONTRACTS[act_brand]['commission'],
                            "Commission_Amt": total_comm, "Payable_To_Brand": cart_df['Payable'].sum(),
                            "Invoice_Ref": "", "Payment_Status": "Unpaid"
                        })
                        
                        st.success(f"Order {oid} Logged!")
                        st.session_state.cart = []
                        st.rerun()
                    else:
                        st.error("Missing Customer Info")
                        
                if st.button("Clear Cart"):
                    st.session_state.cart = []
                    st.rerun()
            else:
                st.info("Cart Empty")
            st.markdown('</div>', unsafe_allow_html=True)

        # LIVE OPS LOG
        st.markdown("### 📡 Live Operations")
        ops_df = get_db(CSV_DISPATCH, cols_dispatch)
        if not ops_df.empty:
            ops_df = ops_df.sort_values("Time", ascending=False)
            for idx, row in ops_df.iterrows():
                glow = "status-alert-red" if row['Notified'] == "NO" else "status-alert-green"
                st.markdown(f"""<div class="glass-card {glow}">
                    <div style="display:flex; justify-content:space-between;">
                        <h4>{row['Order_ID']} | {row['Brand']}</h4>
                        <h4>{row['Total_Value']} TL</h4>
                    </div>
                    <small>{row['Customer']} • {row['Items']}</small>
                """, unsafe_allow_html=True)
                
                # Timeline
                steps = ["Order Received", "Brand Notified", "Dispatched", "Completed"]
                curr = row['Status']
                html = '<div class="timeline-container"><div class="timeline-line"></div>'
                for s in steps:
                    act = "active" if s == curr or (curr in steps and steps.index(s) < steps.index(curr)) else ""
                    html += f'<div class="timeline-step {act}"><div class="timeline-dot"></div>{s}</div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)
                
                # Controls
                c1, c2, c3 = st.columns(3)
                with c1:
                    if row['Notified'] == "NO":
                        if st.button("Mark Notified", key=f"ntf_{idx}"):
                            ops_df.at[idx, 'Notified'] = "YES"
                            ops_df.at[idx, 'Status'] = "Brand Notified"
                            update_db(CSV_DISPATCH, ops_df)
                            st.rerun()
                with c2:
                    if row['Status'] == "Brand Notified":
                        trk = st.text_input("Tracking #", key=f"trk_{idx}")
                        if st.button("Confirm Dispatch", key=f"dsp_{idx}"):
                            ops_df.at[idx, 'Tracking_Num'] = trk
                            ops_df.at[idx, 'Status'] = "Dispatched"
                            update_db(CSV_DISPATCH, ops_df)
                            st.rerun()
                with c3:
                    phone = BRAND_CONTRACTS[row['Brand']]['phone']
                    msg = f"ORDER {row['Order_ID']}\n{row['Items']}\n{row['Customer']}\nShip to address provided."
                    link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{link}" target="_blank"><button style="width:100%;background:#25D366;border:none;padding:10px;border-radius:5px;color:white;">WhatsApp</button></a>', unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 2: INVOICING ---
    with tabs[1]:
        st.markdown("### 🧾 Invoice Generation")
        fin_df = get_db(CSV_FINANCE, cols_finance)
        pending = fin_df[fin_df['Invoice_Ref'] == ""]
        
        if not pending.empty:
            st.dataframe(pending)
            c1, c2 = st.columns(2)
            with c1: t_brand = st.selectbox("Generate Invoice For", list(BRAND_CONTRACTS.keys()))
            with c2:
                if st.button("Generate Invoice"):
                    items = pending[pending['Brand'] == t_brand]
                    if not items.empty:
                        ref = f"INV-{datetime.now().strftime('%Y%m')}-{t_brand[:3]}"
                        comm = items['Commission_Amt'].sum()
                        kdv = comm * 0.20
                        inv_df = get_db(CSV_INVOICES, cols_invoices)
                        save_db(CSV_INVOICES, inv_df, {
                            "Invoice_Ref": ref, "Date": datetime.now().date(), "Brand": t_brand,
                            "Total_Commission": comm, "KDV": kdv, "Total_Due": comm + kdv,
                            "Sent_Status": "Pending", "Paid_Status": "Unpaid"
                        })
                        for i in items.index: fin_df.at[i, 'Invoice_Ref'] = ref
                        update_db(CSV_FINANCE, fin_df)
                        st.success(f"Generated {ref}")
                        st.rerun()
        else:
            st.info("No pending commissions.")
            
        st.markdown("#### Invoice History")
        inv_reg = get_db(CSV_INVOICES, cols_invoices)
        if not inv_reg.empty:
            st.dataframe(inv_reg)

    # --- TAB 3: PAYOUTS ---
    with tabs[2]:
        c1, c2 = st.columns([1, 2])
        fin_df = get_db(CSV_FINANCE, cols_finance)
        pay_df = get_db(CSV_PAYOUTS, cols_payouts)
        
        with c1:
            st.markdown('<div class="glass-card"><h4>🏦 Wallet</h4>', unsafe_allow_html=True)
            p_brand = st.selectbox("Vendor", list(BRAND_CONTRACTS.keys()))
            sales = fin_df[fin_df['Brand'] == p_brand]['Payable_To_Brand'].sum()
            paid = pay_df[pay_df['Brand'] == p_brand]['Amount'].sum()
            bal = sales - paid
            
            st.metric("Balance Due", f"{bal:,.2f} TL")
            st.caption(f"Sales: {sales:,.0f} | Paid: {paid:,.0f}")
            
            amt = st.number_input("Amount", 0.0, float(bal) if bal > 0 else 0.0)
            if st.button("Record Payout"):
                if amt > 0:
                    pid = f"PAY-{datetime.now().strftime('%m%d%H%M')}"
                    save_db(CSV_PAYOUTS, pay_df, {
                        "Payout_ID": pid, "Time": datetime.now(), "Brand": p_brand,
                        "Amount": amt, "Method": "Bank", "Notes": "Payout"
                    })
                    st.success("Recorded")
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        
        with c2:
            st.markdown("### History")
            st.dataframe(pay_df)

    # --- TAB 4: REPORTING ---
    with tabs[3]:
        df = get_db(CSV_DISPATCH, cols_dispatch)
        if not df.empty:
            st.bar_chart(df['Brand'].value_counts())

# ============================================================================
# 7. VIEW: PARTNER DASHBOARD
# ============================================================================

def partner_dashboard():
    load_css()
    brand = st.session_state.logged_brand
    
    # Header
    c1, c2 = st.columns([6,1])
    with c1: 
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:15px;">
            {get_icon('box', '#4ECDC4')}
            <div><h2 style="margin:0">{brand} PORTAL</h2><span style="font-size:12px; opacity:0.7">FULFILLMENT CENTER</span></div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        if st.button("LOGOUT"):
            st.session_state.page = 'login'
            st.session_state.user_role = None
            st.session_state.logged_brand = None
            st.rerun()
    
    st.markdown("---")
    
    df = get_db(CSV_DISPATCH, cols_dispatch)
    brand_df = df[df['Brand'] == brand].copy() if not df.empty else pd.DataFrame(columns=cols_dispatch)
    
    # FILTER PENDING
    pending = brand_df[brand_df['Status'].isin(['Order Received', 'Brand Notified', 'Pending'])]
    
    st.markdown("### 📋 Orders Awaiting Shipment")
    if not pending.empty:
        for idx, row in pending.iterrows():
            # Find original index to update main DB
            orig_idx = df[df['Order_ID'] == row['Order_ID']].index[0]
            
            with st.expander(f"🔔 {row['Order_ID']} | {row['Items']}", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.write(f"**Customer:** {row['Customer']}")
                    st.write(f"**Phone:** {row.get('Phone', 'N/A')}")
                with c2:
                    st.write(f"**Address:** {row.get('Address', 'N/A')}")
                
                # Tracking Input
                track = st.text_input("Enter Tracking Number", key=f"pt_trk_{idx}")
                if st.button("Confirm Shipment", key=f"pt_ship_{idx}"):
                    if track:
                        df.at[orig_idx, 'Tracking_Num'] = track
                        df.at[orig_idx, 'Status'] = 'Dispatched'
                        update_db(CSV_DISPATCH, df)
                        st.success("Shipped!")
                        st.rerun()
                    else:
                        st.error("Tracking required")
    else:
        st.success("No pending orders.")

# ============================================================================
# 8. MAIN EXECUTION ROUTER
# ============================================================================

def main():
    if st.session_state.page == 'login':
        login_view()
    elif st.session_state.page == 'admin_dashboard' and st.session_state.user_role == 'ADMIN':
        admin_dashboard()
    elif st.session_state.page == 'partner_dashboard' and st.session_state.user_role == 'PARTNER':
        partner_dashboard()
    else:
        # Fallback
        st.session_state.page = 'login'
        st.rerun()

if __name__ == "__main__":
    main()
