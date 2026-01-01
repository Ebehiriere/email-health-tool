import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test | Email Solution Pro", page_icon="✉️")

# 2. Premium White-Label CSS (Locked Sidebar & Logo)
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* --- LOCK SIDEBAR & REMOVE TOGGLE --- */
[data-testid="collapsedControl"] {
    display: none !important;
}

/* Ensure sidebar stays open */
section[data-testid="stSidebar"] {
    min-width: 250px !important;
}

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
}

.main-title {
    font-size: 42px !important;
    font-weight: 800 !important;
    letter-spacing: -1.5px !important;
    color: #0f172a !important;
    line-height: 1.1 !important;
    margin-bottom: 0px !important;
}

.sub-title {
    font-size: 20px !important;
    font-weight: 400 !important;
    color: #64748b !important;
    margin-top: -5px !important;
    margin-bottom: 15px !important;
}

.stButton>button {
    width: 100%; border-radius: 8px; height: 3.5em; 
    background-color: #1e293b; color: white; font-weight: bold;
    font-size: 18px; border: none; transition: 0.3s;
}
.stButton>button:hover {
    background-color: #000000;
    transform: translateY(-2px);
}
</style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# 3. SIDEBAR: Logo & Navigation
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.title("Email Solution Pro")
    
    st.markdown("---")
    st.markdown("### 🛠️ More Free Tools")
    st.markdown("🏠 **[Email Health Audit](/)** (Current)")
    st.markdown("🔍 [Blacklist Monitor](https://emailsolutionpro.com/tools/blacklist)")
    st.markdown("📜 [SPF Record Generator](https://emailsolutionpro.com/tools/spf)")
    st.markdown("🔐 [DMARC Lookup Tool](https://emailsolutionpro.com/tools/dmarc)")
    st.markdown("🖼️ [Bimi Record Checker](https://emailsolutionpro.com/tools/bimi)")
    
    st.divider()
    
    st.markdown("### 🚀 Expert Help")
    st.markdown("💼 [Managed Deliverability](https://emailsolutionpro.com/services)")
    st.markdown("📅 [Inbox Strategy Call](https://emailsolutionpro.com/book)")
    
    st.divider()
    st.info("System Status: Online")

# 4. Main Interface
st.markdown('<p class="main-title">Free Email Spam Test</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Instant Email Health & Reputation Analysis</p>', unsafe_allow_html=True)
st.divider()

domain = st.text_input("Enter your domain", value="", placeholder="example.com")

with st.expander("⚙️ Advanced: Manual DKIM Selector"):
    custom_selector = st.text_input("Custom DKIM Selector (Optional)", placeholder="google")

# DNS Setup
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
resolver.timeout = 5

def robust_query(query_domain, record_type):
    try:
        return resolver.resolve(query_domain, record_type)
    except:
        return None

# 5. Audit Logic
if st.button("🚀 Run Free Deliverability Audit"):
    if domain:
        with st.spinner('🛠️ Analyzing Authentication & Reputation...'):
            time.sleep(1.2)
            spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
            active_selector = "None"
            
            c1, c2 = st.columns(2)
            with c1:
                st.subheader("🛡️ Authentication")
                mx_r = robust_query(domain, 'MX')
                if mx_r: mx_s = True; st.success("✅ MX Found")
                else: st.error("❌ MX Record Missing")
                
                txt_r = robust_query(domain, 'TXT')
                if txt_r:
                    spf_find = [r.to_text() for r in txt_r if "v=spf1" in r.to_text()]
                    if spf_find: spf_s = True; st.success("✅ SPF Found")
                    else: st.error("❌ SPF Record Missing")
                else:
                    st.error("❌ TXT Records Missing")
                
                dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
                if dm_r: dmarc_s = True; st.success("✅ DMARC Found")
                else: st.warning("⚠️ DMARC Not Found")

                selectors = ['google', 'default', 'k1', 'smtp', 'selector1']
                if custom_selector: selectors.insert(0, custom_selector.strip())
                for sel in selectors:
                    dk_r = robust_query(f"{sel}._domainkey.{domain}", 'TXT')
                    if dk_r:
                        dkim_s = True; st.success(f"✅ DKIM Found ({sel})")
                        active_selector = sel; break
                if not dkim_s: st.info("ℹ️ DKIM: Selector not found")

            with c2:
                st.subheader("🚩 Reputation")
                try:
                    ip_display = socket.gethostbyname(domain)
                    st.info(f"Domain IP: {ip_display}")
                    rev = ".".join(reversed(ip_display.split(".")))
                    try:
                        resolver.resolve(f"{rev}.zen.spamhaus.org", 'A')
                        st.error("⚠️ ALERT: IP Blacklisted!")
                        black_s = False
                    except: st.success("✅ IP is Clean (Spamhaus)")
                except: st.error("Could not resolve IP address.")

            st.divider()
            score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
            s_color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
            st.subheader(f"📊 Your Health Score: {score}/100")
            if score >= 80: st.balloons()

            # --- COLORFUL HTML REPORT ---
            report_template = """
            <html><body style="font-family: sans-serif; padding: 20px;">
                <div style="max-width: 600px; margin: auto; border-radius: 10px; border: 1px solid #ddd; padding: 30px; border-top: 10px solid {color};">
                    <h2 style="color: #0f172a;">Audit Report: {dom}</h2>
                    <div style="background: {color}; color: white; padding: 15px; text-align: center; font-size: 24px; font-weight: bold; margin: 20px 0;">Score: {scr}/100</div>
                    <p>MX: {mx} | SPF: {spf} | DMARC: {dm}</p>
                    <p>DKIM: {dk} | Reputation: {rep}</p>
                </div>
            </body></html>
            """
            report_html = report_template.format(
                color=s_color, dom=domain, scr=score, 
                mx='PASS' if mx_s else 'FAIL', spf='PASS' if spf_s else 'FAIL',
                dm='PASS' if dmarc_s else 'FAIL', dk='PASS' if dkim_s else 'FAIL',
                rep='CLEAN' if black_s else 'BLACKLISTED'
            )
            
            st.download_button(label="📥 Download Colorful Audit Report", data=report_html, file_name=f"Audit_{domain}.html", mime="text/html")

            st.markdown("---")
            if score < 100:
                st.warning("🚨 Issues detected! Your emails might be landing in spam folders.")
                st.link_button("👉 Fix My Deliverability Now", "https://emailsolutionpro.com/contact")
            else:
                st.success("Great job! Your domain is healthy.")
                st.link_button("👉 Contact Email Solution Pro", "https://emailsolutionpro.com/contact")
    else:
        st.info("Please enter a domain name to begin.")
