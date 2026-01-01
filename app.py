import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", page_icon="✉️")

# 2. White Label & High-End Typography Styling
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

            /* High-end Font Stack */
            html, body, [class*="css"], .stMarkdown {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            }

            /* Main Header Styling: Bold, Tight, and Impactful */
            .main-title {
                font-size: 44px !important;
                font-weight: 800 !important;
                letter-spacing: -1.8px !important;
                color: #0f172a !important; /* Premium Navy Black */
                line-height: 1.1 !important;
                margin-bottom: 0px !important;
                padding-bottom: 5px !important;
            }

            /* Sub-title Styling: Muted Slate with Spacing */
            .sub-title {
                font-size: 20px !important;
                font-weight: 400 !important;
                color: #64748b !important; /* Muted Professional Grey */
                letter-spacing: -0.5px !important;
                margin-top: -5px !important;
                margin-bottom: 25px !important;
            }

            /* Custom styling for the audit button */
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
            }
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. Logo and Professionally Styled Header
try:
    st.image("logo.png", width=350)
except:
    st.title("Email Solution Pro") 

# These use the custom CSS classes defined above
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
if st.button("🚀 Run Free Deliverability Audit"):
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
                    st.success(f"✅ MX Found")
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
                    st.info("ℹ️ DKIM: Custom selector?")

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
                        st.success("✅ IP is Clean")
                except:
                    st.error("Could not resolve IP address.")

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
                <p>{'✅' if mx_s else '❌'} MX Record</p>
                <p>{'✅' if spf_s else '❌'} SPF Record</p>
                <p>{'✅' if dmarc_s else '❌'} DMARC Record</p>
                <p>{'✅' if black_s else '❌'} Clean Reputation</p>
                <h3 style="color: {s_color};">Final Score: {score}/100</h3>
            </div>
            """

            st.download_button(label="📥 Download Detailed Report", data=report_html, file_name=f"Audit_{domain}.html", mime="text/html")
            
            # 8. Business CTA
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
