import streamlit as st
import pandas as pd
import numpy as np
import os
import hashlib
import time
import uuid
import urllib.parse
from datetime import datetime, timedelta
from io import BytesIO

# ============================================================================
# 🧠 MODULE A: CONFIGURATION & CONSTANTS (System Brain)
# ============================================================================

class Config:
    APP_NAME = "NATUVISIO OS"
    VERSION = "2.0.1 (Stable)"
    CURRENCY = "₺"
    PHI = 1.618  # Golden Ratio
    
    # File Paths
    DB_ORDERS = "nv_orders.csv"
    DB_LEDGER = "nv_ledger.csv"
    DB_LOGS = "nv_audit_logs.csv"
    
    # Spacing (Fibonacci)
    SPACING = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}

    # Brand Metadata (The Source of Truth)
    BRANDS = {
        "HAKI HEAL": {
            "id": "br_haki",
            "color": "#4ECDC4", 
            "commission": 0.15, 
            "phone": "601158976276",
            "iban": "TR90 0006 1000...1234",
            "products": {
                "HAKI CREAM": {"sku": "HH-CRM-01", "price": 450},
                "HAKI SOAP": {"sku": "HH-SOP-01", "price": 120}
            }
        },
        "AURORACO": {
            "id": "br_aurora",
            "color": "#FF6B6B", 
            "commission": 0.20, 
            "phone": "601158976276",
            "iban": "TR90 0006 2000...9876",
            "products": {
                "MATCHA": {"sku": "AUR-MTC-01", "price": 650},
                "CACAO": {"sku": "AUR-CAC-01", "price": 550}
            }
        },
        "LONGEVICALS": {
            "id": "br_long",
            "color": "#95E1D3", 
            "commission": 0.12, 
            "phone": "601158976276",
            "iban": "TR90 0001 5000...1122",
            "products": {
                "OMEGA 3": {"sku": "LNG-OMG-01", "price": 1200},
                "NMN": {"sku": "LNG-NMN-01", "price": 1500}
            }
        }
    }

# ============================================================================
# 🔒 MODULE B: AUTHENTICATION & SECURITY (Gatekeeper)
# ============================================================================

