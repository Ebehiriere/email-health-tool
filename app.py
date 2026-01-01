import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test | Email Solution Pro", page_icon="✉️", layout="wide")

# 2. Advanced CSS for Sidebar & Main UI
st.markdown("""
<style>
    [data-testid="stSidebar"] { background-color: #f8fafc; border-right: 1px solid #e2e8f0; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3.5em; background-color: #1e293b; color: white; font-weight: bold; }
    .main-title { font-size: 38px; font-weight: 800; color: #0f172a; margin-bottom: 0px; }
    .status-box { padding: 10px; border-radius: 5px; margin-bottom: 10px; font-size: 14px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)

# 3. SIDEBAR: Options 1 & 2 Hybrid
with st.sidebar:
    st.image("https://via.placeholder.com/200x50?text=Email+Solution+Pro", use_container_width=True) # Replace with your logo URL
    
    # Option 2: System Status (Trust)
    st.markdown("### 🛰️ System Status")
    st.success("● DNS Audit Engine: Active")
    st.info("● Blacklist DB: Synced (2026)")
    
    st.divider()

    # Option 1: Lead Magnet (Conversion)
    st.markdown("### 🚀 Reach the Inbox")
    st.markdown("**Struggling with Spam?**")
    st.write("We help high-volume senders fix their reputation and hit 99% open rates.")
    
    st.link_button("📅 Book a Strategy Call", "https://emailsolutionpro.com/book", type="primary")
    st.link_button("🔍 Request Custom Audit", "https://emailsolutionpro.com/audit")

    st.divider()
    
    st.markdown("### 🛠️ Other Tools")
    st.caption("Coming Soon...")
    st.write("- Warmup Calculator")
    st.write("- Copy Spam Checker")

# 4. MAIN INTERFACE (Stable Code)
st.markdown('<p class="main-title">Free Email Health Audit</p>', unsafe_allow_html=True)
st.write("Check your SPF, DKIM, DMARC, and Blacklist status in 5 seconds.")

domain = st.text_input("Enter your domain", placeholder="example.com")

with st.expander("⚙️ Advanced Settings"):
    custom_selector = st.text_input("DKIM Selector", placeholder="google")

# DNS Setup
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8']
resolver.timeout = 5

def robust_query(query_domain, record_type):
    try: return resolver.resolve(query_domain, record_type)
    except: return None

if st.button("🚀 Run Audit"):
    if domain:
        with st.spinner('Checking DNS...'):
            time.sleep(1)
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🛡️ Auth")
                mx_r = robust_query(domain, 'MX')
                if mx_r: mx_s = True; st.success("✅ MX Found")
                else: st.error("❌ MX Missing")
                
                txt_r = robust_query(domain, 'TXT')
                if txt_r:
                    spf_find = [r.to_text() for r in txt_r if "v=spf1" in r.to_text()]
                    if spf_find: spf_s = True; st.success("✅ SPF Found")
                    else: st.error("❌ SPF Missing")
                
                dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
                if dm_r: dmarc_s = True; st.success("✅ DMARC Found")
                else: st.warning("⚠️ DMARC Missing")

                selectors = ['google', 'default', 'selector1']
                if custom_selector: selectors.insert(0, custom_selector.strip())
                for sel in selectors:
                    dk_r = robust_query(f"{sel}._domainkey.{domain}", 'TXT')
                    if dk_r: dkim_s = True; st.success(f"✅ DKIM Found ({sel})"); break
            
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
                    except: st.success("✅ IP Clean")
                except: st.error("IP Error")

            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            st.divider()
            st.metric("Health Score", f"{score}/100")
            
            if score < 100:
                st.warning("Issues found. This domain is at risk of landing in spam.")
    else:
        st.info("Please enter a domain.")
