import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import urllib.parse

# ============================================================================
# 🌿 NATUVISIO ADMIN PANEL - PREMIUM LOGISTICS OS
# Mountain Vista Design System with Fibonacci Layout
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO Admin OS",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================================
# DATA CONFIGURATION
# ============================================================================

CSV_FILE = "dispatch_history.csv"

DISPATCH_MAP = {
    "HAKI HEAL": {
        "phone": "601158976276",
        "color": "#4ECDC4",
        "icon": "healing",
        "products": {
            "HAKI HEAL CREAM": {"sku": "SKU-HAKI-CRM-01", "price": 450},
            "HAKI HEAL VUCUT LOSYONU": {"sku": "SKU-HAKI-BODY-01", "price": 380},
            "HAKI HEAL SABUN": {"sku": "SKU-HAKI-SOAP-01", "price": 120}
        }
    },
    "AURORACO": {
        "phone": "601158976276",
        "color": "#FF6B6B",
        "icon": "sunrise",
        "products": {
            "AURORACO MATCHA EZMESI": {"sku": "SKU-AUR-MATCHA", "price": 650},
            "AURORACO KAKAO EZMESI": {"sku": "SKU-AUR-CACAO", "price": 550},
            "AURORACO SUPER GIDA": {"sku": "SKU-AUR-SUPER", "price": 800}
        }
    },
    "LONGEVICALS": {
        "phone": "601158976276",
        "color": "#95E1D3",
        "icon": "infinity",
        "products": {
            "LONGEVICALS DHA": {"sku": "SKU-LONG-DHA", "price": 1200},
            "LONGEVICALS EPA": {"sku": "SKU-LONG-EPA", "price": 1150}
        }
    }
}

# ============================================================================
# CUSTOM SVG ICONS
# ============================================================================

