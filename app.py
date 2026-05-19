import streamlit as st
from supabase import create_client, Client
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

st.set_page_config(page_title="AI Copywriter SaaS", page_icon="✍️")

# 1. Initialize API Keys and Clients securely
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
except KeyError:
    st.error("Missing API keys in Streamlit secrets.")
    st.stop()

# Initialize Supabase client
@st.cache_resource
def init_supabase() -> Client:
    return create_client(supabase_url, supabase_key)

supabase = init_supabase()

# Initialize LLM
llm = ChatGroq(api_key=groq_api_key, model_name="llama-3.1-8b-instant")

# 2. Session State Management
if "user" not in st.session_state:
    st.session_state.user = None
if "credits" not in st.session_state:
    st.session_state.credits = 3  # Freemium limit

# 3. Authentication Functions
def sign_up(email, password):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        if response.user:
            st.success("Account created! Please sign in.")
    except Exception as e:
        st.error(f"Sign up failed: {e}")

def sign_in(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if response.user:
            st.session_state.user = response.user
            st.rerun()
    except Exception as e:
        st.error(f"Sign in failed: {e}")

def sign_out():
    supabase.auth.sign_out()
    st.session_state.user = None
    st.rerun()

# 4. User Interface: Logged Out (Auth Screen)
if st.session_state.user is None:
    st.title("🔒 Welcome to AI Copywriter Pro")
    st.write("Generate high-converting marketing copy in seconds. Sign in to access your dashboard.")
    
    tab1, tab2 = st.tabs(["Sign In", "Create Account"])
    
    with tab1:
        st.subheader("Sign In")
        email_in = st.text_input("Email", key="in_email")
        pass_in = st.text_input("Password", type="password", key="in_pass")
        if st.button("Login"):
            sign_in(email_in, pass_in)
            
    with tab2:
        st.subheader("Create Account")
        email_up = st.text_input("Email", key="up_email")
        pass_up = st.text_input("Password", type="password", key="up_pass")
        if st.button("Sign Up"):
            sign_up(email_up, pass_up)

# 5. User Interface: Logged In (SaaS Dashboard)
else:
    # Header with User Info and Logout
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("✍️ AI Copywriter Pro")
        st.write(f"Welcome back, **{st.session_state.user.email}**")
    with col2:
        st.metric(label="Credits Remaining", value=st.session_state.credits)
        if st.button("Sign Out"):
            sign_out()
            
    st.divider()
    
    # Core SaaS Feature
    st.subheader("Generate Marketing Copy")
    product_name = st.text_input("Product Name:")
    target_audience = st.text_input("Target Audience:")
    tone = st.selectbox("Tone:", ["Professional", "Witty", "Urgent", "Casual"])
    
    if st.button("Generate Copy 🚀"):
        if st.session_state.credits > 0:
            if product_name and target_audience:
                with st.spinner("Writing your copy..."):
                    prompt = ChatPromptTemplate.from_messages([
                        ("system", "You are an expert marketing copywriter. Write a short, highly engaging promotional paragraph based on the user's inputs. Do not include hashtags."),
                        ("human", f"Product: {product_name}\nAudience: {target_audience}\nTone: {tone}")
                    ])
                    
                    chain = prompt | llm
                    response = chain.invoke({})
                    
                    st.success("Generation Complete!")
                    st.write(response.content)
                    
                    # Deduct a credit
                    st.session_state.credits -= 1
                    st.rerun() # Refresh UI to update credit counter
            else:
                st.warning("Please fill out all fields.")
        else:
            st.error("⚠️ You have run out of free credits!")
            st.info("In a real SaaS, this is where you would place a Stripe Checkout button to upgrade to a Pro plan.")