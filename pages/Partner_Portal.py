import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Page config
st.set_page_config(
    page_title="Partner Portal | NATUVISIO Bridge",
    page_icon="📦",
    layout="wide"
)

# Load custom CSS
def load_css():
    css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    :root {
        --nv-forest: #183315;
        --nv-sage: #2d4a2b;
        --nv-moss: #4a6b45;
        --nv-cream: #f3f3ec;
        --nv-pearl: #fafaf5;
        --font-serif: 'Lora', Georgia, serif;
        --font-sans: 'Inter', -apple-system, sans-serif;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main {
        background: var(--nv-pearl);
    }
    
    /* Header */
    .nv-partner-header {
        background: linear-gradient(135deg, #2d4a2b 0%, #4a6b45 100%);
        color: var(--nv-cream);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(45, 74, 43, 0.2);
    }
    
    .nv-partner-title {
        font-family: var(--font-serif);
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .nv-partner-subtitle {
        font-family: var(--font-sans);
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Cards */
    .nv-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        box-shadow: 0 4px 16px rgba(24, 51, 21, 0.08);
        margin-bottom: 1.5rem;
    }
    
    .nv-card-title {
        font-family: var(--font-serif);
        font-size: 1.5rem;
        color: var(--nv-forest);
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    /* Order cards */
    .nv-order-card {
        background: white;
        border-left: 4px solid var(--nv-moss);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(24, 51, 21, 0.08);
        transition: transform 0.2s ease;
    }
    
    .nv-order-card:hover {
        transform: translateX(4px);
    }
    
    .nv-order-id {
        font-family: var(--font-sans);
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--nv-forest);
        margin-bottom: 0.5rem;
    }
    
    .nv-order-details {
        font-family: var(--font-sans);
        font-size: 0.95rem;
        color: var(--nv-sage);
        line-height: 1.6;
    }
    
    /* Status badges */
    .nv-status-badge {
        display: inline-block;
        padding: 0.4rem 0.9rem;
        border-radius: 20px;
        font-family: var(--font-sans);
        font-size: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        margin-top: 0.5rem;
    }
    
    .nv-status-pending {
        background: #fff3cd;
        color: #856404;
    }
    
    .nv-status-processing {
        background: #cce5ff;
        color: #004085;
    }
    
    .nv-status-shipped {
        background: #d4edda;
        color: #155724;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--nv-moss) !important;
        color: white !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important;
        font-family: var(--font-sans) !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(74, 107, 69, 0.2) !important;
    }
    
    .stButton > button:hover {
        background: var(--nv-sage) !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Initialize session state
if 'partner_logged_in' not in st.session_state:
    st.session_state.partner_logged_in = False
if 'partner_brand' not in st.session_state:
    st.session_state.partner_brand = None

# Password check
def check_password():
    load_css()
    
    st.markdown("""
    <div class="nv-partner-header">
        <div class="nv-partner-title">
            <span>📦</span> Partner Portal
        </div>
        <div class="nv-partner-subtitle">
            Fulfillment Center · Order Tracking · Real-Time Updates
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="nv-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="nv-card-title">🔐 Brand Partner Access</h3>', unsafe_allow_html=True)
    
    brand = st.selectbox(
        "Select Your Brand",
        ["Longevicals", "Haki Heal", "Auroraco"],
        key="brand_select"
    )
    
    password = st.text_input("Enter Partner Password", type="password", key="partner_pass")
    
    # Password mapping
    passwords = {
        "Longevicals": "longsci",
        "Haki Heal": "haki123",
        "Auroraco": "aurora2025"
    }
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Access Partner Portal", use_container_width=True):
            if password == passwords[brand]:
                st.session_state.partner_logged_in = True
                st.session_state.partner_brand = brand
                st.rerun()
            else:
                st.error("❌ Invalid password")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("← Back to Main Menu"):
        st.switch_page("streamlit_app.py")

# Load dispatch history
def load_dispatch_history():
    if os.path.exists('dispatch_history.csv'):
        return pd.read_csv('dispatch_history.csv')
    else:
        return pd.DataFrame(columns=[
            'order_id', 'brand', 'sku', 'quantity', 'customer_name', 
            'phone', 'timestamp', 'status', 'tracking_number'
        ])

def save_dispatch_history(df):
    df.to_csv('dispatch_history.csv', index=False)

# Partner interface
def partner_interface():
    load_css()
    
    brand = st.session_state.partner_brand
    
    # Header
    st.markdown(f"""
    <div class="nv-partner-header">
        <div class="nv-partner-title">
            <span>🌱</span> {brand} Portal
        </div>
        <div class="nv-partner-subtitle">
            Fulfillment Center · Pack & Ship Orders
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load orders for this brand
    df = load_dispatch_history()
    brand_orders = df[df['brand'] == brand].copy()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "📋 Pending Orders",
        "📦 In Process",
        "✅ Completed"
    ])
    
    # TAB 1: Pending Orders
    with tab1:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="nv-card-title">Orders Awaiting Fulfillment</h3>', unsafe_allow_html=True)
        
        pending = brand_orders[brand_orders['status'] == 'Pending']
        
        if not pending.empty:
            st.info(f"📊 {len(pending)} orders pending fulfillment")
            
            for idx, row in pending.iterrows():
                with st.expander(f"🔔 {row['order_id']} - {row['sku']} × {row['quantity']}", expanded=True):
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown(f"""
                        **Order Details**
                        - Order ID: `{row['order_id']}`
                        - SKU: {row['sku']}
                        - Quantity: {row['quantity']}
                        - Date: {row['timestamp']}
                        """)
                    
                    with col2:
                        st.markdown(f"""
                        **Customer Information**
                        - Name: {row['customer_name']}
                        - Phone: {row['phone']}
                        """)
                    
                    # Actions
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"📦 Start Processing", key=f"process_{idx}"):
                            df.loc[idx, 'status'] = 'Processing'
                            save_dispatch_history(df)
                            st.success("Order moved to processing!")
                            st.rerun()
                    
                    with col2:
                        if st.button(f"✅ Mark as Shipped", key=f"ship_{idx}"):
                            tracking = st.text_input(
                                "Enter Tracking Number",
                                key=f"tracking_{idx}"
                            )
                            if tracking:
                                df.loc[idx, 'status'] = 'Shipped'
                                df.loc[idx, 'tracking_number'] = tracking
                                save_dispatch_history(df)
                                st.success(f"Order shipped! Tracking: {tracking}")
                                st.rerun()
        else:
            st.success("✨ All caught up! No pending orders.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 2: In Process
    with tab2:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="nv-card-title">Orders Being Processed</h3>', unsafe_allow_html=True)
        
        processing = brand_orders[brand_orders['status'] == 'Processing']
        
        if not processing.empty:
            st.info(f"⚙️ {len(processing)} orders in process")
            
            for idx, row in processing.iterrows():
                st.markdown(f"""
                <div class="nv-order-card">
                    <div class="nv-order-id">📦 {row['order_id']}</div>
                    <div class="nv-order-details">
                        <strong>{row['sku']}</strong> × {row['quantity']}<br/>
                        Customer: {row['customer_name']}<br/>
                        Started: {row['timestamp']}
                    </div>
                    <span class="nv-status-badge nv-status-processing">⚙️ PROCESSING</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Ship action
                with st.expander(f"Ship Order {row['order_id']}"):
                    tracking = st.text_input(
                        "Enter Tracking Number",
                        key=f"track_process_{idx}"
                    )
                    
                    if st.button(f"Ship Order", key=f"ship_process_{idx}"):
                        if tracking:
                            df.loc[idx, 'status'] = 'Shipped'
                            df.loc[idx, 'tracking_number'] = tracking
                            save_dispatch_history(df)
                            st.success(f"Order shipped! Tracking: {tracking}")
                            st.rerun()
                        else:
                            st.error("Please enter a tracking number")
        else:
            st.info("No orders currently being processed")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 3: Completed
    with tab3:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="nv-card-title">Shipped Orders</h3>', unsafe_allow_html=True)
        
        shipped = brand_orders[brand_orders['status'].isin(['Shipped', 'Delivered'])]
        
        if not shipped.empty:
            st.success(f"✅ {len(shipped)} orders completed")
            
            # Display as table
            st.dataframe(
                shipped[['order_id', 'sku', 'quantity', 'customer_name', 'tracking_number', 'timestamp']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No shipped orders yet")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown('<div class="nv-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="nv-card-title">📈 Performance Metrics</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Orders", len(brand_orders))
    with col2:
        st.metric("Pending", len(brand_orders[brand_orders['status'] == 'Pending']))
    with col3:
        st.metric("Processing", len(brand_orders[brand_orders['status'] == 'Processing']))
    with col4:
        st.metric("Shipped", len(brand_orders[brand_orders['status'] == 'Shipped']))
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Logout
    if st.button("🚪 Logout"):
        st.session_state.partner_logged_in = False
        st.session_state.partner_brand = None
        st.rerun()

# Main execution
if not st.session_state.partner_logged_in:
    check_password()
else:
    partner_interface()
