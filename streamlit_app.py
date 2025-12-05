import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="NATUVISIO Bridge | Decentralized Logistics OS",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load custom CSS
def load_css():
    css = """
    <style>
    /* ============================================
       NATUVISIO Bridge Design System
       Refined, Zen-Inspired Logistics Interface
       ============================================ */
    
    /* --- Typography Layer --- */
    @import url('https://fonts.googleapis.com/css2?family=Lora:wght@400;500;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    :root {
        /* Color Palette - Nature-Inspired Trust */
        --nv-forest: #183315;
        --nv-sage: #2d4a2b;
        --nv-moss: #4a6b45;
        --nv-cream: #f3f3ec;
        --nv-pearl: #fafaf5;
        --nv-shadow: rgba(24, 51, 21, 0.08);
        --nv-accent: #d4af37;
        --nv-trust-gradient: linear-gradient(135deg, #183315 0%, #2d4a2b 100%);
        
        /* Typography */
        --font-serif: 'Lora', Georgia, serif;
        --font-sans: 'Inter', -apple-system, sans-serif;
    }
    
    /* --- Reset & Foundation --- */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* --- Main Container --- */
    .main {
        background: var(--nv-pearl);
        padding: 0;
    }
    
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* ============================================
       HERO SECTION - Above the Fold
       ============================================ */
    
    .nv-hero {
        position: relative;
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--nv-trust-gradient);
        overflow: hidden;
        padding: 2rem;
    }
    
    /* Organic background pattern */
    .nv-hero::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background-image: 
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.05) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.03) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .nv-hero-content {
        position: relative;
        z-index: 10;
        max-width: 1200px;
        width: 100%;
        text-align: center;
        color: var(--nv-cream);
    }
    
    .nv-logo {
        display: inline-flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 2rem;
        animation: fadeInUp 0.8s ease-out;
    }
    
    .nv-logo-icon {
        font-size: 3rem;
        filter: drop-shadow(0 2px 8px rgba(0, 0, 0, 0.2));
    }
    
    .nv-logo-text {
        font-family: var(--font-serif);
        font-size: 1.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }
    
    .nv-tagline {
        font-family: var(--font-serif);
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.8s ease-out 0.2s both;
    }
    
    .nv-subtitle {
        font-family: var(--font-sans);
        font-size: 1.25rem;
        font-weight: 300;
        line-height: 1.6;
        margin-bottom: 1rem;
        opacity: 0.95;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
        animation: fadeInUp 0.8s ease-out 0.4s both;
    }
    
    .nv-philosophy {
        font-family: var(--font-serif);
        font-size: 1.5rem;
        font-style: italic;
        margin-bottom: 3rem;
        padding: 1.5rem;
        border-left: 3px solid var(--nv-accent);
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 0 8px 8px 0;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        animation: fadeInUp 0.8s ease-out 0.6s both;
    }
    
    /* ============================================
       PORTAL CARDS - Entry Points
       ============================================ */
    
    .nv-portals {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 3rem;
        animation: fadeInUp 0.8s ease-out 0.8s both;
    }
    
    .nv-portal-card {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 16px;
        padding: 2.5rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(20px);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .nv-portal-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--nv-forest), var(--nv-accent));
        transform: scaleX(0);
        transform-origin: left;
        transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .nv-portal-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(24, 51, 21, 0.2);
    }
    
    .nv-portal-card:hover::before {
        transform: scaleX(1);
    }
    
    .nv-portal-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .nv-portal-title {
        font-family: var(--font-serif);
        font-size: 1.75rem;
        color: var(--nv-forest);
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    
    .nv-portal-desc {
        font-family: var(--font-sans);
        font-size: 0.95rem;
        color: var(--nv-sage);
        line-height: 1.6;
        margin-bottom: 1.5rem;
    }
    
    .nv-portal-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: var(--nv-cream);
        border-radius: 20px;
        font-family: var(--font-sans);
        font-size: 0.85rem;
        font-weight: 500;
        color: var(--nv-forest);
        letter-spacing: 0.05em;
    }
    
    /* ============================================
       ARCHITECTURE SECTION - Trust Building
       ============================================ */
    
    .nv-section {
        padding: 8rem 2rem;
        background: var(--nv-pearl);
    }
    
    .nv-section-alt {
        background: white;
    }
    
    .nv-container {
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .nv-section-header {
        text-align: center;
        margin-bottom: 4rem;
    }
    
    .nv-section-title {
        font-family: var(--font-serif);
        font-size: 3rem;
        color: var(--nv-forest);
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .nv-section-subtitle {
        font-family: var(--font-sans);
        font-size: 1.25rem;
        color: var(--nv-moss);
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }
    
    /* Feature Grid */
    .nv-features {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 2.5rem;
        margin-top: 4rem;
    }
    
    .nv-feature {
        text-align: center;
        padding: 2rem;
        border-radius: 12px;
        transition: transform 0.3s ease;
    }
    
    .nv-feature:hover {
        transform: translateY(-4px);
    }
    
    .nv-feature-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
    }
    
    .nv-feature-title {
        font-family: var(--font-serif);
        font-size: 1.5rem;
        color: var(--nv-forest);
        margin-bottom: 0.75rem;
        font-weight: 600;
    }
    
    .nv-feature-desc {
        font-family: var(--font-sans);
        font-size: 1rem;
        color: var(--nv-sage);
        line-height: 1.6;
    }
    
    /* ============================================
       BRIDGE MODEL - Visual Diagram
       ============================================ */
    
    .nv-bridge-diagram {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 2rem;
        flex-wrap: wrap;
        padding: 4rem;
        background: white;
        border-radius: 24px;
        box-shadow: 0 8px 32px rgba(24, 51, 21, 0.08);
        margin-top: 3rem;
    }
    
    .nv-bridge-node {
        flex: 1;
        min-width: 200px;
        text-align: center;
        padding: 2rem;
        border-radius: 16px;
        background: var(--nv-cream);
        border: 2px solid var(--nv-forest);
        position: relative;
    }
    
    .nv-bridge-hub {
        background: var(--nv-trust-gradient);
        color: white;
        box-shadow: 0 8px 24px rgba(24, 51, 21, 0.3);
    }
    
    .nv-bridge-arrow {
        font-size: 2rem;
        color: var(--nv-moss);
        flex-shrink: 0;
    }
    
    /* ============================================
       ANIMATIONS
       ============================================ */
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* ============================================
       RESPONSIVE DESIGN
       ============================================ */
    
    @media (max-width: 768px) {
        .nv-tagline {
            font-size: 2.5rem;
        }
        
        .nv-subtitle {
            font-size: 1.1rem;
        }
        
        .nv-philosophy {
            font-size: 1.25rem;
        }
        
        .nv-section {
            padding: 4rem 1.5rem;
        }
        
        .nv-section-title {
            font-size: 2rem;
        }
        
        .nv-portals {
            grid-template-columns: 1fr;
        }
        
        .nv-bridge-diagram {
            flex-direction: column;
            padding: 2rem;
        }
        
        .nv-bridge-arrow {
            transform: rotate(90deg);
        }
    }
    
    /* ============================================
       STREAMLIT BUTTON STYLING
       ============================================ */
    
    .stButton > button {
        background: var(--nv-forest) !important;
        color: var(--nv-cream) !important;
        border: none !important;
        padding: 1rem 2.5rem !important;
        border-radius: 50px !important;
        font-family: var(--font-sans) !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
        letter-spacing: 0.05em !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        box-shadow: 0 4px 16px rgba(24, 51, 21, 0.2) !important;
    }
    
    .stButton > button:hover {
        background: var(--nv-sage) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(24, 51, 21, 0.3) !important;
    }
    
    .stButton > button:active {
        transform: translateY(0) !important;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_hero():
    hero_html = """
    <div class="nv-hero">
        <div class="nv-hero-content">
            <div class="nv-logo">
                <span class="nv-logo-icon">🌿</span>
                <span class="nv-logo-text">NATUVISIO</span>
            </div>
            
            <h1 class="nv-tagline">The Decentralized<br/>Logistics OS</h1>
            
            <p class="nv-subtitle">
                A high-trust logistics bridge connecting the world's most scientifically 
                validated wellness brands directly to the end consumer.
            </p>
            
            <div class="nv-philosophy">
                "We do not own the inventory.<br/>We own the trust."
            </div>
        </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

