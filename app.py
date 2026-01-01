import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", page_icon="✉️")

# 2. White Label & Premium Typography (The "Better" Style)
hide_st_style = """
            <style>
            /* Import Google Font for a modern SaaS look */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Apply Inter Font to everything */
            html, body, [class*="css"], .stMarkdown {
                font-family: 'Inter', sans-serif;
            }

            /* Main Header: Bold, tight letter-spacing for premium feel */
            h1 {
                font-family: 'Inter', sans-serif;
                font-weight: 800 !important;
                letter-spacing: -1.8px !important;
                color: #0f172a !important; /* Professional Navy Black */
                font-size: 2.8rem !important;
                line-height: 1.1 !important;
                padding-bottom: 0.5rem !important;
            }

            /* Subheader: Muted slate color */
            h3 {
                font-family: 'Inter', sans-serif;
                font-weight: 400 !important;
                color: #64748b !important; 
                letter-spacing: -0.5px !important;
                margin-top: -10px !important;
                padding-bottom: 1rem !important;
            }

            /* Professional Audit Button with soft shadow */
            .stButton>button {
                width: 100%; 
                border-radius: 8px; 
                height: 3.5em; 
                background-color: #1e293b; 
                color: white; 
                font-weight: 700;
                font-size: 18px;
                border: none;
                transition: all 0.3s ease;
                box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
            }
            .stButton>button:hover {
                background-color: #000000;
                transform: translateY(-2px);
                box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1);
                color: white;
            }
            
            /* Success/Error message styling */
            .stAlert {
                border-radius: 10px !important;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Logo and Header
try:
    st.image("logo.png", width=350)
except:
    st.title("Email Solution Pro") 

st.markdown("# Free Email Spam Test & Deliverability Checker")
st.markdown("### Instant Email Health & Reputation Analysis")
st.divider()

# 4. Input Area
domain = st.text_input("Enter your domain to check records", value="", placeholder="e.g. company.com")

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

# 5. Audit Logic
if st.button("🚀 Run Free Deliverability Audit"):
    if domain:
        with st.spinner('🔍 Analyzing Authentication & Reputation...'):
            time.sleep(1.2)
            
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            ip_display = "N/A"

            # Results Display
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("🛡️ Authentication")
                mx_r = robust_query(domain, 'MX')
                if mx_r:
                    st.success(f"✅ MX Found")
                    mx_s = True
                else:
                    st.error("❌ MX Record Missing")
                
                txt_r = robust_query(domain, 'TXT')
                if txt_r:
                    spf_find = [r.to_text() for r in txt_r if "v=spf1" in r.to_text()]
                    if spf_find:
                        st.success(f"✅ SPF Verified")
                        spf_s = True
                    else:
                        st.error("❌ SPF Record Missing")
                
                dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
                if dm_r:
                    st.success(f"✅ DMARC Active")
                    dmarc_s = True
                else:
                    st.warning("⚠️ DMARC Not Found")

                for sel in ['google', 'default', 'k1', 'smtp']:
                    dk_r = robust_query(f"{sel}._domainkey.{domain}", 'TXT')
                    if dk_r:
                        st.success(f"✅ DKIM Found ({sel})")
                        dkim_s = True
                        break
                if not dkim_s:
