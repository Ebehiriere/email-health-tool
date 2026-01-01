import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Email Health Audit | Email Solution Pro", page_icon="✉️", layout="centered")

# 2. Premium Professional Styling (CSS)
st.markdown("""
    <style>
    /* Overall Background */
    .stApp {
        background-color: #fcfcfd;
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Centered Logo Box */
    .header-box {
        text-align: center;
        padding-top: 2rem;
        padding-bottom: 1rem;
    }

    /* Modern Card Container */
    .css-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #f0f1f3;
        margin-bottom: 1.5rem;
    }

    /* Custom Audit Button */
    .stButton>button {
        width: 100%;
        background-color: #000000; /* Sleek Black */
        color: white;
        border-radius: 8px;
        border: none;
        height: 3.5rem;
        font-size: 18px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #334155; /* Dark Slate */
        border: none;
        color: white;
        transform: translateY(-1px);
    }

    /* Subheadings */
    h2, h3 {
        color: #1e293b;
        font-weight: 700 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown('<div class="header-box">', unsafe_allow_html=True)
st.image("logo.png", width=400)
st.markdown("<h2 style='margin-top: -10px;'>Inbox Deliverability Scanner</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #64748b;'>Enterprise-grade domain authentication diagnostic</p>", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# 4. Input Area
domain = st.text_input("Domain for Audit", value="", placeholder="company.com")

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
if st.button("🚀 Start Full Diagnostic"):
    if domain:
        with st.spinner('Accessing global DNS records...'):
            time.sleep(1.2)
            
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            ip_display = "N/A"

            # Result Layout
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="css-card">', unsafe_allow_html=True)
                st.subheader("🛡️ Protocols")
                
                # MX Check
                mx_r = robust_query(domain, 'MX')
                if mx_r:
                    st.success("✅ MX Record: Found")
                    mx_s = True
                else:
                    st.error("❌ MX Record: Missing")
                
                # SPF Check
                txt_r = robust_query(domain, 'TXT')
                if txt_r:
                    spf_find = [r.to_text() for r in txt_r if "v=spf1" in r.to_text()]
                    if spf_find:
                        st.success("✅ SPF: Verified")
                        spf_s = True
                    else:
                        st.error("❌ SPF: Missing")
                
                # DMARC Check
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
            
            st.markdown(f"<h1 style='text-align: center; color: #1e293b;'>Score: {score}%</h1>", unsafe_allow_html=True)
            
            if score >= 80:
                st.balloons()
            
            # 7. Report Download
            s_color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
            report_html = f"""
            <div style="font-family: sans-serif; border-left: 10px solid {s_color}; padding: 30px; background: #fff;">
                <h1 style="color: #1e293b;">Audit Report: {domain}</h1>
                <hr>
                <p>MX Status: {'✅' if mx_s else '❌'}</p>
                <p>SPF Status: {'✅' if spf_s else '❌'}</p>
                <p>DMARC Status: {'✅' if dmarc_s else '❌'}</p>
                <p>Reputation: {'✅' if black_s else '❌'}</p>
                <h2>Health Score: {score}%</h2>
            </div>
            """
            st.download_button("📥 Download PDF-Style Report", data=report_html, file_name=f"Audit_{domain}.html")

            # 8. Business CTA
            if score < 100:
                st.markdown("---")
                st.markdown("<h3 style='text-align: center;'>Warning: Your Deliverability is at Risk</h3>", unsafe_allow_html=True)
                st.link_button("Schedule Professional Fix", "https://emailsolutionpro.com/contact")
    else:
        st.info("Input a domain to initiate diagnostic.")

# Sidebar
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.write("© 2026 Email Solution Pro")
