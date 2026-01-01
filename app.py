import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro",
    page_icon="✉️",
    layout="centered"
)

# 2. Email Solution Pro Brand Styling
hide_st_style = """
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global font application */
    html, body, [class*="css"], .stMarkdown, .stTextInput, .stButton {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 900px;
    }
    
    /* Brand color variables - Email Solution Pro */
    :root {
        --primary-blue: #1e40af;
        --secondary-blue: #3b82f6;
        --accent-blue: #60a5fa;
        --dark-blue: #1e3a8a;
        --light-blue: #dbeafe;
        --success-green: #10b981;
        --warning-orange: #f59e0b;
        --error-red: #ef4444;
    }
    
    /* Gradient background for header section - Brand Blues */
    .header-container {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(30, 64, 175, 0.3);
        text-align: center;
    }
    
    /* Logo styling */
    .logo-container {
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: white;
        border-radius: 16px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Main title */
    .main-title {
        font-size: 48px !important;
        font-weight: 800 !important;
        letter-spacing: -2px !important;
        color: #ffffff !important;
        line-height: 1.1 !important;
        margin-bottom: 12px !important;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    /* Subtitle */
    .sub-title {
        font-size: 20px !important;
        font-weight: 400 !important;
        color: rgba(255, 255, 255, 0.95) !important;
        letter-spacing: 0.5px !important;
        margin-top: 0 !important;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #dbeafe;
        padding: 1rem;
        font-size: 16px;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Button styling - Brand colors */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        font-weight: 700;
        font-size: 18px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(30, 64, 175, 0.4);
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(30, 64, 175, 0.5);
    }
    
    /* Card styling for results */
    .result-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        border: 1px solid #f1f5f9;
    }
    
    /* Subheader styling */
    .stSubheader, h3 {
        color: #1e40af !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        margin-bottom: 1rem !important;
    }
    
    /* Score display - Brand colors */
    .score-container {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 30px rgba(30, 64, 175, 0.3);
    }
    
    .score-text {
        font-size: 48px;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .score-label {
        font-size: 18px;
        color: rgba(255, 255, 255, 0.95);
        margin-top: 8px;
    }
    
    /* Alert boxes - Brand color adjustments */
    .stSuccess {
        background-color: #d1fae5 !important;
        color: #065f46 !important;
        border-left: 4px solid #10b981 !important;
    }
    
    .stError {
        background-color: #fee2e2 !important;
        color: #991b1b !important;
        border-left: 4px solid #ef4444 !important;
    }
    
    .stWarning {
        background-color: #fef3c7 !important;
        color: #92400e !important;
        border-left: 4px solid #f59e0b !important;
    }
    
    .stInfo {
        background-color: #dbeafe !important;
        color: #1e3a8a !important;
        border-left: 4px solid #3b82f6 !important;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #dbeafe, transparent);
    }
    
    /* Link button styling - Brand colors */
    .stLinkButton > a {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        transition: all 0.3s ease !important;
        display: inline-block !important;
    }
    
    .stLinkButton > a:hover {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Sidebar styling - Brand colors */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f0f9ff 0%, #dbeafe 100%);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #1e40af !important;
    }
    
    /* Spinner customization - Brand color */
    .stSpinner > div {
        border-top-color: #3b82f6 !important;
    }
    
    /* Input label */
    .stTextInput > label {
        font-weight: 600 !important;
        color: #1e40af !important;
        font-size: 16px !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Balloons override for brand colors */
    .stBalloon {
        background: #3b82f6 !important;
    }
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Logo Section
try:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("https://emailsolutionpro.com/wp-content/uploads/2025/12/LogoMakr-7if6kh.png", width=300)
    st.markdown('</div>', unsafe_allow_html=True)
except:
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    try:
        st.image("logo.png", width=300)
    except:
        st.markdown("### Email Solution Pro")
    st.markdown('</div>', unsafe_allow_html=True)

# 4. Header Section
st.markdown("""
<div class="header-container">
    <p class="main-title">✉️ Free Email Deliverability Checker</p>
    <p class="sub-title">Professional Authentication & Reputation Analysis</p>
