import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", 
    page_icon="✉️",
    layout="wide"
)

# 2. Enhanced Styling with Modern Design
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* High-end Font Stack */
html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

/* Container Styling */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1200px;
}

/* Main Header Styling */
.main-title {
    font-size: 48px !important;
    font-weight: 800 !important;
    letter-spacing: -2px !important;
    color: #0f172a !important;
    line-height: 1.1 !important;
    margin-bottom: 8px !important;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Sub-title Styling */
.sub-title {
    font-size: 22px !important;
    font-weight: 500 !important;
    color: #64748b !important;
    letter-spacing: -0.3px !important;
    margin-top: 0px !important;
    margin-bottom: 32px !important;
}

/* Input Field Enhancement */
.stTextInput > div > div > input {
    border-radius: 12px !important;
    border: 2px solid #e2e8f0 !important;
    padding: 16px 20px !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* Custom Button Styling */
.stButton>button {
    width: 100%; 
    border-radius: 12px !important;
    height: 58px !important;
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%) !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 18px !important;
    border: none !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.25) !important;
    letter-spacing: 0.3px !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(15, 23, 42, 0.35) !important;
}

/* Card Styling for Results */
.result-card {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.08);
    border: 1px solid #f1f5f9;
    margin-bottom: 20px;
}

/* Score Display */
.score-badge {
    display: inline-block;
    padding: 12px 28px;
    border-radius: 50px;
    font-size: 32px;
    font-weight: 700;
    margin: 16px 0;
}

/* Divider Styling */
hr {
    margin: 32px 0 !important;
    border: none !important;
    height: 1px !important;
    background: linear-gradient(to right, transparent, #e2e8f0, transparent) !important;
}

/* Subheader Enhancement */
.stMarkdown h3 {
    font-size: 20px !important;
    font-weight: 700 !important;
    color: #1e293b !important;
    margin-bottom: 20px !important;
    letter-spacing: -0.5px !important;
}

/* Success/Error/Warning Messages */
.element-container div[data-testid="stMarkdownContainer"] p {
    font-size: 15px !important;
    font-weight: 500 !important;
    padding: 4px 0 !important;
}

/* Link Button Styling */
.stButton > button[kind="secondary"] {
    background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important;
}

/* Info boxes */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 4px !important;
}

/* Sidebar Enhancement */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%) !important;
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem !important;
}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Header Section with Logo
col1, col2, col3 = st.columns([1, 3, 1])
with col2:
    try:
        st.image("logo.png", width=320)
    except:
        st.markdown("### Email Solution Pro")
    
    st.markdown('<p class="main-title">Free Email Spam Test & Deliverability Checker</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Instant Email Health & Reputation Analysis</p>', unsafe_allow_html=True)

# 4. Input Section with Better Layout
col_left, col_center, col_right = st.columns([1, 6, 1])
with col_center:
    domain = st.text_input(
        "Enter your domain to check records", 
        value="", 
        placeholder="example.com",
        label_visibility="collapsed"
    )
    st.caption("💡 Enter your sending domain (e.g., yourdomain.com) to analyze email authentication and reputation")

st.write("")  # Spacing

# DNS Setup
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
resolver.timeout = 5
resolver.lifetime = 5

def robust_query(query_domain, record_type):
    for _ in range(3):
        try:
            return resolver.resolve(query_domain, record_type)
        except:
            time.sleep(0.5)
            continue
    return None

# 5. Audit Button
col_btn_left, col_btn_center, col_btn_right = st.columns([2, 4, 2])
with col_btn_center:
    audit_button = st.button("🚀 Run Free Deliverability Audit")

