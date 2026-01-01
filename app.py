import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", page_icon="✉️")

# 2. Premium White-Label CSS (Locked Sidebar & ESP Brand Colors)
hide_st_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

[data-testid="collapsedControl"] { display: none !important; }

section[data-testid="stSidebar"] {
    min-width: 300px !important;
    max-width: 300px !important;
}

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap');
html, body, [class*="css"], .stMarkdown {
    font-family: 'Inter', sans-serif;
}

.main-title {
    font-size: 42px !important;
    font-weight: 800 !important;
    color: #0f172a !important;
    line-height: 1.1 !important;
}

.stButton>button {
    width: 100%; border-radius: 8px; height: 3.5em; 
    background-color: #1e293b; color: white; font-weight: bold;
    font-size: 18px; border: none; transition: 0.3s;
}
.stButton>button:hover { background-color: #000000; transform: translateY(-2px); }

/* Footer Styling */
.footer {
    position: fixed; left: 300px; bottom: 0; width: calc(100% - 300px);
    background-color: #0f172a; color: #ffffff; text-align: center;
    padding: 15px; font-size: 14px; z-index: 1000; border-top: 1px solid #1e293b;
}
.footer a { color: #38bdf8; text-decoration: none; font-weight: 600; margin: 0 10px; }

.main .block-container { padding-bottom: 120px !important; }
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
    
    st.divider()
    st.markdown("### 🚀 Expert Help")
    st.markdown("💼 [Managed Deliverability](https://emailsolutionpro.com/services)")
    st.markdown("📅 [Inbox Strategy Call](https://emailsolutionpro.com/book)")
    st.divider()
    st.info("System Status: Online")

# 4. Main Interface
st.markdown('<p class="main-title">Free Email Spam Test & Deliverability Checker</p>', unsafe_allow_html=True)
st.markdown('<p style="color: #64748b; font-size: 20px;">Instant Email Health & Reputation Analysis</p>', unsafe_allow_html=True)
st.divider()

domain = st.text_input("Enter your domain", value="", placeholder="example.com")

with st.expander("⚙️ Advanced: Manual DKIM Selector"):
    custom_selector = st.text_input("Custom DKIM Selector (Optional)", placeholder="google")

# DNS Setup
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
resolver.timeout = 5

def robust_query(query_domain, record_type):
    try: return resolver.resolve(query_domain, record_type)
    except: return None

# 5. Audit Logic
if st.button("🚀 Run Free Deliverability Audit"):
    if domain:
        # Step-by-Step Progress Simulation
        status_bar = st.progress(0)
        status_text = st.empty()
        
        stages = [
            (25, "🔍 Checking MX and SPF records..."),
            (50, "🛡️ Validating DMARC policy..."),
            (75, "🚩 Scanning Global Blacklists..."),
            (100, "📊 Finalizing your report...")
        ]
        
        for percent, msg in stages:
            status_text.text(msg)
            status_bar.progress(percent)
            time.sleep(0.6)
        
        status_text.empty()
        status_bar.empty()

        spf_s, dmarc_s, mx_s, dkim_s, black_s = False, False, False, False, True 
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🛡️ Authentication")
            # MX Check
            if robust_query(domain, 'MX'): mx_s = True; st.success("✅ MX Records Found")
            else: st.error("❌ MX Records Missing")
            
            # SPF Check
            txt_r = robust_query(domain, 'TXT')
            if txt_r and any("v=spf1" in r.to_text() for r in txt_r):
                spf_s = True; st.success("✅ SPF Record Found")
            else: st.error("❌ SPF Record Missing")
            
            # DMARC Interpreter
            dm_r = robust_query(f"_dmarc.{domain}", 'TXT')
            if dm_r:
                dmarc_s = True
                record = dm_r[0].to_text()
                if "p=reject" in record: st.success("✅ DMARC: Reject (Maximum Protection)")
                elif "p=quarantine" in record: st.warning("⚠️ DMARC: Quarantine (Partial Protection)")
                else: st.info("ℹ️ DMARC: Monitor Only (No Protection)")
            else: st.error("❌ DMARC Not Found")

            # DKIM Check
            selectors = ['google', 'default', 'k1', 'smtp', 'selector1']
            if custom_selector: selectors.insert(0, custom_selector.strip())
            for sel in selectors:
                if robust_query(f"{sel}._domainkey.{domain}", 'TXT'):
                    dkim_s = True; st.success(f"✅ DKIM Found ({sel})"); break
            if not dkim_s: st.info("ℹ️ DKIM: Common selectors not found")

        with c2:
            st.subheader("🚩 Reputation")
            try:
                ip = socket.gethostbyname(domain)
                rev = ".".join(reversed(ip.split(".")))
                # Multi-Blacklist logic
                blists = {"Spamhaus": "zen.spamhaus.org", "Barracuda": "b.barracudacentral.org"}
                for name, srv in blists.items():
                    try:
                        resolver.resolve(f"{rev}.{srv}", 'A')
                        st.error(f"⚠️ Listed on {name}!")
                        black_s = False
                    except: st.success(f"✅ Clean: {name}")
            except: st.error("Could not resolve domain IP.")

        st.divider()
        score = sum([mx_s, spf_s, dmarc_s, dkim_s, black_s]) * 20
        s_color = "#28a745" if score >= 80 else "#ffc107" if score >= 60 else "#dc3545"
        st.subheader(f"📊 Your Health Score: {score}/100")
        if score >= 80: st.balloons()

        # HTML Report logic
        report_template = """
        <html><body style="font-family: sans-serif; padding: 20px;">
            <div style="max-width: 600px; margin: auto; border: 1px solid #ddd; padding: 30px; border-top: 10px solid {color};">
                <h2>Deliverability Audit: {dom}</h2>
                <div style="background:{color}; color:white; padding:15px; text-align:center; font-size:24px;">Score: {scr}/100</div>
                <p>MX: {mx} | SPF: {spf} | DMARC: {dm} | DKIM: {dk} | Reputation: {rep}</p>
            </div>
        </body></html>
        """
        report_html = report_template.format(
            color=s_color, dom=domain, scr=score,
            mx='PASS' if mx_s else 'FAIL', spf='PASS' if spf_s else 'FAIL',
            dm='PASS' if dmarc_s else 'FAIL', dk='PASS' if dkim_s else 'FAIL',
            rep='CLEAN' if black_s else 'LISTED'
        )
        st.download_button(label="📥 Download Audit Report", data=report_html, file_name=f"Audit_{domain}.html", mime="text/html")
        st.link_button("👉 Fix My Deliverability Now", "https://emailsolutionpro.com/contact")
    else:
        st.info("Please enter a domain name to begin.")

# 6. Footer
st.markdown("""
    <div class="footer">
        <div>© 2026 <b>Email Solution Pro</b> | Precision Deliverability Engineering</div>
        <div style="margin-top: 5px;">
            <a href="https://emailsolutionpro.com">Website</a> | <a href="https://emailsolutionpro.com/privacy">Privacy</a> | <a href="https://emailsolutionpro.com/contact">Support</a>
        </div>
    </div>
""", unsafe_allow_html=True)
