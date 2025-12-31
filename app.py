import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Email Health Tool | Email Solution Pro", page_icon="✉️")

# 2. White Label: Hide Streamlit Menu and Footer
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            /* Custom styling for the audit button */
            .stButton>button {width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Logo and Header
# Updated to look for your renamed file: logo.png
try:
    st.image("logo.png", width=350)
except:
    st.title("Email Solution Pro") # Fallback if image is missing

st.markdown("### Technical Email Health Audit")
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
                
                # MX Check
                mx_r = robust_query(domain, 'MX')
                if mx_r:
                    st.success(f"✅ MX Found: {mx_r[0].exchange}")
                    mx_s = True
                else:
                    st.error("❌ MX Record Missing")
                
                # SPF Check
                txt_r = robust_query(domain, 'TXT')
                if txt_r:
                    spf_find = [r.to_text() for r in txt_r if "v=spf1" in r.to_text()]
                    if spf_find:
                        st.success(f"✅ SPF Found")
                        spf_s = True
                    else:
                        st.error("❌ SPF Record Missing")
                
                # DMARC Check
                dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
                if dm_r:
                    st.success(f"✅ DMARC Found")
                    dmarc_s = True
                else:
                    st.warning("⚠️ DMARC Not Found")

                # DKIM Check
                for sel in ['google', 'default', 'k1', 'smtp']:
                    dk_r = robust_query(f"{sel}._domainkey.{domain}", 'TXT')
                    if dk_r:
                        st.success(f"✅ DKIM Found ({sel})")
                        dkim_s = True
                        break
                if not dkim_s:
                    st.info("ℹ️ DKIM: Custom selector in use?")

            with c2:
                st.subheader("🚩 Reputation")
                try:
                    ip_display = socket.gethostbyname(domain)
                    st.info(f"Domain IP: {ip_display}")
                    
                    rev = ".".join(reversed(ip_display.split(".")))
                    try:
                        resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                        st.error("⚠️ ALERT: IP is Blacklisted!")
                        black_s = False
                    except:
                        st.success("✅ IP is Clean (Spamhaus)")
                except:
                    st.error("Could not resolve IP address.")

            # 6. Scoring & Visuals
            st.divider()
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            s_color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
            
            st.subheader(f"📊 Your Health Score: {score}/100")
            if score >= 80: st.balloons()

            # 7. Colorful Report Generation
            report_html = f"""
            <div style="font-family: Arial; border: 8px solid {s_color}; padding: 25px; border-radius: 15px;">
                <h2 style="color: {s_color};">Email Health Audit Report</h2>
                <p><b>Domain:</b> {domain} | <b>IP:</b> {ip_display}</p>
                <hr>
                <div style="font-size: 18px;">
                    <p>{'✅' if mx_s else '❌'} MX Record</p>
                    <p>{'✅' if spf_s else '❌'} SPF Record</p>
                    <p>{'✅' if dmarc_s else '❌'} DMARC Record</p>
                    <p>{'✅' if dkim_s else '❌'} DKIM Record</p>
                    <p>{'✅' if black_s else '❌'} Clean Reputation</p>
                </div>
                <h3 style="color: {s_color};">Final Score: {score}/100</h3>
                <p style="font-size: 14px;"><b>Need help fixing this?</b> Visit emailsolutionpro.com</p>
            </div>
            """

            st.download_button(
                label="📥 Download Detailed Report",
                data=report_html,
                file_name=f"Audit_{domain}.html",
                mime="text/html"
            )
            
            # 8. Business Call to Action
            if score < 100:
                st.warning("🚨 We detected issues that could send your emails to spam.")
                st.link_button("Contact an Expert to Fix This", "https://emailsolutionpro.com/contact")
    else:
        st.info("Please enter a domain name to begin.")

# Sidebar Info
st.sidebar.title("About")
st.sidebar.info("This professional tool is powered by Email Solution Pro to help businesses achieve 100% inbox delivery.")
