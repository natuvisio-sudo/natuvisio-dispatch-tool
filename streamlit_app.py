import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO UNIFIED OS v10.0 (FINAL PRODUCTION BUILD)
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Bridge OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. CONFIGURATION & CONSTANTS
# ============================================================================

# Security
ADMIN_PASS = "admin2025"
USER_CREDENTIALS = {
    "hakiheal@natuvisio.com": {"password": "Hakiheal2025**", "role": "partner", "brand": "HAKI HEAL"},
    "auroraco@natuvisio.com": {"password": "Auroraco**", "role": "partner", "brand": "AURORACO"},
    "longevicals@natuvisio.com": {"password": "Long2025**", "role": "partner", "brand": "LONGEVICALS"},
    "juliana@natuvisio.com": {"password": "Juliana2025.", "role": "dietitian", "brand": "DRJULIANA"}
}

# Financials
KDV_RATE = 0.20  # 20% VAT on Commission

# Database Files
CSV_ORDERS = "nv_orders_v10.csv"
CSV_INVOICES = "nv_invoices_v10.csv"
CSV_STOCK = "nv_stock_v10.csv"
CSV_LOGS = "nv_logs_v10.csv"

# Brand Registry (Single Source of Truth)
BRANDS = {
    "HAKI HEAL": {
        "phone": "905550001122", 
        "color": "#4ECDC4",
        "commission": 0.15,
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "products": {
            "HAKI HEAL KREM": {"sku": "SKU-HAKI-CRM", "price": 450},
            "HAKI HEAL LOSYON": {"sku": "SKU-HAKI-BODY", "price": 380}
        }
    },
    "AURORACO": {
        "phone": "905550002233",
        "color": "#FF6B6B",
        "commission": 0.20,
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "products": {
            "AURORACO MATCHA": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO CACAO": {"sku": "SKU-AUR-CACAO", "price": 550}
        }
    },
    "LONGEVICALS": {
        "phone": "905550003344",
        "color": "#95E1D3",
        "commission": 0.12,
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "products": {
            "OMEGA-3 ULTRA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "NMN ANTI-AGE": {"sku": "SKU-LONG-NMN", "price": 2500}
        }
    },
    "DRJULIANA": {
        "phone": "905550004455",
        "color": "#A78BFA",
        "commission": 0.25,
        "iban": "TR90 0001 7000 0000 3344 5566 77",
        "products": {
            "CONSULTATION": {"sku": "SKU-JUL-CONSULT", "price": 1500},
            "DIET PLAN": {"sku": "SKU-JUL-DIET", "price": 2500}
        }
    }
}

# ============================================================================
# 2. CSS STYLING
# ============================================================================

