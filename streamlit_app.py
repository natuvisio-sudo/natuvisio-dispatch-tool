import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🏔️ NATUVISIO ADMIN OS - ENHANCED EDITION
# Zero Errors | Super Efficient | Complete Features
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Admin OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# 1. CONFIGURATION & SETUP
# ============================================================================

# Constants
ADMIN_PASS = "admin2025"
CSV_FILE = "dispatch_history.csv"
CSV_PAYMENTS = "brand_payments.csv"
PHI = 1.618  # Golden Ratio

# Spacing System (Fibonacci)
FIBO = {
    'xs': 8,
    'sm': 13,
    'md': 21,
    'lg': 34,
    'xl': 55
}

# Enhanced Data Map with Commission Rates
DISPATCH_MAP = {
    "HAKI HEAL": {
        "phone": "601158976276",
        "color": "#4ECDC4",
        "commission": 0.15,  # 15%
        "iban": "TR90 0006 1000 0000 1234 5678 90",
        "products": {
            "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM-01", "price": 450},
            "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY-01", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP-01", "price": 120}
        }
    },
    "AURORACO": {
        "phone": "601158976276",
        "color": "#FF6B6B",
        "commission": 0.20,  # 20%
        "iban": "TR90 0006 2000 0000 9876 5432 10",
        "products": {
            "AURORACO MATCHA EZMESI": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO KAKAO EZMESI": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SUPER GIDA": {"sku": "SKU-AUR-SUPER", "price": 800}
        }
    },
    "LONGEVICALS": {
        "phone": "601158976276",
        "color": "#95E1D3",
        "commission": 0.12,  # 12%
        "iban": "TR90 0001 5000 0000 1122 3344 55",
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
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
# 3. ENHANCED DESIGN SYSTEM (CSS)
# ============================================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* === CORE FOUNDATION === */
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}

    /* BACKGROUND */
    .stApp {{
        background-image: linear-gradient(rgba(15, 23, 42, 0.88), rgba(15, 23, 42, 0.92)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Inter', -apple-system, sans-serif;
        color: #ffffff;
    }}
    
    .main {{
        padding: {FIBO['md']}px;
    }}
    
    .block-container {{
        padding-top: {FIBO['md']}px !important;
        max-width: 100% !important;
    }}

    /* === GLASS MORPHISM === */
    .glass-card {{
        background: rgba(255, 255, 255, 0.06);
        backdrop-filter: blur({FIBO['md']}px) saturate(180%);
        -webkit-backdrop-filter: blur({FIBO['md']}px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: {FIBO['sm']}px;
        padding: {FIBO['md']}px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        margin-bottom: {FIBO['sm']}px;
        transition: all 0.3s ease;
    }}
    
    .glass-card:hover {{
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.15);
        transform: translateY(-1px);
    }}

    /* === ORDER CARDS WITH STATUS GLOW === */
    .order-card {{
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur({FIBO['sm']}px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: {FIBO['sm']}px;
        padding: {FIBO['md']}px;
        margin-bottom: {FIBO['sm']}px;
        transition: all 0.3s ease;
    }}
    
    .order-card-red {{
        border-left: 4px solid #EF4444;
        animation: pulse-red 2s infinite;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.3);
    }}
    
    .order-card-green {{
        border-left: 4px solid #10B981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.2);
    }}
    
    @keyframes pulse-red {{
        0%, 100% {{ box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }}
        50% {{ box-shadow: 0 0 40px rgba(239, 68, 68, 0.5); }}
    }}

    /* === TIMELINE === */
    .timeline-container {{
        display: flex;
        justify-content: space-between;
        position: relative;
        margin: {FIBO['sm']}px 0;
        padding: {FIBO['sm']}px 0;
    }}
    
    .timeline-line {{
        position: absolute;
        top: {FIBO['sm']}px;
        left: 0;
        width: 100%;
        height: 2px;
        background: rgba(255, 255, 255, 0.1);
        z-index: 0;
    }}
    
    .timeline-step {{
        position: relative;
        z-index: 1;
        text-align: center;
        flex: 1;
    }}
    
    .timeline-dot {{
        width: {FIBO['sm']}px;
        height: {FIBO['sm']}px;
        background: rgba(255, 255, 255, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        margin: 0 auto {FIBO['xs']}px;
        transition: all 0.3s ease;
    }}
    
    .timeline-step.active .timeline-dot {{
        background: #4ECDC4;
        border-color: #4ECDC4;
        box-shadow: 0 0 15px #4ECDC4;
    }}
    
    .timeline-step-label {{
        font-size: 10px;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .timeline-step.active .timeline-step-label {{
        color: #4ECDC4;
        font-weight: 700;
    }}

    /* === TYPOGRAPHY === */
    h1, h2, h3, h4, h5 {{
        font-family: 'Space Grotesk', sans-serif !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
    }}
    
    .metric-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: {FIBO['lg']}px;
        font-weight: 800;
        color: #ffffff;
        line-height: 1;
        margin-bottom: {FIBO['xs']}px;
    }}
    
    .metric-label {{
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
    }}

    /* === STATUS BADGES === */
    .status-badge {{
        display: inline-block;
        padding: 6px {FIBO['sm']}px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        backdrop-filter: blur({FIBO['xs']}px);
    }}
    
    .status-pending {{
        background: rgba(251, 191, 36, 0.2);
        color: #FCD34D;
        border: 1px solid rgba(251, 191, 36, 0.4);
    }}
    
    .status-notified {{
        background: rgba(59, 130, 246, 0.2);
        color: #60A5FA;
        border: 1px solid rgba(59, 130, 246, 0.4);
    }}
    
    .status-dispatched {{
        background: rgba(16, 185, 129, 0.2);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.4);
    }}
    
    .status-completed {{
        background: rgba(139, 92, 246, 0.2);
        color: #A78BFA;
        border: 1px solid rgba(139, 92, 246, 0.4);
    }}

    /* === INPUTS === */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {{
        background: rgba(0, 0, 0, 0.3) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: {FIBO['xs']}px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {{
        background: rgba(0, 0, 0, 0.4) !important;
        border-color: rgba(78, 205, 196, 0.5) !important;
        box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.1) !important;
    }}
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: rgba(255, 255, 255, 0.4) !important;
    }}

    /* === BUTTONS === */
    div.stButton > button {{
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%) !important;
        color: #ffffff !important;
        border: none !important;
        padding: {FIBO['sm']}px {FIBO['md']}px !important;
        border-radius: {FIBO['xs']}px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 600 !important;
        font-size: {FIBO['sm']}px !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 15px rgba(78, 205, 196, 0.3) !important;
        width: 100% !important;
    }}
    
    div.stButton > button:hover {{
        background: linear-gradient(135deg, #44A08D 0%, #4ECDC4 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(78, 205, 196, 0.4) !important;
    }}
    
    div.stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* === DATA TABLES === */
    .dataframe {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur({FIBO['sm']}px);
        border-radius: {FIBO['xs']}px !important;
        overflow: hidden;
    }}
    
    .dataframe thead tr th {{
        background: rgba(255, 255, 255, 0.08) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        padding: {FIBO['sm']}px !important;
        border-bottom: 2px solid rgba(78, 205, 196, 0.3) !important;
    }}
    
    .dataframe tbody tr td {{
        background: rgba(255, 255, 255, 0.02) !important;
        color: rgba(255, 255, 255, 0.9) !important;
        padding: {FIBO['xs']}px {FIBO['sm']}px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}
    
    .dataframe tbody tr:hover td {{
        background: rgba(255, 255, 255, 0.06) !important;
    }}

    /* === TABS === */
    .stTabs [data-baseweb="tab-list"] {{
        gap: {FIBO['xs']}px;
        background: rgba(0, 0, 0, 0.2);
        padding: {FIBO['xs']}px;
        border-radius: {FIBO['xs']}px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: {FIBO['xs']}px;
        padding: {FIBO['xs']}px {FIBO['md']}px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 600;
        font-size: {FIBO['sm']}px;
        border: 1px solid transparent;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: linear-gradient(135deg, rgba(78, 205, 196, 0.2), rgba(78, 205, 196, 0.1)) !important;
        color: #4ECDC4 !important;
        border-color: rgba(78, 205, 196, 0.3) !important;
        box-shadow: 0 0 20px rgba(78, 205, 196, 0.2);
    }}

    /* === HIDE STREAMLIT === */
    #MainMenu, header, footer {{ visibility: hidden; }}
    
    /* === SCROLLBAR === */
    ::-webkit-scrollbar {{
        width: {FIBO['xs']}px;
        height: {FIBO['xs']}px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: rgba(255, 255, 255, 0.05);
        border-radius: {FIBO['xs']}px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: rgba(78, 205, 196, 0.3);
        border-radius: {FIBO['xs']}px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(78, 205, 196, 0.5);
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# 4. DATABASE & STATE MANAGEMENT
# ============================================================================

# Initialize Session State
if 'admin_logged_in' not in st.session_state:
    st.session_state.admin_logged_in = False
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state:
    st.session_state.selected_brand_lock = None

# Database Functions
def init_databases():
    """Initialize all required databases"""
    # Dispatch History
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=[
            "Order_ID", "Time", "Brand", "Customer", "Phone", "Address", 
            "Items", "Total_Value", "Commission_Rate", "Commission_Amt", 
            "Brand_Payout", "Status", "WhatsApp_Sent", "Tracking_Num", "Notes"
        ])
        df.to_csv(CSV_FILE, index=False)
    
    # Brand Payments
    if not os.path.exists(CSV_PAYMENTS):
        df = pd.DataFrame(columns=[
            "Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", "Notes"
        ])
        df.to_csv(CSV_PAYMENTS, index=False)

def load_history():
    """Load dispatch history with error handling"""
    try:
        if os.path.exists(CSV_FILE):
            return pd.read_csv(CSV_FILE)
    except Exception as e:
        st.error(f"Database error: {e}")
    return pd.DataFrame(columns=[
        "Order_ID", "Time", "Brand", "Customer", "Phone", "Address",
        "Items", "Total_Value", "Commission_Rate", "Commission_Amt",
        "Brand_Payout", "Status", "WhatsApp_Sent", "Tracking_Num", "Notes"
    ])

def save_to_history(new_entry):
    """Save entry to history with validation"""
    try:
        df = load_history()
        new_df = pd.DataFrame([new_entry])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Save error: {e}")
        return False

def update_history(df):
    """Update entire history dataframe"""
    try:
        df.to_csv(CSV_FILE, index=False)
        return True
    except Exception as e:
        st.error(f"Update error: {e}")
        return False

def load_payments():
    """Load payment records"""
    try:
        if os.path.exists(CSV_PAYMENTS):
            return pd.read_csv(CSV_PAYMENTS)
    except Exception as e:
        st.error(f"Payment load error: {e}")
    return pd.DataFrame(columns=[
        "Payment_ID", "Time", "Brand", "Amount", "Method", "Reference", "Notes"
    ])

def save_payment(payment_data):
    """Save payment record"""
    try:
        df = load_payments()
        new_df = pd.DataFrame([payment_data])
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_csv(CSV_PAYMENTS, index=False)
        return True
    except Exception as e:
        st.error(f"Payment save error: {e}")
        return False

# Analytics Functions
def get_metrics():
    """Calculate dashboard metrics efficiently"""
    df = load_history()
    
    if df.empty:
        return {
            'total_orders': 0,
            'total_revenue': 0,
            'total_commission': 0,
            'pending_approval': 0,
            'pending_dispatch': 0,
            'today_orders': 0
        }
    
    try:
        df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
        today = datetime.now().date()
        
        return {
            'total_orders': len(df),
            'total_revenue': df['Total_Value'].sum() if 'Total_Value' in df.columns else 0,
            'total_commission': df['Commission_Amt'].sum() if 'Commission_Amt' in df.columns else 0,
            'pending_approval': len(df[df['WhatsApp_Sent'] == 'NO']) if 'WhatsApp_Sent' in df.columns else 0,
            'pending_dispatch': len(df[df['Status'] == 'Notified']) if 'Status' in df.columns else 0,
            'today_orders': len(df[df['Time'].dt.date == today])
        }
    except Exception as e:
        st.error(f"Metrics calculation error: {e}")
        return {
            'total_orders': 0,
            'total_revenue': 0,
            'total_commission': 0,
            'pending_approval': 0,
            'pending_dispatch': 0,
            'today_orders': 0
        }

# ============================================================================
# 5. AUTHENTICATION VIEW
# ============================================================================

def login_screen():
    """Premium login interface"""
    st.markdown("<div style='height: 15vh'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['xl']}px;">
            <div style="font-size: {FIBO['xl']}px; margin-bottom: {FIBO['sm']}px;">🏔️</div>
            <h2 style="margin-bottom: {FIBO['xs']}px;">ADMIN OS</h2>
            <p style="color: rgba(255, 255, 255, 0.6); font-size: 12px; letter-spacing: 0.1em;">
                NATUVISIO LOGISTICS COMMAND
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        password = st.text_input("Access Key", type="password", key="login_pass", label_visibility="collapsed", placeholder="Enter access key")
        
        col_b1, col_b2 = st.columns(2)
        
        with col_b1:
            if st.button("🔓 UNLOCK", use_container_width=True):
                if password == ADMIN_PASS:
                    st.session_state.admin_logged_in = True
                    st.rerun()
                else:
                    st.error("❌ ACCESS DENIED")
        
        with col_b2:
            if st.button("🚪 EXIT", use_container_width=True):
                try:
                    st.switch_page("streamlit_app.py")
                except:
                    st.info("Main app not found. Use logout to return.")

# ============================================================================
# 6. DASHBOARD VIEW
# ============================================================================

def dashboard_screen():
    """Enhanced dashboard with all features"""
    
    # Initialize databases
    init_databases()
    
    # === HEADER ===
    col_h1, col_h2 = st.columns([6, 1])
    
    with col_h1:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: {FIBO['sm']}px;">
            {get_icon('mountain', '#4ECDC4', FIBO['lg'])}
            <div>
                <h1 style="margin: 0; font-size: {FIBO['xl']}px;">ADMIN HQ</h1>
                <span style="font-size: 12px; color: rgba(255, 255, 255, 0.6); letter-spacing: 0.1em;">
                    LOGISTICS COMMAND CENTER
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_h2:
        if st.button("🚪 LOGOUT"):
            st.session_state.admin_logged_in = False
            st.session_state.cart = []
            st.session_state.selected_brand_lock = None
            st.rerun()
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # === METRICS ROW ===
    metrics = get_metrics()
    
    col_m1, col_m2, col_m3, col_m4, col_m5, col_m6 = st.columns(6)
    
    with col_m1:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px;">
            <div class="metric-value">{metrics['total_orders']}</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px;">
            <div class="metric-value">{metrics['total_revenue']:,.0f}₺</div>
            <div class="metric-label">Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m3:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px;">
            <div class="metric-value">{metrics['total_commission']:,.0f}₺</div>
            <div class="metric-label">Commission</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m4:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px; border-top: 3px solid #EF4444;">
            <div class="metric-value" style="color: #EF4444;">{metrics['pending_approval']}</div>
            <div class="metric-label">Need Approval</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m5:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px; border-top: 3px solid #F59E0B;">
            <div class="metric-value" style="color: #F59E0B;">{metrics['pending_dispatch']}</div>
            <div class="metric-label">Pending Ship</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_m6:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px; border-top: 3px solid #10B981;">
            <div class="metric-value" style="color: #10B981;">{metrics['today_orders']}</div>
            <div class="metric-label">Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
    
    # === MAIN TABS ===
    tabs = st.tabs([
        "🚀 NEW DISPATCH",
        "✅ PROCESSING",
        "📦 ALL ORDERS",
        "💰 FINANCIALS",
        "💳 PAYMENTS",
        "📈 ANALYTICS"
    ])
    
    # =======================================================================
    # TAB 1: NEW DISPATCH (WITH CART)
    # =======================================================================
    
    with tabs[0]:
        col_L, col_R = st.columns([PHI, 1])  # Golden Ratio
        
        with col_L:
            # Customer Information
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 👤 Customer Information")
            
            col_n, col_p = st.columns(2)
            with col_n:
                cust_name = st.text_input("Full Name", key="new_cust_name", placeholder="Customer name")
            with col_p:
                cust_phone = st.text_input("Phone", key="new_cust_phone", placeholder="+90 5XX XXX XXXX")
            
            cust_addr = st.text_area("Delivery Address", key="new_cust_addr", height=89, placeholder="Full delivery address")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Product Selection
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🛒 Product Selection")
            
            # Brand Lock Logic
            if st.session_state.cart:
                st.markdown(f"""
                <div style="background: rgba(78, 205, 196, 0.1); border: 1px solid rgba(78, 205, 196, 0.3); 
                     border-radius: {FIBO['xs']}px; padding: {FIBO['xs']}px {FIBO['sm']}px; margin-bottom: {FIBO['sm']}px;">
                    <span style="color: #4ECDC4;">🔒 Locked to: <strong>{st.session_state.selected_brand_lock}</strong></span>
                </div>
                """, unsafe_allow_html=True)
                active_brand = st.session_state.selected_brand_lock
            else:
                active_brand = st.selectbox("Select Brand", list(DISPATCH_MAP.keys()), key="brand_select")
            
            brand_data = DISPATCH_MAP[active_brand]
            products = list(brand_data["products"].keys())
            
            col_p, col_q = st.columns([3, 1])
            with col_p:
                selected_prod = st.selectbox("Product", products, key="product_select")
            with col_q:
                qty = st.number_input("Qty", min_value=1, value=1, key="qty_input")
            
            prod_details = brand_data["products"][selected_prod]
            
            # Show price and commission preview
            line_total = prod_details['price'] * qty
            comm_rate = brand_data['commission']
            comm_amt = line_total * comm_rate
            brand_payout = line_total - comm_amt
            
            st.markdown(f"""
            <div style="background: rgba(255, 255, 255, 0.05); border-radius: {FIBO['xs']}px; 
                 padding: {FIBO['xs']}px {FIBO['sm']}px; margin-top: {FIBO['xs']}px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: rgba(255, 255, 255, 0.6);">Price:</span>
                    <span style="color: #4ECDC4; font-weight: 700;">{line_total:,.0f} ₺</span>
                </div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                    <span style="color: rgba(255, 255, 255, 0.6);">Commission ({comm_rate*100:.0f}%):</span>
                    <span style="color: #FCD34D;">{comm_amt:,.0f} ₺</span>
                </div>
                <div style="display: flex; justify-content: space-between;">
                    <span style="color: rgba(255, 255, 255, 0.6);">Brand Payout:</span>
                    <span style="color: #95E1D3;">{brand_payout:,.0f} ₺</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("➕ ADD TO CART", key="add_cart"):
                st.session_state.cart.append({
                    "brand": active_brand,
                    "product": selected_prod,
                    "sku": prod_details['sku'],
                    "qty": qty,
                    "price": prod_details['price'],
                    "subtotal": line_total,
                    "comm_rate": comm_rate,
                    "comm_amt": comm_amt,
                    "brand_payout": brand_payout
                })
                st.session_state.selected_brand_lock = active_brand
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col_R:
            # Cart Review
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📦 Cart Review")
            
            if st.session_state.cart:
                # Display cart items
                for idx, item in enumerate(st.session_state.cart):
                    st.markdown(f"""
                    <div style="background: rgba(255, 255, 255, 0.05); border-radius: {FIBO['xs']}px; 
                         padding: {FIBO['sm']}px; margin-bottom: {FIBO['xs']}px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <div style="font-weight: 600;">{item['product']}</div>
                            <div style="font-weight: 700; color: #4ECDC4;">{item['subtotal']:,.0f}₺</div>
                        </div>
                        <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5);">
                            {item['sku']} × {item['qty']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Calculate totals
                total_value = sum(item['subtotal'] for item in st.session_state.cart)
                total_commission = sum(item['comm_amt'] for item in st.session_state.cart)
                total_payout = sum(item['brand_payout'] for item in st.session_state.cart)
                
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(78, 205, 196, 0.2), rgba(149, 225, 211, 0.1)); 
                     border: 1px solid rgba(78, 205, 196, 0.3); border-radius: {FIBO['xs']}px; 
                     padding: {FIBO['sm']}px; margin-top: {FIBO['sm']}px;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: {FIBO['xs']}px;">
                        <span style="font-weight: 600;">Total Value:</span>
                        <span style="font-weight: 800; font-size: {FIBO['md']}px; color: #4ECDC4;">{total_value:,.0f}₺</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; margin-bottom: 4px;">
                        <span style="color: rgba(255,255,255,0.7);">Commission:</span>
                        <span style="color: #FCD34D;">{total_commission:,.0f}₺</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px;">
                        <span style="color: rgba(255,255,255,0.7);">Brand Payout:</span>
                        <span style="color: #95E1D3;">{total_payout:,.0f}₺</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown(f"<div style='height: {FIBO['sm']}px'></div>", unsafe_allow_html=True)
                
                priority = st.selectbox(
                    "Order Priority",
                    ["Standard", "🚨 URGENT", "🧊 Cold Chain"],
                    key="priority_select"
                )
                
                if st.button("⚡ CREATE ORDER", type="primary", key="create_order"):
                    if cust_name and cust_phone:
                        # Generate Order
                        order_id = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                        items_str = ", ".join([f"{i['product']} (x{i['qty']})" for i in st.session_state.cart])
                        
                        # Save order with all financial data
                        order_data = {
                            'Order_ID': order_id,
                            'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'Brand': st.session_state.selected_brand_lock,
                            'Customer': cust_name,
                            'Phone': cust_phone,
                            'Address': cust_addr,
                            'Items': items_str,
                            'Total_Value': total_value,
                            'Commission_Rate': DISPATCH_MAP[st.session_state.selected_brand_lock]['commission'],
                            'Commission_Amt': total_commission,
                            'Brand_Payout': total_payout,
                            'Status': 'Pending',
                            'WhatsApp_Sent': 'NO',
                            'Tracking_Num': '',
                            'Notes': priority
                        }
                        
                        if save_to_history(order_data):
                            st.success(f"✅ Order {order_id} created successfully!")
                            
                            # Clear cart
                            st.session_state.cart = []
                            st.session_state.selected_brand_lock = None
                            
                            st.rerun()
                        else:
                            st.error("Failed to save order. Please try again.")
                    else:
                        st.error("⚠️ Please fill in customer name and phone!")
                
                if st.button("🗑️ Clear Cart", key="clear_cart"):
                    st.session_state.cart = []
                    st.session_state.selected_brand_lock = None
                    st.rerun()
            else:
                st.markdown(f"""
                <div style="text-align: center; padding: {FIBO['xl']}px;">
                    <div style="font-size: {FIBO['xl']}px; opacity: 0.3; margin-bottom: {FIBO['sm']}px;">🛒</div>
                    <div style="color: rgba(255, 255, 255, 0.5);">Cart is empty</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # =======================================================================
    # TAB 2: PROCESSING (RED/GREEN APPROVAL SYSTEM)
    # =======================================================================
    
    with tabs[1]:
        st.markdown("### ✅ Order Processing & Approval")
        
        df = load_history()
        
        if not df.empty:
            # Show orders that need action
            for idx, row in df.iterrows():
                # Determine card style
                card_class = "order-card-red" if row.get('WhatsApp_Sent', 'NO') == 'NO' else "order-card-green"
                
                st.markdown(f"""
                <div class="{card_class}">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: {FIBO['sm']}px;">
                        <div>
                            <h3 style="margin: 0;">{row['Order_ID']}</h3>
                            <div style="margin-top: {FIBO['xs']}px;">
                                <span class="status-badge status-{row['Status'].lower()}">{row['Status']}</span>
                            </div>
                        </div>
                        <div style="text-align: right;">
                            <h3 style="margin: 0;">{row['Total_Value']:,.0f} ₺</h3>
                            <div style="font-size: 11px; color: rgba(255, 255, 255, 0.5); margin-top: 4px;">
                                {row['Time']}
                            </div>
                        </div>
                    </div>
                    
                    <div style="background: rgba(0, 0, 0, 0.2); border-radius: {FIBO['xs']}px; padding: {FIBO['sm']}px; margin-bottom: {FIBO['sm']}px;">
                        <div style="margin-bottom: {FIBO['xs']}px;">
                            <strong>Brand:</strong> <span style="color: {DISPATCH_MAP[row['Brand']]['color']};">{row['Brand']}</span>
                        </div>
                        <div style="margin-bottom: {FIBO['xs']}px;">
                            <strong>Customer:</strong> {row['Customer']} | {row.get('Phone', 'N/A')}
                        </div>
                        <div style="margin-bottom: {FIBO['xs']}px;">
                            <strong>Address:</strong> {row.get('Address', 'N/A')}
                        </div>
                        <div style="margin-bottom: {FIBO['xs']}px;">
                            <strong>Items:</strong> {row['Items']}
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: {FIBO['xs']}px; margin-top: {FIBO['sm']}px; padding-top: {FIBO['sm']}px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5);">COMMISSION</div>
                                <div style="font-weight: 700; color: #FCD34D;">{row.get('Commission_Amt', 0):,.0f}₺</div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5);">PAYOUT</div>
                                <div style="font-weight: 700; color: #95E1D3;">{row.get('Brand_Payout', 0):,.0f}₺</div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5);">RATE</div>
                                <div style="font-weight: 700;">{row.get('Commission_Rate', 0)*100:.0f}%</div>
                            </div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Timeline
                steps = ["Pending", "Notified", "Dispatched", "Completed"]
                current_status = row['Status'] if row['Status'] in steps else "Pending"
                current_idx = steps.index(current_status)
                
                timeline_html = '<div class="timeline-container"><div class="timeline-line"></div>'
                for step_idx, step in enumerate(steps):
                    active_class = "active" if step_idx <= current_idx else ""
                    timeline_html += f'''
                    <div class="timeline-step {active_class}">
                        <div class="timeline-dot"></div>
                        <div class="timeline-step-label">{step}</div>
                    </div>
                    '''
                timeline_html += '</div>'
                st.markdown(timeline_html, unsafe_allow_html=True)
                
                # Action Buttons
                col_a1, col_a2, col_a3 = st.columns(3)
                
                with col_a1:
                    if row.get('WhatsApp_Sent', 'NO') == 'NO':
                        # WhatsApp Link
                        phone = DISPATCH_MAP[row['Brand']]['phone'].replace("+", "").replace(" ", "")
                        message = f"""*NATUVISIO DISPATCH*
━━━━━━━━━━━━━━━━━━━━
🆔 {row['Order_ID']}
━━━━━━━━━━━━━━━━━━━━

👤 {row['Customer']}
📞 {row.get('Phone', 'N/A')}
🏠 {row.get('Address', 'N/A')}

📦 ITEMS:
{row['Items']}

━━━━━━━━━━━━━━━━━━━━
💰 Total: {row['Total_Value']:,.0f}₺
💵 Your Payout: {row.get('Brand_Payout', 0):,.0f}₺

⚡ Please pack and ship immediately."""
                        
                        url = f"https://wa.me/{phone}?text={urllib.parse.quote(message)}"
                        
                        st.markdown(f"""
                        <a href="{url}" target="_blank" style="text-decoration: none;">
                            <div style="background: linear-gradient(135deg, #25D366, #128C7E); color: white; 
                                 padding: {FIBO['sm']}px; text-align: center; border-radius: {FIBO['xs']}px; 
                                 font-weight: 700; margin-bottom: {FIBO['xs']}px;">
                                📲 SEND WHATSAPP
                            </div>
                        </a>
                        """, unsafe_allow_html=True)
                        
                        if st.button("✅ Mark as Sent", key=f"approve_{idx}"):
                            df.at[idx, 'WhatsApp_Sent'] = 'YES'
                            df.at[idx, 'Status'] = 'Notified'
                            if update_history(df):
                                st.rerun()
                
                with col_a2:
                    if row['Status'] == 'Notified':
                        tracking = st.text_input("Tracking #", key=f"track_{idx}", placeholder="Enter tracking")
                        if st.button("📦 Mark Dispatched", key=f"dispatch_{idx}"):
                            if tracking:
                                df.at[idx, 'Tracking_Num'] = tracking
                                df.at[idx, 'Status'] = 'Dispatched'
                                if update_history(df):
                                    st.rerun()
                            else:
                                st.error("Enter tracking number!")
                
                with col_a3:
                    if row['Status'] == 'Dispatched':
                        if st.button("✅ Complete", key=f"complete_{idx}"):
                            df.at[idx, 'Status'] = 'Completed'
                            if update_history(df):
                                st.rerun()
                
                st.markdown("</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='height: {FIBO['sm']}px'></div>", unsafe_allow_html=True)
        else:
            st.info("No orders to process.")
    
    # =======================================================================
    # TAB 3: ALL ORDERS
    # =======================================================================
    
    with tabs[2]:
        st.markdown("### 📦 All Orders")
        
        df = load_history()
        
        if not df.empty:
            # Filters
            col_f1, col_f2, col_f3 = st.columns(3)
            
            with col_f1:
                brand_filter = st.multiselect(
                    "Brand",
                    options=df['Brand'].unique().tolist(),
                    default=df['Brand'].unique().tolist(),
                    key="order_brand_filter"
                )
            
            with col_f2:
                status_filter = st.multiselect(
                    "Status",
                    options=df['Status'].unique().tolist(),
                    default=df['Status'].unique().tolist(),
                    key="order_status_filter"
                )
            
            with col_f3:
                date_filter = st.selectbox(
                    "Date Range",
                    ["All Time", "Today", "This Week", "This Month"],
                    key="order_date_filter"
                )
            
            # Apply filters
            filtered_df = df[
                (df['Brand'].isin(brand_filter)) &
                (df['Status'].isin(status_filter))
            ].copy()
            
            # Date filtering
            if date_filter != "All Time":
                try:
                    filtered_df['Time'] = pd.to_datetime(filtered_df['Time'], errors='coerce')
                    today = datetime.now().date()
                    
                    if date_filter == "Today":
                        filtered_df = filtered_df[filtered_df['Time'].dt.date == today]
                    elif date_filter == "This Week":
                        week_ago = today - timedelta(days=7)
                        filtered_df = filtered_df[filtered_df['Time'].dt.date >= week_ago]
                    elif date_filter == "This Month":
                        month_ago = today - timedelta(days=30)
                        filtered_df = filtered_df[filtered_df['Time'].dt.date >= month_ago]
                except Exception as e:
                    st.error(f"Date filtering error: {e}")
            
            st.markdown(f"<div style='height: {FIBO['sm']}px'></div>", unsafe_allow_html=True)
            
            # Display
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.dataframe(
                filtered_df.sort_values('Time', ascending=False),
                use_container_width=True,
                hide_index=True
            )
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Summary
            col_s1, col_s2, col_s3 = st.columns(3)
            
            with col_s1:
                st.metric("Orders", len(filtered_df))
            with col_s2:
                st.metric("Total Value", f"{filtered_df['Total_Value'].sum():,.0f} ₺")
            with col_s3:
                avg_val = filtered_df['Total_Value'].mean() if len(filtered_df) > 0 else 0
                st.metric("Avg Value", f"{avg_val:,.0f} ₺")
        else:
            st.info("No orders yet.")
    
    # =======================================================================
    # TAB 4: FINANCIALS
    # =======================================================================
    
    with tabs[3]:
        st.markdown("### 💰 Financial Dashboard")
        
        df = load_history()
        
        if not df.empty:
            # Summary
            col_f1, col_f2, col_f3, col_f4 = st.columns(4)
            
            with col_f1:
                total_sales = df['Total_Value'].sum()
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px;">
                    <div class="metric-value">{total_sales:,.0f}₺</div>
                    <div class="metric-label">Total Sales</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_f2:
                total_comm = df['Commission_Amt'].sum()
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px; border-top: 3px solid #4ECDC4;">
                    <div class="metric-value" style="color: #4ECDC4;">{total_comm:,.0f}₺</div>
                    <div class="metric-label">Commission</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_f3:
                total_payout = df['Brand_Payout'].sum()
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px; border-top: 3px solid #95E1D3;">
                    <div class="metric-value" style="color: #95E1D3;">{total_payout:,.0f}₺</div>
                    <div class="metric-label">Brand Payout</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_f4:
                avg_rate = (total_comm / total_sales * 100) if total_sales > 0 else 0
                st.markdown(f"""
                <div class="glass-card" style="text-align: center; padding: {FIBO['sm']}px;">
                    <div class="metric-value">{avg_rate:.1f}%</div>
                    <div class="metric-label">Avg Rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
            
            # By Brand
            st.markdown("#### Commission by Brand")
            
            for brand in DISPATCH_MAP.keys():
                brand_df = df[df['Brand'] == brand]
                
                if not brand_df.empty:
                    brand_sales = brand_df['Total_Value'].sum()
                    brand_comm = brand_df['Commission_Amt'].sum()
                    brand_pay = brand_df['Brand_Payout'].sum()
                    brand_color = DISPATCH_MAP[brand]['color']
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4 style="color: {brand_color}; margin-bottom: {FIBO['sm']}px;">{brand}</h4>
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: {FIBO['md']}px;">
                            <div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5); margin-bottom: 4px;">SALES</div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700;">{brand_sales:,.0f}₺</div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5); margin-bottom: 4px;">COMMISSION</div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #4ECDC4;">{brand_comm:,.0f}₺</div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5); margin-bottom: 4px;">PAYOUT</div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #95E1D3;">{brand_pay:,.0f}₺</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No financial data yet.")
    
    # =======================================================================
    # TAB 5: PAYMENTS
    # =======================================================================
    
    with tabs[4]:
        st.markdown("### 💳 Payment Management")
        
        df_orders = load_history()
        df_payments = load_payments()
        
        if not df_orders.empty:
            for brand in DISPATCH_MAP.keys():
                brand_orders = df_orders[df_orders['Brand'] == brand]
                
                if not brand_orders.empty:
                    total_owed = brand_orders['Brand_Payout'].sum()
                    brand_payments = df_payments[df_payments['Brand'] == brand]
                    total_paid = brand_payments['Amount'].sum() if not brand_payments.empty else 0
                    balance = total_owed - total_paid
                    brand_color = DISPATCH_MAP[brand]['color']
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <div style="display: flex; justify-content: space-between; margin-bottom: {FIBO['md']}px;">
                            <div>
                                <h3 style="margin: 0; color: {brand_color};">{brand}</h3>
                                <div style="font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 4px;">
                                    {DISPATCH_MAP[brand]['iban']}
                                </div>
                            </div>
                        </div>
                        
                        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: {FIBO['md']}px; 
                             background: rgba(0,0,0,0.2); border-radius: {FIBO['xs']}px; padding: {FIBO['md']}px;">
                            <div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5); margin-bottom: 4px;">OWED</div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #F59E0B;">{total_owed:,.0f}₺</div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5); margin-bottom: 4px;">PAID</div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: #10B981;">{total_paid:,.0f}₺</div>
                            </div>
                            <div>
                                <div style="font-size: 10px; color: rgba(255,255,255,0.5); margin-bottom: 4px;">BALANCE</div>
                                <div style="font-size: {FIBO['md']}px; font-weight: 700; color: {'#EF4444' if balance > 0 else '#4ECDC4'};">{balance:,.0f}₺</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"💸 Record Payment for {brand}"):
                        col_p1, col_p2 = st.columns(2)
                        
                        with col_p1:
                            pay_amt = st.number_input(
                                "Amount",
                                min_value=0.0,
                                max_value=float(balance) if balance > 0 else 0.0,
                                value=float(balance) if balance > 0 else 0.0,
                                key=f"pay_{brand}"
                            )
                        
                        with col_p2:
                            pay_method = st.selectbox(
                                "Method",
                                ["Bank Transfer", "Cash", "Check"],
                                key=f"method_{brand}"
                            )
                        
                        pay_ref = st.text_input("Reference", key=f"ref_{brand}")
                        
                        if st.button(f"💰 Record", key=f"btn_{brand}"):
                            if pay_amt > 0:
                                payment_id = f"PAY-{datetime.now().strftime('%m%d%H%M%S')}"
                                
                                payment_data = {
                                    'Payment_ID': payment_id,
                                    'Time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                    'Brand': brand,
                                    'Amount': pay_amt,
                                    'Method': pay_method,
                                    'Reference': pay_ref,
                                    'Notes': f"Payment to {brand}"
                                }
                                
                                if save_payment(payment_data):
                                    st.success(f"✅ Payment {payment_id} recorded!")
                                    st.rerun()
                            else:
                                st.error("Enter valid amount!")
                    
                    st.markdown("</div>", unsafe_allow_html=True)
            
            # Payment History
            st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
            st.markdown("### Payment History")
            
            if not df_payments.empty:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.dataframe(
                    df_payments.sort_values('Time', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.info("No payments recorded.")
        else:
            st.info("No orders yet.")
    
    # =======================================================================
    # TAB 6: ANALYTICS
    # =======================================================================
    
    with tabs[5]:
        st.markdown("### 📈 Analytics")
        
        df = load_history()
        
        if not df.empty:
            col_c1, col_c2 = st.columns(2)
            
            with col_c1:
                st.markdown("#### Sales by Brand")
                brand_sales = df.groupby('Brand')['Total_Value'].sum().sort_values(ascending=False)
                st.bar_chart(brand_sales)
            
            with col_c2:
                st.markdown("#### Orders by Brand")
                brand_orders = df['Brand'].value_counts()
                st.bar_chart(brand_orders)
            
            st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
            
            col_c3, col_c4 = st.columns(2)
            
            with col_c3:
                st.markdown("#### Status Distribution")
                status_dist = df['Status'].value_counts()
                st.bar_chart(status_dist)
            
            with col_c4:
                st.markdown("#### Commission vs Payout")
                comparison = pd.DataFrame({
                    'Commission': df.groupby('Brand')['Commission_Amt'].sum(),
                    'Payout': df.groupby('Brand')['Brand_Payout'].sum()
                })
                st.bar_chart(comparison)
            
            # Time series
            if len(df) > 5:
                st.markdown(f"<div style='height: {FIBO['md']}px'></div>", unsafe_allow_html=True)
                st.markdown("#### Orders Over Time")
                
                try:
                    df_time = df.copy()
                    df_time['Time'] = pd.to_datetime(df_time['Time'], errors='coerce')
                    df_time['Date'] = df_time['Time'].dt.date
                    daily_orders = df_time.groupby('Date').size()
                    st.line_chart(daily_orders)
                except Exception as e:
                    st.error(f"Time series error: {e}")
        else:
            st.info("No data for analytics yet.")

# ============================================================================
# 7. MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    if not st.session_state.admin_logged_in:
        login_screen()
    else:
        dashboard_screen()