def render_portals():
    portals_html = """
    <div style="background: linear-gradient(135deg, #183315 0%, #2d4a2b 100%); padding: 4rem 2rem;">
        <div style="max-width: 1200px; margin: 0 auto;">
            <div class="nv-portals">
                <div class="nv-portal-card">
                    <span class="nv-portal-icon">🎯</span>
                    <h3 class="nv-portal-title">Admin HQ</h3>
                    <p class="nv-portal-desc">
                        Command center for order validation, aggregation, and dispatch. 
                        Orchestrate the entire fulfillment network from one dashboard.
                    </p>
                    <span class="nv-portal-badge">🔐 HQ ACCESS</span>
                </div>
                
                <div class="nv-portal-card">
                    <span class="nv-portal-icon">📦</span>
                    <h3 class="nv-portal-title">Partner Portal</h3>
                    <p class="nv-portal-desc">
                        Secure gateway for brand partners to receive standardized pack & ship 
                        orders in real-time. Track fulfillment status seamlessly.
                    </p>
                    <span class="nv-portal-badge">🤝 PARTNER ACCESS</span>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(portals_html, unsafe_allow_html=True)

def render_architecture():
    arch_html = """
    <div class="nv-section">
        <div class="nv-container">
            <div class="nv-section-header">
                <h2 class="nv-section-title">The Bridge Model</h2>
                <p class="nv-section-subtitle">
                    Bypassing centralized warehousing for sensitive products ensures customers 
                    receive products exactly as producers intended—fresh, potent, and untouched 
                    by middlemen.
                </p>
            </div>
            
            <div class="nv-bridge-diagram">
                <div class="nv-bridge-node">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">🌱</div>
                    <div style="font-family: var(--font-serif); font-size: 1.25rem; font-weight: 600; color: var(--nv-forest);">
                        Brand Partners
                    </div>
                    <div style="font-family: var(--font-sans); font-size: 0.9rem; color: var(--nv-sage); margin-top: 0.5rem;">
                        Longevicals • Haki Heal • Auroraco
                    </div>
                </div>
                
                <div class="nv-bridge-arrow">→</div>
                
                <div class="nv-bridge-node nv-bridge-hub">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">🌿</div>
                    <div style="font-family: var(--font-serif); font-size: 1.5rem; font-weight: 600;">
                        NATUVISIO Bridge
                    </div>
                    <div style="font-family: var(--font-sans); font-size: 0.9rem; opacity: 0.9; margin-top: 0.5rem;">
                        Central Nervous System
                    </div>
                </div>
                
                <div class="nv-bridge-arrow">→</div>
                
                <div class="nv-bridge-node">
                    <div style="font-size: 2.5rem; margin-bottom: 1rem;">👤</div>
                    <div style="font-family: var(--font-serif); font-size: 1.25rem; font-weight: 600; color: var(--nv-forest);">
                        End Consumer
                    </div>
                    <div style="font-family: var(--font-sans); font-size: 0.9rem; color: var(--nv-sage); margin-top: 0.5rem;">
                        Fresh • Potent • Direct
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(arch_html, unsafe_allow_html=True)

