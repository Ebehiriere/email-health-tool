import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test | Email Solution Pro", page_icon="✉️")

# 2. Clean & Sophisticated CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Typography */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', sans-serif;
    }

    /* Main Container Spacing */
    .block-container {
        padding-top: 2rem !important;
        max-width: 800px;
    }

    /* Professional Headers */
    .main-header {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
        letter-spacing: -1.5px !important;
        line-height: 1.1;
        margin-bottom: 8px;
    }
    .sub-header {
        font-size: 18px !important;
        color: #64748b !important;
        margin-bottom: 30px;
    }

    /* Input Styling */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        padding: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* Button Styling */
    .stButton > button {
        width: 100%;
        background-color: #0f172a !important;
        color: white !important;
        border-radius: 8px !important;
        height: 3.5rem !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #334155 !important;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar: Resources & Tools
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.subheader("Email Solution Pro")
    
    st.markdown("### 📚 Resources")
    st.markdown("""
    Find guides and documentation to help you master email deliverability.
    
    * [DMARC Implementation Guide](https://emailsolutionpro.com/dmarc)
    * [SPF & DKIM Explained](https://emailsolutionpro.com/dns)
    * [Avoid Spam Filters](https://emailsolutionpro.com/tips)
    """)
    
    st.divider()
    
    st.markdown("### 🛠️ Other Tools")
    st.markdown("""
    * [Blacklist Monitor](https://emailsolutionpro.com/tools/blacklist)
    * [SPF Record Generator](https://emailsolutionpro.com/tools/spf)
    * [Contact an Expert](https://emailsolutionpro.com/contact)
    """)
    
    st.divider()
    st.info("Ensuring your emails reach the inbox, every time.")

# 4. Main UI Content
st.markdown('<p class="main-header">Email Health Audit</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Identify technical issues preventing your emails from reaching the inbox.</p>', unsafe_allow_html=True)

domain = st.text_input("Enter your domain", placeholder="example.com", label_visibility="collapsed")

# DNS Helper
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
resolver.timeout = 5

def check_dns(d, t):
    try: return resolver.resolve(d, t)
    except: return None

# 5. Execution Logic
if st.button("Run Technical Audit"):
    if domain:
        with st.spinner("Analyzing domain records..."):
            time.sleep(1)
            
            # Checks
            mx = check_dns(domain, 'MX')
            txt = check_dns(domain, 'TXT')
            dmarc = check_dns(f"_dmarc.{domain}", 'TXT')
            
            spf_found = any("v=spf1" in r.to_text() for r in txt) if txt else False
            dkim_found = any(check_dns(f"{s}._domainkey.{domain}", 'TXT') for s in ['google', 'default', 'k1', 'smtp'])
            
            # Reputation
            try:
                ip = socket.gethostbyname(domain)
                rev = ".".join(reversed(ip.split(".")))
                is_blacklisted = False
                try: 
                    resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                    is_blacklisted = True
                except: pass
            except:
                ip = "N/A"
                is_blacklisted = False

            # Display Results
            score = sum([bool(mx), spf_found, bool(dmarc), dkim_found, not is_blacklisted]) * 20
            
            st.divider()
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 🛡️ Authentication")
                st.write(f"{'✅' if mx else '❌'} MX Record")
                st.write(f"{'✅' if spf_found else '❌'} SPF Record")
                st.write(f"{'✅' if dmarc else '❌'} DMARC Record")
                st.write(f"{'✅' if dkim_found else '❌'} DKIM Record")
                
            with col2:
                st.markdown("### 🚩 Reputation")
                st.write(f"**IP Address:** {ip}")
                if is_blacklisted:
                    st.error("⚠️ IP Blacklisted (Spamhaus)")
                else:
                    st.success("✅ Reputation is Clean")

            st.markdown(f"## Health Score: {score}/100")
            
            st.divider()
            
            if score < 100:
                st.warning("We found issues that could cause your emails to land in the spam folder.")
                st.link_button("👉 Fix My Deliverability Now", "https://emailsolutionpro.com/contact")
            else:
                st.success("Your technical setup looks great!")
                st.link_button("👉 Maintain Your Reputation", "https://emailsolutionpro.com/contact")
    else:
        st.error("Please enter a domain name.")
