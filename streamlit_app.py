"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NATUVISIO PARTNER PANEL v7.0                                                 ║
║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ║
║  A Premium Wellness Partner Operating System                                  ║
║  Design Language: Scandinavian Zen meets Tokyo Minimalism                    ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
import hashlib
import time

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="NATUVISIO Partner",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Database files
DB_ORDERS = "partner_orders.csv"
DB_STOCK = "partner_stock.csv"
DB_SALES = "partner_sales.csv"
DB_WORKFLOW = "partner_workflow.csv"

# Partner credentials (in production, use proper auth)
PARTNERS = {
    "dr.ahmet": {
        "password": "partner2025",
        "name": "Dr. Ahmet Yılmaz",
        "clinic": "Yılmaz Klinik",
        "role": "Premium Partner",
        "avatar": "🧑‍⚕️"
    },
    "elif.kaya": {
        "password": "partner2025",
        "name": "Elif Kaya",
        "clinic": "Wellness Hub",
        "role": "Elite Partner",
        "avatar": "👩‍💼"
    },
    "demo": {
        "password": "demo",
        "name": "Demo Partner",
        "clinic": "Demo Clinic",
        "role": "Partner",
        "avatar": "👤"
    }
}

# Products configuration
PRODUCTS = {
    "OXIFIT": {
        "sku": "NV-OXI-001",
        "price": 850,
        "partner_price": 595,
        "color": "#E07A5F",
        "icon": "🫁"
    },
    "BLACK STUFF": {
        "sku": "NV-BLK-001", 
        "price": 720,
        "partner_price": 504,
        "color": "#3D405B",
        "icon": "⚫"
    },
    "HAKI HEAL KREM": {
        "sku": "NV-HKH-001",
        "price": 450,
        "partner_price": 315,
        "color": "#81B29A",
        "icon": "🧴"
    },
    "LONGEVICALS DHA": {
        "sku": "NV-LNG-001",
        "price": 1200,
        "partner_price": 840,
        "color": "#F2CC8F",
        "icon": "💊"
    }
}

# ═══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM - Scandinavian Zen meets Tokyo Minimalism
# ═══════════════════════════════════════════════════════════════════════════════

