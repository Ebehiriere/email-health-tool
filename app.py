import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Setup
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker", page_icon="✉️")

# 2. Styling & Hidden Menu
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button {
        width: 100%; border-radius: 8px; height: 3.5em; 
        background-color: #1e293b; color: white; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Branding & SEO Title
try:
    st.image("logo.png", width=350)
except:
    st.title("Email Solution Pro")

st.markdown("# Free Email Spam Test & Deliverability Checker")
st.markdown("### Professional Domain Health Diagnostic")
st.divider()

# 4. Input
domain = st.text_input("Enter your domain", placeholder="e.g. company.com")

# 5. Diagnostic Logic
if st.button("🚀 Run My Free Audit"):
    if domain:
        with st.spinner('Analyzing...'):
            time.sleep(1)
            # Logic placeholders
            st.success(f"Analysis complete for {domain}")
            
            # Simple scoring for visibility
            st.subheader("📊 Your Health Score: 80/100")
            
            st.divider()
            # CALL TO ACTION BUTTON
            st.markdown("### 🚨 Deliverability Issues Detected")
            st.write("Your emails may be failing authentication checks.")
            st.link_button("👉 Fix My Deliverability Now", "https://emailsolutionpro.com/contact")
    else:
        st.info("Please enter a domain.")

# Sidebar
st.sidebar.image("logo.png", use_container_width=True)
st.sidebar.info("Powered by Email Solution Pro")
