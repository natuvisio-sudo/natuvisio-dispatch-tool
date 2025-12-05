import streamlit as st
import pandas as pd
from datetime import datetime
import os
import urllib.parse

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Admin HQ | NATUVISIO Bridge",
    page_icon="🎯",
    layout="wide"
)

# --- 2. CSS & STYLING ---
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
    
    .stApp {
        background: var(--nv-pearl);
    }
    
    /* Header */
    .nv-admin-header {
        background: linear-gradient(135deg, #183315 0%, #2d4a2b 100%);
        color: var(--nv-cream);
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(24, 51, 21, 0.2);
    }
    
    .nv-admin-title {
        font-family: var(--font-serif);
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .nv-admin-subtitle {
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
    
    /* Buttons */
    .stButton > button {
        background: var(--nv-forest) !important;
        color: var(--nv-cream) !important;
        border: none !important;
        padding: 0.75rem 2rem !important;
        border-radius: 50px !important;
        font-family: var(--font-sans) !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 16px rgba(24, 51, 21, 0.2) !important;
    }
    
    .stButton > button:hover {
        background: var(--nv-sage) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea,
    .stNumberInput > div > div > input {
        border-radius: 8px !important;
        border: 2px solid #e0e0e0 !important;
        font-family: var(--font-sans) !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--nv-forest) !important;
        box-shadow: 0 0 0 2px rgba(24, 51, 21, 0.1) !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- 3. DATABASE FUNCTIONS ---
CSV_FILE = 'dispatch_history.csv'

def load_dispatch_history():
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    else:
        return pd.DataFrame(columns=[
            'order_id', 'brand', 'sku', 'quantity', 'customer_name', 
            'phone', 'timestamp', 'status', 'tracking_number'
        ])

def save_dispatch_history(df):
    df.to_csv(CSV_FILE, index=False)

# --- 4. AUTHENTICATION ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

def check_password():
    load_css()
    
    st.markdown("""
    <div class="nv-admin-header">
        <div class="nv-admin-title">
            <span>🎯</span> Admin HQ
        </div>
        <div class="nv-admin-subtitle">
            Command Center · Order Generation · Network Orchestration
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="nv-card">', unsafe_allow_html=True)
    st.markdown('<h3 class="nv-card-title">🔐 Secure Access</h3>', unsafe_allow_html=True)
    
    password = st.text_input("Enter Admin Password", type="password", key="admin_pass")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Access Admin HQ", use_container_width=True):
            if password == "admin2025":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid password")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Back to Landing Page
    if st.button("← Back to Main Menu"):
        st.switch_page("streamlit_app.py")

# --- 5. MAIN ADMIN INTERFACE ---
def admin_interface():
    load_css()
    
    # Header
    st.markdown("""
    <div class="nv-admin-header">
        <div class="nv-admin-title">
            <span>🎯</span> Admin HQ
        </div>
        <div class="nv-admin-subtitle">
            Command Center · Order Generation · Network Orchestration
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 New Dispatch",
        "📊 Active Orders",
        "📈 Analytics",
        "⚙️ Settings"
    ])
    
    # TAB 1: New Dispatch
    with tab1:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="nv-card-title">Create New Dispatch Order</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Order Details")
            
            brand = st.selectbox(
                "Select Brand Partner",
                ["Longevicals", "Haki Heal", "Auroraco"],
                key="brand_select"
            )
            
            # Brand-specific SKUs
            sku_options = {
                "Longevicals": ["NMN 500mg", "NMN 1000mg", "Resveratrol"],
                "Haki Heal": ["Matcha Premium", "Matcha Classic", "Green Tea Extract"],
                "Auroraco": ["Lavender Oil", "Rose Oil", "Bergamot Oil"]
            }
            
            sku = st.selectbox(
                "Select SKU",
                sku_options.get(brand, []),
                key="sku_select"
            )
            
            quantity = st.number_input("Quantity", min_value=1, value=1)
            
            cold_chain = st.checkbox("🧊 Cold Chain Required") if brand == "Longevicals" else False
            
        with col2:
            st.subheader("Customer Information")
            
            customer_name = st.text_input("Customer Name")
            phone = st.text_input("Phone Number (Format: 90532XXXXXXX)")
            address = st.text_area("Delivery Address", height=100)
            notes = st.text_area("Special Instructions")
        
        st.markdown("---")
        
        # Dispatch Logic
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("⚡ Generate Dispatch Order", use_container_width=True):
                if customer_name and phone:
                    # Create order
                    order_id = f"NV{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    
                    # Generate WhatsApp message content
                    whatsapp_msg = f"""*NATUVISIO DISPATCH ORDER*
━━━━━━━━━━━━━━━━━━━
🆔 Order ID: {order_id}
📦 Brand: {brand}
🏷️ SKU: {sku}
🔢 Quantity: {quantity}
{'🧊 COLD CHAIN PRIORITY' if cold_chain else ''}

👤 Customer: {customer_name}
📞 Phone: {phone}
🏠 Address: {address}

📝 Notes: {notes}
━━━━━━━━━━━━━━━━━━━
Please Pack & Ship Immediately. Confirm Tracking."""
                    
                    # Save to CSV history
                    df = load_dispatch_history()
                    new_row = pd.DataFrame([{
                        'order_id': order_id,
                        'brand': brand,
                        'sku': sku,
                        'quantity': quantity,
                        'customer_name': customer_name,
                        'phone': phone,
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'status': 'Pending',
                        'tracking_number': ''
                    }])
                    
                    # Concat and Save
                    df = pd.concat([df, new_row], ignore_index=True)
                    save_dispatch_history(df)
                    
                    # Display success
                    st.success(f"✅ Order {order_id} created successfully!")
                    
                    # Display Raw Message for Review
                    st.markdown("### 📱 Flash Dispatch Preview")
                    st.code(whatsapp_msg, language=None)
                    
                    # Generate Robust WhatsApp Deep Link
                    encoded_msg = urllib.parse.quote(whatsapp_msg)
                    clean_phone = phone.replace("+", "").replace(" ", "")
                    whatsapp_link = f"https://wa.me/{clean_phone}?text={encoded_msg}"
                    
                    # Clickable Button
                    st.markdown(f"""
                    <a href="{whatsapp_link}" target="_blank" style="text-decoration: none;">
                        <div style="background: #25D366; color: white; padding: 15px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 18px; box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);">
                            📲 OPEN IN WHATSAPP
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.error("⚠️ Please fill in Customer Name and Phone Number")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 2: Active Orders
    with tab2:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="nv-card-title">Active Dispatch Orders</h3>', unsafe_allow_html=True)
        
        df = load_dispatch_history()
        
        if not df.empty:
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                brand_filter = st.multiselect(
                    "Filter by Brand",
                    options=df['brand'].unique().tolist(),
                    default=df['brand'].unique().tolist()
                )
            with col2:
                status_filter = st.multiselect(
                    "Filter by Status",
                    options=df['status'].unique().tolist(),
                    default=df['status'].unique().tolist()
                )
            
            # Apply filters
            filtered_df = df[
                (df['brand'].isin(brand_filter)) &
                (df['status'].isin(status_filter))
            ]
            
            # Display dataframe
            st.dataframe(
                filtered_df.sort_values('timestamp', ascending=False),
                use_container_width=True,
                hide_index=True
            )
            
            # Quick stats
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Orders", len(filtered_df))
            c2.metric("Pending", len(filtered_df[filtered_df['status'] == 'Pending']))
            c3.metric("Shipped", len(filtered_df[filtered_df['status'] == 'Shipped']))
            c4.metric("Delivered", len(filtered_df[filtered_df['status'] == 'Delivered']))
        else:
            st.info("No orders yet. Create your first dispatch order!")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 3: Analytics
    with tab3:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="nv-card-title">Network Performance Analytics</h3>', unsafe_allow_html=True)
        
        df = load_dispatch_history()
        
        if not df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Orders by Brand")
                brand_counts = df['brand'].value_counts()
                st.bar_chart(brand_counts)
            
            with col2:
                st.subheader("Order Status Distribution")
                status_counts = df['status'].value_counts()
                st.bar_chart(status_counts)
            
            # Recent activity
            st.subheader("Recent Activity Log")
            st.dataframe(
                df.sort_values('timestamp', ascending=False).head(10),
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("No data available for analytics")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # TAB 4: Settings
    with tab4:
        st.markdown('<div class="nv-card">', unsafe_allow_html=True)
        st.markdown('<h3 class="nv-card-title">System Settings</h3>', unsafe_allow_html=True)
        
        st.subheader("Partner Configuration")
        
        partners = [
            {"name": "Longevicals", "status": "Active", "password": "longsci"},
            {"name": "Haki Heal", "status": "Active", "password": "haki123"},
            {"name": "Auroraco", "status": "Active", "password": "aurora2025"}
        ]
        
        for partner in partners:
            with st.expander(f"🌱 {partner['name']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.text(f"Status: {partner['status']}")
                    st.text(f"Portal Password: {partner['password']}")
                with col2:
                    st.text("Integration: WhatsApp API")
                    st.text("Cold Chain: " + ("Yes" if partner['name'] == "Longevicals" else "No"))
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Logout
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# --- 6. EXECUTION ---
if not st.session_state.logged_in:
    check_password()
else:
    admin_interface()
