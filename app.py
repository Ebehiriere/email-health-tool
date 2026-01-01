import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", page_icon="✉️")

# 2. White Label & Premium Typography Styling
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

            /* High-end Font Stack */
            html, body, [class*="css"], .stMarkdown {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            }

            /* Professional Main Header Styling */
            .main-title {
                font-size: 44px !important;
                font-weight: 800 !important;
                letter-spacing: -1.8px !important;
                color: #0f172a !important;
                line-height: 1.1 !important;
                margin-bottom: 0px !important;
                padding-bottom: 5px !important;
            }

            /* Professional Sub-title Styling */
            .sub-title {
                font-size: 20px !important;
                font-weight: 400 !important;
                color: #64748b !important;
                letter-spacing: -0.5px !important;
                margin-top: -5px !important;
                margin-bottom: 25px !important;
            }

            /* Custom styling for the audit button */
            .stButton>button {
                width: 100%; border-radius: 5px; height: 3em; 
                background-color: #007bff; color: white;
                font-weight: bold;
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Logo and Professionally Styled Header
try:
    st.image("logo.png", width=350)
except:
    st.title("Email Solution Pro") 

st.markdown('<p class="main-title">Free Email Spam Test & Deliverability Checker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Instant Email Health & Reputation Analysis</p>', unsafe_allow_html=True)
st.divider()

# 4. Input Area
domain = st.text_input("Enter your domain to check records", value="", placeholder="example.com")

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
if st.button("🚀 Start Full Audit"):
    if domain:
        with st.spinner('🛠️ Analyzing Authentication & Reputation...'):
            time.sleep(1.2)
            
            # Variables for Scoring
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            ip_display = "N/A"

            # Results Display
            c1, c2 = st.columns(2)
            
            with c1:
                st.subheader("🛡️ Authentication")
                mx_r = robust_query(domain, 'MX')
                if mx_r:
                    st.success(f"✅ MX Found: {mx_r[0].exchange}")
                    mx_s = True
                else:
                    st.error("❌ MX Record Missing")
                
                txt_r = robust_query(domain, 'TXT')
                if txt_r:
                    spf_find = [r.to_text() for r in txt_r if "v=spf1" in r.to_text()]
                    if spf_find:
                        st.success(f"✅ SPF Found")
                        spf_s = True
                    else:
