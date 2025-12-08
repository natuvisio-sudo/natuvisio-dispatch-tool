import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO BRIDGE OS v9.0 - COMPLETE FINANCIAL & LOGISTICS SUITE
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Bridge OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. SYSTEM CONFIGURATION & CONSTANTS
# ============================================================================

# Security & Roles
ADMIN_PASS = "admin2025"
USER_CREDENTIALS = {
    "hakiheal@natuvisio.com": {"password": "Hakiheal2025**", "role": "partner", "brand": "HAKI HEAL"},
    "auroraco@natuvisio.com": {"password": "Auroraco**", "role": "partner", "brand": "AURORACO"},
    "longevicals@natuvisio.com": {"password": "Long2025**", "role": "partner", "brand": "LONGEVICALS"},
    "juliana@natuvisio.com": {"password": "Juliana2025.", "role": "dietitian", "brand": "DRJULIANA"}
}

# Financial Constants
KDV_RATE = 0.20  # 20% VAT on Commission

# File Paths (Local Persistence)
CSV_ORDERS = "nv_orders.csv"
CSV_INVOICES = "nv_invoices.csv"
CSV_STOCK = "nv_stock.csv"
CSV_LOGS = "nv_logs.csv"

# UI Assets
LOGO_URL = "https://res.cloudinary.com/deb1j92hy/image/upload/f_auto,q_auto/v1764805291/natuvisio_logo_gtqtfs.png"
BG_IMAGE = "https://images.unsplash.com/photo-1519681393784-d120267933ba?q=80&w=2070&auto=format&fit=crop"

