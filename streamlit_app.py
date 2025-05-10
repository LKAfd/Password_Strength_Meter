import streamlit as st
from src.password_strength import PasswordValidator
from src.password_utils import PasswordGenerator

# Initialize components
validator = PasswordValidator()
generator = PasswordGenerator()

# App configuration
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔐",
    layout="centered"
)

# Custom CSS
st.markdown("""
<style>
    .weak { color: #ff4b4b !important; font-weight: bold; }
    .moderate { color: #f4b400 !important; font-weight: bold; }
    .strong { color: #0f9d58 !important; font-weight: bold; }
    .recommendation { background-color: #f0f2f6; padding: 1em; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

def display_strength(result):
    strength_class = result['strength'].lower()
    st.markdown(f"<h2 class='{strength_class}'>Strength: {result['strength']} ({result['score']}/10)</h2>", 
                unsafe_allow_html=True)
    
    if result['suggestions']:
        with st.expander("🔍 Recommendations", expanded=True):
            for suggestion in result['suggestions']:
                st.markdown(f"• {suggestion}")
    else:
        st.success("✅ Excellent! This password meets all security requirements")

def generate_password_callback():
    generated_pwd = generator.generate_strong_password()
    st.session_state.generated_password = generated_pwd

# Main app layout
st.title("🔐 Password Strength Analyzer")
st.markdown("Check your password security and get improvement recommendations")

col1, col2 = st.columns([3, 1])
with col1:
    password = st.text_input(
        "Enter your password:", 
        type="password",
        placeholder="Type or paste password...",
        help="We don't store or transmit any passwords"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Generate Strong Password"):
        generate_password_callback()

# Show generated password
if 'generated_password' in st.session_state:
    st.code(f"Generated Password: {st.session_state.generated_password}")
    st.markdown(f"""
    <button onclick="navigator.clipboard.writeText('{st.session_state.generated_password}')" 
        class="btn btn-outline-secondary" style="padding: 0.25rem 0.5rem;">
        📋 Copy to Clipboard
    </button>
    """, unsafe_allow_html=True)

# Analysis section
if password:
    result = validator.evaluate_password(password)
    
    # Security warnings
    if "Very Weak" in result['strength']:
        st.error("🚨 This password is in common password databases!")
    
    if any("common patterns" in s for s in result['suggestions']):
        st.warning("⚠️ Warning: Password contains predictable patterns")
    
    # Display results
    display_strength(result)

    # Security meter
    st.progress(result['score'] / 10)