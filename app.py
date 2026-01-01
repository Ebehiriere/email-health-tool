import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test | Email Solution Pro", page_icon="✉️")

# 2. THE NUCLEAR CSS (Targets toggle, header, and mobile menu)
st.markdown("""
<style>
    /* Hide the top header entirely */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Target the sidebar toggle button specifically */
    button[kind="header"] {
        display: none !important;
    }

    /* Hide the 'collapsed' control arrow */
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Fix the sidebar width and prevent it from being interactive */
    section[data-testid="stSidebar"] > div {
        width: 300px !important;
    }

    /* Custom Title Styling */
    .main-title {
        font-size: 42px !important;
        font-weight: 800 !important;
        color: #0f172a !important;
    }
    
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: #1e293b; color: white; font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR: Logo & Navigation
with st.sidebar:
    # Attempt to load logo, fallback to Text if not found
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.markdown("## Email Solution Pro")
    
    st.markdown("---")
    st.markdown("### 🛠️ More Free Tools")
    st.markdown("🏠 **[Email Health Audit](/)**")
    st.markdown("🔍 [Blacklist Monitor](https://emailsolutionpro.com/tools/blacklist)")
    st.markdown("📜 [SPF Record Generator](https://emailsolutionpro.com/tools/spf)")
    st.markdown("🔐 [DMARC Lookup Tool](https://emailsolutionpro.com/tools/dmarc)")
    
    st.divider()
    st.markdown("### 🚀 Expert Help")
    st.markdown("💼 [Managed Deliverability](https://emailsolutionpro.com/services)")
    st.markdown("📅 [Inbox Strategy Call](https://emailsolutionpro.com/book)")
    st.divider()
    st.info("System Status: Online")

# 4. Main Interface
st.markdown('<p class="main-title">Free Email Spam Test</p>', unsafe_allow_html=True)
st.write("Instant Email Health & Reputation Analysis")
st.divider()

domain = st.text_input("Enter your domain", value="", placeholder="example.com")

with st.expander("⚙️ Advanced: Manual DKIM Selector"):
    custom_selector = st.text_input("Custom DKIM Selector", placeholder="google")

# DNS Setup
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']
resolver.timeout = 5

def robust_query(query_domain, record_type):
    try: return resolver.resolve(query_domain, record_type)
    except: return None

# 5. Audit Logic
if st.button("🚀 Run Free Deliverability Audit"):
    if domain:
        with st.spinner('🛠️ Analyzing Authentication...'):
            time.sleep(1)
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🛡️ Authentication")
                if robust_query(domain, 'MX'): mx_s = True; st.success("✅ MX Found")
                else: st.error("❌ MX Missing")
                
                txt_r = robust_query(domain, 'TXT')
                if txt_r and any("v=spf1" in r.to_text() for r in txt_r):
                    spf_s = True; st.success("✅ SPF Found")
                else: st.error("❌ SPF Missing")
                
                if robust_query(f"_dmarc.{domain}", 'TXT'):
                    dmarc_s = True; st.success("✅ DMARC Found")
                else: st.warning("⚠️ DMARC Missing")

                selectors = ['google', 'default', 'k1', 'smtp', 'selector1']
                if custom_selector: selectors.insert(0, custom_selector.strip())
                for sel in selectors:
                    if robust_query(f"{sel}._domainkey.{domain}", 'TXT'):
                        dkim_s = True; st.success(f"✅ DKIM ({sel})"); break
            
            with c2:
                st.subheader("🚩 Reputation")
                try:
                    ip = socket.gethostbyname(domain)
                    st.info(f"IP: {ip}")
                    rev = ".".join(reversed(ip.split(".")))
                    try:
                        resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                        st.error("⚠️ Blacklisted!")
                        black_s = False
                    except: st.success("✅ IP is Clean")
                except: st.error("DNS Resolution Error")

            st.divider()
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            st.subheader(f"📊 Your Health Score: {score}/100")
            if score >= 80: st.balloons()

            report_template = """
            <html><body style="font-family: sans-serif; padding: 20px;">
                <div style="max-width: 600px; margin: auto; border-radius: 10px; border: 1px solid #ddd; padding: 30px; border-top: 10px solid #1e293b;">
                    <h2>Audit Report: {dom}</h2>
                    <div style="background: #1e293b; color: white; padding: 15px; text-align: center; font-size: 24px; font-weight: bold;">Score: {scr}/100</div>
                    <p>Results: MX={mx} | SPF={spf} | DMARC={dm} | DKIM={dk} | Rep={rep}</p>
                </div>
            </body></html>
            """
            report_html = report_template.format(
                dom=domain, scr=score, mx=mx_s, spf=spf_s, dm=dmarc_s, dk=dkim_s, rep=black_s
            )
            st.download_button("📥 Download Report", data=report_html, file_name=f"Audit_{domain}.html", mime="text/html")

            st.markdown("---")
            st.link_button("👉 Fix My Deliverability", "https://emailsolutionpro.com/contact")
    else:
        st.info("Please enter a domain.")