# Brand Registry (The "Source of Truth")
BRANDS = {
    "HAKI HEAL": {
        "phone": "905550001122", # Example format
        "color": "#4ECDC4",
        "commission": 0.25, # 25% Commission
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "company_name": "HAKI HEAL KOZMETIK A.S.",
        "products": {
            "HAKI HEAL KREM": {"sku": "SKU-HAKI-CRM", "price": 450},
            "HAKI HEAL LOSYON": {"sku": "SKU-HAKI-BODY", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP", "price": 120}
        }
    },
    "AURORACO": {
        "phone": "905550002233",
        "color": "#FF6B6B",
        "commission": 0.30, # 30% Commission
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "company_name": "AURORACO GIDA LTD.",
        "products": {
            "AURORACO MATCHA": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO CACAO": {"sku": "SKU-AUR-CACAO", "price": 550}
        }
    },
    "LONGEVICALS": {
        "phone": "905550003344",
        "color": "#95E1D3",
        "commission": 0.20, # 20% Commission
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "company_name": "LONGEVICALS HEALTH INC.",
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
        "company_name": "DR JULIANA KLINIK",
        "products": {
            "ONLINE DANISMANLIK": {"sku": "SKU-JUL-CONSULT", "price": 1500},
            "DIET PLAN": {"sku": "SKU-JUL-DIET", "price": 2500}
        }
    }
}

# ============================================================================
# 2. CSS STYLING (Glassmorphism)
# ============================================================================

def load_css():
    st.markdown(f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
        
        .stApp {{
            background-image: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.95)), url("{BG_IMAGE}");
            background-size: cover;
            background-attachment: fixed;
            font-family: 'Inter', sans-serif;
            color: #ffffff;
        }}
        
        .glass-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
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

        .status-badge {{
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .status-pending {{ background: rgba(245, 158, 11, 0.2); color: #FCD34D; border: 1px solid #FCD34D; }}
        .status-completed {{ background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid #34D399; }}
        .status-dispatched {{ background: rgba(59, 130, 246, 0.2); color: #60A5FA; border: 1px solid #60A5FA; }}
        
        h1, h2, h3 {{ font-family: 'Space Grotesk', sans-serif !important; color: white !important; }}
        
        div.stButton > button {{
            background: linear-gradient(135deg, #4ECDC4 0%, #2E8B57 100%);
            border: none;
            color: white;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            transition: all 0.3s;
        }}
        div.stButton > button:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(78, 205, 196, 0.4); }}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 3. DATA LAYER (CSV Persistence)
# ============================================================================

def init_db():
    if not os.path.exists(CSV_ORDERS):
        df = pd.DataFrame(columns=[
            "Order_ID", "Date", "Brand", "Customer", "Phone", "Address", 
            "Items", "Total_Sale", "Comm_Rate", "Comm_Amt", "Comm_KDV", 
            "Net_Payout", "Status", "Tracking", "Invoice_Ref"
        ])
        df.to_csv(CSV_ORDERS, index=False)
        
    if not os.path.exists(CSV_INVOICES):
        df = pd.DataFrame(columns=[
            "Invoice_ID", "Date_Gen", "Brand", "Total_Comm_Base", 
            "Total_KDV", "Total_Invoice_Amt", "Order_IDs", "Status", "Paid_Date"
        ])
        df.to_csv(CSV_INVOICES, index=False)

    if not os.path.exists(CSV_STOCK):
        df = pd.DataFrame(columns=["Log_ID", "Date", "User", "Product", "Action", "Qty", "Balance"])
        df.to_csv(CSV_STOCK, index=False)

def load_data(file):
    try:
        return pd.read_csv(file)
    except:
        return pd.DataFrame()

def save_data(df, file):
    df.to_csv(file, index=False)

# ============================================================================
# 4. HELPER FUNCTIONS
# ============================================================================

def generate_whatsapp_link(phone, order_id, customer, items, address):
    # Sanitize phone
    phone = str(phone).replace("+", "").replace(" ", "")
    
    message = f"""
🚨 *NATUVISIO DISPATCH REQUEST*
---------------------------
🆔 *Order:* {order_id}
👤 *Customer:* {customer}
📦 *Items:* {items}
📍 *Address:* {address}
---------------------------
Please ship immediately and update tracking in Portal.
"""
    encoded_msg = urllib.parse.quote(message)
    return f"https://wa.me/{phone}?text={encoded_msg}"

def calculate_financials(price, qty, comm_rate):
    total_sale = price * qty
    comm_base = total_sale * comm_rate
    comm_kdv = comm_base * KDV_RATE
    # Natuvisio Keeps: Comm_Base + Comm_KDV
    # Brand Gets: Total_Sale - (Comm_Base + Comm_KDV)
    net_payout = total_sale - (comm_base + comm_kdv)
    return total_sale, comm_base, comm_kdv, net_payout

# ============================================================================
# 5. CORE INTERFACE: LOGIN
# ============================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    load_css()
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,1,1])
    with col2:
        st.markdown(f"<center><img src='{LOGO_URL}' width='100'></center>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center;'>NATUVISIO BRIDGE OS</h2>", unsafe_allow_html=True)
        
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("SECURE LOGIN")
            
            if submitted:
                if email == "admin" and password == ADMIN_PASS:
                    st.session_state.logged_in = True
                    st.session_state.role = "admin"
                    st.session_state.user = "Admin"
                    st.rerun()
                elif email in USER_CREDENTIALS and USER_CREDENTIALS[email]['password'] == password:
                    st.session_state.logged_in = True
                    st.session_state.role = USER_CREDENTIALS[email]['role']
                    st.session_state.user = email
                    st.session_state.brand = USER_CREDENTIALS[email]['brand']
                    st.rerun()
                else:
                    st.error("Access Denied")

# ============================================================================
# 6. ADMIN DASHBOARD (The "Brain")
# ============================================================================

def admin_dashboard():
    # --- Sidebar ---
    with st.sidebar:
        st.image(LOGO_URL, width=50)
        st.markdown("### ADMIN HQ")
        page = st.radio("Navigation", ["⚡ Dispatch Center", "📦 Order Management", "💰 Finance & Invoicing", "⚙️ Settings"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # --- Page 1: Dispatch Center (Order Creation) ---
    if page == "⚡ Dispatch Center":
        st.title("⚡ Flash Dispatch")
        st.markdown("Create order and generate instant bridge notifications.")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("1. Customer Details")
            c_name = st.text_input("Full Name")
            c_phone = st.text_input("Phone Number")
            c_addr = st.text_area("Shipping Address")
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("2. Cart Builder")
            s_brand = st.selectbox("Select Brand Partner", list(BRANDS.keys()))
            
            brand_products = BRANDS[s_brand]['products']
            s_prod = st.selectbox("Select Product", list(brand_products.keys()))
            s_qty = st.number_input("Quantity", 1, 100, 1)
            
            # Live Calculation
            u_price = brand_products[s_prod]['price']
            u_comm = BRANDS[s_brand]['commission']
            
            t_sale, t_comm, t_kdv, t_net = calculate_financials(u_price, s_qty, u_comm)
            
            st.info(f"💰 Financial Preview:\nTotal Sale: {t_sale}₺ | Comm: {t_comm:.2f}₺ | KDV: {t_kdv:.2f}₺ | **Payout: {t_net:.2f}₺**")
            
            if st.button("CONFIRM ORDER & GENERATE DISPATCH"):
                if c_name and c_phone:
                    order_id = f"NV-{datetime.now().strftime('%m%d-%H%M')}"
                    new_order = {
                        "Order_ID": order_id,
                        "Date": datetime.now().strftime("%Y-%m-%d"),
                        "Brand": s_brand,
                        "Customer": c_name,
                        "Phone": c_phone,
                        "Address": c_addr,
                        "Items": f"{s_prod} (x{s_qty})",
                        "Total_Sale": t_sale,
                        "Comm_Rate": u_comm,
                        "Comm_Amt": t_comm,
                        "Comm_KDV": t_kdv,
                        "Net_Payout": t_net,
                        "Status": "Pending",
                        "Tracking": "",
                        "Invoice_Ref": ""
                    }
                    df = load_data(CSV_ORDERS)
                    df = pd.concat([df, pd.DataFrame([new_order])], ignore_index=True)
                    save_data(df, CSV_ORDERS)
                    st.success(f"Order {order_id} Created Successfully!")
                    st.session_state.last_order = new_order
                else:
                    st.error("Missing Customer Data")
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.subheader("3. Bridge Notification")
            if 'last_order' in st.session_state:
                lo = st.session_state.last_order
                brand_phone = BRANDS[lo['Brand']]['phone']
                
                wa_link = generate_whatsapp_link(brand_phone, lo['Order_ID'], lo['Customer'], lo['Items'], lo['Address'])
                
                st.markdown(f"""
                <div style="text-align: center;">
                    <h1 style="font-size: 50px;">📲</h1>
                    <p>Order {lo['Order_ID']} Created.</p>
                    <a href="{wa_link}" target="_blank">
                        <button style="background-color: #25D366; color: white; padding: 10px 20px; border: none; border-radius: 5px; font-weight: bold; width: 100%; cursor: pointer;">
                            OPEN WHATSAPP DISPATCH
                        </button>
                    </a>
                    <p style="font-size: 10px; margin-top: 10px;">Clicking opens WhatsApp Web with pre-filled shipping data.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.info("Waiting for order generation...")
            st.markdown('</div>', unsafe_allow_html=True)

    # --- Page 2: Order Management ---
    elif page == "📦 Order Management":
        st.title("📦 Order Database")
        df = load_data(CSV_ORDERS)
        
        # Filter
        status_filter = st.multiselect("Filter Status", df['Status'].unique())
        if status_filter:
            df = df[df['Status'].isin(status_filter)]
            
        st.dataframe(df, use_container_width=True)

    # --- Page 3: FINANCE (The Missing Link) ---
    elif page == "💰 Finance & Invoicing":
        st.title("💰 Financial HQ")
        st.markdown("Generate invoices for commissions and manage payouts.")
        
        orders = load_data(CSV_ORDERS)
        invoices = load_data(CSV_INVOICES)
        
        tab1, tab2 = st.tabs(["Generate Invoices", "Invoice History & Payouts"])
        
        with tab1:
            st.subheader("Pending Invoicing")
            # Filter orders that are Completed but not Invoiced
            pending = orders[(orders['Status'] == 'Completed') & (orders['Invoice_Ref'].isnull() | (orders['Invoice_Ref'] == ""))]
            
            if pending.empty:
                st.info("No completed orders pending invoicing.")
            else:
                # Group by Brand
                sel_brand = st.selectbox("Select Brand to Invoice", pending['Brand'].unique())
                brand_pending = pending[pending['Brand'] == sel_brand]
                
                st.dataframe(brand_pending[['Order_ID', 'Date', 'Total_Sale', 'Comm_Amt', 'Comm_KDV', 'Net_Payout']])
                
                # Calculation totals
                sum_comm = brand_pending['Comm_Amt'].sum()
                sum_kdv = brand_pending['Comm_KDV'].sum()
                sum_total = sum_comm + sum_kdv
                
                st.markdown(f"""
                <div class="glass-card">
                    <h3>Invoice Summary: {sel_brand}</h3>
                    <p><strong>Brand Company:</strong> {BRANDS[sel_brand]['company_name']}</p>
                    <hr>
                    <div style="display:flex; justify-content:space-between;"><span>Commission Subtotal:</span> <strong>{sum_comm:.2f}₺</strong></div>
                    <div style="display:flex; justify-content:space-between;"><span>KDV (20%):</span> <strong>{sum_kdv:.2f}₺</strong></div>
                    <div style="display:flex; justify-content:space-between; font-size: 18px; margin-top: 10px;"><span>TOTAL INVOICE AMOUNT:</span> <strong style="color: #4ECDC4;">{sum_total:.2f}₺</strong></div>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button(f"📄 GENERATE INVOICE FOR {len(brand_pending)} ORDERS"):
                    inv_id = f"INV-{datetime.now().strftime('%Y%m')}-{len(invoices)+1:03d}"
                    
                    # 1. Create Invoice Record
                    new_inv = {
                        "Invoice_ID": inv_id,
                        "Date_Gen": datetime.now().strftime("%Y-%m-%d"),
                        "Brand": sel_brand,
                        "Total_Comm_Base": sum_comm,
                        "Total_KDV": sum_kdv,
                        "Total_Invoice_Amt": sum_total,
                        "Order_IDs": ",".join(brand_pending['Order_ID'].tolist()),
                        "Status": "Unpaid",
                        "Paid_Date": ""
                    }
                    invoices = pd.concat([invoices, pd.DataFrame([new_inv])], ignore_index=True)
                    save_data(invoices, CSV_INVOICES)
                    
                    # 2. Update Orders with Invoice Ref
                    orders.loc[orders['Order_ID'].isin(brand_pending['Order_ID']), 'Invoice_Ref'] = inv_id
                    save_data(orders, CSV_ORDERS)
                    
                    st.success(f"Invoice {inv_id} Generated! Please send to brand.")
                    st.rerun()

        with tab2:
            st.subheader("Invoice Ledger")
            # Show invoices
            for i, inv in invoices.iterrows():
                with st.expander(f"{inv['Invoice_ID']} | {inv['Brand']} | {inv['Total_Invoice_Amt']:.2f}₺ | {inv['Status']}"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write(f"**Date:** {inv['Date_Gen']}")
                        st.write(f"**Orders:** {inv['Order_IDs']}")
                    with col_b:
                        if inv['Status'] == "Unpaid":
                            if st.button("Mark as PAID", key=inv['Invoice_ID']):
                                invoices.at[i, 'Status'] = "Paid"
                                invoices.at[i, 'Paid_Date'] = datetime.now().strftime("%Y-%m-%d")
                                save_data(invoices, CSV_INVOICES)
                                st.rerun()
                        else:
                            st.success(f"Paid on {inv['Paid_Date']}")

# ============================================================================
# 7. PARTNER PORTAL (Fulfillment)
# ============================================================================

def partner_dashboard():
    brand = st.session_state.brand
    brand_color = BRANDS[brand]['color']
    
    st.markdown(f"""
    <div style="border-left: 5px solid {brand_color}; padding-left: 20px;">
        <h1>{brand} PARTNER PORTAL</h1>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_data(CSV_ORDERS)
    my_orders = df[df['Brand'] == brand]
    
    tab1, tab2, tab3 = st.tabs(["🚀 Pending Shipments", "📜 Order History", "💰 My Earnings"])
    
    with tab1:
        st.subheader("Action Required")
        # Pending orders
        pending = my_orders[my_orders['Status'].isin(['Pending', 'Notified'])]
        
        if pending.empty:
            st.info("No pending orders. Good job!")
        
        for idx, row in pending.iterrows():
            with st.expander(f"📦 {row['Order_ID']} - {row['Items']}", expanded=True):
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown(f"**Ship To:**\n{row['Customer']}\n{row['Address']}\n📞 {row['Phone']}")
                with c2:
                    st.markdown(f"**Payout:** {row['Net_Payout']:.2f}₺")
                    tracking_input = st.text_input("Enter Tracking Code", key=f"t_{row['Order_ID']}")
                    
                    if st.button("CONFIRM SHIPMENT", key=f"b_{row['Order_ID']}"):
                        if tracking_input:
                            # Update global DF properly
                            idx_global = df[df['Order_ID'] == row['Order_ID']].index[0]
                            df.at[idx_global, 'Status'] = 'Completed'
                            df.at[idx_global, 'Tracking'] = tracking_input
                            save_data(df, CSV_ORDERS)
                            st.success("Marked Shipped!")
                            st.rerun()
                        else:
                            st.error("Tracking code required.")

    with tab2:
        st.dataframe(my_orders)
        
    with tab3:
        st.subheader("Financial Statement")
        
        # Calculate totals
        total_payout = my_orders['Net_Payout'].sum()
        completed_payout = my_orders[my_orders['Status'] == 'Completed']['Net_Payout'].sum()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Sales Volume", f"{my_orders['Total_Sale'].sum():.2f}₺")
        c2.metric("Commissions Paid (incl. VAT)", f"{(my_orders['Comm_Amt'].sum() + my_orders['Comm_KDV'].sum()):.2f}₺")
        c3.metric("NET EARNINGS", f"{total_payout:.2f}₺")
        
        st.markdown("### Payout Settings")
        st.markdown(f"**Registered IBAN:** `{BRANDS[brand]['iban']}`")
        st.info("Payouts are processed T+14 days after order completion.")

# ============================================================================
# 8. DIETITIAN DASHBOARD (Inventory)
# ============================================================================

def dietitian_dashboard():
    st.title("🍏 Dr. Juliana Dashboard")
    st.markdown("Monitor inventory levels for clinic.")
    
    stock_df = load_data(CSV_STOCK)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Update Stock")
        prod = st.selectbox("Product", ["CONSULTATION", "DIET PLAN", "SUPPLEMENT PACK"])
        action = st.radio("Action", ["ADD STOCK", "USE STOCK"])
        qty = st.number_input("Quantity", 1, 100, 1)
        
        if st.button("UPDATE LOG"):
            # Calculate new balance
            prev_bal = 0
            if not stock_df.empty:
                prod_hist = stock_df[stock_df['Product'] == prod]
                if not prod_hist.empty:
                    prev_bal = prod_hist.iloc[-1]['Balance']
            
            new_bal = prev_bal + qty if action == "ADD STOCK" else prev_bal - qty
            
            new_entry = {
                "Log_ID": f"LOG-{len(stock_df)+1}",
                "Date": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "User": "Dr. Juliana",
                "Product": prod,
                "Action": action,
                "Qty": qty,
                "Balance": new_bal
            }
            stock_df = pd.concat([stock_df, pd.DataFrame([new_entry])], ignore_index=True)
            save_data(stock_df, CSV_STOCK)
            st.success("Inventory Updated")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.subheader("Inventory History")
        st.dataframe(stock_df.sort_values(by="Date", ascending=False), use_container_width=True)

# ============================================================================
# 9. MAIN APP ROUTER
# ============================================================================

def main():
    load_css()
    init_db()
    
    if not st.session_state.logged_in:
        login_page()
    else:
        if st.session_state.role == "admin":
            admin_dashboard()
        elif st.session_state.role == "partner":
            partner_dashboard()
        elif st.session_state.role == "dietitian":
            dietitian_dashboard()

if __name__ == "__main__":
    main()