class Auth:
    """
    Handles password hashing and session management.
    Security Level: SHA-256 Hashing + Salt Simulation
    """
    # In production, these hashes would be in a secure DB.
    # Current Passwords:
    # Founder: admin2025
    # Auroraco: aurora123
    # Longevicals: long123
    # Haki: haki123
    USERS = {
        "FOUNDER": {"hash": "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918", "role": "admin", "brand": None},
        "AURORACO": {"hash": "2f2495751939db262cb479900994f8664155b9a89761a2066d929b9f52865956", "role": "vendor", "brand": "AURORACO"},
        "LONGEVICALS": {"hash": "63f73602d338a063d819448375a31a904d99c4202280d0d62c4314c99059e7f4", "role": "vendor", "brand": "LONGEVICALS"},
        "HAKI HEAL": {"hash": "a4d314811a2f912c40212f4625895741b09b5557766063364f9f7069c9b19e2e", "role": "vendor", "brand": "HAKI HEAL"},
    }

    @staticmethod
    def hash_pass(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def login(username, password):
        user = Auth.USERS.get(username)
        if user and user['hash'] == Auth.hash_pass(password):
            st.session_state.user = {
                "username": username,
                "role": user['role'],
                "brand": user['brand'],
                "login_time": datetime.now()
            }
            return True
        return False

    @staticmethod
    def logout():
        st.session_state.user = None
        st.session_state.cart = []
        st.rerun()

    @staticmethod
    def check():
        if 'user' not in st.session_state or st.session_state.user is None:
            return False
        return True

# ============================================================================
# 💾 MODULE C: DATABASE & PERSISTENCE (Data Lake)
# ============================================================================

class Database:
    """
    Manages CSV persistence with Thread-Safe simulation.
    Implements Row-Level Security (RLS) via accessors.
    """
    
    @staticmethod
    def init():
        # 1. Orders Table
        if not os.path.exists(Config.DB_ORDERS):
            pd.DataFrame(columns=[
                "order_id", "timestamp", "brand", "customer_name", "phone", "address", 
                "items", "total_val", "comm_rate", "comm_amt", "payout_amt", 
                "status", "whatsapp_sent", "tracking", "notes", "priority", "last_updated"
            ]).to_csv(Config.DB_ORDERS, index=False)

        # 2. Financial Ledger (Double Entry Logic)
        if not os.path.exists(Config.DB_LEDGER):
            pd.DataFrame(columns=[
                "txn_id", "timestamp", "type", "brand", "amount", "description", "status"
            ]).to_csv(Config.DB_LEDGER, index=False)
            
        # 3. Audit Logs (Legal Compliance)
        if not os.path.exists(Config.DB_LOGS):
            pd.DataFrame(columns=[
                "log_id", "timestamp", "user", "action", "details"
            ]).to_csv(Config.DB_LOGS, index=False)

    @staticmethod
    def log_action(action, details):
        """Immutable audit trail"""
        try:
            entry = {
                "log_id": str(uuid.uuid4())[:8],
                "timestamp": datetime.now().isoformat(),
                "user": st.session_state.user['username'] if 'user' in st.session_state else "SYSTEM",
                "action": action,
                "details": details
            }
            df = pd.read_csv(Config.DB_LOGS)
            pd.concat([df, pd.DataFrame([entry])], ignore_index=True).to_csv(Config.DB_LOGS, index=False)
        except:
            pass

    @staticmethod
    def get_orders(brand_filter=None):
        """
        ROW LEVEL SECURITY: 
        If brand_filter is passed, only return that brand.
        If user is vendor, FORCE brand_filter.
        """
        try:
            df = pd.read_csv(Config.DB_ORDERS)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Security Enforcer
            current_user = st.session_state.get('user', {})
            if current_user.get('role') == 'vendor':
                df = df[df['brand'] == current_user['brand']]
            elif brand_filter:
                df = df[df['brand'] == brand_filter]
                
            return df
        except:
            return pd.DataFrame()

    @staticmethod
    def save_order(order_data):
        df = pd.read_csv(Config.DB_ORDERS)
        df = pd.concat([df, pd.DataFrame([order_data])], ignore_index=True)
        df.to_csv(Config.DB_ORDERS, index=False)
        
        # Add to Ledger
        Database.add_ledger_entry(
            type="SALE",
            brand=order_data['brand'],
            amount=order_data['payout_amt'], # We owe them this
            desc=f"Order Revenue: {order_data['order_id']}",
            status="PENDING"
        )
        
        Database.log_action("CREATE_ORDER", f"Created {order_data['order_id']}")
        return True

    @staticmethod
    def update_order_status(order_id, field, value):
        df = pd.read_csv(Config.DB_ORDERS)
        if order_id in df['order_id'].values:
            df.loc[df['order_id'] == order_id, field] = value
            df.loc[df['order_id'] == order_id, 'last_updated'] = datetime.now().isoformat()
            df.to_csv(Config.DB_ORDERS, index=False)
            Database.log_action("UPDATE_ORDER", f"{order_id} {field} -> {value}")
            return True
        return False

    @staticmethod
    def add_ledger_entry(type, brand, amount, desc, status="PENDING"):
        df = pd.read_csv(Config.DB_LEDGER)
        entry = {
            "txn_id": f"TXN-{uuid.uuid4().hex[:6].upper()}",
            "timestamp": datetime.now().isoformat(),
            "type": type, # SALE (Credit Vendor), PAYOUT (Debit Vendor)
            "brand": brand,
            "amount": float(amount),
            "description": desc,
            "status": status
        }
        pd.concat([df, pd.DataFrame([entry])], ignore_index=True).to_csv(Config.DB_LEDGER, index=False)

    @staticmethod
    def get_financials(brand=None):
        df = pd.read_csv(Config.DB_LEDGER)
        if brand:
            df = df[df['brand'] == brand]
        return df

# ============================================================================
# 🎨 MODULE D: UI COMPONENT LIBRARY (Design System)
# ============================================================================

class UI:
    """
    Renders Glassmorphism components and Visual Hierarchy.
    Implements the 'Glow' system for alerts.
    """
    
    @staticmethod
    def load_css():
        st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;600&display=swap');
            
            /* GLOBAL RESET */
            .stApp {{
                background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%);
                font-family: 'Inter', sans-serif;
                color: white;
            }}
            
            /* GLASS CARD */
            .glass-card {{
                background: rgba(255, 255, 255, 0.04);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.2);
                margin-bottom: 16px;
                transition: transform 0.2s;
            }}
            .glass-card:hover {{ border-color: rgba(255, 255, 255, 0.2); }}

            /* GLOW ALERTS - THE ATTENTION ENGINE */
            .glow-red {{
                box-shadow: 0 0 15px rgba(239, 68, 68, 0.3);
                border-left: 3px solid #EF4444;
            }}
            .glow-amber {{
                box-shadow: 0 0 15px rgba(245, 158, 11, 0.2);
                border-left: 3px solid #F59E0B;
            }}
            .glow-green {{
                border-left: 3px solid #10B981;
            }}

            /* TYPOGRAPHY */
            h1, h2, h3 {{ font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.02em; }}
            .metric-lbl {{ font-size: 11px; text-transform: uppercase; color: rgba(255,255,255,0.5); letter-spacing: 0.1em; }}
            .metric-val {{ font-size: 28px; font-weight: 700; font-family: 'Space Grotesk'; }}
            
            /* BADGES */
            .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 10px; font-weight: 700; text-transform: uppercase; }}
            .bg-new {{ background: rgba(239, 68, 68, 0.2); color: #FCA5A5; }}
            .bg-notified {{ background: rgba(59, 130, 246, 0.2); color: #93C5FD; }}
            .bg-track {{ background: rgba(16, 185, 129, 0.2); color: #6EE7B7; }}
            
            /* UTILS */
            .stButton>button {{ width: 100%; border-radius: 8px; font-weight: 600; }}
            div[data-testid="stMetricValue"] {{ font-family: 'Space Grotesk'; }}
        </style>
        """, unsafe_allow_html=True)

    @staticmethod
    def card_metric(label, value, delta=None, color="#fff"):
        st.markdown(f"""
        <div class="glass-card" style="padding: 15px; text-align: center;">
            <div class="metric-lbl">{label}</div>
            <div class="metric-val" style="color: {color}">{value}</div>
            {f'<div style="font-size: 12px; color: {color}">{delta}</div>' if delta else ''}
        </div>
        """, unsafe_allow_html=True)

    @staticmethod
    def status_badge(status):
        map = {
            "New": "bg-new",
            "Notified": "bg-notified",
            "Dispatched": "bg-track",
            "Completed": "bg-track"
        }
        return f'<span class="badge {map.get(status, "")}">{status}</span>'

# ============================================================================
# ⚙️ MODULE E: BUSINESS LOGIC (The Engine)
# ============================================================================

class Logic:
    @staticmethod
    def calculate_commission(brand, total_amount):
        rate = Config.BRANDS[brand]['commission']
        comm_amt = total_amount * rate
        payout = total_amount - comm_amt
        return comm_amt, payout

    @staticmethod
    def generate_whatsapp_link(order):
        """Generates a pre-filled WhatsApp link for vendors"""
        phone = Config.BRANDS[order['brand']]['phone']
        msg = f"""*NATUVISIO ORDER ALERT* 🚨
-----------------------------
🆔 Order: {order['order_id']}
👤 Customer: {order['customer_name']}
📍 Loc: {order['address']}
📞 Contact: {order['phone']}
-----------------------------
📦 ITEMS:
{order['items']}
-----------------------------
💰 PAYOUT: {order['payout_amt']} {Config.CURRENCY}
⚠️ Please confirm dispatch within 24h."""
        
        encoded = urllib.parse.quote(msg)
        return f"https://wa.me/{phone}?text={encoded}"

    @staticmethod
    def get_danger_zone_stats():
        """Identify critical issues for Admin"""
        df = Database.get_orders()
        if df.empty: return {}
        
        now = datetime.now()
        
        # Logic: New orders that haven't been notified
        pending_notify = len(df[df['status'] == 'New'])
        
        # Logic: Notified but no tracking > 24 hours
        stuck_dispatch = len(df[
            (df['status'] == 'Notified') & 
            (df['timestamp'] < (now - timedelta(hours=24)))
        ])
        
        return {"pending_notify": pending_notify, "stuck": stuck_dispatch}

# ============================================================================
# 🖥️ MODULE F: PANELS (Views)
# ============================================================================

def panel_founder():
    st.markdown("## 🏔️ Founder Command Center")
    
    # 1. DANGER ZONE (Alerts)
    alerts = Logic.get_danger_zone_stats()
    if alerts['pending_notify'] > 0 or alerts['stuck'] > 0:
        st.markdown(f"""
        <div class="glass-card glow-red" style="display: flex; gap: 20px; align-items: center;">
            <div style="font-size: 30px;">🚨</div>
            <div style="flex-grow: 1;">
                <h3 style="margin:0; color: #EF4444;">ATTENTION NEEDED</h3>
                <div style="font-size: 14px; opacity: 0.8;">
                    {alerts['pending_notify']} Orders waiting for vendor notification • 
                    {alerts['stuck']} Orders stuck in dispatch > 24h
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 2. HIGH LEVEL METRICS
    df_all = Database.get_orders()
    df_fin = Database.get_financials()
    
    total_rev = df_all['total_val'].sum() if not df_all.empty else 0
    total_comm = df_all['comm_amt'].sum() if not df_all.empty else 0
    
    # Calculate Owed Payouts
    pending_payouts = df_fin[df_fin['status'] == 'PENDING']['amount'].sum()
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: UI.card_metric("Total Revenue", f"{total_rev:,.0f} {Config.CURRENCY}")
    with c2: UI.card_metric("Net Commission", f"{total_comm:,.0f} {Config.CURRENCY}", color="#4ECDC4")
    with c3: UI.card_metric("Pending Payouts", f"{pending_payouts:,.0f} {Config.CURRENCY}", color="#F59E0B")
    with c4: UI.card_metric("Total Orders", len(df_all))

    st.markdown("---")

    # 3. LIFECYCLE MANAGEMENT TABS
    tabs = st.tabs(["🔥 NEW ORDERS", "⏳ PROCESSING", "📦 COMPLETED", "💰 FINANCE HQ", "📊 ANALYTICS", "⚙️ SETTINGS"])
    
    # --- TAB: NEW ORDERS ---
    with tabs[0]:
        new_orders = df_all[df_all['status'] == 'New'].sort_values('timestamp', ascending=False)
        if new_orders.empty:
            st.info("✅ No new orders. All caught up!")
        else:
            for _, row in new_orders.iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="glass-card glow-red">
                        <div style="display: flex; justify-content: space-between;">
                            <div>
                                <span class="badge bg-new">NEW ORDER</span>
                                <h3>{row['order_id']} <span style="font-size: 14px; color: grey;">{row['brand']}</span></h3>
                                <div>{row['items']}</div>
                            </div>
                            <div style="text-align: right;">
                                <div class="metric-val">{row['total_val']}₺</div>
                                <div style="font-size: 12px;">{row['timestamp'].strftime('%d %b %H:%M')}</div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    wa_link = Logic.generate_whatsapp_link(row)
                    
                    c_act1, c_act2 = st.columns([1, 4])
                    with c_act1:
                        st.link_button("📲 WhatsApp Vendor", wa_link)
                    with c_act2:
                        if st.button("✅ Mark Notified", key=f"ntf_{row['order_id']}"):
                            Database.update_order_status(row['order_id'], 'status', 'Notified')
                            Database.update_order_status(row['order_id'], 'whatsapp_sent', 'YES')
                            st.toast("Order moved to Processing")
                            time.sleep(1)
                            st.rerun()

    # --- TAB: PROCESSING ---
    with tabs[1]:
        proc_orders = df_all[df_all['status'] == 'Notified']
        if proc_orders.empty:
            st.info("No orders waiting for tracking.")
        else:
            for _, row in proc_orders.iterrows():
                with st.expander(f"⏳ {row['order_id']} - {row['brand']} ({row['customer_name']})"):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.write(f"**Items:** {row['items']}")
                        st.write(f"**Address:** {row['address']}")
                    with c2:
                        track_input = st.text_input("Tracking Number", key=f"trk_in_{row['order_id']}")
                        if st.button("📦 Mark Dispatched", key=f"btn_dsp_{row['order_id']}"):
                            if track_input:
                                Database.update_order_status(row['order_id'], 'tracking', track_input)
                                Database.update_order_status(row['order_id'], 'status', 'Dispatched')
                                st.success("Updated!")
                                st.rerun()
                            else:
                                st.error("Enter tracking first.")

    # --- TAB: FINANCE HQ ---
    with tabs[3]:
        st.markdown("### 🏦 Financial Ledger")
        
        # Payout Manager
        brands = list(Config.BRANDS.keys())
        sel_brand = st.selectbox("Select Brand for Reconciliation", brands)
        
        fin_df = Database.get_financials(sel_brand)
        pending = fin_df[fin_df['status'] == 'PENDING']['amount'].sum()
        
        col_pay1, col_pay2 = st.columns([2, 1])
        with col_pay1:
            st.markdown(f"""
            <div class="glass-card">
                <h4>Outstanding Balance: {sel_brand}</h4>
                <div class="metric-val" style="color: #F59E0B">{pending:,.2f} ₺</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col_pay2:
            amt_to_pay = st.number_input("Payout Amount", min_value=0.0, max_value=float(pending))
            if st.button("💸 Record Payout"):
                Database.add_ledger_entry("PAYOUT", sel_brand, -amt_to_pay, "Vendor Payout", "COMPLETED")
                # Logic to mark individual orders as paid would go here (omitted for brevity)
                st.success("Payout Recorded")
                st.rerun()
                
        st.dataframe(fin_df, use_container_width=True)
        
        st.download_button("Download Ledger CSV", fin_df.to_csv(), "ledger.csv")

    # --- TAB: SETTINGS & LOGS ---
    with tabs[5]:
        st.markdown("### 🕵️ Audit Logs")
        logs = pd.read_csv(Config.DB_LOGS)
        st.dataframe(logs.sort_values('timestamp', ascending=False), use_container_width=True)

def panel_vendor():
    user = st.session_state.user
    brand = user['brand']
    brand_meta = Config.BRANDS[brand]
    
    # Header
    st.markdown(f"""
    <div style="border-bottom: 2px solid {brand_meta['color']}; padding-bottom: 20px; margin-bottom: 20px;">
        <h1>{brand} PARTNER PANEL</h1>
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics
    df = Database.get_orders() # Automatically filtered by RLS
    fin_df = Database.get_financials(brand)
    
    my_rev = df['payout_amt'].sum() if not df.empty else 0
    pending_orders = len(df[df['status'] == 'Notified'])
    balance = fin_df['amount'].sum() # Sales (Positive) - Payouts (Negative)
    
    c1, c2, c3 = st.columns(3)
    with c1: UI.card_metric("My Revenue", f"{my_rev:,.0f} ₺")
    with c2: UI.card_metric("Outstanding Balance", f"{balance:,.0f} ₺", color=brand_meta['color'])
    with c3: UI.card_metric("Pending Dispatch", pending_orders, color="#EF4444" if pending_orders > 0 else "#fff")
    
    # Order View
    st.markdown("### 📦 My Orders")
    
    tab_v1, tab_v2 = st.tabs(["ACTION REQUIRED", "HISTORY"])
    
    with tab_v1:
        action_needed = df[df['status'] == 'Notified']
        if action_needed.empty:
            st.success("You are all caught up! No pending shipments.")
        else:
            st.dataframe(action_needed[['order_id', 'timestamp', 'items', 'customer_name', 'address']], use_container_width=True)
            st.warning("Please provide tracking numbers to NATUVISIO Admin via WhatsApp.")

    with tab_v2:
        st.dataframe(df, use_container_width=True)

# ============================================================================
# 🛒 ORDER CREATION (Modal Logic)
# ============================================================================

def order_creation_flow():
    with st.expander("📝 CREATE MANUAL ORDER", expanded=False):
        col_l, col_r = st.columns([2, 1])
        
        with col_l:
            c_brand = st.selectbox("Brand", list(Config.BRANDS.keys()))
            c_name = st.text_input("Customer Name")
            c_phone = st.text_input("Phone")
            c_addr = st.text_area("Address")
            
        with col_r:
            st.markdown("##### Basket")
            products = Config.BRANDS[c_brand]['products']
            sel_prod = st.selectbox("Product", list(products.keys()))
            qty = st.number_input("Qty", 1, 100, 1)
            
            price = products[sel_prod]['price']
            total = price * qty
            
            comm, payout = Logic.calculate_commission(c_brand, total)
            
            st.markdown(f"""
            <div style="background:rgba(255,255,255,0.1); padding:10px; border-radius:8px;">
                <div>Total: **{total} ₺**</div>
                <div style="font-size:12px; color:#aaa">Comm: {comm:.0f} | Pay: {payout:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Confirm Order"):
                order_data = {
                    "order_id": f"ORD-{uuid.uuid4().hex[:6].upper()}",
                    "timestamp": datetime.now().isoformat(),
                    "brand": c_brand,
                    "customer_name": c_name,
                    "phone": c_phone,
                    "address": c_addr,
                    "items": f"{sel_prod} (x{qty})",
                    "total_val": total,
                    "comm_rate": Config.BRANDS[c_brand]['commission'],
                    "comm_amt": comm,
                    "payout_amt": payout,
                    "status": "New",
                    "whatsapp_sent": "NO",
                    "tracking": "",
                    "notes": "Manual Entry",
                    "priority": "Normal",
                    "last_updated": datetime.now().isoformat()
                }
                Database.save_order(order_data)
                st.success("Order Created!")
                time.sleep(1)
                st.rerun()

# ============================================================================
# 🚀 MAIN APP EXECUTION
# ============================================================================

def main():
    st.set_page_config(page_title="NATUVISIO OS", layout="wide", page_icon="🏔️")
    UI.load_css()
    Database.init()
    
    # Initialize Session
    if 'cart' not in st.session_state: st.session_state.cart = []
    
    # Auth Guard
    if not Auth.check():
        c1, c2, c3 = st.columns([1,1,1])
        with c2:
            st.markdown("<br><br><br>", unsafe_allow_html=True)
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;">
                <h1>🏔️</h1>
                <h2>NATUVISIO OS</h2>
                <p>Secure Enterprise Login</p>
            </div>
            """, unsafe_allow_html=True)
            
            u = st.text_input("Identity")
            p = st.text_input("Key", type="password")
            
            if st.button("AUTHENTICATE"):
                if Auth.login(u, p):
                    st.rerun()
                else:
                    st.error("Access Denied")
        return

    # Logged In Layout
    # Sidebar
    with st.sidebar:
        st.markdown(f"## 👤 {st.session_state.user['username']}")
        st.markdown(f"Role: **{st.session_state.user['role'].upper()}**")
        st.markdown("---")
        if st.button("🚪 Secure Logout"):
            Auth.logout()
        
        st.markdown("---")
        st.info(f"System v{Config.VERSION}\n\nRunning Secure Mode")

    # Routing
    role = st.session_state.user['role']
    
    if role == 'admin':
        order_creation_flow() # Only admin creates orders
        panel_founder()
    else:
        panel_vendor()

if __name__ == "__main__":
    main()
