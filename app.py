import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration (SEO Meta Title)
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", page_icon="✉️", layout="centered")

# 2. Premium Professional Styling (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #fcfcfd; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Header Container */
    .header-box { text-align: center; padding-top: 2rem; padding-bottom: 1rem; }
    
    /* Modern Card Container */
    .css-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #f0f1f3;
        margin-bottom: 1.5rem;
    }

    /* Main Action Button */
    .stButton>button {
        width: 100%;
        background-color: #1e293b; /* Professional Deep Slate */
        color: white;
        border-radius: 8px;
        border: none;
        height: 3.8rem;
        font-size: 20px;
        font-weight: 700;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button:hover { 
        background-color: #0f172a; 
        color: white; 
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }

    /* Typography */
    h1 { font-size: 2.5rem !important; color: #1e293b !important; line-height: 1.2 !important; }
    .cta-text { font-size: 1.2rem; color: #475569; margin-bottom: 2rem; }
    </style>
    """, unsafe_allow_html=True)

# 3. SEO-Optimized Header & Branding
st.markdown('<div class="header-box">', unsafe_allow_html=True)
st.image("logo.png", width=420)
st.markdown("<h1>Free Email Spam Test & Deliverability Checker</h1>", unsafe_allow_html=True)
st.markdown('<p class="cta-text">Check your domain authentication and blacklist status to stop emails from hitting spam.</p>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 4. Input Area
domain = st.text_input("Enter your domain name to begin", value="", placeholder="e.g. yourcompany.com")

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
if st.button("🚀 Run My Free Audit"):
    if domain:
        with st.spinner('Performing technical diagnostic...'):
            time.sleep(1.2)
            
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            ip_display = "N/A"

            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("🛡️ Domain Setup")
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
                    st.warning("⚠️ DMARC: Missing")
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("🚩 Inbox Security")
                try:
                    ip_display = socket.gethostbyname(domain)
                    st.info(f"Sender IP: {ip_display}")
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

            # 6. Final Score
            st.divider()
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            st.markdown(f"<h1 style='text-align: center; color: #1e293b;'>Deliverability Score: {score}%</h1>", unsafe_allow_html=True)
            
            if score >= 80: st.balloons()
            
            # 7. Report Download
            s_color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
            report_html = f"""
            <div style="font-family: sans-serif; border-left: 10px solid {s_color}; padding: 30px; background: #fff; border-radius: 10px; border: 1px solid #eee;">
                <h1 style="color: #1e293b;">Technical Audit Report: {domain}</h1>
                <hr>
                <p>MX Configuration: {'✅' if mx_s else '❌'}</p>
                <p>SPF Authentication: {'✅' if spf_s else '❌'}</p>
                <p>DMARC Security: {'✅' if dmarc_s else '❌'}</p>
                <p>Sender Reputation: {'✅' if black_s else '❌'}</p>
                <h2 style="color: {s_color};">Final Health Score: {score}%</h2>
                <p>Generated by Email Solution Pro</p>
            </div>
            """
            st.download_button("📥 Download This Audit Report", data=report_html, file_name=f"Spam_Test_{domain}.html")

            # 8. CALL TO ACTION BUTTON
            if score < 100:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="css-card" style="text-align: center; border-top: 4px solid #dc3545;">', unsafe_allow_html=True)
                st.markdown("<h3>🚨 Want to Reach 100% Inbox Placement?</h3>", unsafe_allow_html=True)
                st.markdown("<p>We found issues that are actively hurting your email reputation. Let our experts fix your setup today.</p>", unsafe_allow_html=True)
                st.link_button("👉 Fix My Deliverability Now", "https://emailsolutionpro.com/contact")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="css-card" style="text-align: center; border-top: 4px solid #28a745;">', unsafe_allow_html=True)
                st.markdown("<h3>Looking for Managed Email Solutions?</h3>", unsafe_allow_html=True)
                st.link_button("Contact Email Solution Pro", "https://emailsolutionpro.com/contact")
                st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("Please enter a domain to start the free deliverability checker.")

# Sidebar
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.write("© 2026 **Email Solution Pro**")
st.sidebar.write("Technical Support for Inbox Deliverability.")