def get_svg_icon(icon_name, size=24, color="#ffffff"):
    """Premium custom SVG icons for logistics OS"""
    
    icons = {
        "dashboard": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="3" y="3" width="7" height="7" rx="1" stroke="{color}" stroke-width="2"/>
                <rect x="14" y="3" width="7" height="7" rx="1" stroke="{color}" stroke-width="2"/>
                <rect x="3" y="14" width="7" height="7" rx="1" stroke="{color}" stroke-width="2"/>
                <rect x="14" y="14" width="7" height="7" rx="1" stroke="{color}" stroke-width="2"/>
            </svg>
        ''',
        "orders": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 7H4L2 17H22L20 7Z" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
                <path d="M9 11V6C9 4.34315 10.3431 3 12 3C13.6569 3 15 4.34315 15 6V11" stroke="{color}" stroke-width="2"/>
                <circle cx="8" cy="14" r="1" fill="{color}"/>
                <circle cx="16" cy="14" r="1" fill="{color}"/>
            </svg>
        ''',
        "analytics": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 3V18C3 19.1046 3.89543 20 5 20H21" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
                <path d="M7 15L11 11L15 13L21 7" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="21" cy="7" r="2" fill="{color}"/>
            </svg>
        ''',
        "truck": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M1 6H15V14H1V6Z" stroke="{color}" stroke-width="2"/>
                <path d="M15 8H19L22 11V14H15V8Z" stroke="{color}" stroke-width="2"/>
                <circle cx="6" cy="17" r="2" stroke="{color}" stroke-width="2"/>
                <circle cx="18" cy="17" r="2" stroke="{color}" stroke-width="2"/>
            </svg>
        ''',
        "package": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L3 7V17L12 22L21 17V7L12 2Z" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
                <path d="M12 12L3 7" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
                <path d="M12 12V22" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
                <path d="M12 12L21 7" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            </svg>
        ''',
        "clock": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="9" stroke="{color}" stroke-width="2"/>
                <path d="M12 6V12L16 14" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            </svg>
        ''',
        "money": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect x="2" y="6" width="20" height="12" rx="2" stroke="{color}" stroke-width="2"/>
                <circle cx="12" cy="12" r="3" stroke="{color}" stroke-width="2"/>
                <path d="M18 12H19" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
                <path d="M5 12H6" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            </svg>
        ''',
        "check": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M20 6L9 17L4 12" stroke="{color}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        ''',
        "alert": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 20H22L12 2Z" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
                <path d="M12 9V13" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="17" r="1" fill="{color}"/>
            </svg>
        ''',
        "whatsapp": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 11.5C21 16.75 16.75 21 11.5 21C10 21 8.5 20.5 7.25 19.75L3 21L4.25 16.75C3.5 15.5 3 14 3 12.5C3 7.25 7.25 3 12.5 3C17.75 3 21 7.25 21 11.5Z" stroke="{color}" stroke-width="2"/>
                <path d="M9 9.5C9 9.5 9.5 8 12 8C14.5 8 15 9.5 15 9.5C15 11 13 11.5 13 13V13.5" stroke="{color}" stroke-width="1.5" stroke-linecap="round"/>
                <circle cx="13" cy="16" r="0.5" fill="{color}"/>
            </svg>
        ''',
        "fire": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2C8 6 6 10 6 13C6 17.4183 9.58172 21 14 21C18.4183 21 22 17.4183 22 13C22 10 20 6 16 2C16 4 15 5 13 5C12 5 11 4 11 3C11 2.5 11.5 2 12 2Z" stroke="{color}" stroke-width="2"/>
                <path d="M14 14C14 15.1046 13.1046 16 12 16C10.8954 16 10 15.1046 10 14C10 12.8954 11 11 12 11C13 11 14 12.8954 14 14Z" stroke="{color}" stroke-width="1.5"/>
            </svg>
        ''',
        "mountain": f'''
            <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M3 20L9 8L12 14L15 6L21 20H3Z" stroke="{color}" stroke-width="2" stroke-linejoin="round"/>
                <path d="M9 8L7 12" stroke="{color}" stroke-width="2" stroke-linecap="round"/>
            </svg>
        '''
    }
    
    return icons.get(icon_name, icons["dashboard"])

# ============================================================================
# FIBONACCI LAYOUT CONSTANTS (Golden Ratio: 1.618)
# ============================================================================

PHI = 1.618  # Golden Ratio
FIBO = {
    'xs': 13,      # fibonacci(7)
    'sm': 21,      # fibonacci(8)
    'md': 34,      # fibonacci(9)
    'lg': 55,      # fibonacci(10)
    'xl': 89,      # fibonacci(11)
    'xxl': 144,    # fibonacci(12)
}

# ============================================================================
# PREMIUM STYLING - MOUNTAIN VISTA THEME
# ============================================================================

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');
    
    /* ==========================================
       GLOBAL RESET & FOUNDATION
       ========================================== */
    
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    /* Hide Streamlit Elements */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* ==========================================
       MOUNTAIN VISTA BACKGROUND - RETINA OPTIMIZED
       ========================================== */
    
    .stApp {{
        background-image: url('https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp');
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        position: relative;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #ffffff;
    }}
    
    /* Retina Optimization */
    @media 
        (-webkit-min-device-pixel-ratio: 2), 
        (min-resolution: 192dpi) {{
        .stApp {{
            background-image: url('https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp');
            image-rendering: -webkit-optimize-contrast;
            image-rendering: crisp-edges;
        }}
    }}
    
    /* Dark Overlay for Readability */
    .stApp::before {{
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(
            135deg,
            rgba(15, 23, 42, 0.85) 0%,
            rgba(30, 41, 59, 0.75) 50%,
            rgba(51, 65, 85, 0.70) 100%
        );
        backdrop-filter: blur(2px);
        z-index: 0;
        pointer-events: none;
    }}
    
    /* Content Layer */
    .main {{
        position: relative;
        z-index: 1;
        padding: {FIBO['sm']}px;
    }}
    
    .block-container {{
        padding-top: {FIBO['md']}px !important;
        padding-bottom: {FIBO['md']}px !important;
        max-width: 100% !important;
    }}
    
    /* ==========================================
       GLASSMORPHISM CARDS - FIBONACCI SPACING
       ========================================== */
    
    .glass-card {{
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur({FIBO['sm']}px) saturate(180%);
        -webkit-backdrop-filter: blur({FIBO['sm']}px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: {FIBO['xs']}px;
        padding: {FIBO['md']}px;
        box-shadow: 
            0 8px {FIBO['md']}px rgba(0, 0, 0, 0.3),
            0 0 1px rgba(255, 255, 255, 0.2) inset;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: {FIBO['sm']}px;
    }}
    
    .glass-card:hover {{
        background: rgba(255, 255, 255, 0.12);
        border-color: rgba(255, 255, 255, 0.25);
        transform: translateY(-2px);
        box-shadow: 
            0 {FIBO['sm']}px {FIBO['lg']}px rgba(0, 0, 0, 0.4),
            0 0 1px rgba(255, 255, 255, 0.3) inset;
    }}
    
    /* Metric Cards - Fibonacci Proportions */
    .metric-card {{
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.1) 0%,
            rgba(255, 255, 255, 0.05) 100%
        );
        backdrop-filter: blur({FIBO['sm']}px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: {FIBO['xs']}px;
        padding: {FIBO['sm']}px;
        text-align: center;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }}
    
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #4ECDC4 0%, #95E1D3 100%);
        opacity: 0;
        transition: opacity 0.3s ease;
    }}
    
    .metric-card:hover::before {{
        opacity: 1;
    }}
    
    .metric-card:hover {{
        background: linear-gradient(
            135deg,
            rgba(255, 255, 255, 0.15) 0%,
            rgba(255, 255, 255, 0.08) 100%
        );
        transform: translateY(-4px);
        box-shadow: 0 {FIBO['sm']}px {FIBO['md']}px rgba(0, 0, 0, 0.3);
    }}
    
    /* ==========================================
       TYPOGRAPHY - SPACE HIERARCHY
       ========================================== */
    
    .hero-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: {FIBO['lg']}px;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: {FIBO['sm']}px;
        background: linear-gradient(135deg, #ffffff 0%, #94a3b8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: 0 2px {FIBO['sm']}px rgba(0, 0, 0, 0.3);
    }}
    
    .section-title {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: {FIBO['md']}px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: {FIBO['sm']}px;
        display: flex;
        align-items: center;
        gap: {FIBO['xs']}px;
    }}
    
    .metric-value {{
        font-family: 'Space Grotesk', sans-serif;
        font-size: {FIBO['lg']}px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1;
        margin-bottom: {FIBO['xs']}px;
    }}
    
    .metric-label {{
        font-size: {FIBO['xs']}px;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 0.1em;
    }}
    
    /* ==========================================
       CUSTOM INPUT FIELDS
       ========================================== */
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stNumberInput > div > div > input {{
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: {FIBO['xs']}px !important;
        color: #ffffff !important;
        font-family: 'Inter', sans-serif !important;
        padding: {FIBO['xs']}px {FIBO['sm']}px !important;
        backdrop-filter: blur({FIBO['sm']}px);
        transition: all 0.3s ease !important;
    }}
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stNumberInput > div > div > input:focus {{
        background: rgba(255, 255, 255, 0.12) !important;
        border-color: rgba(78, 205, 196, 0.6) !important;
        box-shadow: 0 0 0 3px rgba(78, 205, 196, 0.15) !important;
    }}
    
    .stTextInput > div > div > input::placeholder,
    .stTextArea > div > div > textarea::placeholder {{
        color: rgba(255, 255, 255, 0.4) !important;
    }}
    
    /* ==========================================
       PREMIUM BUTTONS
       ========================================== */
    
    .stButton > button {{
        background: linear-gradient(135deg, #4ECDC4 0%, #44A08D 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: {FIBO['xs']}px !important;
        padding: {FIBO['xs']}px {FIBO['md']}px !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: {FIBO['xs']}px !important;
        font-weight: 600 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        box-shadow: 0 4px {FIBO['sm']}px rgba(78, 205, 196, 0.3) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        cursor: pointer !important;
        width: 100% !important;
    }}
    
    .stButton > button:hover {{
        background: linear-gradient(135deg, #44A08D 0%, #4ECDC4 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px {FIBO['md']}px rgba(78, 205, 196, 0.4) !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}
    
    /* WhatsApp Button */
    .wa-button {{
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important;
        box-shadow: 0 4px {FIBO['sm']}px rgba(37, 211, 102, 0.3) !important;
    }}
    
    .wa-button:hover {{
        background: linear-gradient(135deg, #128C7E 0%, #25D366 100%) !important;
        box-shadow: 0 8px {FIBO['md']}px rgba(37, 211, 102, 0.4) !important;
    }}
    
    /* ==========================================
       DATA TABLES
       ========================================== */
    
    .dataframe {{
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur({FIBO['sm']}px);
        border-radius: {FIBO['xs']}px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        overflow: hidden;
    }}
    
    .dataframe thead tr th {{
        background: rgba(255, 255, 255, 0.1) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
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
        background: rgba(255, 255, 255, 0.08) !important;
    }}
    
    /* ==========================================
       PROGRESS & STATUS INDICATORS
       ========================================== */
    
    .status-badge {{
        display: inline-block;
        padding: {FIBO['xs']}px {FIBO['sm']}px;
        border-radius: {FIBO['xs']}px;
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        backdrop-filter: blur({FIBO['xs']}px);
    }}
    
    .status-pending {{
        background: rgba(251, 191, 36, 0.15);
        color: #FCD34D;
        border: 1px solid rgba(251, 191, 36, 0.3);
    }}
    
    .status-active {{
        background: rgba(34, 197, 94, 0.15);
        color: #86EFAC;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }}
    
    .status-urgent {{
        background: rgba(239, 68, 68, 0.15);
        color: #FCA5A5;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }}
    
    /* ==========================================
       CUSTOM SCROLLBAR
       ========================================== */
    
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
        border: 2px solid transparent;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: rgba(78, 205, 196, 0.5);
    }}
    
    /* ==========================================
       DIVIDERS
       ========================================== */
    
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(
            90deg,
            transparent 0%,
            rgba(255, 255, 255, 0.2) 50%,
            transparent 100%
        );
        margin: {FIBO['md']}px 0;
    }}
    
    /* ==========================================
       ANIMATIONS
       ========================================== */
    
    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY({FIBO['sm']}px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}
    
    @keyframes pulse {{
        0%, 100% {{
            opacity: 1;
        }}
        50% {{
            opacity: 0.7;
        }}
    }}
    
    .animate-fade-in {{
        animation: fadeInUp 0.6s ease-out;
    }}
    
    /* ==========================================
       RESPONSIVE FIBONACCI BREAKPOINTS
       ========================================== */
    
    @media (max-width: {FIBO['xl'] * 13}px) {{
        .hero-title {{
            font-size: {FIBO['md']}px;
        }}
        
        .section-title {{
            font-size: {FIBO['sm']}px;
        }}
        
        .metric-value {{
            font-size: {FIBO['md']}px;
        }}
        
        .glass-card {{
            padding: {FIBO['sm']}px;
        }}
    }}
    
    /* ==========================================
       RETINA DISPLAYS
       ========================================== */
    
    @media (-webkit-min-device-pixel-ratio: 2), (min-resolution: 192dpi) {{
        .glass-card,
        .metric-card {{
            border-width: 0.5px;
        }}
        
        .dataframe {{
            border-width: 0.5px;
        }}
    }}
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DATA FUNCTIONS
# ============================================================================

def load_history():
    """Load dispatch history from CSV"""
    if os.path.exists(CSV_FILE):
        return pd.read_csv(CSV_FILE)
    return pd.DataFrame(columns=["Order_ID", "Time", "Brand", "Customer", "Items", "Total_Value", "Status"])

def save_to_history(new_entry):
    """Save new entry to dispatch history"""
    df = load_history()
    new_df = pd.DataFrame([new_entry])
    df = pd.concat([df, new_df], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)

def get_dashboard_metrics():
    """Calculate real-time dashboard metrics"""
    df = load_history()
    
    if df.empty:
        return {
            'total_orders': 0,
            'total_revenue': 0,
            'pending_orders': 0,
            'active_brands': 0,
            'today_orders': 0,
            'avg_order_value': 0
        }
    
    # Parse datetime
    df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
    today = datetime.now().date()
    
    metrics = {
        'total_orders': len(df),
        'total_revenue': df['Total_Value'].sum() if 'Total_Value' in df.columns else 0,
        'pending_orders': len(df[df['Status'] == 'Generated']),
        'active_brands': df['Brand'].nunique(),
        'today_orders': len(df[df['Time'].dt.date == today]),
        'avg_order_value': df['Total_Value'].mean() if 'Total_Value' in df.columns and len(df) > 0 else 0
    }
    
    return metrics

# ============================================================================
# SESSION STATE
# ============================================================================

if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'selected_brand_lock' not in st.session_state:
    st.session_state.selected_brand_lock = None
if 'admin_view' not in st.session_state:
    st.session_state.admin_view = 'dashboard'

# ============================================================================
# HEADER SECTION
# ============================================================================

st.markdown(f"""
<div class="glass-card animate-fade-in">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: {FIBO['sm']}px;">
            {get_svg_icon('mountain', size=FIBO['lg'], color='#4ECDC4')}
            <div>
                <div class="hero-title">NATUVISIO ADMIN OS</div>
                <div style="color: rgba(255, 255, 255, 0.7); font-size: {FIBO['xs']}px; letter-spacing: 0.1em;">
                    DECENTRALIZED LOGISTICS COMMAND CENTER
                </div>
            </div>
        </div>
        <div style="text-align: right;">
            <div style="color: rgba(255, 255, 255, 0.5); font-size: 11px; letter-spacing: 0.1em; margin-bottom: 4px;">
                LIVE STATUS
            </div>
            <div style="display: flex; align-items: center; gap: 8px; justify-content: flex-end;">
                <div style="width: 8px; height: 8px; background: #4ECDC4; border-radius: 50%; box-shadow: 0 0 {FIBO['xs']}px #4ECDC4; animation: pulse 2s infinite;"></div>
                <span style="color: #4ECDC4; font-weight: 600; font-size: {FIBO['xs']}px;">OPERATIONAL</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# NAVIGATION TABS
# ============================================================================

st.markdown("<div style='height: 21px;'></div>", unsafe_allow_html=True)

tab_col1, tab_col2, tab_col3, tab_col4 = st.columns(4)

with tab_col1:
    if st.button(f"📊 DASHBOARD", use_container_width=True):
        st.session_state.admin_view = 'dashboard'

with tab_col2:
    if st.button(f"🚀 NEW DISPATCH", use_container_width=True):
        st.session_state.admin_view = 'dispatch'

with tab_col3:
    if st.button(f"📦 ORDERS", use_container_width=True):
        st.session_state.admin_view = 'orders'

with tab_col4:
    if st.button(f"📈 ANALYTICS", use_container_width=True):
        st.session_state.admin_view = 'analytics'

st.markdown("<div style='height: 34px;'></div>", unsafe_allow_html=True)

# ============================================================================
# DASHBOARD VIEW
# ============================================================================

if st.session_state.admin_view == 'dashboard':
    
    # Get metrics
    metrics = get_dashboard_metrics()
    
    # Metrics Grid - Fibonacci Layout
    met_col1, met_col2, met_col3, met_col4 = st.columns(4)
    
    with met_col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="margin-bottom: {FIBO['xs']}px;">
                {get_svg_icon('package', size=FIBO['md'], color='#4ECDC4')}
            </div>
            <div class="metric-value">{metrics['total_orders']}</div>
            <div class="metric-label">Total Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with met_col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="margin-bottom: {FIBO['xs']}px;">
                {get_svg_icon('money', size=FIBO['md'], color='#95E1D3')}
            </div>
            <div class="metric-value">{metrics['total_revenue']:,.0f} ₺</div>
            <div class="metric-label">Total Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with met_col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="margin-bottom: {FIBO['xs']}px;">
                {get_svg_icon('clock', size=FIBO['md'], color='#FFE66D')}
            </div>
            <div class="metric-value">{metrics['pending_orders']}</div>
            <div class="metric-label">Pending Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    with met_col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="margin-bottom: {FIBO['xs']}px;">
                {get_svg_icon('fire', size=FIBO['md'], color='#FF6B6B')}
            </div>
            <div class="metric-value">{metrics['today_orders']}</div>
            <div class="metric-label">Today's Orders</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='height: {FIBO['md']}px;'></div>", unsafe_allow_html=True)
    
    # Brand Performance Section
    st.markdown(f"""
    <div class="section-title">
        {get_svg_icon('analytics', size=FIBO['md'])}
        <span>Brand Performance</span>
    </div>
    """, unsafe_allow_html=True)
    
    brand_col1, brand_col2, brand_col3 = st.columns(3)
    
    df = load_history()
    
    for idx, (brand_name, brand_data) in enumerate(DISPATCH_MAP.items()):
        brand_orders = df[df['Brand'] == brand_name] if not df.empty else pd.DataFrame()
        brand_count = len(brand_orders)
        brand_revenue = brand_orders['Total_Value'].sum() if not brand_orders.empty else 0
        
        col = [brand_col1, brand_col2, brand_col3][idx]
        
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; align-items: center; gap: {FIBO['xs']}px; margin-bottom: {FIBO['sm']}px;">
                    <div style="width: {FIBO['md']}px; height: {FIBO['md']}px; background: linear-gradient(135deg, {brand_data['color']}40, {brand_data['color']}20); border-radius: 8px; display: flex; align-items: center; justify-content: center; border: 1px solid {brand_data['color']}60;">
                        {get_svg_icon('package', size=FIBO['sm'], color=brand_data['color'])}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-size: {FIBO['sm']}px; font-weight: 700; color: #ffffff; margin-bottom: 4px;">
                            {brand_name}
                        </div>
                        <div style="font-size: 11px; color: rgba(255, 255, 255, 0.6);">
                            {len(brand_data['products'])} Products
                        </div>
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: {FIBO['xs']}px; padding-top: {FIBO['xs']}px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
                    <div>
                        <div style="font-size: {FIBO['sm']}px; font-weight: 700; color: {brand_data['color']};">
                            {brand_count}
                        </div>
                        <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5); text-transform: uppercase; letter-spacing: 0.1em;">
                            Orders
                        </div>
                    </div>
                    <div>
                        <div style="font-size: {FIBO['sm']}px; font-weight: 700; color: {brand_data['color']};">
                            {brand_revenue:,.0f}₺
                        </div>
                        <div style="font-size: 10px; color: rgba(255, 255, 255, 0.5); text-transform: uppercase; letter-spacing: 0.1em;">
                            Revenue
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown(f"<div style='height: {FIBO['md']}px;'></div>", unsafe_allow_html=True)
    
    # Recent Activity
    st.markdown(f"""
    <div class="section-title">
        {get_svg_icon('clock', size=FIBO['md'])}
        <span>Recent Activity</span>
    </div>
    """, unsafe_allow_html=True)
    
    if not df.empty:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        recent_df = df.sort_values('Time', ascending=False).head(5)
        st.dataframe(
            recent_df[['Order_ID', 'Time', 'Brand', 'Customer', 'Total_Value', 'Status']],
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 55px;">
            <div style="font-size: 55px; margin-bottom: 21px; opacity: 0.3;">📦</div>
            <div style="color: rgba(255, 255, 255, 0.6); font-size: 13px;">
                No orders yet. Create your first dispatch to get started.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# NEW DISPATCH VIEW
# ============================================================================

elif st.session_state.admin_view == 'dispatch':
    
    st.markdown(f"""
    <div class="section-title">
        {get_svg_icon('truck', size=FIBO['md'])}
        <span>Create New Dispatch Order</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Golden Ratio Layout: 61.8% / 38.2%
    col_left, col_right = st.columns([1.618, 1])
    
    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size: {FIBO['sm']}px; font-weight: 600; color: #ffffff; margin-bottom: {FIBO['sm']}px;">
            👤 Customer Information
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            cust_name = st.text_input("Full Name", placeholder="Enter customer name", key="cust_name")
        with c2:
            cust_phone = st.text_input("Phone Number", placeholder="+90 5XX XXX XXXX", key="cust_phone")
        
        cust_addr = st.text_area("Delivery Address", height=89, placeholder="Full delivery address", key="cust_addr")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f"<div style='height: {FIBO['sm']}px;'></div>", unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size: {FIBO['sm']}px; font-weight: 600; color: #ffffff; margin-bottom: {FIBO['sm']}px;">
            🛒 Product Selection
        </div>
        """, unsafe_allow_html=True)
        
        # Brand Lock Logic
        if st.session_state.cart:
            st.markdown(f"""
            <div style="background: rgba(78, 205, 196, 0.1); border: 1px solid rgba(78, 205, 196, 0.3); border-radius: {FIBO['xs']}px; padding: {FIBO['xs']}px {FIBO['sm']}px; margin-bottom: {FIBO['sm']}px;">
                <span style="color: #4ECDC4;">🔒 Locked to: <strong>{st.session_state.selected_brand_lock}</strong></span>
            </div>
            """, unsafe_allow_html=True)
            active_brand = st.session_state.selected_brand_lock
        else:
            active_brand = st.selectbox(
                "Select Brand Partner",
                list(DISPATCH_MAP.keys()),
                key="brand_select"
            )
        
        brand_data = DISPATCH_MAP[active_brand]
        
        cp, cq = st.columns([2, 1])
        with cp:
            selected_prod = st.selectbox(
                "Product",
                list(brand_data["products"].keys()),
                key="product_select"
            )
        with cq:
            qty = st.number_input("Quantity", min_value=1, value=1, key="qty_input")
        
        prod_details = brand_data["products"][selected_prod]
        
        st.markdown(f"""
        <div style="background: rgba(255, 255, 255, 0.05); border-radius: {FIBO['xs']}px; padding: {FIBO['xs']}px {FIBO['sm']}px; margin-top: {FIBO['xs']}px; margin-bottom: {FIBO['sm']}px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: rgba(255, 255, 255, 0.7); font-size: 11px;">SKU: {prod_details['sku']}</span>
                <span style="color: #4ECDC4; font-weight: 600;">{prod_details['price']} ₺</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"➕ Add to Cart", key="add_cart"):
            st.session_state.cart.append({
                "brand": active_brand,
                "product": selected_prod,
                "sku": prod_details['sku'],
                "qty": qty,
                "subtotal": prod_details['price'] * qty
            })
            st.session_state.selected_brand_lock = active_brand
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="font-size: {FIBO['sm']}px; font-weight: 600; color: #ffffff; margin-bottom: {FIBO['sm']}px;">
            📦 Cart Review
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.cart:
            # Display Cart
            for idx, item in enumerate(st.session_state.cart):
                st.markdown(f"""
                <div style="background: rgba(255, 255, 255, 0.05); border-radius: {FIBO['xs']}px; padding: {FIBO['sm']}px; margin-bottom: {FIBO['xs']}px;">
                    <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 8px;">
                        <div>
                            <div style="font-weight: 600; color: #ffffff; font-size: {FIBO['xs']}px;">
                                {item['product']}
                            </div>
                            <div style="color: rgba(255, 255, 255, 0.5); font-size: 10px; margin-top: 4px;">
                                {item['sku']} × {item['qty']}
                            </div>
                        </div>
                        <div style="font-weight: 700; color: #4ECDC4; font-size: {FIBO['sm']}px;">
                            {item['subtotal']} ₺
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            total = sum(item['subtotal'] for item in st.session_state.cart)
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, rgba(78, 205, 196, 0.2), rgba(149, 225, 211, 0.1)); border: 1px solid rgba(78, 205, 196, 0.3); border-radius: {FIBO['xs']}px; padding: {FIBO['sm']}px; margin-top: {FIBO['sm']}px; margin-bottom: {FIBO['sm']}px;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: rgba(255, 255, 255, 0.8); font-size: {FIBO['xs']}px; font-weight: 500;">TOTAL VALUE</span>
                    <span style="color: #4ECDC4; font-size: {FIBO['md']}px; font-weight: 700;">{total:,.0f} ₺</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            priority = st.selectbox(
                "Order Priority",
                ["Standard Delivery", "🚨 URGENT", "🧊 Cold Chain Required"],
                key="priority_select"
            )
            
            st.markdown(f"<div style='height: {FIBO['sm']}px;'></div>", unsafe_allow_html=True)
            
            if st.button("⚡ GENERATE DISPATCH", key="generate_dispatch", use_container_width=True):
                if cust_name and cust_phone:
                    # Generate Order
                    oid = f"NV-{datetime.now().strftime('%m%d%H%M%S')}"
                    items_str = ", ".join([f"{i['product']}(x{i['qty']})" for i in st.session_state.cart])
                    
                    # Save to History
                    save_to_history({
                        "Order_ID": oid,
                        "Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Brand": active_brand,
                        "Customer": cust_name,
                        "Items": items_str,
                        "Total_Value": total,
                        "Status": "Generated"
                    })
                    
                    # Create WhatsApp Message
                    safe_addr = cust_addr.replace("\n", ", ")
                    target_phone = brand_data['phone'].replace("+", "").replace(" ", "")
                    
                    msg = (
                        f"*{priority} - NATUVISIO DISPATCH*\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"🆔 Order: {oid}\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n\n"
                        f"👤 Customer: {cust_name}\n"
                        f"📞 Phone: {cust_phone}\n"
                        f"🏠 Address: {safe_addr}\n\n"
                        f"━━━━━━━━━━━━━━━━━━━━\n"
                        f"📦 ORDER ITEMS:\n\n"
                    )
                    
                    for item in st.session_state.cart:
                        msg += f"• {item['product']}\n  Qty: {item['qty']} | Amount: {item['subtotal']} ₺\n\n"
                    
                    msg += f"━━━━━━━━━━━━━━━━━━━━\n"
                    msg += f"💰 TOTAL: {total:,.0f} ₺\n\n"
                    msg += "⚡ Please pack and ship immediately.\n"
                    msg += "Reply with tracking number."
                    
                    url = f"https://wa.me/{target_phone}?text={urllib.parse.quote(msg)}"
                    
                    st.success(f"✅ Order {oid} Generated Successfully!")
                    
                    st.markdown(f"""
                    <a href="{url}" target="_blank" style="text-decoration: none;">
                        <div class="wa-button" style="background: linear-gradient(135deg, #25D366 0%, #128C7E 100%) !important; color: white; padding: {FIBO['sm']}px; text-align: center; border-radius: {FIBO['xs']}px; font-weight: 700; font-size: {FIBO['sm']}px; margin-top: {FIBO['sm']}px; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: {FIBO['xs']}px;">
                            {get_svg_icon('whatsapp', size=FIBO['md'])}
                            <span>OPEN WHATSAPP</span>
                        </div>
                    </a>
                    """, unsafe_allow_html=True)
                    
                    # Clear Cart
                    st.session_state.cart = []
                    st.session_state.selected_brand_lock = None
                else:
                    st.error("⚠️ Please fill in customer name and phone number!")
            
            st.markdown(f"<div style='height: {FIBO['xs']}px;'></div>", unsafe_allow_html=True)
            
            if st.button("🗑️ Clear Cart", key="clear_cart"):
                st.session_state.cart = []
                st.session_state.selected_brand_lock = None
                st.rerun()
        
        else:
            st.markdown("""
            <div style="text-align: center; padding: 55px 21px; opacity: 0.5;">
                <div style="font-size: 55px; margin-bottom: 13px;">🛒</div>
                <div style="color: rgba(255, 255, 255, 0.6); font-size: 13px;">
                    Cart is empty.<br/>Add products to get started.
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# ORDERS VIEW
# ============================================================================

elif st.session_state.admin_view == 'orders':
    
    st.markdown(f"""
    <div class="section-title">
        {get_svg_icon('orders', size=FIBO['md'])}
        <span>All Dispatch Orders</span>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_history()
    
    if not df.empty:
        # Filter options
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            brand_filter = st.multiselect(
                "Filter by Brand",
                options=df['Brand'].unique().tolist(),
                default=df['Brand'].unique().tolist(),
                key="brand_filter"
            )
        
        with filter_col2:
            status_filter = st.multiselect(
                "Filter by Status",
                options=df['Status'].unique().tolist(),
                default=df['Status'].unique().tolist(),
                key="status_filter"
            )
        
        with filter_col3:
            date_range = st.selectbox(
                "Date Range",
                ["All Time", "Today", "This Week", "This Month"],
                key="date_filter"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Apply filters
        filtered_df = df[
            (df['Brand'].isin(brand_filter)) &
            (df['Status'].isin(status_filter))
        ]
        
        # Date filtering
        if date_range != "All Time":
            filtered_df['Time'] = pd.to_datetime(filtered_df['Time'], errors='coerce')
            today = datetime.now().date()
            
            if date_range == "Today":
                filtered_df = filtered_df[filtered_df['Time'].dt.date == today]
            elif date_range == "This Week":
                week_ago = today - timedelta(days=7)
                filtered_df = filtered_df[filtered_df['Time'].dt.date >= week_ago]
            elif date_range == "This Month":
                month_ago = today - timedelta(days=30)
                filtered_df = filtered_df[filtered_df['Time'].dt.date >= month_ago]
        
        st.markdown(f"<div style='height: {FIBO['sm']}px;'></div>", unsafe_allow_html=True)
        
        # Display orders
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.dataframe(
            filtered_df.sort_values('Time', ascending=False),
            use_container_width=True,
            hide_index=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Summary stats
        st.markdown(f"<div style='height: {FIBO['sm']}px;'></div>", unsafe_allow_html=True)
        
        sum_col1, sum_col2, sum_col3 = st.columns(3)
        
        with sum_col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(filtered_df)}</div>
                <div class="metric-label">Filtered Orders</div>
            </div>
            """, unsafe_allow_html=True)
        
        with sum_col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{filtered_df['Total_Value'].sum():,.0f} ₺</div>
                <div class="metric-label">Total Value</div>
            </div>
            """, unsafe_allow_html=True)
        
        with sum_col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{filtered_df['Total_Value'].mean():,.0f} ₺</div>
                <div class="metric-label">Avg Order Value</div>
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 89px;">
            <div style="font-size: 89px; margin-bottom: 21px; opacity: 0.3;">📦</div>
            <div style="color: rgba(255, 255, 255, 0.6); font-size: 13px;">
                No orders found. Start creating dispatches to see them here.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# ANALYTICS VIEW
# ============================================================================

elif st.session_state.admin_view == 'analytics':
    
    st.markdown(f"""
    <div class="section-title">
        {get_svg_icon('analytics', size=FIBO['md'])}
        <span>Business Analytics</span>
    </div>
    """, unsafe_allow_html=True)
    
    df = load_history()
    
    if not df.empty:
        # Revenue by Brand
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"<div style='font-size: {FIBO['sm']}px; font-weight: 600; margin-bottom: {FIBO['sm']}px;'>Revenue by Brand</div>", unsafe_allow_html=True)
        
        brand_revenue = df.groupby('Brand')['Total_Value'].sum().sort_values(ascending=False)
        st.bar_chart(brand_revenue)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f"<div style='height: {FIBO['sm']}px;'></div>", unsafe_allow_html=True)
        
        # Top Products
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: {FIBO['sm']}px; font-weight: 600; margin-bottom: {FIBO['sm']}px;'>Orders by Brand</div>", unsafe_allow_html=True)
            
            brand_counts = df['Brand'].value_counts()
            st.bar_chart(brand_counts)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: {FIBO['sm']}px; font-weight: 600; margin-bottom: {FIBO['sm']}px;'>Status Distribution</div>", unsafe_allow_html=True)
            
            status_counts = df['Status'].value_counts()
            st.bar_chart(status_counts)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Time series (if enough data)
        if len(df) > 5:
            st.markdown(f"<div style='height: {FIBO['sm']}px;'></div>", unsafe_allow_html=True)
            
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(f"<div style='font-size: {FIBO['sm']}px; font-weight: 600; margin-bottom: {FIBO['sm']}px;'>Orders Over Time</div>", unsafe_allow_html=True)
            
            df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
            df['Date'] = df['Time'].dt.date
            daily_orders = df.groupby('Date').size()
            st.line_chart(daily_orders)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown("""
        <div class="glass-card" style="text-align: center; padding: 89px;">
            <div style="font-size: 89px; margin-bottom: 21px; opacity: 0.3;">📈</div>
            <div style="color: rgba(255, 255, 255, 0.6); font-size: 13px;">
                No data available for analytics yet.<br/>Create some orders to see insights.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown(f"<div style='height: {FIBO['lg']}px;'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div class="glass-card" style="text-align: center; padding: {FIBO['md']}px;">
    <div style="display: flex; align-items: center; justify-content: center; gap: {FIBO['xs']}px; margin-bottom: {FIBO['xs']}px;">
        {get_svg_icon('mountain', size=FIBO['sm'], color='#4ECDC4')}
        <span style="font-weight: 700; font-size: {FIBO['sm']}px;">NATUVISIO ADMIN OS</span>
    </div>
    <div style="color: rgba(255, 255, 255, 0.5); font-size: 11px; letter-spacing: 0.1em;">
        DECENTRALIZED LOGISTICS COMMAND CENTER
    </div>
    <div style="margin-top: {FIBO['sm']}px; padding-top: {FIBO['sm']}px; border-top: 1px solid rgba(255, 255, 255, 0.1);">
        <div style="color: rgba(255, 255, 255, 0.4); font-size: 10px;">
            © 2025 NATUVISIO Operations • Built for Speed, Science, and Trust
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
