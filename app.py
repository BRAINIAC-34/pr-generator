import streamlit as st
import google.generativeai as genai
import time

# --- CONFIGURATION & SECRETS ---
# You need to set these in Streamlit Cloud > Advanced Settings > Secrets
# If running locally, create a .streamlit/secrets.toml file
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    ACCESS_CODE = st.secrets["ACCESS_CODE"]
    WHOP_URL = st.secrets["WHOP_URL"] # Your Whop Checkout Link
except:
    st.error("Secrets not found! Please set GOOGLE_API_KEY, ACCESS_CODE, and WHOP_URL in Streamlit secrets.")
    st.stop()

genai.configure(api_key=GOOGLE_API_KEY)

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="PR Pitch Deck | Get Press Ready", 
    page_icon="🚀",
    layout="centered"
)

# --- SESSION STATE MANAGEMENT ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "landing" # Options: landing, login, tool

# --- NAVIGATION FUNCTIONS ---
def go_to_login():
    st.session_state.page = "login"

def go_to_landing():
    st.session_state.page = "landing"

def verify_code():
    if st.session_state.user_code == ACCESS_CODE:
        st.session_state.authenticated = True
        st.session_state.page = "tool"
        st.success("Access Granted! Redirecting...")
        time.sleep(1)
        st.rerun()
    else:
        st.error("❌ Invalid Code. Please check your Whop receipt.")

def logout():
    st.session_state.authenticated = False
    st.session_state.page = "landing"
    st.rerun()

# --- VIEW 1: LANDING PAGE ---
if st.session_state.page == "landing":
    st.title("🚀 Get Press Coverage. Zero Effort.")
    st.markdown("### Generate journalist-ready Press Releases & Cold Pitches in 30 seconds.")
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **❌ The Old Way:**
        *   Hire a PR agency ($2,000+)
        *   Struggle to write a press release
        *   Get ignored by journalists
        """)
        
    with col2:
        st.markdown("""
        **✅ The PR Pitch Deck Way:**
        *   Enter your product details
        *   **AI generates the perfect angle**
        *   Get a Press Release + Cold Email instantly
        """)
        
    st.divider()
    
    st.markdown("#### 💡 Stop launching in silence. Get the attention you deserve.")
    
    # CTA SECTION
    st.info("🔥 **Launch Special:** Lifetime Access for just **$9**")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        # This link button goes straight to payment
        st.link_button("👉 Get Instant Access ($5)", WHOP_URL, type="primary", use_container_width=True)
    with c2:
        # This button goes to login view
        st.button("🔑 Already have a code? Login", on_click=go_to_login, use_container_width=True)

    st.markdown("---")
    st.caption("Trusted by Indie Hackers & Solopreneurs. Powered by Gemini AI.")

# --- VIEW 2: LOGIN PAGE ---
elif st.session_state.page == "login":
    st.title("🔐 Member Login")
    st.markdown("Enter the Access Code sent to your email after purchase.")
    
    st.text_input("Enter Access Code", key="user_code", type="password")
    
    c1, c2 = st.columns(2)
    with c1:
        st.button("Login", on_click=verify_code, type="primary", use_container_width=True)
    with c2:
        st.button("← Back to Home", on_click=go_to_landing, use_container_width=True)

# --- VIEW 3: THE TOOL (Protected) ---
elif st.session_state.page == "tool":
    if not st.session_state.authenticated:
        st.session_state.page = "landing"
        st.rerun()

    # Sidebar for logout
    with st.sidebar:
        st.write("Logged in.")
        st.button("Log out", on_click=logout)

    st.title("⚡ PR Pitch Generator")
    st.markdown("Fill in the details below to generate your Media Kit.")

    with st.form("pr_form"):
        product_name = st.text_input("Product Name", placeholder="e.g. SupaTask")
        target_audience = st.text_input("Target Audience", placeholder="e.g. Remote Project Managers")
        key_features = st.text_area("Key Features (Bullet points)", placeholder="- AI auto-scheduling\n- Slack integration\n- Dark mode")
        tone = st.selectbox("Tone", ["Professional & Corporate", "Exciting & Startup-y", "Controversial & Bold"])
        
        submitted = st.form_submit_button("Generate PR Kit 🚀")

    if submitted and product_name and key_features:
        with st.spinner("Consulting the PR Gods..."):
            try:
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                prompt = f"""
                Act as a world-class PR Specialist. 
                I need two things for a product launch.
                
                Product Name: {product_name}
                Target Audience: {target_audience}
                Key Features: {key_features}
                Tone: {tone}
                
                OUTPUT 1: A formal, formatted PRESS RELEASE. Include a catchy headline, dateline, body, and 'About' section.
                OUTPUT 2: A short, punchy COLD EMAIL to a journalist. Subject line should be clickbait (in a good way). Body under 150 words.
                """
                
                response = model.generate_content(prompt)
                
                st.success("Boom! Here is your kit.")
                st.divider()
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
