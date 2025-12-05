import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NATUVISIO Bridge",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM CSS STYLING ---
st.markdown("""
    <style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600&family=Inter:wght@300;400;600&display=swap');

    /* BACKGROUND */
    .stApp {
        background-image: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.5)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* GLASS CARDS */
    .custom-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 3rem 2rem;
        text-align: center;
        transition: transform 0.3s ease, background 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .custom-card:hover {
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(160, 232, 175, 0.5);
    }

    /* TYPOGRAPHY */
    h1 {
        font-family: 'Lora', serif;
        color: white !important;
        font-weight: 500;
        letter-spacing: 3px;
        text-transform: uppercase;
        text-shadow: 0 4px 10px rgba(0,0,0,0.5);
        margin: 0;
        text-align: center;
        font-size: 3.5rem;
    }
    
    h3 {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0 !important;
        font-weight: 300;
        font-size: 1.1rem;
        letter-spacing: 2px;
        margin-top: 0.5rem;
        text-align: center;
        text-transform: uppercase;
    }
    
    .card-header {
        color: white;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-family: 'Lora', serif;
    }
    
    .card-text {
        color: #d0d0d0;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }

    /* BUTTONS */
    div.stButton > button {
        background: linear-gradient(135deg, #7C9A86 0%, #31462f 100%);
        color: white;
        width: 100%;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        border: 1px solid rgba(255,255,255,0.1);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    
    div.stButton > button:hover {
        background: linear-gradient(135deg, #A0E8AF 0%, #7C9A86 100%);
        color: #183315;
        box-shadow: 0 0 20px rgba(160, 232, 175, 0.4);
        transform: translateY(-2px);
        border-color: white;
    }
    
    /* HIDE DEFAULT ELEMENTS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. MAIN LAYOUT ---
def main():
    # Spacing from top
    st.markdown("<div style='height: 10vh'></div>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("<h1>NATUVISIO</h1>", unsafe_allow_html=True)
    st.markdown("<h3>BRIDGE LOGISTICS PLATFORM</h3>", unsafe_allow_html=True)
    
    st.markdown("<div style='height: 8vh'></div>", unsafe_allow_html=True)

    # Portal Grid
    # We use columns to center the content on wide screens
    _, col_left, col_right, _ = st.columns([1, 4, 4, 1], gap="large")

    with col_left:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🏢</div>
            <div class="card-header">Admin HQ</div>
            <div class="card-text">Internal Dispatch Command Center</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Button container (negative margin to pull it up visually near the card)
        st.markdown("<div style='margin-top: -20px; position: relative; z-index: 10;'>", unsafe_allow_html=True)
        if st.button("Enter Command Center", key="btn_hq"):
            st.switch_page("pages/Admin_HQ.py")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
        <div class="custom-card">
            <div style="font-size: 3rem; margin-bottom: 1rem;">🔐</div>
            <div class="card-header">Partner Portal</div>
            <div class="card-text">Secure Brand Fulfillment Access</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: -20px; position: relative; z-index: 10;'>", unsafe_allow_html=True)
        if st.button("Partner Login", key="btn_partner"):
            st.switch_page("pages/Partner_Portal.py")
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; color: rgba(255,255,255,0.5); font-family: "Inter"; font-size: 0.8rem;'>
            © 2025 NATUVISIO OPERATIONS • AUTHORIZED ACCESS ONLY
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