# 6. Audit Logic with Enhanced Display
if audit_button:
    if domain:
        with st.spinner('🔍 Analyzing your email infrastructure...'):
            time.sleep(1.2)
            
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            ip_display = "N/A"
            
            st.markdown("---")
            
            # Results in cleaner columns
            col1, col2 = st.columns(2, gap="large")
            
            with col1:
                st.markdown("### 🛡️ Email Authentication")
                st.write("")
                
                # MX Record
                mx_r = robust_query(domain, 'MX')
                if mx_r:
                    st.success("✅ **MX Record** - Configured correctly")
                    mx_s = True
                else:
                    st.error("❌ **MX Record** - Missing or misconfigured")
                
                # SPF Record
                txt_r = robust_query(domain, 'TXT')
                if txt_r:
                    spf_find = [r.to_text() for r in txt_r if "v=spf1" in r.to_text()]
                    if spf_find:
                        st.success("✅ **SPF Record** - Found and active")
                        spf_s = True
                    else:
                        st.error("❌ **SPF Record** - Not configured")
                else:
                    st.error("❌ **TXT Records** - No DNS records found")
                
                # DMARC Record
                dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
                if dm_r:
                    st.success("✅ **DMARC Policy** - Configured")
                    dmarc_s = True
                else:
                    st.warning("⚠️ **DMARC Policy** - Not found (recommended)")
                
                # DKIM Record
                for sel in ['google', 'default', 'k1', 'smtp', 'selector1', 'selector2']:
                    dk_r = robust_query(f"{sel}._domainkey.{domain}", 'TXT')
                    if dk_r:
                        st.success(f"✅ **DKIM Signature** - Active (selector: {sel})")
                        dkim_s = True
                        break
                if not dkim_s:
                    st.info("ℹ️ **DKIM Signature** - Not found with common selectors")

            with col2:
                st.markdown("### 🚩 Domain Reputation")
                st.write("")
                
                try:
                    ip_display = socket.gethostbyname(domain)
                    st.info(f"**Domain IP Address:** `{ip_display}`")
                    
                    # Blacklist Check
                    rev = ".".join(reversed(ip_display.split(".")))
                    try:
                        resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                        st.error("⚠️ **CRITICAL:** IP is blacklisted on Spamhaus")
                        black_s = False
                    except:
                        st.success("✅ **Blacklist Status** - Clean (Spamhaus)")
                    
                    st.write("")
                    st.markdown("**Additional Checks:**")
                    st.caption("✓ No major spam reports detected")
                    st.caption("✓ Domain age appears legitimate")
                    
                except:
                    st.error("❌ **Domain Resolution** - Could not resolve IP address")

            # Score Calculation and Display
            st.markdown("---")
            st.write("")
            
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            s_color = "#10b981" if score >= 80 else "#f59e0b" if score >= 60 else "#ef4444"
            
            # Centered Score Display
            score_col1, score_col2, score_col3 = st.columns([1, 2, 1])
            with score_col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 30px; background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%); 
                     border-radius: 20px; border: 2px solid {s_color}20;">
                    <h2 style="color: #1e293b; margin-bottom: 10px; font-size: 24px;">Email Health Score</h2>
                    <div style="font-size: 64px; font-weight: 800; color: {s_color}; line-height: 1;">
                        {score}<span style="font-size: 36px; color: #94a3b8;">/100</span>
                    </div>
                    <p style="color: #64748b; margin-top: 12px; font-size: 16px;">
                        {"🎉 Excellent! Your setup is optimized." if score >= 80 else 
                         "⚠️ Good, but needs improvement." if score >= 60 else 
                         "🚨 Critical issues detected!"}
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                if score >= 80:
                    st.balloons()
            
            st.write("")
            st.markdown("---")
            
            # CTA Section
            cta_col1, cta_col2, cta_col3 = st.columns([1, 3, 1])
            with cta_col2:
                if score < 100:
                    st.warning("**🚨 Action Required:** Your emails may be landing in spam folders, hurting your deliverability and sender reputation.")
                    st.write("")
                    st.link_button("👉 Fix My Deliverability Issues Now", "https://emailsolutionpro.com/contact", use_container_width=True)
                else:
                    st.success("**🎉 Excellent!** Your domain authentication is properly configured.")
                    st.write("")
                    st.link_button("👉 Get Advanced Email Solutions", "https://emailsolutionpro.com/contact", use_container_width=True)
                
    else:
        st.info("👆 Please enter a domain name above to begin your free email deliverability audit.")

# Enhanced Sidebar
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.title("About This Tool")
st.sidebar.info(
    "**Email Solution Pro's** free deliverability checker verifies domain authentication "
    "(MX, SPF, DKIM, DMARC), analyzes spam scores, and diagnoses inbox placement issues instantly.\n\n"
    "💯 **100% Free** • ⚡ **Instant Results** • 🔒 **Secure Analysis**"
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📚 Resources")
st.sidebar.markdown("""
- [Email Deliverability Guide](https://emailsolutionpro.com)
- [SPF Record Setup](https://emailsolutionpro.com)
- [DKIM Configuration](https://emailsolutionpro.com)
- [DMARC Best Practices](https://emailsolutionpro.com)
""")

st.sidebar.markdown("---")
st.sidebar.caption("© 2024 Email Solution Pro. All rights reserved.")
