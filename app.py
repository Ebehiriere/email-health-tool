import streamlit as st
import dns.resolver
import socket
import time

# 1. Page Configuration
st.set_page_config(page_title="Free Email Spam Test & Deliverability Checker | Email Solution Pro", page_icon="✉️")

# 2. Premium White-Label CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}

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
                padding-bottom: 5px !important;
            }

            .sub-title {
                font-size: 20px !important;
                font-weight: 400 !important;
                color: #64748b !important;
                letter-spacing: -0.5px !important;
                margin-top: -5px !important;
                margin-bottom: 15px !important;
            }

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

# 3. Sidebar
with st.sidebar:
    try:
        st.image("logo.png", use_container_width=True)
    except:
        st.subheader("Email Solution Pro")
    
    st.markdown("### 🛠️ More Tools")
    st.markdown("- [Blacklist Monitor](https
