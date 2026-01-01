import streamlit as st
import dns.resolver
import socket
import time

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro",
    page_icon="✉️",
    layout="centered"
)

# -------------------------------------------------
# Global Styling (Premium SaaS Feel)
# -------------------------------------------------
custom_css = """
<style>
#MainMenu, footer, header {visibility: hidden;}

:root {
    --primary: #0f172a;
    --secondary: #475569;
    --accent: #2563eb;
    --success: #16a34a;
    --warning: #f59e0b;
    --danger: #dc2626;
    --bg-card: #ffffff;
    --border-soft: #e5e7eb;
}

/* Font */
html, body, [class*="css"] {
    font-family: Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI',
                 Roboto, Helvetica, Arial, sans-serif;
}

/* Headings */
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: var(--primary);
    letter-spacing: -1.6px;
    margin-bottom: 6px;
}

.sub-title {
    font-size: 18px;
    color: var(--secondary);
    margin-bottom: 28px;
}

/* Input */
.stTextInput input {
    height: 3.2em;
    font-size: 16px;
}

/* Buttons */
.stButton>button {
    width: 100%;
    height: 3.4em;
    border-radius: 10px;
    font-size: 17px;
    font-weight: 600;
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
    color: white;
    border: none;
    transition: all 0.25s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.35);
}

/* Cards */
.card {
    background: var(--bg-card);
    border-radius: 14px;
    padding: 20px;
    border: 1px solid var(--border-soft);
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.04);
    margin-bottom: 18px;
}

/* Section headers */
.section-title {
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 12px;
}

/* Divider spacing */
hr {
    margin: 24px 0;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# -------------------------------------------------
# Header
# -------------------------------------------------
try:
    st.image("logo.png", width=320)
except:
    st.title("Email Solution Pro")

st.markdown('<div class="main-title">Free Email Spam Test & Deliverability Checker</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Instant email authentication & reputation analysis</div>', unsafe_allow_html=True)

domain = st.text_input(
    "Domain name",
    placeholder="example.com",
    label_visibility="collapsed"
)

# -------------------------------------------------
# DNS Resolver
# -------------------------------------------------
resolver = dns.resolver.Resolver()
resolver.nameservers = ['8.8.8.8', '8.8.4.4']
resolver.timeout = 5
resolver.lifetime = 5

def robust_query(q, t):
    for _ in range(3):
        try:
            return resolver.resolve(q, t)
        except:
            time.sleep(0.4)
    return None

# -------------------------------------------------
# Audit
# -------------------------------------------------
if st.button("🚀 Run Free Deliverability Audit"):
    if not domain:
        st.info("Please enter a domain to continue.")
    else:
        with st.spinner("Running deep deliverability checks…"):
            time.sleep(1)

            spf, dmarc, mx, dkim, clean = False, False, False, False, True

            c1, c2 = st.columns(2)

            with c1:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🛡️ Authentication</div>', unsafe_allow_html=True)

                if robust_query(domain, "MX"):
                    st.success("MX record found")
                    mx = True
                else:
                    st.error("MX record missing")

                txt = robust_query(domain, "TXT")
                if txt and any("v=spf1" in r.to_text() for r in txt):
                    st.success("SPF configured")
                    spf = True
                else:
                    st.error("SPF missing")

                if robust_query(f"_dmarc.{domain}", "TXT"):
                    st.success("DMARC configured")
                    dmarc = True
                else:
                    st.warning("DMARC not found")

                for sel in ["google", "default", "k1", "smtp"]:
                    if robust_query(f"{sel}._domainkey.{domain}", "TXT"):
                        st.success(f"DKIM found ({sel})")
                        dkim = True
                        break
                if not dkim:
                    st.info("DKIM not detected")

                st.markdown('</div>', unsafe_allow_html=True)

            with c2:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown('<div class="section-title">🚩 Reputation</div>', unsafe_allow_html=True)

                try:
                    ip = socket.gethostbyname(domain)
                    st.info(f"Sending IP: {ip}")
                    rev = ".".join(reversed(ip.split(".")))
                    try:
                        resolver.resolve(f"{rev}.zen.spamhaus.org", "A")
                        st.error("IP is blacklisted")
                        clean = False
                    except:
                        st.success("IP is clean (Spamhaus)")
                except:
                    st.error("Could not resolve IP")

                st.markdown('</div>', unsafe_allow_html=True)

            st.divider()

            score = sum([mx, spf, dmarc, dkim, clean]) * 20
            st.subheader(f"📊 Deliverability Score: {score}/100")

            if score >= 80:
                st.success("Excellent — your setup is solid.")
                st.balloons()
            else:
                st.warning("Issues detected — emails may land in spam.")

            st.link_button(
                "👉 Fix My Deliverability",
                "https://emailsolutionpro.com/contact"
            )

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.markdown("### About")
st.sidebar.info(
    "Email Solution Pro helps businesses fix email spam issues, "
    "configure SPF/DKIM/DMARC, and improve inbox placement."
)
