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

# 2. Enhanced Modern Styling
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
    
    /* Gradient background for header section */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2.5rem;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        text-align: center;
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
        color: rgba(255, 255, 255, 0.9) !important;
        letter-spacing: 0.5px !important;
        margin-top: 0 !important;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 16px;
        transition: all 0.3s ease;
        background: white;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        font-size: 18px;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5);
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
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 22px !important;
        margin-bottom: 1rem !important;
    }
    
    /* Score display */
    .score-container {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 8px 30px rgba(240, 147, 251, 0.3);
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
        color: rgba(255, 255, 255, 0.9);
        margin-top: 8px;
    }
    
    /* Alert boxes */
    .stSuccess, .stError, .stWarning, .stInfo {
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
    }
    
    /* Divider styling */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
    }
    
    /* Link button styling */
    .stLinkButton > a {
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    /* Sidebar styling */
    .css-1d391kg, [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
    }
    
    /* Spinner customization */
    .stSpinner > div {
        border-top-color: #667eea !important;
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Input label */
    .stTextInput > label {
        font-weight: 600 !important;
        color: #334155 !important;
        font-size: 16px !important;
        margin-bottom: 0.5rem !important;
    }
</style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Header Section
st.markdown("""
<div class="header-container">
    <p class="main-title">✉️ Email Deliverability Checker</p>
    <p class="sub-title">Instant Authentication & Reputation Analysis</p>
</div>
""", unsafe_allow_html=True)

# 4. Input Section
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

# 5. Audit Logic
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
            
            # Score Display
            if score >= 80:
                gradient = "linear-gradient(135deg, #11998e 0%, #38ef7d 100%)"
                st.balloons()
            elif score >= 60:
                gradient = "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)"
            else:
                gradient = "linear-gradient(135deg, #fa709a 0%, #fee140 100%)"
            
            st.markdown(f"""
            <div class="score-container" style="background: {gradient};">
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
                
                st.link_button("🔧 Fix My Email Deliverability", "https://emailsolutionpro.com/contact")
            else:
                st.success("🎉 **Excellent!** Your domain is fully configured for optimal deliverability.")
                st.link_button("💬 Contact Email Solution Pro", "https://emailsolutionpro.com/contact")
    else:
        st.info("👆 Please enter a domain name to begin the analysis.")

# Sidebar
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("### Email Solution Pro")
    
    st.markdown("---")
    st.subheader("📊 About This Tool")
    st.info(
        "This free tool checks your domain's email authentication records "
        "(MX, SPF, DKIM, DMARC) and reputation status to help diagnose "
        "deliverability issues and prevent emails from landing in spam folders."
    )
    
    st.markdown("---")
    st.subheader("🎯 What We Check")
    st.markdown("""
    - **MX Records**: Mail server configuration
    - **SPF**: Sender authentication
    - **DKIM**: Email signing
    - **DMARC**: Email policy
    - **Blacklist**: IP reputation
    """)
    
    st.markdown("---")
    st.caption("Made with ❤️ by Email Solution Pro")
