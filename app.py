import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration (SEO Meta Title)
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", page_icon="✉️")

# 2. White Label & Premium Typography
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Professional Font Stack */
            html, body, [class*="css"]  {
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            }
            
            /* Main Title Styling */
            .main-title {
                font-size: 42px;
                font-weight: 800;
                color: #1e293b;
                letter-spacing: -1px;
                margin-bottom: 0px;
            }
            
            /* Sub-title Styling */
            .sub-title {
                font-size: 20px;
                color: #64748b;
                margin-top: -10px;
                margin-bottom: 20px;
            }

            /* Custom styling for the audit button */
            .stButton>button {
                width: 100%; 
                border-radius: 8px; 
                height: 3.5em; 
                background-color: #1e293b; 
                color: white; 
                font-weight: bold;
                border: none;
                transition: 0.3s;
                font-size: 18px;
            }
            .stButton>button:hover {
                background-color: #000000;
                transform: translateY(-2px);
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Logo and Updated Headers
try:
    st.image("logo.png", width=380)
except:
    st.title("Email Solution Pro")

# Updated catchy, professional titles
st.markdown('<p class="main-title">Free Email Spam Test & Deliverability Checker</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Instant Email Health & Reputation Analysis</p>', unsafe_allow_html=True)
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
                        st.error("❌ SPF Missing")
                
                dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
                if dm_r:
                    st.success(f"✅ DMARC Active")
                    dmarc_s = True
                else:
                    st.warning("⚠️ DMARC Not Found")

            with c2:
                st.subheader("🚩 Reputation")
                try:
                    ip_display = socket.gethostbyname(domain)
                    st.info(f"Server IP: {ip_display}")
                    rev = ".".join(reversed(ip_display.split(".")))
                    try:
                        resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                        st.error("🚨 IP Blacklisted!")
                        black_s = False
                    except:
                        st.success("✅ IP is Clean")
                except:
                    st.error("Could not resolve IP.")

            # 6. Scoring & Visuals
            st.divider()
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            s_color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
            
            st.subheader(f"📊 Your Health Score: {score}/100")
            if score >= 80: st.balloons()

            # 7. Report Generation
            report_html = f"""
            <div style="font-family: Arial; border: 8px solid {s_color}; padding: 25px; border-radius: 15px;">
                <h2 style="color: {s_color};">Email Health Audit Report</h2>
                <p><b>Domain:</b> {domain}</p>
                <hr>
                <div style="font-size: 18px;">
                    <p>{'✅' if mx_s else '❌'} MX Record</p>
                    <p>{'✅' if spf_s else '❌'} SPF Record</p>
                    <p>{'✅' if dmarc_s else '❌'} DMARC Record</p>
                    <p>{'✅' if black_s else '❌'} Clean Reputation</p>
                </div>
                <h3 style="color: {s_color};">Final Score: {score}/100</h3>
            </div>
            """

            st.download_button(
                label="📥 Download Detailed Report",
                data=report_html,
                file_name=f"Audit_{domain}.html",
                mime="text/html"
            )
            
            # 8. CTA Button
            st.markdown("---")
            if score < 100:
                st.warning("🚨 Issues detected! Your emails might be landing in spam folders.")
                st.link_button("👉 Fix My Deliverability Now", "https://emailsolutionpro.com/contact")
            else:
                st.success("Great job! Your domain is healthy.")
                st.link_button("👉 Contact Email Solution Pro", "https://emailsolutionpro.com/contact")
                
    else:
        st.info("Please enter a domain name to begin.")

# Sidebar Info
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.title("About")
st.sidebar.info("Professional tool by Email Solution Pro.")
