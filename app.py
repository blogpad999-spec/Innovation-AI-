import streamlit as st
from google import genai
import os

# =====================================================================
# 1. CONFIGURATION & PAGE SETUP
# =====================================================================
st.set_page_config(
    page_title="Innovation AI - Code-Free App Generator",
    page_icon="🚀",
    layout="centered"
)

st.markdown("""
    <style>
    .main-title {
        font-size: 2.5rem;
        color: #1E3A8A;
        text-align: center;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #4B5563;
        text-align: center;
        margin-bottom: 30px;
    }
    .stButton>button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        padding: 10px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================================================
# 2. API INITIALIZATION (New google-genai SDK format)
# =====================================================================
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")

# Initialize the new Google GenAI Client
if GEMINI_API_KEY != "YOUR_GEMINI_API_KEY_HERE" and GEMINI_API_KEY.strip():
    client = genai.Client(api_key=GEMINI_API_KEY)
else:
    client = None

# =====================================================================
# 3. APPLICATION UI
# =====================================================================
st.markdown("<div class='main-title'>🚀 Innovation AI</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Turn your app ideas into fully working Web & Mobile applications instantly—No Code Needed!</div>", unsafe_allow_html=True)

st.divider()

with st.form(key="app_generator_form"):
    app_idea = st.text_area(
        "Describe your app idea in detail:",
        placeholder="e.g., A fitness tracking app where users can log daily water intake, set step goals, and see a visual progress chart.",
        height=150
    )
    
    platform_type = st.selectbox(
        "Target Platform:",
        ["Responsive Web Application", "Mobile App UI/UX Layout", "Full-Stack Single Page App"]
    )
    
    design_style = st.selectbox(
        "Design Theme & Style:",
        ["Modern Minimalist", "Dark Mode Tech", "Vibrant & Playful", "Professional Corporate"]
    )
    
    submit_button = st.form_submit_button(label="Generate Complete Application")

# =====================================================================
# 4. AI GENERATION & PROCESSING
# =====================================================================
if submit_button:
    if not app_idea.strip():
        st.error("❌ Please provide an app idea before clicking generate.")
    elif client is None:
        st.warning("⚠️ Please insert your valid Gemini API Key in the source code first.")
    else:
        with st.spinner("✨ Innovation AI is architecture-planning and coding your application..."):
            try:
                prompt = f"""
                You are Innovation AI, an expert autonomous software engineer. 
                The user wants to generate a complete application from this idea: "{app_idea}"
                Target Platform: {platform_type}
                Design Style: {design_style}

                Please provide a comprehensive response with the following sections:
                1. ## Application Architecture & Features Checklist
                2. ## Complete Production-Ready Source Code (Provide fully working, beautiful Single-Page HTML with embedded CSS and JavaScript inside a clear markdown code block so the user can copy/paste it). Make sure it matches the requested style: {design_style}.
                3. ## Deployment & Next Steps (How to host it instantly without coding).
                """
                
                # Using the latest and supported model: gemini-2.5-flash
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                st.success("🎉 Your application files have been successfully generated!")
                st.markdown("---")
                st.markdown(response.text)
                
                st.download_button(
                    label="📥 Download Blueprint & Documentation",
                    data=response.text,
                    file_name="innovation_ai_output.md",
                    mime="text/markdown"
                )
                
            except Exception as e:
                st.error(f"An error occurred during generation: {str(e)}")

st.markdown("---")
st.caption("Powered by Innovation AI • Built for seamless creation on Web & Mobile.")
              