def render_features():
    features_html = """
    <div class="nv-section nv-section-alt">
        <div class="nv-container">
            <div class="nv-section-header">
                <h2 class="nv-section-title">Platform Capabilities</h2>
                <p class="nv-section-subtitle">
                    The command center that replaces chaos with clarity
                </p>
            </div>
            
            <div class="nv-features">
                <div class="nv-feature">
                    <span class="nv-feature-icon">🛒</span>
                    <h3 class="nv-feature-title">Smart Cart Logic</h3>
                    <p class="nv-feature-desc">
                        Build mixed SKUs from a single brand into one consolidated shipment 
                        for maximum efficiency.
                    </p>
                </div>
                
                <div class="nv-feature">
                    <span class="nv-feature-icon">🔐</span>
                    <h3 class="nv-feature-title">Role-Based Access</h3>
                    <p class="nv-feature-desc">
                        Secure login for Admin HQ vs. specific Brand Partners with granular 
                        permission controls.
                    </p>
                </div>
                
                <div class="nv-feature">
                    <span class="nv-feature-icon">⚡</span>
                    <h3 class="nv-feature-title">Flash Dispatch</h3>
                    <p class="nv-feature-desc">
                        Generate pre-formatted WhatsApp commands to warehouse managers 
                        instantly with one click.
                    </p>
                </div>
                
                <div class="nv-feature">
                    <span class="nv-feature-icon">🧊</span>
                    <h3 class="nv-feature-title">Cold Chain Priority</h3>
                    <p class="nv-feature-desc">
                        Specific flags for temperature-sensitive items like Longevicals NMN 
                        with special handling protocols.
                    </p>
                </div>
                
                <div class="nv-feature">
                    <span class="nv-feature-icon">🗃️</span>
                    <h3 class="nv-feature-title">Unified Audit Log</h3>
                    <p class="nv-feature-desc">
                        Shared, immutable ledger of every item sent, its value, and tracking 
                        status for complete transparency.
                    </p>
                </div>
                
                <div class="nv-feature">
                    <span class="nv-feature-icon">📊</span>
                    <h3 class="nv-feature-title">Real-Time Analytics</h3>
                    <p class="nv-feature-desc">
                        Track performance metrics, fulfillment times, and partner efficiency 
                        across the entire network.
                    </p>
                </div>
            </div>
        </div>
    </div>
    """
    st.markdown(features_html, unsafe_allow_html=True)

def main():
    load_css()
    
    # Hero section
    render_hero()
    
    # Portal selection
    render_portals()
    
    # Interactive portal buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<div style='padding: 3rem 0;'>", unsafe_allow_html=True)
        
        if st.button("🎯 Enter Admin HQ", key="admin"):
            st.switch_page("pages/Admin_HQ.py")
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        if st.button("📦 Enter Partner Portal", key="partner"):
            st.switch_page("pages/Partner_Portal.py")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Architecture section
    render_architecture()
    
    # Features section
    render_features()
    
    # Footer
    st.markdown("""
    <div style="background: var(--nv-forest); color: var(--nv-cream); text-align: center; padding: 3rem 2rem;">
        <div style="font-family: var(--font-serif); font-size: 1.5rem; margin-bottom: 1rem;">
            🌿 NATUVISIO Operations
        </div>
        <div style="font-family: var(--font-sans); font-size: 0.95rem; opacity: 0.8;">
            Built for Speed, Science, and Trust
        </div>
        <div style="font-family: var(--font-sans); font-size: 0.85rem; opacity: 0.6; margin-top: 1.5rem;">
            © 2025 NATUVISIO. All rights reserved.
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
