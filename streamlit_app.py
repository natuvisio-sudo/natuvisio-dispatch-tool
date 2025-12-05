import streamlit as st
import pandas as pd
import numpy as np
import time
import uuid
import urllib.parse
from datetime import datetime, timedelta
from typing import Optional, List
import bcrypt  # Security
import plotly.express as px  # Elite Charts
import plotly.graph_objects as go
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, DataReturnMode, JsCode # Pro Tables

# === ELITE DATA STACK ===
from sqlmodel import Field, Session, SQLModel, create_engine, select
from pydantic import BaseModel, validator

# ============================================================================
# 1. CONFIGURATION & DESIGN SYSTEM (The Aesthetics)
# ============================================================================

st.set_page_config(
    page_title="NATUVISIO OS | Elite",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

class DesignSystem:
    # Fibonacci Spacing
    FIBO = {'xs': 8, 'sm': 13, 'md': 21, 'lg': 34, 'xl': 55}
    PHI = 1.618
    
    # Brand Palette
    COLORS = {
        "HAKI HEAL": "#4ECDC4",
        "AURORACO": "#FF6B6B",
        "LONGEVICALS": "#95E1D3",
        "DANGER": "#EF4444",
        "SUCCESS": "#10B981",
        "WARN": "#F59E0B"
    }

    @staticmethod
    def inject_css():
        st.markdown(f"""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;600&display=swap');
            
            /* === CORE & BACKGROUND === */
            .stApp {{
                background-image: linear-gradient(rgba(15, 23, 42, 0.90), rgba(15, 23, 42, 0.95)), 
                                  url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
                background-size: cover;
                background-attachment: fixed;
                font-family: 'Inter', sans-serif;
            }}
            
            /* === GLASSMORPHISM CARDS === */
            .glass-card {{
                background: rgba(255, 255, 255, 0.03);
                backdrop-filter: blur(20px);
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 16px;
                padding: 24px;
                box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
                transition: transform 0.2s, border-color 0.2s;
            }}
            .glass-card:hover {{
                border-color: rgba(255, 255, 255, 0.2);
                transform: translateY(-2px);
            }}

            /* === TYPOGRAPHY === */
            h1, h2, h3, h4 {{ font-family: 'Space Grotesk', sans-serif !important; letter-spacing: -0.03em; }}
            
            /* === GLOW STATES === */
            .glow-red {{ box-shadow: 0 0 20px rgba(239, 68, 68, 0.15); border-left: 3px solid #EF4444; }}
            .glow-green {{ box-shadow: 0 0 20px rgba(16, 185, 129, 0.15); border-left: 3px solid #10B981; }}
            
            /* === CUSTOM METRICS === */
            div[data-testid="stMetricValue"] {{ font-family: 'Space Grotesk'; font-weight: 700; }}
            
            /* === AGGRID THEME OVERRIDE === */
            .ag-theme-alpine-dark {{ --ag-background-color: rgba(20, 20, 20, 0.5); }}
            
            /* === UTILS === */
            .block-container {{ padding-top: 2rem; }}
            .stButton>button {{ width: 100%; border-radius: 8px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; }}
        </style>
        """, unsafe_allow_html=True)

# ============================================================================
# 2. DATA MODELS (SQLModel + Pydantic) - The "Zero Error" Core
# ============================================================================

# Database Setup
sqlite_file_name = "natuvisio_elite.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
engine = create_engine(sqlite_url)

class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_ref: str = Field(index=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    brand: str
    customer_name: str
    phone: str
    address: str
    items_json: str  # Storing as JSON string for SQLite simplicity
    total_value: float
    commission_amt: float
    brand_payout: float
    status: str = Field(default="New") # New, Notified, Dispatched, Completed
    whatsapp_sent: bool = Field(default=False)
    tracking_num: Optional[str] = None
    priority: str = Field(default="Standard")

class LedgerEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    txn_ref: str
    timestamp: datetime = Field(default_factory=datetime.now)
    brand: str
    type: str # SALE, PAYOUT
    amount: float
    description: str
    status: str = "COMPLETED"

class AuditLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    user: str
    action: str
    details: str

def init_db():
    SQLModel.metadata.create_all(engine)

# ============================================================================
# 3. BACKEND LOGIC & CONTROLLERS
# ============================================================================

class AuthController:
    # Simulated Hash Database (In production, use a real Users table)
    # Passwords: FOUNDER->admin2025, AURORACO->aurora123, etc.
    USERS = {
        "FOUNDER": {"hash": b'$2b$12$eXo.y2.5.1.5.1.5.1.5.1.5.1.5.1.5.1.5.1.5.1.5.1.5.1', "role": "admin"}, # Placeholder hash
        "AURORACO": {"hash": b'$2b$12$eXo...', "role": "vendor", "color": "#FF6B6B"},
    }
    
    @staticmethod
    def check_password(plain_pass: str, correct_hash: bytes) -> bool:
        # For this demo, we use a simple string check to ensure it runs without generating new hashes manually
        # In real production, use: return bcrypt.checkpw(plain_pass.encode(), correct_hash)
        return True # BYPASS FOR DEMO - Implement bcrypt in production

class OrderController:
    @staticmethod
    def create_order(data: dict):
        with Session(engine) as session:
            # 1. Create Order
            order = Order(**data)
            session.add(order)
            
            # 2. Create Ledger Entry (Credit Vendor)
            ledger = LedgerEntry(
                txn_ref=f"TXN-{uuid.uuid4().hex[:6].upper()}",
                brand=data['brand'],
                type="SALE",
                amount=data['brand_payout'],
                description=f"Revenue: {data['order_ref']}"
            )
            session.add(ledger)
            
            # 3. Create Audit Log
            log = AuditLog(user=st.session_state.get('user', 'SYSTEM'), action="CREATE_ORDER", details=f"Created {data['order_ref']}")
            session.add(log)
            
            session.commit()
            return True

    @staticmethod
    def get_orders_df(brand_filter: str = None):
        with Session(engine) as session:
            statement = select(Order)
            if brand_filter:
                statement = statement.where(Order.brand == brand_filter)
            results = session.exec(statement).all()
            return pd.DataFrame([o.dict() for o in results])

    @staticmethod
    def update_status(order_id: int, new_status: str, tracking: str = None):
        with Session(engine) as session:
            order = session.get(Order, order_id)
            if order:
                order.status = new_status
                if tracking: order.tracking_num = tracking
                if new_status == "Notified": order.whatsapp_sent = True
                session.add(order)
                session.commit()
                return True
        return False

# ============================================================================
# 4. UI COMPONENTS (The "Shopify" Polish)
# ============================================================================

class UIComponents:
    @staticmethod
    def render_kpi_row(metrics):
        cols = st.columns(len(metrics))
        for idx, (label, value, delta, color) in enumerate(metrics):
            with cols[idx]:
                st.markdown(f"""
                <div class="glass-card" style="padding: 16px; border-top: 3px solid {color}; text-align: center;">
                    <div style="font-size: 11px; text-transform: uppercase; color: rgba(255,255,255,0.6); letter-spacing: 1px;">{label}</div>
                    <div style="font-size: 28px; font-family: 'Space Grotesk'; font-weight: 700; margin: 4px 0;">{value}</div>
                    {f'<div style="font-size: 12px; color: {color};">{delta}</div>' if delta else ''}
                </div>
                """, unsafe_allow_html=True)

    @staticmethod
    def render_aggrid(df, key_suffix=""):
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True)
        gb.configure_side_bar()
        gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
        
        # Style specific columns
        gb.configure_column("status", cellStyle={'textAlign': 'center'})
        gb.configure_column("total_value", type=["numericColumn", "numberColumnFilter", "customCurrencyFormat"], custom_currency_symbol="₺")
        
        # Color coding for status via JS
        cellsytle_jscode = JsCode("""
        function(params) {
            if (params.value == 'New') { return {'color': '#EF4444', 'fontWeight': 'bold'}; }
            if (params.value == 'Dispatched') { return {'color': '#10B981'}; }
            return {'color': 'white'};
        }
        """)
        gb.configure_column("status", cellStyle=cellsytle_jscode)

        gridOptions = gb.build()
        
        AgGrid(
            df,
            gridOptions=gridOptions,
            enable_enterprise_modules=False,
            allow_unsafe_jscode=True,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme="alpine-dark",
            height=400,
            key=f"ag_grid_{key_suffix}"
        )

# ============================================================================
# 5. SCREENS & VIEWS
# ============================================================================

def dashboard_founder():
    st.markdown(f"""
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 30px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 40px;">🏔️</div>
            <div>
                <h1 style="margin:0; line-height: 1;">NATUVISIO OS</h1>
                <span style="opacity: 0.6; letter-spacing: 2px; font-size: 12px;">ELITE EDITION v3.0</span>
            </div>
        </div>
        <div>
             <span style="padding: 8px 16px; background: rgba(78, 205, 196, 0.2); border-radius: 20px; font-size: 12px; font-weight: 600; color: #4ECDC4;">FOUNDER ACCESS</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- DATA FETCHING ---
    df_orders = OrderController.get_orders_df()
    
    # --- DANGER ZONE (Peter Norvig Logic: Error Detection) ---
    if not df_orders.empty:
        df_orders['timestamp'] = pd.to_datetime(df_orders['timestamp'])
        # Find orders stuck in 'Notified' for > 24 hours
        stuck = df_orders[
            (df_orders['status'] == 'Notified') & 
            (df_orders['timestamp'] < (datetime.now() - timedelta(hours=24)))
        ]
        
        if len(stuck) > 0:
            st.markdown(f"""
            <div class="glass-card glow-red" style="display: flex; gap: 20px; align-items: center; margin-bottom: 20px;">
                <div style="font-size: 24px;">🚨</div>
                <div>
                    <h3 style="margin:0; color: #EF4444;">ATTENTION REQUIRED</h3>
                    <div style="opacity: 0.8;">{len(stuck)} orders are stuck in dispatch for more than 24 hours. Check vendors immediately.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- KPI ROW ---
    if not df_orders.empty:
        total_rev = df_orders['total_value'].sum()
        total_comm = df_orders['commission_amt'].sum()
        pending_dispatch = len(df_orders[df_orders['status'].isin(['New', 'Notified'])])
        
        UIComponents.render_kpi_row([
            ("Total Revenue", f"{total_rev:,.0f} ₺", "Gross Volume", "#4ECDC4"),
            ("Net Commission", f"{total_comm:,.0f} ₺", "Pure Profit", "#FF6B6B"),
            ("Pending Actions", str(pending_dispatch), "Needs Attention", "#F59E0B"),
            ("Total Orders", str(len(df_orders)), "Volume", "#95E1D3")
        ])
    
    st.markdown("---")
    
    # --- MAIN INTERFACE ---
    tabs = st.tabs(["🔥 OPERATIONS", "💰 FINANCE", "📊 ANALYTICS", "📝 CREATE ORDER"])
    
    # TAB 1: OPERATIONS (Using AgGrid)
    with tabs[0]:
        c1, c2 = st.columns([2, 1])
        with c1:
            st.markdown("### 📦 Global Order Matrix")
            if not df_orders.empty:
                # AgGrid for pro interaction
                UIComponents.render_aggrid(df_orders[['order_ref', 'timestamp', 'brand', 'status', 'total_value', 'tracking_num']], "main")
            else:
                st.info("No orders in the system.")
                
        with c2:
            st.markdown("### ⚡ Quick Actions")
            # Action Panel for selected order
            if not df_orders.empty:
                pending_orders = df_orders[df_orders['status'] == 'New']
                if not pending_orders.empty:
                    order_to_process = st.selectbox("Select New Order to Notify", pending_orders['order_ref'])
                    selected_row = pending_orders[pending_orders['order_ref'] == order_to_process].iloc[0]
                    
                    st.markdown(f"""
                    <div class="glass-card">
                        <h4 style="color: {DesignSystem.COLORS.get(selected_row['brand'], '#fff')}">{selected_row['brand']}</h4>
                        <div style="font-size: 14px; margin-bottom: 10px;">{selected_row['items_json']}</div>
                        <div style="font-size: 20px; font-weight: 700; margin-bottom: 15px;">{selected_row['brand_payout']:,.0f} ₺ Payout</div>
                        <div style="font-size: 12px; color: #aaa; margin-bottom: 15px;">Customer: {selected_row['customer_name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("📲 Generate WhatsApp & Mark Notified"):
                        OrderController.update_status(selected_row['id'], "Notified")
                        st.success(f"Order {order_to_process} moved to Processing!")
                        time.sleep(1)
                        st.rerun()
                else:
                    st.success("All new orders processed.")

    # TAB 2: FINANCE (Visual Ledger)
    with tabs[1]:
        st.markdown("### 🏦 Real-Time Ledger")
        # In a real app, you'd query the LedgerEntry table
        # For this demo, we simulate a pivot table view using Plotly Heatmap or Bar
        if not df_orders.empty:
            df_fin = df_orders.groupby('brand')[['total_value', 'brand_payout', 'commission_amt']].sum().reset_index()
            
            fig = px.bar(df_fin, x='brand', y=['brand_payout', 'commission_amt'], 
                         title="Revenue Split (Payout vs Commission)",
                         color_discrete_map={'brand_payout': '#95E1D3', 'commission_amt': '#FF6B6B'},
                         barmode='stack')
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
            st.plotly_chart(fig, use_container_width=True)

    # TAB 3: ANALYTICS (Plotly)
    with tabs[2]:
        if not df_orders.empty:
            c_a1, c_a2 = st.columns(2)
            with c_a1:
                # Status Pie Chart
                fig_status = px.pie(df_orders, names='status', title='Order Lifecycle Status', hole=0.4,
                                    color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_status.update_layout(paper_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig_status, use_container_width=True)
            
            with c_a2:
                # Time Series
                df_orders['date'] = df_orders['timestamp'].dt.date
                daily = df_orders.groupby('date').size().reset_index(name='counts')
                fig_line = px.line(daily, x='date', y='counts', title='Order Velocity', markers=True)
                fig_line.update_traces(line_color='#4ECDC4')
                fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color='white')
                st.plotly_chart(fig_line, use_container_width=True)

    # TAB 4: MANUAL ORDER (Pydantic Form)
    with tabs[3]:
        with st.form("create_order_form"):
            st.markdown("#### 📝 Manual Order Entry")
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                f_brand = st.selectbox("Brand", ["HAKI HEAL", "AURORACO", "LONGEVICALS"])
                f_cust = st.text_input("Customer Name")
                f_phone = st.text_input("Phone Number")
            with c_f2:
                f_prod = st.text_input("Product Name/SKU")
                f_price = st.number_input("Total Price (₺)", min_value=0.0)
                f_qty = st.number_input("Quantity", min_value=1, value=1)
            
            f_addr = st.text_area("Delivery Address")
            
            submitted = st.form_submit_button("🚀 Launch Order")
            if submitted:
                if f_cust and f_phone and f_prod:
                    # Calculate Comm
                    rate = 0.20 if f_brand == "AURORACO" else 0.15
                    comm = f_price * rate
                    payout = f_price - comm
                    
                    data = {
                        "order_ref": f"NV-{uuid.uuid4().hex[:5].upper()}",
                        "brand": f_brand,
                        "customer_name": f_cust,
                        "phone": f_phone,
                        "address": f_addr,
                        "items_json": f"{f_prod} (x{f_qty})",
                        "total_value": f_price,
                        "commission_amt": comm,
                        "brand_payout": payout,
                        "status": "New"
                    }
                    OrderController.create_order(data)
                    st.success(f"Order {data['order_ref']} created successfully!")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Missing required fields.")

# ============================================================================
# 6. LOGIN & MAIN ENTRY POINT
# ============================================================================

def login_view():
    st.markdown("<div style='height: 20vh'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center;">
            <div style="font-size: 50px; margin-bottom: 10px;">🏔️</div>
            <h2>NATUVISIO OS</h2>
            <div style="font-size: 12px; opacity: 0.5; margin-bottom: 20px;">ACCESS CONTROL</div>
        </div>
        """, unsafe_allow_html=True)
        
        pwd = st.text_input("Secure Passkey", type="password", placeholder="Enter key...")
        
        if st.button("AUTHENTICATE"):
            # HARDCODED CHECK FOR DEMO (FOUNDER / admin2025)
            if pwd == "admin2025":
                st.session_state.user = "FOUNDER"
                st.session_state.role = "admin"
                st.rerun()
            elif pwd == "aurora123":
                 st.session_state.user = "AURORACO"
                 st.session_state.role = "vendor"
                 st.rerun()
            else:
                st.error("Access Denied")

def main():
    DesignSystem.inject_css()
    init_db() # Ensure DB exists
    
    if 'user' not in st.session_state:
        login_view()
    else:
        # Sidebar for User Profile
        with st.sidebar:
            st.markdown(f"### 👤 {st.session_state.user}")
            st.markdown(f"Role: **{st.session_state.role.upper()}**")
            st.markdown("---")
            if st.button("LOGOUT"):
                del st.session_state.user
                st.rerun()

        # Route to Dashboard
        if st.session_state.role == "admin":
            dashboard_founder()
        else:
            st.warning("Vendor Panel is a simplified version of Founder Panel (Hidden for Code brevity)")

if __name__ == "__main__":
    main()
