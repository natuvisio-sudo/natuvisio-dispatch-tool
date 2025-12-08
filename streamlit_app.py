import streamlit as st

st.set_page_config(
    page_title="NATUVISIO Bridge",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- PREMIUM STYLING ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;600&family=Inter:wght@300;400;600&display=swap');
    
    .stApp {
        background-image: linear-gradient(rgba(15, 23, 42, 0.9), rgba(15, 23, 42, 0.8)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 40px;
        text-align: center;
        transition: transform 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .glass-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.1);
        border-color: rgba(160, 232, 175, 0.5);
    }
    
    h1 { font-family: 'Space Grotesk', sans-serif; color: white !important; font-size: 3.5rem; margin-bottom: 0; }
    h3 { font-family: 'Inter', sans-serif; color: #a0aec0 !important; font-weight: 300; letter-spacing: 2px; margin-top: 0; }
    
    div.stButton > button {
        background: linear-gradient(135deg, #7C9A86 0%, #31462f 100%);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 15px;
        border-radius: 12px;
        font-weight: 600;
        text-transform: uppercase;
        width: 100%;
        transition: all 0.3s ease;
    }
    div.stButton > button:hover {
        background: linear-gradient(135deg, #A0E8AF 0%, #7C9A86 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(160, 232, 175, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# --- LAYOUT ---
def main():
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center'>NATUVISIO</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center'>BRIDGE LOGISTICS OS</h3>", unsafe_allow_html=True)
    st.markdown("<div style='height: 8vh'></div>", unsafe_allow_html=True)

    _, c1, c2, _ = st.columns([1, 4, 4, 1], gap="large")

    with c1:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size: 40px; margin-bottom: 20px;">🏢</div>
            <div style="color: white; font-size: 24px; font-weight: 600; margin-bottom: 10px;">Admin HQ</div>
            <div style="color: #cbd5e0; margin-bottom: 30px;">Internal Command Center</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: -30px; position: relative; z-index: 2;'>", unsafe_allow_html=True)
        if st.button("Enter HQ", key="btn_hq"):
            st.switch_page("pages/Admin_HQ.py")
        st.markdown("</div>", unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size: 40px; margin-bottom: 20px;">🔐</div>
            <div style="color: white; font-size: 24px; font-weight: 600; margin-bottom: 10px;">Partner Portal</div>
            <div style="color: #cbd5e0; margin-bottom: 30px;">Secure Brand Access</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='margin-top: -30px; position: relative; z-index: 2;'>", unsafe_allow_html=True)
        if st.button("Partner Login", key="btn_partner"):
            st.switch_page("pages/Partner_Portal.py")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<br><br><br><div style='text-align: center; color: rgba(255,255,255,0.3);'>© 2025 NATUVISIO OPERATIONS</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