def inject_global_styles():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=Instrument+Serif:ital@0;1&display=swap');
        
        :root {
            --bg-primary: #FAF9F7;
            --bg-secondary: #F5F3EF;
            --bg-card: #FFFFFF;
            --text-primary: #1A1A1A;
            --text-secondary: #6B6B6B;
            --text-muted: #9B9B9B;
            --accent-sage: #81B29A;
            --accent-terracotta: #E07A5F;
            --accent-navy: #3D405B;
            --accent-sand: #F2CC8F;
            --border-light: rgba(0,0,0,0.06);
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.04);
            --shadow-md: 0 4px 20px rgba(0,0,0,0.06);
            --shadow-lg: 0 12px 40px rgba(0,0,0,0.08);
            --radius-sm: 8px;
            --radius-md: 12px;
            --radius-lg: 20px;
            --glow-warning: 0 0 20px rgba(224, 122, 95, 0.4), 0 0 40px rgba(224, 122, 95, 0.2);
            --glow-success: 0 0 20px rgba(129, 178, 154, 0.4), 0 0 40px rgba(129, 178, 154, 0.2);
        }
        
        * {
            font-family: 'DM Sans', -apple-system, sans-serif !important;
        }
        
        .stApp {
            background: var(--bg-primary) !important;
        }
        
        /* Hide Streamlit defaults */
        #MainMenu, header, footer, .stDeployButton { visibility: hidden; }
        .block-container { padding-top: 2rem !important; max-width: 1400px !important; }
        
        /* Typography */
        .headline-serif {
            font-family: 'Instrument Serif', Georgia, serif !important;
            font-size: 3rem;
            font-weight: 400;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            line-height: 1.1;
        }
        
        .subtitle {
            font-size: 0.875rem;
            color: var(--text-muted);
            letter-spacing: 0.1em;
            text-transform: uppercase;
            font-weight: 500;
        }
        
        /* Card System */
        .zen-card {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-lg);
            padding: 28px;
            box-shadow: var(--shadow-sm);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }
        
        .zen-card:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }
        
        /* Glowing Cards for Status */
        .card-glow-warning {
            box-shadow: var(--glow-warning);
            border: 1px solid rgba(224, 122, 95, 0.3);
            animation: pulse-warning 2s infinite;
        }
        
        .card-glow-success {
            box-shadow: var(--glow-success);
            border: 1px solid rgba(129, 178, 154, 0.3);
            animation: pulse-success 2s infinite;
        }
        
        @keyframes pulse-warning {
            0%, 100% { box-shadow: 0 0 20px rgba(224, 122, 95, 0.3), 0 0 40px rgba(224, 122, 95, 0.15); }
            50% { box-shadow: 0 0 30px rgba(224, 122, 95, 0.5), 0 0 60px rgba(224, 122, 95, 0.25); }
        }
        
        @keyframes pulse-success {
            0%, 100% { box-shadow: 0 0 20px rgba(129, 178, 154, 0.3), 0 0 40px rgba(129, 178, 154, 0.15); }
            50% { box-shadow: 0 0 30px rgba(129, 178, 154, 0.5), 0 0 60px rgba(129, 178, 154, 0.25); }
        }
        
        /* Stat Display */
        .stat-value {
            font-family: 'Instrument Serif', serif !important;
            font-size: 2.5rem;
            font-weight: 400;
            color: var(--text-primary);
            line-height: 1;
        }
        
        .stat-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 8px;
        }
        
        /* Navigation Pills */
        .nav-container {
            display: flex;
            gap: 8px;
            padding: 6px;
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            margin-bottom: 32px;
        }
        
        .nav-pill {
            padding: 12px 24px;
            border-radius: var(--radius-sm);
            font-size: 0.875rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
            border: none;
            background: transparent;
            color: var(--text-secondary);
            position: relative;
        }
        
        .nav-pill.active {
            background: var(--bg-card);
            color: var(--text-primary);
            box-shadow: var(--shadow-sm);
        }
        
        .nav-pill .badge {
            position: absolute;
            top: 6px;
            right: 6px;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: badge-pulse 1.5s infinite;
        }
        
        .badge-warning { background: var(--accent-terracotta); }
        .badge-success { background: var(--accent-sage); }
        
        @keyframes badge-pulse {
            0%, 100% { transform: scale(1); opacity: 1; }
            50% { transform: scale(1.3); opacity: 0.7; }
        }
        
        /* Tables */
        .zen-table {
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
        }
        
        .zen-table th {
            text-align: left;
            padding: 16px 20px;
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--text-muted);
            border-bottom: 1px solid var(--border-light);
            font-weight: 600;
        }
        
        .zen-table td {
            padding: 20px;
            border-bottom: 1px solid var(--border-light);
            font-size: 0.9rem;
            color: var(--text-primary);
            vertical-align: middle;
        }
        
        .zen-table tr:last-child td {
            border-bottom: none;
        }
        
        /* Buttons */
        div.stButton > button {
            background: var(--accent-navy) !important;
            color: white !important;
            border: none !important;
            padding: 14px 28px !important;
            border-radius: var(--radius-sm) !important;
            font-weight: 600 !important;
            font-size: 0.875rem !important;
            letter-spacing: 0.02em !important;
            transition: all 0.2s !important;
        }
        
        div.stButton > button:hover {
            background: var(--text-primary) !important;
            transform: translateY(-1px);
        }
        
        /* Input Fields */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stSelectbox > div > div {
            background: var(--bg-secondary) !important;
            border: 1px solid var(--border-light) !important;
            border-radius: var(--radius-sm) !important;
            padding: 12px 16px !important;
            font-size: 0.9rem !important;
        }
        
        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus {
            border-color: var(--accent-sage) !important;
            box-shadow: 0 0 0 3px rgba(129, 178, 154, 0.15) !important;
        }
        
        /* Status Badges */
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 12px;
            border-radius: 100px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .status-pending {
            background: rgba(224, 122, 95, 0.12);
            color: #C25A3F;
        }
        
        .status-processing {
            background: rgba(242, 204, 143, 0.2);
            color: #B8923F;
        }
        
        .status-completed {
            background: rgba(129, 178, 154, 0.12);
            color: #5A8F6E;
        }
        
        /* Product Cards */
        .product-card {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            padding: 20px;
            display: flex;
            align-items: center;
            gap: 16px;
            transition: all 0.2s;
        }
        
        .product-card:hover {
            border-color: var(--accent-sage);
        }
        
        .product-icon {
            width: 48px;
            height: 48px;
            border-radius: var(--radius-sm);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
        }
        
        /* Workflow Item */
        .workflow-item {
            background: var(--bg-card);
            border: 1px solid var(--border-light);
            border-radius: var(--radius-md);
            padding: 24px;
            margin-bottom: 12px;
            transition: all 0.3s;
        }
        
        .workflow-item.urgent {
            border-left: 4px solid var(--accent-terracotta);
            box-shadow: var(--glow-warning);
        }
        
        .workflow-item.ready {
            border-left: 4px solid var(--accent-sage);
            box-shadow: var(--glow-success);
        }
        
        /* Scrollbar */
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.15); border-radius: 3px; }
        
        /* Login Specific */
        .login-container {
            max-width: 420px;
            margin: 80px auto;
            text-align: center;
        }
        
        .login-brand {
            font-family: 'Instrument Serif', serif !important;
            font-size: 2rem;
            color: var(--text-primary);
            margin-bottom: 8px;
        }
        
        .login-tagline {
            font-size: 0.875rem;
            color: var(--text-muted);
            margin-bottom: 48px;
        }
        
        /* Header */
        .header-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 0;
            margin-bottom: 40px;
            border-bottom: 1px solid var(--border-light);
        }
        
        .header-brand {
            font-family: 'Instrument Serif', serif !important;
            font-size: 1.5rem;
            color: var(--text-primary);
        }
        
        .header-user {
            display: flex;
            align-items: center;
            gap: 12px;
        }
        
        /* Progress Ring */
        .progress-ring {
            width: 60px;
            height: 60px;
            position: relative;
        }
        
        .progress-ring svg {
            transform: rotate(-90deg);
        }
        
        .progress-ring circle {
            fill: none;
            stroke-width: 4;
        }
        
        .progress-ring .bg {
            stroke: var(--bg-secondary);
        }
        
        .progress-ring .progress {
            stroke: var(--accent-sage);
            stroke-linecap: round;
            transition: stroke-dashoffset 0.5s;
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 60px 20px;
            color: var(--text-muted);
        }
        
        .empty-state-icon {
            font-size: 3rem;
            margin-bottom: 16px;
            opacity: 0.5;
        }
    </style>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE OPERATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def init_databases():
    """Initialize CSV databases with sample data if they don't exist"""
    
    # Stock database
    if not os.path.exists(DB_STOCK):
        stock_data = []
        for partner_id in PARTNERS.keys():
            for product, info in PRODUCTS.items():
                stock_data.append({
                    "Partner_ID": partner_id,
                    "Product": product,
                    "SKU": info["sku"],
                    "Initial_Stock": 50,
                    "Current_Stock": np.random.randint(15, 45),
                    "Last_Updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
        pd.DataFrame(stock_data).to_csv(DB_STOCK, index=False)
    
    # Orders database
    if not os.path.exists(DB_ORDERS):
        pd.DataFrame(columns=[
            "Order_ID", "Partner_ID", "Product", "Quantity", "Status",
            "Customer_Name", "Customer_Phone", "Created_At", "Updated_At"
        ]).to_csv(DB_ORDERS, index=False)
    
    # Sales database
    if not os.path.exists(DB_SALES):
        # Create sample sales history
        sales_data = []
        statuses = ["Completed", "Completed", "Completed", "Processing", "Pending"]
        for i in range(15):
            partner = np.random.choice(list(PARTNERS.keys()))
            product = np.random.choice(list(PRODUCTS.keys()))
            status = np.random.choice(statuses)
            days_ago = np.random.randint(0, 30)
            sales_data.append({
                "Sale_ID": f"SL-{1000+i}",
                "Partner_ID": partner,
                "Product": product,
                "Quantity": np.random.randint(1, 5),
                "Unit_Price": PRODUCTS[product]["price"],
                "Partner_Margin": PRODUCTS[product]["price"] - PRODUCTS[product]["partner_price"],
                "Status": status,
                "Customer": f"Müşteri {i+1}",
                "Created_At": (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d %H:%M:%S')
            })
        pd.DataFrame(sales_data).to_csv(DB_SALES, index=False)
    
    # Workflow database
    if not os.path.exists(DB_WORKFLOW):
        workflow_data = [
            {
                "Task_ID": "WF-001",
                "Partner_ID": "dr.ahmet",
                "Type": "stock_request",
                "Title": "OXIFIT Stok Talebi",
                "Description": "20 adet OXIFIT siparişi onay bekliyor",
                "Status": "pending",
                "Priority": "high",
                "Created_At": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                "Task_ID": "WF-002",
                "Partner_ID": "dr.ahmet",
                "Type": "delivery",
                "Title": "Kargo Teslimatı",
                "Description": "BLACK STUFF kargosu yola çıktı",
                "Status": "processing",
                "Priority": "medium",
                "Created_At": (datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S')
            },
            {
                "Task_ID": "WF-003",
                "Partner_ID": "dr.ahmet",
                "Type": "completed",
                "Title": "Satış Tamamlandı",
                "Description": "5 adet HAKI HEAL satışı onaylandı",
                "Status": "completed",
                "Priority": "low",
                "Created_At": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
            }
        ]
        pd.DataFrame(workflow_data).to_csv(DB_WORKFLOW, index=False)

def load_stock(partner_id):
    try:
        df = pd.read_csv(DB_STOCK)
        return df[df['Partner_ID'] == partner_id]
    except:
        return pd.DataFrame()

def load_sales(partner_id):
    try:
        df = pd.read_csv(DB_SALES)
        return df[df['Partner_ID'] == partner_id]
    except:
        return pd.DataFrame()

def load_workflow(partner_id):
    try:
        df = pd.read_csv(DB_WORKFLOW)
        return df[df['Partner_ID'] == partner_id]
    except:
        return pd.DataFrame()

def save_sale(sale_data):
    try:
        df = pd.read_csv(DB_SALES) if os.path.exists(DB_SALES) else pd.DataFrame()
        df = pd.concat([df, pd.DataFrame([sale_data])], ignore_index=True)
        df.to_csv(DB_SALES, index=False)
        return True
    except:
        return False

def update_stock(partner_id, product, quantity_sold):
    try:
        df = pd.read_csv(DB_STOCK)
        mask = (df['Partner_ID'] == partner_id) & (df['Product'] == product)
        if mask.any():
            current = df.loc[mask, 'Current_Stock'].values[0]
            df.loc[mask, 'Current_Stock'] = max(0, current - quantity_sold)
            df.loc[mask, 'Last_Updated'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            df.to_csv(DB_STOCK, index=False)
            return True
    except:
        pass
    return False

def complete_workflow_task(task_id):
    try:
        df = pd.read_csv(DB_WORKFLOW)
        df.loc[df['Task_ID'] == task_id, 'Status'] = 'completed'
        df.to_csv(DB_WORKFLOW, index=False)
        return True
    except:
        return False

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'partner_id' not in st.session_state:
    st.session_state.partner_id = None
if 'current_page' not in st.session_state:
    st.session_state.current_page = "dashboard"

# ═══════════════════════════════════════════════════════════════════════════════
# LOGIN SCREEN
# ═══════════════════════════════════════════════════════════════════════════════

def render_login():
    inject_global_styles()
    
    st.markdown("""
    <div class="login-container">
        <div class="login-brand">NATUVISIO</div>
        <div class="login-tagline">Partner Operating System</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("""
        <div class="zen-card" style="padding: 40px;">
            <h3 style="font-family: 'Instrument Serif', serif; font-weight: 400; margin-bottom: 8px; text-align: center;">Hoş Geldiniz</h3>
            <p style="color: var(--text-muted); font-size: 0.875rem; text-align: center; margin-bottom: 32px;">Partner hesabınıza giriş yapın</p>
        </div>
        """, unsafe_allow_html=True)
        
        username = st.text_input("Kullanıcı Adı", placeholder="örn: dr.ahmet", key="login_user")
        password = st.text_input("Şifre", type="password", placeholder="••••••••", key="login_pass")
        
        st.markdown("<div style='height: 16px'></div>", unsafe_allow_html=True)
        
        if st.button("Giriş Yap", use_container_width=True):
            if username in PARTNERS and PARTNERS[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.partner_id = username
                st.rerun()
            else:
                st.error("Geçersiz kullanıcı adı veya şifre")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 24px; color: var(--text-muted); font-size: 0.75rem;">
            Demo için: <strong>demo</strong> / <strong>demo</strong>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# HEADER COMPONENT
# ═══════════════════════════════════════════════════════════════════════════════

def render_header():
    partner = PARTNERS[st.session_state.partner_id]
    
    col1, col2, col3 = st.columns([2, 4, 2])
    
    with col1:
        st.markdown(f"""
        <div style="font-family: 'Instrument Serif', serif; font-size: 1.5rem; color: var(--text-primary);">
            NATUVISIO
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: flex-end; gap: 12px;">
            <div style="text-align: right;">
                <div style="font-weight: 600; font-size: 0.9rem;">{partner['name']}</div>
                <div style="font-size: 0.75rem; color: var(--text-muted);">{partner['role']}</div>
            </div>
            <div style="width: 40px; height: 40px; background: var(--bg-secondary); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;">
                {partner['avatar']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════

def render_navigation():
    partner_id = st.session_state.partner_id
    
    # Count pending tasks for badges
    workflow_df = load_workflow(partner_id)
    pending_count = len(workflow_df[workflow_df['Status'] == 'pending']) if not workflow_df.empty else 0
    completed_count = len(workflow_df[workflow_df['Status'] == 'completed']) if not workflow_df.empty else 0
    
    nav_items = [
        ("dashboard", "◉ Dashboard", None),
        ("stock", "📦 Stok Takibi", None),
        ("workflow", "⚡ İş Akışı", "warning" if pending_count > 0 else None),
        ("completed", "✓ Tamamlananlar", "success" if completed_count > 0 else None),
        ("logout", "← Çıkış", None)
    ]
    
    cols = st.columns(len(nav_items))
    
    for i, (key, label, badge) in enumerate(nav_items):
        with cols[i]:
            is_active = st.session_state.current_page == key
            badge_html = f'<span class="badge badge-{badge}" style="position: absolute; top: 8px; right: 8px;"></span>' if badge else ''
            
            if st.button(
                label,
                key=f"nav_{key}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                if key == "logout":
                    st.session_state.logged_in = False
                    st.session_state.partner_id = None
                    st.session_state.current_page = "dashboard"
                    st.rerun()
                else:
                    st.session_state.current_page = key
                    st.rerun()
    
    st.markdown("<hr style='border: none; border-top: 1px solid var(--border-light); margin: 24px 0;'>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# DASHBOARD PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_dashboard():
    partner_id = st.session_state.partner_id
    partner = PARTNERS[partner_id]
    
    # Welcome section
    st.markdown(f"""
    <div style="margin-bottom: 40px;">
        <div class="subtitle">Partner Dashboard</div>
        <h1 class="headline-serif">Merhaba, {partner['name'].split()[0]}</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    stock_df = load_stock(partner_id)
    sales_df = load_sales(partner_id)
    workflow_df = load_workflow(partner_id)
    
    # Calculate metrics
    total_stock = stock_df['Current_Stock'].sum() if not stock_df.empty else 0
    total_sales = len(sales_df) if not sales_df.empty else 0
    total_revenue = (sales_df['Unit_Price'] * sales_df['Quantity']).sum() if not sales_df.empty else 0
    pending_tasks = len(workflow_df[workflow_df['Status'] == 'pending']) if not workflow_df.empty else 0
    
    # Stats Grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="zen-card">
            <div class="stat-label">Toplam Stok</div>
            <div class="stat-value">{total_stock}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">adet</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="zen-card">
            <div class="stat-label">Bu Ay Satış</div>
            <div class="stat-value">{total_sales}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">işlem</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="zen-card">
            <div class="stat-label">Toplam Ciro</div>
            <div class="stat-value">{total_revenue:,.0f}₺</div>
            <div style="font-size: 0.8rem; color: var(--accent-sage); margin-top: 4px;">+12% geçen aya göre</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        glow_class = "card-glow-warning" if pending_tasks > 0 else ""
        st.markdown(f"""
        <div class="zen-card {glow_class}">
            <div class="stat-label">Bekleyen İşlem</div>
            <div class="stat-value" style="color: {'var(--accent-terracotta)' if pending_tasks > 0 else 'var(--text-primary)'};">{pending_tasks}</div>
            <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">{'aksiyon gerekli' if pending_tasks > 0 else 'tamamlandı'}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 32px'></div>", unsafe_allow_html=True)
    
    # Two column layout
    col_left, col_right = st.columns([1.5, 1])
    
    with col_left:
        st.markdown("""
        <div class="subtitle" style="margin-bottom: 16px;">Hızlı Satış Kaydı</div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="zen-card">', unsafe_allow_html=True)
        
        product_options = list(PRODUCTS.keys())
        selected_product = st.selectbox("Ürün Seçin", product_options, key="quick_product")
        
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            quantity = st.number_input("Adet", min_value=1, max_value=50, value=1, key="quick_qty")
        with col_q2:
            customer = st.text_input("Müşteri Adı", key="quick_customer")
        
        if st.button("💾 Satışı Kaydet", key="quick_save", use_container_width=True):
            if customer:
                sale_data = {
                    "Sale_ID": f"SL-{int(time.time())}",
                    "Partner_ID": partner_id,
                    "Product": selected_product,
                    "Quantity": quantity,
                    "Unit_Price": PRODUCTS[selected_product]["price"],
                    "Partner_Margin": PRODUCTS[selected_product]["price"] - PRODUCTS[selected_product]["partner_price"],
                    "Status": "Completed",
                    "Customer": customer,
                    "Created_At": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
                if save_sale(sale_data) and update_stock(partner_id, selected_product, quantity):
                    st.success(f"✓ {quantity}x {selected_product} satışı kaydedildi")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Kayıt sırasında hata oluştu")
            else:
                st.warning("Lütfen müşteri adını girin")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown("""
        <div class="subtitle" style="margin-bottom: 16px;">Stok Durumu</div>
        """, unsafe_allow_html=True)
        
        if not stock_df.empty:
            for _, row in stock_df.iterrows():
                product = row['Product']
                current = row['Current_Stock']
                initial = row['Initial_Stock']
                pct = (current / initial) * 100 if initial > 0 else 0
                color = PRODUCTS.get(product, {}).get('color', '#81B29A')
                icon = PRODUCTS.get(product, {}).get('icon', '📦')
                
                warning = "⚠️" if pct < 30 else ""
                
                st.markdown(f"""
                <div class="product-card" style="margin-bottom: 8px;">
                    <div class="product-icon" style="background: {color}20;">{icon}</div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; font-size: 0.9rem;">{product} {warning}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">{current} / {initial} adet</div>
                    </div>
                    <div style="font-family: 'Instrument Serif', serif; font-size: 1.2rem; color: {color};">{pct:.0f}%</div>
                </div>
                """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# STOCK TRACKING PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_stock():
    partner_id = st.session_state.partner_id
    
    st.markdown(f"""
    <div style="margin-bottom: 40px;">
        <div class="subtitle">Envanter Yönetimi</div>
        <h1 class="headline-serif">Stok Takibi</h1>
    </div>
    """, unsafe_allow_html=True)
    
    stock_df = load_stock(partner_id)
    
    if not stock_df.empty:
        for _, row in stock_df.iterrows():
            product = row['Product']
            current = row['Current_Stock']
            initial = row['Initial_Stock']
            pct = (current / initial) * 100 if initial > 0 else 0
            color = PRODUCTS.get(product, {}).get('color', '#81B29A')
            icon = PRODUCTS.get(product, {}).get('icon', '📦')
            sku = PRODUCTS.get(product, {}).get('sku', 'N/A')
            price = PRODUCTS.get(product, {}).get('price', 0)
            partner_price = PRODUCTS.get(product, {}).get('partner_price', 0)
            margin = price - partner_price
            
            is_low = pct < 30
            card_class = "card-glow-warning" if is_low else ""
            
            st.markdown(f"""
            <div class="zen-card {card_class}" style="margin-bottom: 16px;">
                <div style="display: flex; align-items: center; gap: 24px;">
                    <div class="product-icon" style="background: {color}20; width: 64px; height: 64px; font-size: 2rem;">{icon}</div>
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
                            <span style="font-family: 'Instrument Serif', serif; font-size: 1.5rem;">{product}</span>
                            {'<span class="status-badge status-pending">Düşük Stok</span>' if is_low else ''}
                        </div>
                        <div style="display: flex; gap: 32px; font-size: 0.85rem; color: var(--text-muted);">
                            <span>SKU: {sku}</span>
                            <span>Satış Fiyatı: {price}₺</span>
                            <span>Partner Maliyeti: {partner_price}₺</span>
                            <span style="color: var(--accent-sage);">Kar Marjı: {margin}₺</span>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-family: 'Instrument Serif', serif; font-size: 2.5rem; color: {color};">{current}</div>
                        <div style="font-size: 0.75rem; color: var(--text-muted);">/ {initial} adet</div>
                    </div>
                </div>
                <div style="margin-top: 20px; background: var(--bg-secondary); border-radius: 100px; height: 8px; overflow: hidden;">
                    <div style="width: {pct}%; height: 100%; background: {color}; border-radius: 100px; transition: width 0.5s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 32px'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="subtitle" style="margin-bottom: 16px;">Stok Talebi Oluştur</div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="zen-card">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            reorder_product = st.selectbox("Ürün", list(PRODUCTS.keys()), key="reorder_product")
        with col2:
            reorder_qty = st.number_input("Sipariş Adedi", min_value=10, max_value=100, value=20, step=10, key="reorder_qty")
        with col3:
            st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)
            if st.button("📤 Talep Gönder", key="reorder_submit", use_container_width=True):
                st.success(f"✓ {reorder_qty} adet {reorder_product} talebi gönderildi")
        
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📦</div>
            <div>Henüz stok kaydı bulunmuyor</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# WORKFLOW PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_workflow():
    partner_id = st.session_state.partner_id
    
    workflow_df = load_workflow(partner_id)
    pending_df = workflow_df[workflow_df['Status'].isin(['pending', 'processing'])] if not workflow_df.empty else pd.DataFrame()
    
    pending_count = len(pending_df)
    
    st.markdown(f"""
    <div style="margin-bottom: 40px;">
        <div class="subtitle">Operasyonlar</div>
        <h1 class="headline-serif">İş Akışı</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if pending_count > 0:
        st.markdown(f"""
        <div class="zen-card card-glow-warning" style="margin-bottom: 24px; background: rgba(224, 122, 95, 0.05);">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 2rem;">⚡</div>
                <div>
                    <div style="font-weight: 600; font-size: 1.1rem; color: var(--accent-terracotta);">{pending_count} Bekleyen İşlem</div>
                    <div style="font-size: 0.85rem; color: var(--text-muted);">Aşağıdaki işlemleri tamamlamanız bekleniyor</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if not pending_df.empty:
        for idx, row in pending_df.iterrows():
            task_id = row['Task_ID']
            title = row['Title']
            desc = row['Description']
            status = row['Status']
            priority = row['Priority']
            created = row['Created_At']
            
            is_urgent = priority == 'high'
            status_class = "status-pending" if status == 'pending' else "status-processing"
            status_text = "Bekliyor" if status == 'pending' else "İşleniyor"
            card_class = "card-glow-warning" if is_urgent else ""
            
            st.markdown(f"""
            <div class="zen-card {card_class}" style="margin-bottom: 16px; border-left: 4px solid {'var(--accent-terracotta)' if is_urgent else 'var(--accent-sand)'};">
                <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
                    <div>
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 4px;">
                            <span style="font-weight: 600; font-size: 1.1rem;">{title}</span>
                            <span class="status-badge {status_class}">{status_text}</span>
                            {'<span class="status-badge status-pending">Acil</span>' if is_urgent else ''}
                        </div>
                        <div style="font-size: 0.9rem; color: var(--text-secondary);">{desc}</div>
                    </div>
                    <div style="font-size: 0.75rem; color: var(--text-muted);">{task_id}</div>
                </div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border-light);">
                    <div style="font-size: 0.8rem; color: var(--text-muted);">Oluşturulma: {created}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([3, 1, 1])
            with col2:
                if st.button("🔄 İşleme Al", key=f"process_{task_id}"):
                    st.info("İşleme alındı")
            with col3:
                if st.button("✓ Tamamla", key=f"complete_{task_id}"):
                    if complete_workflow_task(task_id):
                        st.success("Tamamlandı!")
                        time.sleep(0.5)
                        st.rerun()
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">✨</div>
            <div style="font-size: 1.1rem; font-weight: 500; margin-bottom: 8px;">Harika!</div>
            <div>Bekleyen işlem bulunmuyor</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# COMPLETED TASKS PAGE
# ═══════════════════════════════════════════════════════════════════════════════

def render_completed():
    partner_id = st.session_state.partner_id
    
    workflow_df = load_workflow(partner_id)
    completed_df = workflow_df[workflow_df['Status'] == 'completed'] if not workflow_df.empty else pd.DataFrame()
    
    sales_df = load_sales(partner_id)
    completed_sales = sales_df[sales_df['Status'] == 'Completed'] if not sales_df.empty else pd.DataFrame()
    
    completed_count = len(completed_df) + len(completed_sales)
    
    st.markdown(f"""
    <div style="margin-bottom: 40px;">
        <div class="subtitle">Tamamlanan İşlemler</div>
        <h1 class="headline-serif">Başarılar</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if completed_count > 0:
        st.markdown(f"""
        <div class="zen-card card-glow-success" style="margin-bottom: 24px; background: rgba(129, 178, 154, 0.05);">
            <div style="display: flex; align-items: center; gap: 16px;">
                <div style="font-size: 2rem;">🎉</div>
                <div>
                    <div style="font-weight: 600; font-size: 1.1rem; color: var(--accent-sage);">{completed_count} Tamamlanan İşlem</div>
                    <div style="font-size: 0.85rem; color: var(--text-muted);">Bu dönemde başarıyla tamamladığınız işlemler</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Workflow completions
    if not completed_df.empty:
        st.markdown("""
        <div class="subtitle" style="margin-bottom: 16px;">Tamamlanan Görevler</div>
        """, unsafe_allow_html=True)
        
        for idx, row in completed_df.iterrows():
            st.markdown(f"""
            <div class="zen-card" style="margin-bottom: 12px; border-left: 4px solid var(--accent-sage);">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span style="font-size: 1.2rem;">✓</span>
                        <div>
                            <div style="font-weight: 600;">{row['Title']}</div>
                            <div style="font-size: 0.85rem; color: var(--text-muted);">{row['Description']}</div>
                        </div>
                    </div>
                    <span class="status-badge status-completed">Tamamlandı</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Sales completions
    if not completed_sales.empty:
        st.markdown("""
        <div class="subtitle" style="margin: 32px 0 16px 0;">Tamamlanan Satışlar</div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="zen-card">', unsafe_allow_html=True)
        
        table_html = """
        <table class="zen-table">
            <thead>
                <tr>
                    <th>Satış ID</th>
                    <th>Ürün</th>
                    <th>Adet</th>
                    <th>Tutar</th>
                    <th>Müşteri</th>
                    <th>Tarih</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for _, row in completed_sales.head(10).iterrows():
            total = row['Unit_Price'] * row['Quantity']
            table_html += f"""
            <tr>
                <td><span style="font-weight: 500;">{row['Sale_ID']}</span></td>
                <td>{row['Product']}</td>
                <td>{row['Quantity']}</td>
                <td style="font-weight: 600;">{total:,.0f}₺</td>
                <td>{row['Customer']}</td>
                <td style="color: var(--text-muted);">{row['Created_At'][:10]}</td>
            </tr>
            """
        
        table_html += "</tbody></table>"
        st.markdown(table_html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if completed_count == 0:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">📋</div>
            <div>Henüz tamamlanan işlem bulunmuyor</div>
        </div>
        """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    init_databases()
    
    if not st.session_state.logged_in:
        render_login()
    else:
        inject_global_styles()
        render_header()
        render_navigation()
        
        page = st.session_state.current_page
        
        if page == "dashboard":
            render_dashboard()
        elif page == "stock":
            render_stock()
        elif page == "workflow":
            render_workflow()
        elif page == "completed":
            render_completed()

if __name__ == "__main__":
    main()
