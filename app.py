import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration - Meta Title for Google
st.set_page_config(page_title="Free Email Deliverability & Spam Test | Email Solution Pro", page_icon="✉️", layout="centered")

# 2. Premium Professional Styling (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfd; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .header-box { text-align: center; padding-top: 2rem; padding-bottom: 1rem; }
    .css-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #f0f1f3;
        margin-bottom: 1.5rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #000000;
        color: white;
        border-radius: 8px;
        border: none;
        height: 3.5rem;
        font-size: 18px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background-color: #334155; color: white; transform: translateY(-1px); }
    h1 { font-size: 2.2rem !important; color: #1e293b !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. SEO-Optimized Header
st.markdown('<div class="header-box">', unsafe_allow_html=True)
st.image("logo.png", width=400)
# This H1 tag is critical for SEO
st.markdown("<h1>Free Email Deliverability & Spam Test</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b; font-size: 1.1rem;'>Instantly check SPF, DKIM, DMARC, and Blacklist status to stop emails from hitting spam.</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 4. Input Area
domain = st.text_input("Enter your domain to scan", value="", placeholder="e.g. yourcompany.com")

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
if st.button("🚀 Run Deliverability Audit"):
    if domain:
        with st.spinner('Checking DNS records and sender reputation...'):
            time.sleep(1.2)
            
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            ip_display = "N/A"

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("🛡️ Authentication")
                mx_r = robust_query(domain, 'MX')
                if mx_r:
                    st.success("✅ MX Record: Found")
                    mx_s = True
                else:
                    st.error("❌ MX Record: Missing")
                
                txt_r = robust_query(domain, 'TXT')
                if txt_r:
                    spf_find = [r.to_text() for r in txt_r if "v=spf1" in r.to_text()]
                    if spf_find:
                        st.success("✅ SPF: Verified")
                        spf_s = True
                    else:
                        st.error("❌ SPF: Missing")
                
                dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
                if dm_r:
                    st.success("✅ DMARC: Active")
                    dmarc_s = True
                else:
                    st.warning("⚠️ DMARC: Inactive")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("🚩 Reputation")
                try:
                    ip_display = socket.gethostbyname(domain)
                    st.info(f"Server IP: {ip_display}")
                    rev = ".".join(reversed(ip_display.split(".")))
                    try:
                        resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                        st.error("🚨 Blacklisted (Spamhaus)")
                        black_s = False
                    except:
                        st.success("✅ IP Status: Clean")
                except:
                    st.error("Unable to resolve IP.")
                st.markdown('</div>', unsafe_allow_html=True)

            # 6. Scoring Section
            st.divider()
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            st.markdown(f"<h1 style='text-align: center;'>Your Deliverability Score: {score}%</h1>", unsafe_allow_html=True)
            
            if score >= 80: st.balloons()
            
            # 7. Report Download
            s_color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
            report_html = f"""
            <div style="font-family: sans-serif; border-left: 10px solid {s_color}; padding: 30px; background: #fff;">
                <h1 style="color: #1e293b;">Deliverability Audit: {domain}</h1>
                <hr>
                <p>MX Status: {'✅' if mx_s else '❌'}</p>
                <p>SPF Status: {'✅' if spf_s else '❌'}</p>
                <p>DMARC Status: {'✅' if dmarc_s else '❌'}</p>
                <p>Reputation Status: {'✅' if black_s else '❌'}</p>
                <h2>Final Health Score: {score}%</h2>
                <p>Fixing these issues will ensure your emails reach the inbox.</p>
            </div>
            """
            st.download_button("📥 Download My Full Audit Report", data=report_html, file_name=f"Email_Audit_{domain}.html")

            # 8. Business CTA
            if score < 100:
                st.markdown("---")
                st.markdown("<h3 style='text-align: center;'>Want to reach 100% Inbox Placement?</h3>", unsafe_allow_html=True)
                st.link_button("Get Help Fixing Your Deliverability", "https://emailsolutionpro.com/contact")
    else:
        st.info("Please enter a domain to start your free deliverability scan.")

# Sidebar
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.write("Powered by **Email Solution Pro**")