def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        .stApp {
            background-image: linear-gradient(rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.98));
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }
        
        .glass-card {
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
        }
        
        h1, h2, h3 { font-family: 'Space Grotesk', sans-serif !important; color: white !important; }
        
        .metric-value { font-size: 24px; font-weight: 700; font-family: 'Space Grotesk'; }
        .metric-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.7; }
        
        div.stButton > button {
            background: linear-gradient(135deg, #4ECDC4 0%, #2E8B57 100%);
            border: none;
            color: white;
            font-weight: 600;
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 3. DATA LAYER
# ============================================================================

def init_db():
    if not os.path.exists(CSV_ORDERS):
        df = pd.DataFrame(columns=[
            "Order_ID", "Date", "Brand", "Customer", "Phone", "Address", 
            "Items", "Qty", "Total_Sale", "Comm_Rate", "Comm_Amt", "Comm_KDV", 
            "Net_Payout", "Status", "Tracking", "Invoice_Ref"
        ])
        df.to_csv(CSV_ORDERS, index=False)
        
    if not os.path.exists(CSV_INVOICES):
        df = pd.DataFrame(columns=[
            "Invoice_ID", "Date_Gen", "Brand", "Total_Comm", 
            "Total_KDV", "Invoice_Amt", "Order_Count", "Status"
        ])
        df.to_csv(CSV_INVOICES, index=False)

    if not os.path.exists(CSV_STOCK):
        df = pd.DataFrame(columns=["Log_ID", "Date", "Product", "Action", "Qty", "Balance"])
        df.to_csv(CSV_STOCK, index=False)

def load_data(file):
    try: return pd.read_csv(file)
    except: return pd.DataFrame()

def save_data(df, file):
    df.to_csv(file, index=False)

# ============================================================================
# 4. LOGIC ENGINE
# ============================================================================

def calc_finance(price, qty, rate):
    total = price * qty
    comm_base = total * rate
    comm_kdv = comm_base * KDV_RATE
    # Brand Payout = Total - (Commission + VAT on Commission)
    payout = total - (comm_base + comm_kdv)
    return total, comm_base, comm_kdv, payout

def generate_wa_link(phone, order_id, items, address):
    # Sanitize phone
    clean_phone = str(phone).replace("+", "").replace(" ", "")
    msg = f"""🚨 *NATUVISIO DISPATCH*
🆔 *Order:* {order_id}
📦 *Items:* {items}
📍 *Address:* {address}
------------------
Please confirm tracking number in portal."""
    encoded = urllib.parse.quote(msg)
    return f"https://wa.me/{clean_phone}?text={encoded}"

# ============================================================================
# 5. VIEWS
# ============================================================================

def login_view():
    st.markdown("<div style='height:15vh'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.title("NATUVISIO OS")
        st.markdown("UNIFIED ACCESS PORTAL")
        
        email = st.text_input("Identity")
        pwd = st.text_input("Access Key", type="password")
        
        if st.button("AUTHENTICATE"):
            if email == "admin" and pwd == ADMIN_PASS:
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.session_state.user_email = "admin"
                st.rerun()
            elif email in USER_CREDENTIALS and USER_CREDENTIALS[email]['password'] == pwd:
                st.session_state.logged_in = True
                st.session_state.role = USER_CREDENTIALS[email]['role']
                st.session_state.user_email = email
                st.session_state.brand = USER_CREDENTIALS[email]['brand']
                st.rerun()
            else:
                st.error("Access Denied")

def admin_view():
    st.markdown(f"### 🏔️ ADMIN HQ")
    
    tabs = st.tabs(["⚡ DISPATCH", "📦 ORDERS", "💰 FINANCE", "⚙️ LOGS"])
    
    # --- TAB 1: DISPATCH ---
    with tabs[0]:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("New Order")
            cust_name = st.text_input("Customer Name")
            cust_phone = st.text_input("Phone")
            cust_addr = st.text_area("Address")
            
            s_brand = st.selectbox("Select Brand", list(BRANDS.keys()))
            s_prod = st.selectbox("Product", list(BRANDS[s_brand]['products'].keys()))
            s_qty = st.number_input("Qty", 1, 10, 1)
            
            # Real-time Calc
            u_price = BRANDS[s_brand]['products'][s_prod]['price']
            t_sale, t_comm, t_kdv, t_pay = calc_finance(u_price, s_qty, BRANDS[s_brand]['commission'])
            
            st.info(f"💵 Sale: {t_sale}₺ | Comm: {t_comm:.2f}₺ | KDV: {t_kdv:.2f}₺ | **Payout: {t_pay:.2f}₺**")
            
            if st.button("CREATE & DISPATCH"):
                if cust_name:
                    order_id = f"NV-{datetime.now().strftime('%m%d%H%M')}"
                    new_order = {
                        "Order_ID": order_id,
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Brand": s_brand,
                        "Customer": cust_name,
                        "Phone": cust_phone,
                        "Address": cust_addr,
                        "Items": s_prod,
                        "Qty": s_qty,
                        "Total_Sale": t_sale,
                        "Comm_Rate": BRANDS[s_brand]['commission'],
                        "Comm_Amt": t_comm,
                        "Comm_KDV": t_kdv,
                        "Net_Payout": t_pay,
                        "Status": "Pending",
                        "Tracking": "",
                        "Invoice_Ref": ""
                    }
                    df = load_data(CSV_ORDERS)
                    df = pd.concat([df, pd.DataFrame([new_order])], ignore_index=True)
                    save_data(df, CSV_ORDERS)
                    st.success(f"Order {order_id} Created!")
                    st.session_state.last_dispatch = new_order
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            
        with c2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("Bridge Link")
            if 'last_dispatch' in st.session_state:
                ld = st.session_state.last_dispatch
                link = generate_wa_link(BRANDS[ld['Brand']]['phone'], ld['Order_ID'], f"{ld['Items']} (x{ld['Qty']})", ld['Address'])
                st.markdown(f"""
                <a href="{link}" target="_blank">
                    <button style="background:#25D366; color:white; padding:15px; border-radius:8px; border:none; width:100%; cursor:pointer;">
                        📲 OPEN WHATSAPP
                    </button>
                </a>
                """, unsafe_allow_html=True)
            else:
                st.info("Create order to generate link")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: ORDERS ---
    with tabs[1]:
        df = load_data(CSV_ORDERS)
        st.dataframe(df, use_container_width=True)

    # --- TAB 3: FINANCE (INVOICING) ---
    with tabs[2]:
        df = load_data(CSV_ORDERS)
        # Find completed orders without invoice
        pending = df[(df['Status'] == 'Completed') & (df['Invoice_Ref'].isnull() | (df['Invoice_Ref'] == ""))]
        
        st.subheader("Pending Invoices")
        if not pending.empty:
            target_brand = st.selectbox("Select Brand for Invoicing", pending['Brand'].unique())
            to_invoice = pending[pending['Brand'] == target_brand]
            
            st.dataframe(to_invoice)
            
            inv_total = to_invoice['Comm_Amt'].sum() + to_invoice['Comm_KDV'].sum()
            
            if st.button(f"📄 GENERATE INVOICE (₺{inv_total:.2f})"):
                inv_id = f"INV-{datetime.now().strftime('%Y%m')}-{len(load_data(CSV_INVOICES))+1}"
                
                # Save Invoice
                new_inv = {
                    "Invoice_ID": inv_id,
                    "Date_Gen": datetime.now().strftime("%Y-%m-%d"),
                    "Brand": target_brand,
                    "Total_Comm": to_invoice['Comm_Amt'].sum(),
                    "Total_KDV": to_invoice['Comm_KDV'].sum(),
                    "Invoice_Amt": inv_total,
                    "Order_Count": len(to_invoice),
                    "Status": "Unpaid"
                }
                inv_df = load_data(CSV_INVOICES)
                inv_df = pd.concat([inv_df, pd.DataFrame([new_inv])], ignore_index=True)
                save_data(inv_df, CSV_INVOICES)
                
                # Update Orders
                df.loc[df['Order_ID'].isin(to_invoice['Order_ID']), 'Invoice_Ref'] = inv_id
                save_data(df, CSV_ORDERS)
                st.success(f"Invoice {inv_id} Generated!")
                st.rerun()
        else:
            st.info("No completed orders pending invoice.")
            
        st.markdown("---")
        st.subheader("Invoice History")
        st.dataframe(load_data(CSV_INVOICES), use_container_width=True)

def partner_view():
    brand = st.session_state.brand
    color = BRANDS[brand]['color']
    st.markdown(f"<h2 style='color:{color}'>{brand} PORTAL</h2>", unsafe_allow_html=True)
    
    df = load_data(CSV_ORDERS)
    my_orders = df[df['Brand'] == brand]
    
    tabs = st.tabs(["🚀 ACTION REQUIRED", "📊 HISTORY", "💰 EARNINGS"])
    
    with tabs[0]:
        pending = my_orders[my_orders['Status'] == 'Pending']
        if pending.empty:
            st.info("All caught up!")
        else:
            for idx, row in pending.iterrows():
                with st.expander(f"📦 {row['Order_ID']} | {row['Items']} (x{row['Qty']})"):
                    st.write(f"**Customer:** {row['Customer']}")
                    st.write(f"**Address:** {row['Address']}")
                    
                    track = st.text_input("Tracking Number", key=f"t_{row['Order_ID']}")
                    if st.button("MARK SHIPPED", key=f"b_{row['Order_ID']}"):
                        if track:
                            # Use order ID to find index in main DF
                            main_idx = df[df['Order_ID'] == row['Order_ID']].index[0]
                            df.at[main_idx, 'Status'] = 'Completed'
                            df.at[main_idx, 'Tracking'] = track
                            save_data(df, CSV_ORDERS)
                            st.success("Shipped!")
                            st.rerun()
                        else:
                            st.error("Tracking required")

    with tabs[1]:
        st.dataframe(my_orders)

    with tabs[2]:
        c1, c2 = st.columns(2)
        total_sales = my_orders['Total_Sale'].sum()
        net_earnings = my_orders['Net_Payout'].sum()
        
        with c1:
            st.markdown(f"<div class='glass-card'><h3>Gross Sales</h3><h2>{total_sales:,.2f}₺</h2></div>", unsafe_allow_html=True)
        with c2:
            st.markdown(f"<div class='glass-card'><h3>Net Payout (After Comm+VAT)</h3><h2 style='color:{color}'>{net_earnings:,.2f}₺</h2></div>", unsafe_allow_html=True)

def dietitian_view():
    st.markdown("### 🍏 DR. JULIANA CLINIC")
    
    tabs = st.tabs(["📦 STOCK", "📜 LOGS"])
    
    with tabs[0]:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            prod = st.selectbox("Item", ["CONSULTATION", "DIET PLAN"])
            act = st.radio("Action", ["ADD", "USE"])
            qty = st.number_input("Qty", 1)
            if st.button("UPDATE"):
                st.success("Stock Updated")
            st.markdown('</div>', unsafe_allow_html=True)
            
    with tabs[1]:
        st.info("Activity logs will appear here.")

# ============================================================================
# 6. MAIN APP
# ============================================================================

def main():
    load_css()
    init_db()
    
    if not st.session_state.get('logged_in'):
        login_view()
    else:
        role = st.session_state.role
        
        # Sidebar
        with st.sidebar:
            st.markdown(f"### Logged in as: {role.upper()}")
            if st.button("LOGOUT"):
                st.session_state.clear()
                st.rerun()
        
        if role == "admin":
            admin_view()
        elif role == "partner":
            partner_view()
        elif role == "dietitian":
            dietitian_view()

if __name__ == "__main__":
    main()
