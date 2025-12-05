import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="NATUVISIO Bridge",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    .custom-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    h1 { color: white !important; font-weight: 200; letter-spacing: 3px; margin: 0; text-align: center; }
    h3 { color: #e0e0e0 !important; font-weight: 300; margin: 0; text-align: center; }
    
    div.stButton > button {
        background: linear-gradient(135deg, #7C9A86 0%, #5a7564 100%);
        color: white;
        width: 100%;
        padding: 15px;
        border-radius: 10px;
        border: none;
        font-weight: 600;
        text-transform: uppercase;
    }
    </style>
""", unsafe_allow_html=True)

# --- LAYOUT ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h1>NATUVISIO</h1>", unsafe_allow_html=True)
st.markdown("<h3>BRIDGE LOGISTICS PLATFORM</h3>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🏢 Admin HQ")
    st.write("Internal Dispatch Command Center")
    # This path MUST match the file location exactly
    if st.button("Enter HQ", key="btn_hq"):
        st.switch_page("pages/Admin_HQ.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🔐 Partner Portal")
    st.write("Secure Brand Fulfillment Access")
    # This path MUST match the file location exactly
    if st.button("Enter Portal", key="btn_partner"):
        st.switch_page("pages/Partner_Portal.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.caption("© 2025 NATUVISIO | Authorized Access Only")