</div>
""", unsafe_allow_html=True)

# 5. Input Section
domain = st.text_input(
    "🌐 Enter Your Domain",
    value="",
    placeholder="example.com",
    help="Enter your domain without http:// or www"
)

# DNS Setup
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
resolver.timeout = 5
resolver.lifetime = 5

def robust_query(query_domain, record_type):
    """Robust DNS query with retry logic"""
    for _ in range(3):
        try:
            return resolver.resolve(query_domain, record_type)
        except:
            time.sleep(0.5)
            continue
    return None

# 6. Audit Logic
if st.button("🚀 Run Free Deliverability Audit"):
    if domain:
        with st.spinner('🔍 Analyzing your email configuration...'):
            time.sleep(1)
            
            # Initialize results
            spf_status, dmarc_status, mx_status, dkim_status, blacklist_clean = False, False, False, False, True
            ip_address = "N/A"
            
            # Create two columns for results
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("🛡️ Authentication Records")
                
                # MX Record Check
                mx_result = robust_query(domain, 'MX')
                if mx_result:
                    st.success("✅ MX Record: Configured")
                    mx_status = True
                else:
                    st.error("❌ MX Record: Missing")
                
                # SPF Record Check
                txt_result = robust_query(domain, 'TXT')
                if txt_result:
                    spf_records = [r.to_text() for r in txt_result if "v=spf1" in r.to_text()]
                    if spf_records:
                        st.success("✅ SPF Record: Configured")
                        spf_status = True
                    else:
                        st.error("❌ SPF Record: Missing")
                else:
                    st.error("❌ TXT Records: Not Found")
                
                # DMARC Record Check
                dmarc_result = robust_query(f"_dmarc.{domain}", 'TXT')
                if dmarc_result:
                    st.success("✅ DMARC Record: Configured")
                    dmarc_status = True
                else:
                    st.warning("⚠️ DMARC Record: Not Found")
                
                # DKIM Record Check
                selectors = ['google', 'default', 'k1', 'smtp', 'selector1', 'selector2']
                for selector in selectors:
                    dkim_result = robust_query(f"{selector}._domainkey.{domain}", 'TXT')
                    if dkim_result:
                        st.success(f"✅ DKIM Record: Found ({selector})")
                        dkim_status = True
                        break
                
                if not dkim_status:
                    st.info("ℹ️ DKIM: Not found (may use custom selector)")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("🔍 Reputation Check")
                
                # IP Resolution
                try:
                    ip_address = socket.gethostbyname(domain)
                    st.info(f"📍 Domain IP: `{ip_address}`")
                    
                    # Blacklist Check (Spamhaus)
                    reversed_ip = ".".join(reversed(ip_address.split(".")))
                    try:
                        resolver.resolve(f"{reversed_ip}.zen.spamhaus.org", 'A')
                        st.error("🚨 ALERT: IP is Blacklisted!")
                        blacklist_clean = False
                    except:
                        st.success("✅ IP Clean (Spamhaus)")
                except:
                    st.error("❌ Could not resolve IP address")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Calculate Score
            score = sum([mx_status, spf_status, dmarc_status, dkim_status, blacklist_clean]) * 20
            
            # Score Display - Always use brand colors
            if score >= 80:
                st.balloons()
            
            st.markdown(f"""
            <div class="score-container">
                <p class="score-text">{score}/100</p>
                <p class="score-label">Deliverability Health Score</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Recommendations
            if score < 100:
                st.warning("⚠️ **Action Required:** Issues detected that may affect email deliverability.")
                
                missing_items = []
                if not mx_status:
                    missing_items.append("MX Records")
                if not spf_status:
                    missing_items.append("SPF Record")
                if not dmarc_status:
                    missing_items.append("DMARC Record")
                if not dkim_status:
                    missing_items.append("DKIM Record")
                if not blacklist_clean:
                    missing_items.append("Blacklist Status")
                
                if missing_items:
                    st.markdown(f"**Missing/Issues:** {', '.join(missing_items)}")
                
                st.link_button("🔧 Fix My Email Deliverability Now", "https://emailsolutionpro.com/contact")
            else:
                st.success("🎉 **Excellent!** Your domain is fully configured for optimal deliverability.")
                st.link_button("💬 Contact Email Solution Pro", "https://emailsolutionpro.com/contact")
    else:
        st.info("👆 Please enter a domain name to begin the analysis.")

# Sidebar - Brand styled
with st.sidebar:
    try:
        st.image("https://emailsolutionpro.com/wp-content/uploads/2025/12/LogoMakr-7if6kh.png", use_container_width=True)
    except:
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.markdown("### Email Solution Pro")
    
    st.markdown("---")
    st.subheader("📊 About This Tool")
    st.info(
        "Professional email deliverability checker by Email Solution Pro. "
        "This free tool analyzes your domain's authentication records "
        "(MX, SPF, DKIM, DMARC) and reputation to ensure optimal email delivery."
    )
    
    st.markdown("---")
    st.subheader("🎯 What We Check")
    st.markdown("""
    - **MX Records**: Mail server configuration
    - **SPF**: Sender Policy Framework
    - **DKIM**: DomainKeys Identified Mail
    - **DMARC**: Domain-based Message Authentication
    - **Blacklist**: IP reputation status
    """)
    
    st.markdown("---")
    st.subheader("🚀 Our Services")
    st.markdown("""
    - Professional Email Setup
    - Spam Protection & Security
    - Email Management
    - Inbox Cleanup & Organization
    - Email Marketing
    - Migration Services
    """)
    
    st.markdown("---")
    st.caption("© 2025 Email Solution Pro | Professional Email Solutions")
    st.link_button("Visit Our Website", "https://emailsolutionpro.com")
