import streamlit as st

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="NATUVISIO Bridge",
    page_icon="NATUVISIO Bridge",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- PREMIUM STYLING (Sage Green & Matte) ---
st.markdown("""
    <style>
    /* BACKGROUND IMAGE */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.4)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    /* CARD STYLING (Matte Glass) */
    .custom-card {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    .custom-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.25);
        border: 1px solid rgba(160, 232, 175, 0.5); /* Fluorescent Sage Border */
    }

    /* TYPOGRAPHY */
    h1 {
        font-family: 'Helvetica Neue', sans-serif;
        color: white !important;
        font-weight: 200;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        margin-bottom: 0px;
        text-align: center;
    }
    h3 {
        color: #e0e0e0 !important;
        font-weight: 300;
        font-size: 1.2rem;
        margin-top: 0px;
        text-align: center;
    }
    p { color: white !important; font-weight: 400; }

    /* BUTTON STYLING (Metallic Sage) */
    div.stButton > button {
        background: linear-gradient(135deg, #7C9A86 0%, #5a7564 100%);
        color: white;
        width: 100%;
        padding: 15px;
        border-radius: 10px;
        border: none;
        font-size: 16px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #A0E8AF 0%, #7C9A86 100%); /* Fluorescent Sage Hover */
        box-shadow: 0 0 20px rgba(160, 232, 175, 0.6); /* Glow Effect */
        color: #1a1a1a;
    }
    </style>
""", unsafe_allow_html=True)

# --- LAYOUT ---
st.markdown("<br><br>", unsafe_allow_html=True) # Spacing
st.markdown("<h1>NATUVISIO</h1>", unsafe_allow_html=True)
st.markdown("<h3>BRIDGE LOGISTICS PLATFORM</h3>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🏢 Admin HQ")
    st.write("Internal Dispatch Command Center")
    if st.button("Enter HQ", key="btn_hq"):
        st.switch_page("pages/Admin_HQ.py")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown("### 🔐 Partner Portal")
    st.write("Secure Brand Fulfillment Access")
    if st.button("Enter Portal", key="btn_partner"):
        st.switch_page("pages/Partner_Portal.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)
st.caption("© 2025 NATUVISIO | Authorized Access Only")

