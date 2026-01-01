import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(
    page_title="Email Health Audit | Email Solution Pro",
    page_icon="✉️",
    layout="wide"
)

# 2. Advanced Professional Styling (Enterprise CSS)
st.markdown("""
    <style>
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Import Inter Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', sans-serif;
    }

    /* Background and Container */
    .main {
        background-color: #f8fafc;
    }

    /* Hero Section */
    .hero-container {
        padding: 2rem 0rem;
        text-align: left;
    }
    
    .main-title {
        font-size: 48px !important;
        font-weight: 800 !important;
        letter-spacing: -2px !important;
        color: #1e293b !important;
        line-height: 1 !important;
        margin-bottom: 10px !important;
    }

    .sub-title {
        font-size: 22px !important;
        color: #64748b !important;
        margin-bottom: 30px !important;
    }

    /* Card Styling */
    .audit-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #1e293b !important;
        color: white !important;
    }
    
    section[data-testid="stSidebar"] .stMarkdown, section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2, section[data-testid="stSidebar"] h3 {
        color: white !important;
    }

    /* Button Styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3.5em;
        background-color: #2563eb !important;
        color: white !important;
        font-weight: 600;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1d4ed8 !important;
        transform: translateY(-1px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar Construction
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.subheader("✉️ Email Solution Pro")
    
    st.markdown("---")
    
    st.markdown("### 🛠️ More Tools")
    st.page_link("https://emailsolutionpro.com/tools/blacklist-checker", label="Blacklist Monitor", icon="🚫")
    st.page_link("https://emailsolutionpro.com/tools/spf-generator", label="SPF Record Generator", icon="📝")
    st.page_link("https://emailsolutionpro.com/tools/dmarc-lookup", label="DMARC Lookup", icon="🔍")
    
    st.markdown("---")
    
    st.markdown("### 📚 Resources")
    st.markdown("""
    * [Deliverability Guide 2026](https://emailsolutionpro.com/blog)
    * [Avoid the Spam Folder](https://emailsolutionpro.com/tips)
    * [API Documentation](https://emailsolutionpro.com/docs)
    """)
    
    st.markdown("---")
    st.info("Instant health check for your domain reputation.")

# 4. Main Interface
st.markdown('<div class="hero-container">', unsafe_allow_html=True)
st.markdown('<p class="main-title">Technical Email Health Audit</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Verify DNS authentication and server reputation in seconds.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Layout for Input
col_a, col_b = st.columns([2, 1])
with col_a:
    domain = st.text_input("Domain Name", placeholder="e.g. yourcompany.com", label_visibility="collapsed")
with col_b:
    run_audit = st.button("Analyze Domain")

# DNS Helper Functions
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
resolver.timeout = 5
resolver.lifetime = 5

def robust_query(query_domain, record_type):
    for _ in range(3):
        try: return resolver.resolve(query_domain, record_type)
        except: time.sleep(0.5); continue
    return None

# 5. Logic & Presentation
if run_audit:
    if domain:
        with st.spinner('Running deep technical analysis...'):
            time.sleep(1)
            
            # Data Collection
            mx_r = robust_query(domain, 'MX')
            txt_r = robust_query(domain, 'TXT')
            dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
            
            # Scores
            spf_s = any("v=spf1" in r.to_text() for r in txt_r) if txt_r else False
            dkim_s = any(robust_query(f"{s}._domainkey.{domain}", 'TXT') for s in ['google', 'default', 'k1', 'smtp'])
            mx_s = True if mx_r else False
            dmarc_s = True if dm_r else False
            
            # Reputation Check
            try:
                ip = socket.gethostbyname(domain)
                rev = ".".join(reversed(ip.split(".")))
                try:
                    resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                    black_s = False
                except:
                    black_s = True
            except:
                black_s = True
                ip = "Unresolved"

            # Display Results in Clean Cards
            res_1, res_2, res_3 = st.columns(3)
            
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            
            with res_1:
                st.metric("Health Score", f"{score}%", delta=f"{score-100}%" if score < 100 else "Perfect")
            with res_2:
                st.metric("Primary IP", ip)
            with res_3:
                status = "Clean" if black_s else "Listed"
                st.metric("Reputation", status)

            st.divider()

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("### 🛡️ Authentication")
                st.write(f"{'✅' if mx_s else '❌'} **MX Records:** Required for receiving mail.")
                st.write(f"{'✅' if spf_s else '❌'} **SPF Record:** Authorizes your sending IP.")
                st.write(f"{'✅' if dmarc_s else '❌'} **DMARC Record:** Policy for failed auth.")
                st.write(f"{'✅' if dkim_s else '❌'} **DKIM Record:** Cryptographic signature.")

            with c2:
                st.markdown("### 🚩 Recommendations")
                if score < 100:
                    st.error("Action Required: Your deliverability is at risk.")
                    st.link_button("Get Professional Help", "https://emailsolutionpro.com/contact")
                else:
                    st.success("Your technical setup is optimal for inbox delivery.")
                    st.link_button("View Advanced Monitoring", "https://emailsolutionpro.com/pricing")

    else:
        st.toast("Please enter a domain first!", icon="⚠️")
