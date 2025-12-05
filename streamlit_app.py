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
# 2. PREMIUM ASSETS (SVG Icons)
# ============================================================================

def get_icon(name, color="#ffffff", size=24):
    icons = {
        "mountain": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M3 20L9 8L12 14L15 6L21 20H3Z"/><path d="M9 8L7 12"/></svg>',
        "box": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
        "truck": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="1" y="3" width="15" height="13"/><polygon points="16 8 20 8 23 11 23 16 16 16 16 8"/><circle cx="5.5" cy="18.5" r="2.5"/><circle cx="18.5" cy="18.5" r="2.5"/></svg>',
        "chart": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>',
        "whatsapp": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>',
        "money": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="3"/></svg>',
        "check": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3"><path d="M20 6L9 17L4 12"/></svg>',
        "alert": f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><circle cx="12" cy="16" r="0.5" fill="{color}"/></svg>'
    }
    return icons.get(name, "")

# ============================================================================
# 3. PREMIUM CSS
# ============================================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* BASE THEME */
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.92)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Inter', sans-serif;
        color: #ffffff;
    }}
    
    .main {{ padding: {FIBO['md']}px; }}
    .block-container {{ padding-top: {FIBO['md']}px !important; max-width: 100% !important; }}

    /* GLASS CARDS */
    .glass-card {{
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur({FIBO['md']}px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: {FIBO['sm']}px;
        padding: {FIBO['md']}px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: {FIBO['sm']}px;
    }}

    /* ALERTS */
    @keyframes pulse-red {{ 0% {{ box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }} 50% {{ box-shadow: 0 0 40px rgba(239, 68, 68, 0.5); }} }}
    .status-alert-red {{ border-left: 4px solid #EF4444; animation: pulse-red 2s infinite; }}
    .status-alert-green {{ border-left: 4px solid #10B981; }}

    /* TIMELINE */
    .timeline-container {{ display: flex; justify-content: space-between; position: relative; margin: 20px 0; }}
    .timeline-line {{ position: absolute; top: 6px; left: 0; width: 100%; height: 2px; background: rgba(255, 255, 255, 0.1); z-index: 0; }}
    .timeline-step {{ position: relative; z-index: 1; text-align: center; flex: 1; }}
    .timeline-dot {{ width: 12px; height: 12px; background: rgba(255, 255, 255, 0.2); border-radius: 50%; margin: 0 auto 5px; border: 2px solid transparent; }}
    .timeline-step.active .timeline-dot {{ background: #4ECDC4; box-shadow: 0 0 10px #4ECDC4; }}
    .timeline-step-label {{ font-size: 10px; color: rgba(255, 255, 255, 0.5); text-transform: uppercase; }}
    .timeline-step.active .timeline-step-label {{ color: #4ECDC4; font-weight: 700; }}

    /* TYPOGRAPHY */
    h1, h2, h3, h4, h5 {{ font-family: 'Space Grotesk', sans-serif !important; color: #ffffff !important; letter-spacing: -0.02em; }}
    .metric-value {{ font-family: 'Space Grotesk'; font-size: {FIBO['lg']}px; font-weight: 800; color: #ffffff; margin-bottom: 8px; }}
    .metric-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 1px; color: rgba(255, 255, 255, 0.6); }}

    /* INPUTS & BUTTONS */
    .stTextInput > div > div > input, .stSelectbox > div > div > select, .stNumberInput > div > div > input {{
        background: rgba(0, 0, 0, 0.3) !important; border: 1px solid rgba(255, 255, 255, 0.15) !important; color: white !important; border-radius: 8px !important;
    }}
    div.stButton > button {{
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%) !important; color: white !important; border: none !important;
        border-radius: 8px !important; font-weight: 600 !important; text-transform: uppercase !important; width: 100% !important;
    }}
    
    #MainMenu, header, footer {{ visibility: hidden; }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 4. DATABASE ENGINE
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
# 5. AUTHENTICATION
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
        
        pwd = st.text_input("Access Key", type="password", label_visibility="collapsed")
        c_a, c_b = st.columns(2)
        with c_a:
            if st.button("UNLOCK", use_container_width=True):
                if pwd == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("ACCESS DENIED")
        with c_b:
            if st.button("EXIT", use_container_width=True): st.switch_page("streamlit_app.py")

# ============================================================================
# 6. DASHBOARD
# ============================================================================

def dashboard_screen():
    # Header
    col_h1, col_h2 = st.columns([6, 1])
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: {FIBO['sm']}px;">
            {get_icon('mountain', '#4ECDC4', FIBO['lg'])}
            <div>
                <h1 style="margin: 0; font-size: {FIBO['xl']}px;">ADMIN HQ</h1>
                <span style="font-size: 12px; color: rgba(255, 255, 255, 0.6); letter-spacing: 0.1em;">LOGISTICS COMMAND CENTER</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_h2:
        if st.button("🚪 LOGOUT"):
            st.session_state.admin_logged_in = False
            st.session_state.cart = []
            st.rerun()

    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)

    # Metrics
    df = get_db(CSV_DISPATCH, cols_dispatch)
    fin_df = get_db(CSV_FINANCE, cols_finance)
    
    total_rev = fin_df['Commission_Amt'].sum() if not fin_df.empty else 0
    pending_ship = len(df[df['Status'] == 'Order Received']) if not df.empty else 0
    today_ct = len(df[pd.to_datetime(df['Time']).dt.date == datetime.now().date()]) if not df.empty else 0

    m1, m2, m3, m4 = st.columns(4)
    with m1: st.markdown(f"""<div class="glass-card"><div class="metric-value">{len(df)}</div><div class="metric-label">TOTAL ORDERS</div></div>""", unsafe_allow_html=True)
    with m2: st.markdown(f"""<div class="glass-card"><div class="metric-value">{total_rev:,.0f}₺</div><div class="metric-label">NET REVENUE</div></div>""", unsafe_allow_html=True)
    with m3: st.markdown(f"""<div class="glass-card" style="border-top: 3px solid #EF4444;"><div class="metric-value">{pending_ship}</div><div class="metric-label">PENDING ACTION</div></div>""", unsafe_allow_html=True)
    with m4: st.markdown(f"""<div class="glass-card"><div class="metric-value">{today_ct}</div><div class="metric-label">TODAY</div></div>""", unsafe_allow_html=True)

    st.markdown("---")

    tabs = st.tabs(["🚀 DISPATCH", "✅ PROCESSING", "📦 ALL ORDERS", "💰 FINANCIALS", "💳 PAYMENTS", "📈 ANALYTICS"])

    # --- TAB 1: NEW DISPATCH ---
    with tabs[0]:
        col_L, col_R = st.columns([1.618, 1])
        
        with col_L:
            st.markdown('<div class="glass-card"><h4>👤 Customer</h4>', unsafe_allow_html=True)
            if 'cart' not in st.session_state: st.session_state.cart = []
            
            c_name = st.text_input("Name")
            c_phone = st.text_input("Phone")
            c_addr = st.text_area("Address")
            st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="glass-card"><h4>🛒 Products</h4>', unsafe_allow_html=True)
            if st.session_state.cart:
                active_brand = st.session_state.cart[0]['Brand']
                st.info(f"Locked to {active_brand}")
            else:
                active_brand = st.selectbox("Brand", list(BRAND_CONTRACTS.keys()))
            
            prod_list = list(PRODUCT_DB[active_brand].keys())
            cp, cq = st.columns([3, 1])
            with cp: prod = st.selectbox("Item", prod_list)
            with cq: qty = st.number_input("Qty", 1, value=1)
            
            if st.button("➕ Add Item"):
                p_data = PRODUCT_DB[active_brand][prod]
                rate = BRAND_CONTRACTS[active_brand]["commission"]
                total = p_data['price'] * qty
                comm = total * rate
                st.session_state.cart.append({
                    "Brand": active_brand, "Product": prod, "SKU": p_data['sku'],
                    "Qty": qty, "Total": total, "Comm": comm, "Payable": total - comm
                })
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        with col_R:
            st.markdown('<div class="glass-card"><h4>📦 Manifest</h4>', unsafe_allow_html=True)
            if st.session_state.cart:
                cart_df = pd.DataFrame(st.session_state.cart)
                st.dataframe(cart_df[["Product", "Qty", "Total"]], use_container_width=True, hide_index=True)
                
                total_val = cart_df['Total'].sum()
                st.markdown(f"<h2 style='text-align:right;'>{total_val:,.0f} ₺</h2>", unsafe_allow_html=True)
                
                if st.button("⚡ FLASH DISPATCH"):
                    if c_name and c_phone:
                        oid = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                        items = ", ".join([f"{x['Product']}(x{x['Qty']})" for x in st.session_state.cart])
                        
                        # Save Dispatch
                        d_df = get_db(CSV_DISPATCH, cols_dispatch)
                        d_new = {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": active_brand,
                            "Customer": c_name, "Items": items, "Total_Value": total_val,
                            "Status": "Order Received", "Tracking_Num": "", "Notified": "NO", "Notified_Method": ""
                        }
                        save_db(CSV_DISPATCH, d_df, d_new)
                        
                        # Save Finance
                        f_df = get_db(CSV_FINANCE, cols_finance)
                        f_new = {
                            "Order_ID": oid, "Time": datetime.now(), "Brand": active_brand,
                            "Total_Sale": total_val, "Commission_Rate": BRAND_CONTRACTS[active_brand]['commission'],
                            "Commission_Amt": cart_df['Comm'].sum(), "Payable_To_Brand": cart_df['Payable'].sum(),
                            "Invoice_Ref": "", "Payment_Status": "Unpaid"
                        }
                        save_db(CSV_FINANCE, f_df, f_new)
                        
                        st.success("Logged!")
                        st.session_state.cart = []
                        st.rerun()
                    else:
                        st.error("Missing Customer Details")
                
                if st.button("Clear"):
                    st.session_state.cart = []
                    st.rerun()
            else:
                st.info("Empty")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: PROCESSING ---
    with tabs[1]:
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
                
                # TIMELINE
                steps = ["Order Received", "Brand Notified", "Dispatched", "Completed"]
                current = row['Status']
                html = '<div class="timeline-container"><div class="timeline-line"></div>'
                for s in steps:
                    active = "active" if s == current or (current in steps and steps.index(s) < steps.index(current)) else ""
                    html += f'<div class="timeline-step {active}"><div class="timeline-dot"></div><div class="timeline-step-label">{s}</div></div>'
                html += '</div>'
                st.markdown(html, unsafe_allow_html=True)
                
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
                        trk = st.text_input("Tracking", key=f"trk_{idx}")
                        if st.button("Dispatch", key=f"dsp_{idx}"):
                            ops_df.at[idx, 'Tracking_Num'] = trk
                            ops_df.at[idx, 'Status'] = "Dispatched"
                            update_db(CSV_DISPATCH, ops_df)
                            st.rerun()
                with c3:
                    phone = BRAND_CONTRACTS[row['Brand']]['phone']
                    msg = f"ORDER {row['Order_ID']}\n{row['Items']}\n{row['Customer']}"
                    link = f"https://wa.me/{phone}?text={urllib.parse.quote(msg)}"
                    st.markdown(f'<a href="{link}" target="_blank"><button style="width:100%;background:#25D366;border:none;padding:10px;border-radius:5px;color:white;">WhatsApp</button></a>', unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)

    # --- TAB 3: FINANCIALS ---
    with tabs[3]:
        fin_df = get_db(CSV_FINANCE, cols_finance)
        pending = fin_df[fin_df['Invoice_Ref'] == ""]
        
        st.markdown("### 🧾 Invoicing")
        if not pending.empty:
            st.dataframe(pending)
            c1, c2 = st.columns(2)
            with c1: t_brand = st.selectbox("Generate For:", list(BRAND_CONTRACTS.keys()))
            with c2:
                if st.button("Generate Invoice"):
                    b_items = pending[pending['Brand'] == t_brand]
                    if not b_items.empty:
                        ref = f"INV-{datetime.now().strftime('%Y%m')}-{t_brand[:3]}"
                        tot = b_items['Commission_Amt'].sum()
                        
                        inv_df = get_db(CSV_INVOICES, cols_invoices)
                        save_db(CSV_INVOICES, inv_df, {
                            "Invoice_Ref": ref, "Date": datetime.now().date(), "Brand": t_brand,
                            "Total_Commission": tot, "KDV": tot*0.2, "Total_Due": tot*1.2,
                            "Sent_Status": "Pending", "Paid_Status": "Unpaid"
                        })
                        
                        for i in b_items.index: fin_df.at[i, 'Invoice_Ref'] = ref
                        update_db(CSV_FINANCE, fin_df)
                        st.success(f"Generated {ref}")
                        st.rerun()

# ============================================================================
# 7. EXECUTION
# ============================================================================

if not st.session_state.admin_logged_in:
    login_screen()
else:
    dashboard_screen()
