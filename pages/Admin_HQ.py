import streamlit as st
import pandas as pd
import plotly.express as px  # Added for better charts
from datetime import datetime, timedelta
import os
import urllib.parse
import random

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NATUVISIO Bridge HQ",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. CSS & STYLING (The "Scientific Trust" Aesthetic) ---
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    :root {
        --nv-forest: #183315;
        --nv-sage: #2d4a2b;
        --nv-gold: #d4af37;
        --nv-cream: #f4f4f0;
        --nv-white: #ffffff;
    }
    
    .stApp {
        background-color: var(--nv-cream);
    }
    
    /* Typography */
    h1, h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--nv-forest) !important;
    }
    
    p, div, span, label {
        font-family: 'Inter', sans-serif !important;
        color: #333;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--nv-forest);
    }
    
    section[data-testid="stSidebar"] * {
        color: var(--nv-cream) !important;
    }

    /* Cards */
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid var(--nv-forest);
        text-align: center;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: var(--nv-forest);
        font-family: 'Playfair Display', serif;
    }

    .metric-label {
        font-size: 14px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Custom Buttons */
    div.stButton > button {
        background-color: var(--nv-forest);
        color: white;
        border-radius: 4px;
        border: none;
        padding: 0.5rem 1rem;
        font-family: 'Inter', sans-serif;
    }
    div.stButton > button:hover {
        background-color: var(--nv-sage);
        border: 1px solid var(--nv-gold);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- 3. DATA MANAGER (Persistence Layer) ---
class DataManager:
    def __init__(self):
        self.orders_file = 'nv_orders.csv'
        self.inventory_file = 'nv_inventory.csv'
        self.init_files()

    def init_files(self):
        # Initialize Orders if not exists
        if not os.path.exists(self.orders_file):
            # Create dummy data for visualization
            data = {
                'Order ID': [f'NV-{1000+i}' for i in range(5)],
                'Date': [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(5)],
                'Customer': ['Alice Yilmaz', 'Bob Kaya', 'Charlie Demir', 'Diana Celik', 'Evan Ozturk'],
                'Brand': ['Longevicals', 'Haki Heal', 'Auroraco', 'Longevicals', 'Haki Heal'],
                'Product': ['NMN 500mg', 'Matcha Set', 'Lavender Oil', 'Resveratrol', 'Face Cream'],
                'Amount': [1200, 850, 450, 1500, 600],
                'Status': ['Pending', 'Shipped', 'Delivered', 'Pending', 'Processing'],
                'Phone': ['905320000001'] * 5
            }
            pd.DataFrame(data).to_csv(self.orders_file, index=False)

        # Initialize Inventory if not exists
        if not os.path.exists(self.inventory_file):
            data = {
                'SKU': ['LNG-001', 'LNG-002', 'HKH-001', 'HKH-002', 'AUR-001'],
                'Brand': ['Longevicals', 'Longevicals', 'Haki Heal', 'Haki Heal', 'Auroraco'],
                'Product Name': ['NMN 500mg', 'Resveratrol', 'Matcha Set', 'Face Cream', 'Lavender Oil'],
                'Price': [1200, 1500, 850, 600, 450],
                'Stock Level': [50, 30, 100, 80, 200],
                'Commission %': [15, 15, 20, 20, 25]
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

# --- 4. AUTHENTICATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def login_screen():
    st.markdown("<div style='height: 20vh;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.markdown("<h1 style='text-align: center;'>NATUVISIO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Bridge Operating System v2.0</p>", unsafe_allow_html=True)
        password = st.text_input("Enter Access Key", type="password")
        if st.button("Initialize Bridge", use_container_width=True):
            if password == "admin2025":  # Simple auth
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Access Denied")

# --- 5. ADMIN SECTIONS ---

def section_dashboard():
    st.title("Executive Dashboard")
    df = db.load_orders()
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    total_rev = df['Amount'].sum()
    pending_count = len(df[df['Status'] == 'Pending'])
    
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">₺{total_rev:,.0f}</div><div class="metric-label">Total Revenue</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(df)}</div><div class="metric-label">Total Orders</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{pending_count}</div><div class="metric-label">Pending Dispatch</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-value">3</div><div class="metric-label">Active Partners</div></div>', unsafe_allow_html=True)

    st.markdown("---")
    
    # Charts
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Revenue by Brand")
        rev_by_brand = df.groupby('Brand')['Amount'].sum().reset_index()
        fig = px.pie(rev_by_brand, values='Amount', names='Brand', color_discrete_sequence=['#183315', '#2d4a2b', '#d4af37'])
        st.plotly_chart(fig, use_container_width=True)
    
    with c2:
        st.subheader("Order Velocity (Last 7 Days)")
        # Mocking time series for demo
        st.line_chart(df.groupby('Brand')['Amount'].sum())

def section_dispatch():
    st.title("⚡ Dispatch Center (The Bridge)")
    st.markdown("Generate orders and trigger the decentralized fulfillment network.")
    
    inv_df = db.load_inventory()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 1. Order Details")
        with st.form("dispatch_form"):
            c1, c2 = st.columns(2)
            customer = c1.text_input("Customer Name")
            phone = c2.text_input("Phone (905...)")
            address = st.text_area("Shipping Address")
            
            st.markdown("### 2. Item Selection")
            brand_sel = st.selectbox("Brand Partner", inv_df['Brand'].unique())
            # Filter products by brand
            avail_prods = inv_df[inv_df['Brand'] == brand_sel]
            product_sel = st.selectbox("Product", avail_prods['Product Name'].unique())
            
            # Get price automatically
            unit_price = avail_prods[avail_prods['Product Name'] == product_sel]['Price'].values[0]
            
            qty = st.number_input("Quantity", 1, 10, 1)
            
            submit = st.form_submit_button("Generate Bridge Order")
    
    with col2:
        st.markdown("### 3. Verification")
        if submit and customer and phone:
            total = unit_price * qty
            order_id = f"NV-{random.randint(10000,99999)}"
            
            # Save to DB
            new_order = {
                'Order ID': order_id,
                'Date': datetime.now().strftime('%Y-%m-%d'),
                'Customer': customer,
                'Brand': brand_sel,
                'Product': product_sel,
                'Amount': total,
                'Status': 'Pending',
                'Phone': phone
            }
            db.save_order(new_order)
            
            st.success("Order Created in Database!")
            
            # WhatsApp Logic
            st.markdown("### 4. Notify Partner")
            msg = f"""🚨 *NATUVISIO DISPATCH*
Ref: {order_id}
Item: {product_sel} (x{qty})
Customer: {customer}
Addr: {address}
Please confirm tracking."""
            
            encoded_msg = urllib.parse.quote(msg)
            clean_phone = phone.replace(" ", "").replace("+", "")
            wa_link = f"https://wa.me/{clean_phone}?text={encoded_msg}"
            
            st.code(msg, language="text")
            st.markdown(f'''
                <a href="{wa_link}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; font-weight:bold; cursor:pointer; width:100%;">
                        📲 Send via WhatsApp
                    </button>
                </a>
                ''', unsafe_allow_html=True)

def section_orders():
    st.title("Order Management")
    st.markdown("View and update status of active shipments.")
    
    df = db.load_orders()
    
    # Filters
    f1, f2 = st.columns(2)
    with f1:
        status_filter = st.multiselect("Filter Status", df['Status'].unique())
    with f2:
        brand_filter = st.multiselect("Filter Brand", df['Brand'].unique())
    
    if status_filter:
        df = df[df['Status'].isin(status_filter)]
    if brand_filter:
        df = df[df['Brand'].isin(brand_filter)]
        
    st.dataframe(df, use_container_width=True)

def section_inventory():
    st.title("Inventory & Products")
    st.markdown("Manage SKUs across the decentralized network.")
    
    df = db.load_inventory()
    
    # Editable Dataframe
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)
    
    if st.button("Save Changes to Inventory"):
        db.update_inventory(edited_df)
        st.success("Inventory updated successfully!")

def section_partners():
    st.title("Partner Network")
    st.markdown("Manage relationships with fulfillment nodes.")
    
    partners = [
        {"name": "Longevicals", "role": "Science Anchor", "status": "Active", "sla": "98%", "contact": "Dr. Aris"},
        {"name": "Haki Heal", "role": "Holistic Anchor", "status": "Active", "sla": "96%", "contact": "Selin H."},
        {"name": "Auroraco", "role": "Lifestyle Anchor", "status": "Warning", "sla": "89%", "contact": "Can K."}
    ]
    
    for p in partners:
        with st.expander(f"{p['name']} ({p['status']})"):
            c1, c2 = st.columns(2)
            c1.write(f"**Role:** {p['role']}")
            c1.write(f"**Contact:** {p['contact']}")
            c2.metric("SLA Performance", p['sla'])
            c2.progress(int(p['sla'].strip('%')))

def section_financials():
    st.title("Financials & Commission")
    st.markdown("Track Gross Transaction Value (GTV) and Platform Revenue.")
    
    df = db.load_orders()
    inv = db.load_inventory()
    
    # Merge orders with inventory to get commission rates
    merged = pd.merge(df, inv[['Product Name', 'Commission %']], left_on='Product', right_on='Product Name', how='left')
    merged['Commission Revenue'] = merged['Amount'] * (merged['Commission %'] / 100)
    
    st.dataframe(merged[['Order ID', 'Brand', 'Amount', 'Commission %', 'Commission Revenue']], use_container_width=True)
    
    total_comm = merged['Commission Revenue'].sum()
    st.markdown(f"### Total Platform Revenue: ₺{total_comm:,.2f}")

def section_crm():
    st.title("Customer Relations (CRM)")
    st.markdown("High-Trust client database.")
    
    df = db.load_orders()
    
    # Group by customer
    cust_df = df.groupby('Customer').agg({
        'Order ID': 'count',
        'Amount': 'sum',
        'Date': 'max'
    }).rename(columns={'Order ID': 'Total Orders', 'Amount': 'Lifetime Value', 'Date': 'Last Active'})
    
    st.dataframe(cust_df, use_container_width=True)

def section_settings():
    st.title("System Settings")
    
    st.subheader("Admin Configuration")
    st.text_input("Admin Email", value="founders@natuvisio.com")
    st.text_input("Change Password", type="password")
    
    st.subheader("Data Management")
    if st.button("Export All Data (CSV)"):
        st.info("Exporting database...")
        
    st.subheader("System Logs")
    st.code("""
    [INFO] 2023-10-27 10:00:01 - System Startup
    [INFO] 2023-10-27 10:05:23 - Order NV-1004 created
    [WARN] 2023-10-27 11:20:00 - Auroraco latency > 500ms
    """)

# --- 6. MAIN APP LOGIC ---
def main():
    load_css()
    
    if not st.session_state.logged_in:
        login_screen()
        return

    # Sidebar Navigation
    with st.sidebar:
        st.markdown("## NATUVISIO")
        st.markdown("*Strategic Platform Architecture*")
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

    # Routing
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
