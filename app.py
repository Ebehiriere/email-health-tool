import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Email Health Audit | Email Solution Pro", page_icon="✉️", layout="centered")

# 2. Advanced Professional Styling (CSS)
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Hide Streamlit Header/Footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Center the Logo */
    .logo-container {
        display: flex;
        justify-content: center;
        padding: 20px 0px;
    }

    /* Professional Card Look */
    .result-card {
        background-color: white;
        padding: 25px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 20px;
        border: 1px solid #e9ecef;
    }

    /* Custom Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #007bff 0%, #0056b3 100%);
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 15px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        opacity: 0.9;
        transform: translateY(-2px);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Branded Header
st.markdown('<div class="logo-container">', unsafe_allow_html=True)
st.image("logo.png", width=450)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: #1e293b;'>Email Health Audit</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Verify your domain authentication and reputation in real-time.</p>", unsafe_allow_html=True)
st.divider()

# 4. Input Area
domain = st.text_input("Enter your domain", value="", placeholder="e.g. company.com")

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
if st.button("🚀 Run Full Diagnostic"):
    if domain:
        with st.spinner('Scanning DNS records...'):
            time.sleep(1)
            
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            ip_display = "N/A"

            # Layout for Analysis
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("🛡️ Security")
                
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
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("🚩 Reputation")
                try:
                    ip_display = socket.gethostbyname(domain)
                    st.info(f"IP: {ip_display}")
                    
                    rev = ".".join(reversed(ip_display.split(".")))
                    try:
                        resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                        st.error("🚨 Blacklisted (Spamhaus)")
                        black_s = False
                    except:
                        st.success("✅ IP Reputation: Clean")
                except:
                    st.error("Could not resolve IP.")
                st.markdown('</div>', unsafe_allow_html=True)

            # 6. Final Score & CTA
            st.divider()
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            
            # Using a metric for a dashboard feel
            st.metric(label="Overall Health Score", value=f"{score}%")
            
            if score >= 80:
                st.balloons()
                st.success("Excellent! Your domain is well-protected.")
            else:
                st.warning("We found vulnerabilities that could impact your deliverability.")
                st.link_button("Fix These Issues Now", "https://emailsolutionpro.com/contact")

    else:
        st.info("Please enter a domain to begin.")

# Sidebar
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("---")
st.sidebar.write("Powered by **Email Solution Pro**")
