import streamlit as st

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="NATUVISIO Bridge",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. PREMIUM DESIGN SYSTEM (CSS) ---
def load_css():
    st.markdown("""
    <style>
    /* TYPOGRAPHY IMPORT */
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;600&family=Inter:wght@300;400;600&display=swap');

    /* ROOT VARIABLES */
    :root {
        --glass-border: rgba(255, 255, 255, 0.2);
        --glass-bg: rgba(255, 255, 255, 0.1);
        --sage-glow: rgba(160, 232, 175, 0.4);
        --forest-green: #183315;
    }

    /* GLOBAL RESET */
    .stApp {
        background-image: linear-gradient(rgba(24, 51, 21, 0.5), rgba(24, 51, 21, 0.7)), 
                          url("https://res.cloudinary.com/deb1j92hy/image/upload/v1764848571/man-standing-brown-mountain-range_elqddb.webp");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Inter', sans-serif;
    }

    /* HIDE STREAMLIT ELEMENTS */
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding-top: 2rem;}

    /* HERO TYPOGRAPHY */
    .hero-title {
        font-family: 'Lora', serif;
        font-size: 4rem;
        font-weight: 600;
        color: #f3f3ec;
        text-align: center;
        text-shadow: 0 4px 20px rgba(0,0,0,0.5);
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .hero-subtitle {
        font-family: 'Inter', sans-serif;
        font-size: 1.2rem;
        color: #e0e0e0;
        text-align: center;
        font-weight: 300;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        margin-bottom: 4rem;
    }

    /* GLASS CARD CONTAINERS */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        border-radius: 24px;
        padding: 3rem 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .glass-card:hover {
        transform: translateY(-8px);
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(160, 232, 175, 0.6);
        box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    }

    .card-icon {
        font-size: 3.5rem;
        margin-bottom: 1.5rem;
        display: block;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
    }

    .card-title {
        color: white;
        font-family: 'Lora', serif;
        font-size: 1.8rem;
        margin-bottom: 1rem;
        font-weight: 500;
    }

    .card-desc {
        color: #d0d0d0;
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 2rem;
    }

    /* PREMIUM BUTTONS */
    div.stButton > button {
        background: linear-gradient(135deg, #7C9A86 0%, #31462f 100%);
        color: white;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    div.stButton > button:hover {
        background: linear-gradient(135deg, #A0E8AF 0%, #7C9A86 100%);
        color: #183315;
        box-shadow: 0 0 25px var(--sage-glow);
        border-color: white;
    }

    /* FOOTER */
    .footer {
        text-align: center;
        color: rgba(255,255,255,0.4);
        margin-top: 5rem;
        font-size: 0.8rem;
        letter-spacing: 1px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. LAYOUT & CONTENT ---
def main():
    load_css()
    
    # Spacing
    st.markdown("<div style='height: 5vh'></div>", unsafe_allow_html=True)
    
    # Hero Section
    st.markdown('<div class="hero-title">NATUVISIO</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Decentralized Logistics OS</div>', unsafe_allow_html=True)
    
    # Main Navigation Grid
    c1, c2, c3 = st.columns([1, 1, 1]) # Centering trick if layout is wide, or adjust to 2 cols
    
    # We use a centered layout within wide columns
    col_left, col_center, col_right = st.columns([1, 8, 1])
    
    with col_center:
        grid_c1, grid_c2 = st.columns(2, gap="large")
        
        # --- ADMIN HQ CARD ---
        with grid_c1:
            st.markdown("""
            <div class="glass-card">
                <div>
                    <span class="card-icon">🏢</span>
                    <h3 class="card-title">Admin HQ</h3>
                    <p class="card-desc">
                        Internal Command Center for order validation, 
                        cart aggregation, and flash dispatching.
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Button (Streamlit buttons cannot be inside HTML div, so we place it below)
            st.markdown("<div style='margin-top: -20px; position: relative; z-index: 2;'>", unsafe_allow_html=True)
            if st.button("Enter Command Center", key="btn_hq"):
                st.switch_page("pages/Admin_HQ.py")
            st.markdown("</div>", unsafe_allow_html=True)

        # --- PARTNER PORTAL CARD ---
        with grid_c2:
            st.markdown("""
            <div class="glass-card">
                <div>
                    <span class="card-icon">🔐</span>
                    <h3 class="card-title">Partner Portal</h3>
                    <p class="card-desc">
                        Secure Fulfillment Gateway for brands 
                        (Haki Heal, Auroraco, Longevicals).
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top: -20px; position: relative; z-index: 2;'>", unsafe_allow_html=True)
            if st.button("Partner Access", key="btn_partner"):
                st.switch_page("pages/Partner_Portal.py")
            st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div class="footer">
        © 2025 NATUVISIO OPERATIONS • BUILT FOR SPEED, SCIENCE, AND TRUST
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
