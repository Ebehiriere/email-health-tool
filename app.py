import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", page_icon="✉️")

# 2. Premium White-Label CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

            /* High-end Font Stack */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
            html, body, [class*="css"], .stMarkdown {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            }

            .main-title {
                font-size: 42px !important;
                font-weight: 800 !important;
                letter-spacing: -1.5px !important;
                color: #0f172a !important;
                line-height: 1.1 !important;
                margin-bottom: 0px !important;
                padding-bottom: 5px !important;
            }

            .sub-title {
                font-size: 20px !important;
                font-weight: 400 !important;
                color: #64748b !important;
                letter-spacing: -0.5px !important;
                margin-top: -5px !important;
                margin-bottom: 15px !important;
            }

            hr {
                margin-top: 5px !important;
                margin-bottom: 20px !important;
            }

            .stButton>button {
                width: 100%; 
                border-radius: 8px; 
                height: 3.5em; 
                background-color: #1e293b; 
                color: white; 
                font-weight: bold;
                font-size: 18px;
                border: none;
                transition: 0.3s;
            }
            .stButton>button:hover {
                background-color: #000000;
                transform: translateY(-2px);
                box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Sidebar: Branding & Resources
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.subheader("Email Solution Pro")
    
    st.markdown("### 🛠️ More Tools")
    st.markdown("- [Blacklist Monitor](https://emailsolutionpro.com/tools/blacklist)\n- [SPF Record Generator](https://emailsolutionpro.com/tools/spf)\n- [DMARC Lookup](https://emailsolutionpro.com/tools/dmarc)")
    st.divider()
    st.markdown("### 📚 Resources")
    st.markdown("- [DMARC Guide 2026](https://emailsolutionpro.com/dmarc)\n- [Avoid Spam Folders](https://emailsolutionpro.com/tips)\n- [Contact Support](https://emailsolutionpro.com/contact)")

# 4. Main Interface
st.markdown('<p class="main-title">Free Email Spam Test & Deliverability Checker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Instant Email Health & Reputation Analysis</p>', unsafe_allow_html=True)
st.divider()

domain = st.text_input("Enter your domain to check records", value="", placeholder="example.com")

with st.expander("⚙️ Advanced: Manual DKIM Selector"):
    custom_selector = st.text_input("Custom DKIM Selector (Optional)", placeholder="e.g., s1, mandrill, m1")

# DNS Setup
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
resolver.timeout = 5

def robust_query(query_domain, record_type):
    try:
        return resolver.resolve(query_domain, record_type)
    except:
        return None

# 5. Audit Logic
if st.button("🚀 Run Free Deliverability Audit"):
    if domain:
        with st.spinner('🛠️ Analyzing Authentication & Reputation...'):
            time.sleep(1.2)
            
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            ip_display = "N/A"
            active_selector = "None"

            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("🛡️ Authentication")
                mx_r = robust_query(domain, 'MX')
                if mx_r:
                    st.success("✅ MX Found")
                    mx_s = True
                else
