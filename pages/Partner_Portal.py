import streamlit as st
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Partner Portal", page_icon="🔐", layout="wide")

# --- SHARED SETTINGS ---
# This must match the filename in your main streamlit_app.py
CSV_FILE = "dispatch_history.csv"

# --- BRAND CREDENTIALS ---
# Give these passwords to your partners
CREDENTIALS = {
    "HAKI HEAL": "haki123",
    "AURORACO": "aurora2025",
    "LONGEVICALS": "longsci"
}

# --- PREMIUM UI & CSS (MATCHING MAIN APP) ---
st.markdown(f"""
    <style>
    /* BACKGROUND IMAGE */
    .stApp {{
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.5)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* GLASSMORPHISM CARDS */
    .stMarkdown, .stDataFrame, .stDataEditor {{
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }}
    
    /* TYPOGRAPHY */
    h1, h2, h3 {{ 
        color: white !important; 
        font-family: 'Helvetica Neue', sans-serif;
        text-shadow: 0 2px 5px rgba(0,0,0,0.5); 
    }}
    
    /* BUTTONS */
    div.stButton > button {{
        background: linear-gradient(135deg, #7C9A86 0%, #31462f 100%);
        color: white;
        border: none;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
    }}
    div.stButton > button:hover {{
        background: linear-gradient(135deg, #8FB59B 0%, #3e593b 100%);
        transform: translateY(-2px);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- LOGIN LOGIC ---
if 'logged_in_brand' not in st.session_state:
    st.title("🔐 Partner Access Portal")
    st.markdown("##### *Secure Logistics Login*")
    
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        brand_user = st.selectbox("Select Your Brand", list(CREDENTIALS.keys()))
    with col2:
        password_input = st.text_input("Access Key", type="password")
        
    if st.button("Authenticate Portal"):
        if CREDENTIALS[brand_user] == password_input:
            st.session_state.logged_in_brand = brand_user
            st.success("Access Granted.")
            st.rerun()
        else:
            st.error("❌ Invalid Access Key")
    st.stop() # Stop execution here if not logged in

# --- LOGGED IN DASHBOARD ---
brand = st.session_state.logged_in_brand

# Header & Logout
col_head, col_logout = st.columns([6, 1])
with col_head:
    st.title(f"👋 {brand} Fulfillment Panel")
with col_logout:
    if st.button("Log Out"):
        del st.session_state.logged_in_brand
        st.rerun()

st.info("👇 **Action Required:** Please mark orders as **Shipped** and enter the **Tracking Number** below. Changes save automatically to NATUVISIO HQ.")

# Load Data
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
    
    # Filter for THIS brand only
    brand_df = df[df['Brand'] == brand].copy()
    
    if not brand_df.empty:
        # Sort so 'Pending' is at the top
        brand_df = brand_df.sort_values(by="Status", ascending=True)
        
        # Interactive Editor
        edited_df = st.data_editor(
            brand_df,
            column_config={
                "Status": st.column_config.SelectboxColumn(
                    "Shipment Status",
                    options=["Pending", "Shipped", "Cancelled"],
                    required=True,
                    width="medium"
                ),
                "Tracking_Num": st.column_config.TextColumn(
                    "Tracking Code",
                    placeholder="Enter Cargo Code...",
                    help="Paste the cargo tracking number here",
                    width="medium"
                ),
                "Order_ID": st.column_config.TextColumn("Order ID", disabled=True, width="small"),
                "Time": st.column_config.TextColumn("Date/Time", disabled=True, width="small"),
                "Customer": st.column_config.TextColumn("Customer", disabled=True),
                "Items": st.column_config.TextColumn("Package Contents", disabled=True, width="large"),
                "Total_Value": st.column_config.NumberColumn("Value (TL)", disabled=True, format="%d TL"),
                "Brand": st.column_config.TextColumn(disabled=True)
            },
            hide_index=True,
            use_container_width=True,
            num_rows="fixed",
            key="partner_editor"
        )
        
        # Save Logic
        if st.button("💾 CONFIRM & SAVE UPDATES"):
            # We iterate through the edited rows and update the main dataframe
            for index, row in edited_df.iterrows():
                # Find the matching row in the original full database by Order_ID
                mask = df['Order_ID'] == row['Order_ID']
                
                # Update specific fields
                df.loc[mask, 'Status'] = row['Status']
                df.loc[mask, 'Tracking_Num'] = row['Tracking_Num']
            
            # Write back to CSV
            df.to_csv(CSV_FILE, index=False)
            st.balloons()
            st.success("✅ Synchronization Complete! HQ has been updated.")
            
    else:
        st.warning(f"No active orders found for {brand} yet.")
else:
    st.error("⚠️ Database connection pending. No orders have been generated by HQ yet.")
