import streamlit as st
import pandas as pd
import numpy as np
import os
import urllib.parse
from datetime import datetime, timedelta
import random

# ============================================================================
# 🏔️ NATUVISIO BRIDGE OS v9.1 (Native Charts Version)
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Bridge HQ",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# 1. CSS & STYLING
# ============================================================================
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    /* Global Variables */
    :root {
        --nv-forest: #183315;
        --nv-sage: #2d4a2b;
        --nv-gold: #d4af37;
        --nv-cream: #f4f4f0;
    }
    
    .stApp {
        background-color: var(--nv-cream);
        color: #333333;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--nv-forest) !important;
        font-weight: 700 !important;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: var(--nv-forest);
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3, 
    section[data-testid="stSidebar"] span, 
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    
    /* Metric Cards */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-left: 6px solid var(--nv-forest);
        text-align: center;
    }
    .metric-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--nv-forest);
        font-family: 'Space Grotesk', sans-serif;
    }
    .metric-label {
        font-size: 12px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
        margin-top: 5px;
    }

    /* Buttons */
    div.stButton > button {
        background: linear-gradient(135deg, #183315 0%, #2d4a2b 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(24, 51, 21, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# 2. DATA MANAGER (Persistence Layer)
# ============================================================================

class DataManager:
    def __init__(self):
        self.orders_file = 'nv_orders.csv'
        self.inventory_file = 'nv_inventory.csv'
        self.init_files()

    def init_files(self):
        # --- Initialize Orders CSV with Dummy Data ---
        if not os.path.exists(self.orders_file):
            data = {
                'Order_ID': [f'NV-{1000+i}' for i in range(5)],
                'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)],
                'Customer': ['Alice Yilmaz', 'Bob Kaya', 'Charlie Demir', 'Diana Celik', 'Evan Ozturk'],
                'Brand': ['Longevicals', 'Haki Heal', 'Auroraco', 'Longevicals', 'Haki Heal'],
                'Product': ['NMN 500mg', 'Matcha Set', 'Lavender Oil', 'Resveratrol', 'Face Cream'],
                'Amount': [1200, 850, 450, 1500, 600],
                'Status': ['Pending', 'Shipped', 'Delivered', 'Pending', 'Processing'],
                'Phone': ['905320000001'] * 5
            }
            pd.DataFrame(data).to_csv(self.orders_file, index=False)

        # --- Initialize Inventory CSV ---
        if not os.path.exists(self.inventory_file):
            data = {
                'SKU': ['LNG-001', 'LNG-002', 'HKH-001', 'HKH-002', 'AUR-001'],
                'Brand': ['Longevicals', 'Longevicals', 'Haki Heal', 'Haki Heal', 'Auroraco'],
                'Product_Name': ['NMN 500mg', 'Resveratrol', 'Matcha Set', 'Face Cream', 'Lavender Oil'],
                'Price': [1200.0, 1500.0, 850.0, 600.0, 450.0],
                'Stock_Level': [50, 30, 100, 80, 200],
                'Commission_Pct': [15, 15, 20, 20, 25]
            }
            pd.DataFrame(data).to_csv(self.inventory_file, index=False)

    def load_orders(self):
        return pd.read_csv(self.orders_file)

    def save_order(self, order_dict):
        df = self.load_orders()
        new_row = pd.DataFrame([order_dict])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(self.orders_file, index=False)

    def load_inventory(self):
        return pd.read_csv(self.inventory_file)

    def update_inventory(self, df):
        df.to_csv(self.inventory_file, index=False)

db = DataManager()

# ============================================================================
# 3. AUTHENTICATION
# ============================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    st.markdown("<div style='height: 15vh;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>NATUVISIO HQ</h1>", unsafe_allow_html=True)
        st.markdown("<div style='text-align: center; color: #666; margin-bottom: 20px;'>Bridge Operating System v9.1</div>", unsafe_allow_html=True)
        
        with st.form("login"):
            password = st.text_input("Access Key", type="password")
            submit = st.form_submit_button("INITIALIZE SYSTEM", use_container_width=True)
            
            if submit:
                if password == "admin2025":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("⛔ Access Denied")

# ============================================================================
# 4. ADMIN SECTIONS
# ============================================================================

def section_dashboard():
    st.title("📊 Executive Dashboard")
    df = db.load_orders()
    
    # --- KPI Cards ---
    col1, col2, col3, col4 = st.columns(4)
    total_rev = df['Amount'].sum()
    pending_count = len(df[df['Status'] == 'Pending'])
    
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">₺{total_rev:,.0f}</div><div class="metric-label">Total Revenue</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Total Orders</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:#d4af37;">{pending_count}</div><div class="metric-label">Pending Dispatch</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">3</div><div class="metric-label">Active Partners</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # --- Native Streamlit Charts (No Plotly) ---
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by Brand")
        # Prepare data for bar chart
        rev_by_brand = df.groupby('Brand')['Amount'].sum()
        st.bar_chart(rev_by_brand, color="#183315")
    
    with c2:
        st.subheader("Order Status")
        status_counts = df['Status'].value_counts()
        st.bar_chart(status_counts, color="#d4af37")

def section_dispatch():
    st.title("⚡ Dispatch Center (The Bridge)")
    st.markdown("Generate orders and trigger the decentralized fulfillment network.")
    
    inv_df = db.load_inventory()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 1. Customer Details")
        with st.form("dispatch_form"):
            c1, c2 = st.columns(2)
            customer = c1.text_input("Customer Name")
            phone = c2.text_input("Phone (905...)")
            address = st.text_area("Shipping Address")
            
            st.markdown("### 2. Item Selection")
            brand_sel = st.selectbox("Brand Partner", inv_df['Brand'].unique())
            
            # Filter products by brand
            avail_prods = inv_df[inv_df['Brand'] == brand_sel]
            
            if not avail_prods.empty:
                product_sel = st.selectbox("Product", avail_prods['Product_Name'].unique())
                
                # Get price automatically
                unit_price = avail_prods[avail_prods['Product_Name'] == product_sel]['Price'].values[0]
                st.info(f"Unit Price: ₺{unit_price:,.2f}")
                
                qty = st.number_input("Quantity", 1, 10, 1)
                submit = st.form_submit_button("GENERATE BRIDGE ORDER")
            else:
                st.warning("No products found for this brand.")
                submit = False
    
    with col2:
        st.markdown("### 3. Bridge Action")
        if submit and customer and phone:
            total = unit_price * qty
            order_id = f"NV-{random.randint(10000,99999)}"
            
            # Save to DB
            new_order = {
                'Order_ID': order_id,
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Customer': customer,
                'Brand': brand_sel,
                'Product': product_sel,
                'Amount': total,
                'Status': 'Pending',
                'Phone': phone
            }
            db.save_order(new_order)
            
            st.success(f"✅ Order {order_id} Saved!")
            
            # WhatsApp Logic
            st.markdown("### 4. Notify Partner")
            msg = f"""🚨 *NATUVISIO DISPATCH*
------------------
Ref: {order_id}
Item: {product_sel} (x{qty})
Customer: {customer}
Addr: {address}
------------------
Please confirm tracking."""
            
            encoded_msg = urllib.parse.quote(msg)
            clean_phone = phone.replace(" ", "").replace("+", "")
            wa_link = f"https://wa.me/{clean_phone}?text={encoded_msg}"
            
            st.code(msg, language="text")
            st.markdown(f'''
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <div style="background-color:#25D366; color:white; padding:15px; border-radius:8px; text-align:center; font-weight:bold; box-shadow:0 4px 6px rgba(0,0,0,0.1);">
                        📲 CLICK TO SEND VIA WHATSAPP
                    </div>
                </a>
                ''', unsafe_allow_html=True)

def section_orders():
    st.title("📦 Order Management")
    st.markdown("View and update status of active shipments.")
    
    df = db.load_orders()
    
    # Filters
    f1, f2 = st.columns(2)
    with f1:
        status_filter = st.multiselect("Filter Status", df['Status'].unique())
    with f2:
        brand_filter = st.multiselect("Filter Brand", df['Brand'].unique())
    
    filtered_df = df.copy()
    if status_filter:
        filtered_df = filtered_df[filtered_df['Status'].isin(status_filter)]
    if brand_filter:
        filtered_df = filtered_df[filtered_df['Brand'].isin(brand_filter)]
        
    st.dataframe(
        filtered_df, 
        use_container_width=True,
        column_config={
            "Amount": st.column_config.NumberColumn("Amount (₺)", format="₺%d")
        }
    )

def section_inventory():
    st.title("🧘 Inventory & SKU")
    st.markdown("Manage SKUs across the decentralized network.")
    
    df = db.load_inventory()
    
    # Editable Dataframe
    edited_df = st.data_editor(
        df, 
        num_rows="dynamic", 
        use_container_width=True,
        column_config={
            "Price": st.column_config.NumberColumn("Price (₺)", format="₺%.2f"),
            "Commission_Pct": st.column_config.ProgressColumn("Commission %", format="%d%%", min_value=0, max_value=100)
        }
    )
    
    if st.button("💾 Save Changes to Inventory"):
        db.update_inventory(edited_df)
        st.success("Inventory updated successfully!")

def section_partners():
    st.title("🤝 Partner Network")
    st.markdown("Manage relationships with fulfillment nodes.")
    
    partners = [
        {"name": "Longevicals", "role": "Science Anchor", "status": "Active", "sla": 98, "contact": "Dr. Aris"},
        {"name": "Haki Heal", "role": "Holistic Anchor", "status": "Active", "sla": 96, "contact": "Selin H."},
        {"name": "Auroraco", "role": "Lifestyle Anchor", "status": "Warning", "sla": 89, "contact": "Can K."}
    ]
    
    for p in partners:
        with st.expander(f"{p['name']} ({p['status']})"):
            c1, c2 = st.columns(2)
            c1.write(f"**Role:** {p['role']}")
            c1.write(f"**Contact:** {p['contact']}")
            
            # Custom SLA Bar
            c2.write("**SLA Performance**")
            c2.progress(p['sla'] / 100)
            c2.caption(f"{p['sla']}% On-Time Shipping Rate")

def section_financials():
    st.title("💰 Financials")
    st.markdown("Track Gross Transaction Value (GTV) and Platform Revenue.")
    
    df = db.load_orders()
    inv = db.load_inventory()
    
    # Merge orders with inventory to get commission rates
    # Note: Column names must match. Inventory uses 'Product_Name', Orders uses 'Product'
    merged = pd.merge(df, inv[['Product_Name', 'Commission_Pct']], left_on='Product', right_on='Product_Name', how='left')
    
    # Fill NaN for safety
    merged['Commission_Pct'] = merged['Commission_Pct'].fillna(0)
    
    # Calculate
    merged['Commission_Revenue'] = merged['Amount'] * (merged['Commission_Pct'] / 100)
    
    # Display Table
    st.dataframe(
        merged[['Order_ID', 'Brand', 'Amount', 'Commission_Pct', 'Commission_Revenue']], 
        use_container_width=True,
        column_config={
            "Amount": st.column_config.NumberColumn("Sale Price", format="₺%.2f"),
            "Commission_Revenue": st.column_config.NumberColumn("Bridge Revenue", format="₺%.2f"),
            "Commission_Pct": st.column_config.NumberColumn("Comm %", format="%d%%")
        }
    )
    
    # Total
    total_comm = merged['Commission_Revenue'].sum()
    st.markdown("---")
    st.markdown(f"### 💵 Total Platform Revenue: **₺{total_comm:,.2f}**")

def section_crm():
    st.title("👥 CRM (High-Trust Clients)")
    st.markdown("Longevity customer database.")
    
    df = db.load_orders()
    
    if not df.empty:
        # Group by customer
        cust_df = df.groupby('Customer').agg({
            'Order_ID': 'count',
            'Amount': 'sum',
            'Date': 'max'
        }).reset_index()
        
        cust_df.columns = ['Customer Name', 'Total Orders', 'Lifetime Value', 'Last Active']
        
        st.dataframe(
            cust_df, 
            use_container_width=True,
            column_config={
                "Lifetime Value": st.column_config.NumberColumn("LTV (₺)", format="₺%d"),
                "Last Active": st.column_config.DateColumn("Last Purchase")
            }
        )
    else:
        st.info("No customer data yet.")

def section_settings():
    st.title("⚙️ System Settings")
    
    st.subheader("Admin Configuration")
    st.text_input("Admin Email", value="founders@natuvisio.com")
    
    st.subheader("Data Management")
    if st.button("Export All Data (CSV)"):
        st.info("Exporting database... (Feature active in production)")
        
    st.subheader("System Logs")
    st.code(f"""
    [INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - System Startup Successful
    [INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Inventory DB Loaded
    [INFO] {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - Orders DB Loaded
    """, language="text")

# ============================================================================
# 5. MAIN ROUTING
# ============================================================================

def main():
    load_css()
    
    if not st.session_state.logged_in:
        login_screen()
        return

    # --- Sidebar ---
    with st.sidebar:
        st.title("NATUVISIO")
        st.caption("Strategic Platform Architecture")
        st.markdown("---")
        
        menu = st.radio(
            "Navigation", 
            [
                "📊 Dashboard", 
                "⚡ Dispatch Center", 
                "📦 Order Management", 
                "🧘 Inventory & SKU", 
                "🤝 Partner Network", 
                "💰 Financials", 
                "👥 CRM", 
                "⚙️ Settings"
            ]
        )
        
        st.markdown("---")
        if st.button("Log Out"):
            st.session_state.logged_in = False
            st.rerun()

    # --- Router ---
    if menu == "📊 Dashboard":
        section_dashboard()
    elif menu == "⚡ Dispatch Center":
        section_dispatch()
    elif menu == "📦 Order Management":
        section_orders()
    elif menu == "🧘 Inventory & SKU":
        section_inventory()
    elif menu == "🤝 Partner Network":
        section_partners()
    elif menu == "💰 Financials":
        section_financials()
    elif menu == "👥 CRM":
        section_crm()
    elif menu == "⚙️ Settings":
        section_settings()

if __name__ == "__main__":
    main()
