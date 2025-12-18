import streamlit as st
import os
from dotenv import load_dotenv
from fpdf import FPDF
import pyttsx3
from google import genai
import threading

# ------------------ ENV SETUP ------------------
load_dotenv()

# ------------------ STREAMLIT CONFIG ------------------
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="📘",
    layout="centered"
)

st.title("📘 AI Study Buddy – Exam Planner")
st.write("An AI-powered exam preparation assistant")

# ------------------ SESSION STATE INITIALIZATION ------------------
if 'study_plan' not in st.session_state:
    st.session_state['study_plan'] = None
if 'tts_played' not in st.session_state:
    st.session_state['tts_played'] = False

# ------------------ UTIL FUNCTIONS ------------------
def clean_text(text):
    """Remove special characters for PDF compatibility"""
    replacements = {
        "–": "-",
        "—": "-",
        """: '"',
        """: '"',
        "'": "'",
        "'": "'",
        "•": "-",
        "→": "->",
        "★": "*",
        "✓": "v",
        "✗": "x"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    
    # Remove non-ASCII characters
    text = text.encode('ascii', 'ignore').decode('ascii')
    return text


def generate_pdf(content):
    """Generate PDF from text content"""
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        cleaned = clean_text(content)
        for line in cleaned.split("\n"):
            if line.strip():  # Skip empty lines
                pdf.multi_cell(0, 8, line)

        file_path = "AI_Study_Plan.pdf"
        pdf.output(file_path)
        return file_path
    except Exception as e:
        st.error(f"Error generating PDF: {str(e)}")
        return None


def speak_text_async(text):
    """Convert text to speech in a separate thread"""
    def _speak():
        engine = None
        try:
            engine = pyttsx3.init()
            # Clean text for better speech
            clean = clean_text(text)
            # Limit length for speech (first 500 chars)
            speech_text = clean[:500] + "..." if len(clean) > 500 else clean
            engine.say(speech_text)
            engine.runAndWait()
        except Exception as e:
            print(f"Error with text-to-speech: {str(e)}")
        finally:
            if engine:
                try:
                    engine.stop()
                except:
                    pass
    
    # Run TTS in a separate thread to avoid blocking
    thread = threading.Thread(target=_speak, daemon=True)
    thread.start()


# ------------------ SIDEBAR INPUT ------------------
st.sidebar.header("📌 Exam Details")

subject = st.sidebar.text_input("Subject")
exam_date = st.sidebar.text_input("Exam Date (e.g., 2024-12-25)")
weak_topics = st.sidebar.text_area("Weak Topics (comma separated)")
study_hours = st.sidebar.slider("Daily Study Hours", 1, 12, 4)

generate_btn = st.sidebar.button("🚀 Generate Study Plan")

# ------------------ MODEL INITIALIZATION ------------------
try:
    client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    MODEL_NAME = "gemini-2.5-flash"
    st.sidebar.success(f"✅ Using model: {MODEL_NAME}")
        
except Exception as e:
    st.error(f"Error initializing AI model: {str(e)}")
    st.info("Please check your GOOGLE_API_KEY in .env file")
    st.stop()

system_instruction = """
You are an AI Study Buddy.
Create realistic, stress-free exam study plans.
Focus more on weak topics.
Include breaks, revision, and exam-day tips.
Use simple language and clear formatting.
"""

# ------------------ MAIN LOGIC ------------------
if generate_btn:
    if not subject or not exam_date or not weak_topics:
        st.warning("⚠️ Please fill all fields")
    else:
        # Reset TTS flag when generating new plan
        st.session_state['tts_played'] = False
        
        with st.spinner("Generating your study plan..."):
            try:
                prompt = f"""
{system_instruction}

Create a personalized exam study plan.

Subject: {subject}
Exam Date: {exam_date}
Weak Topics: {weak_topics}
Daily Study Time: {study_hours} hours

Include:
1. Time-based schedule
2. Focus on weak topics
3. Breaks and revision
4. Exam-day tips
"""

                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=prompt
                )
                study_plan = response.text
                
                # Store in session state for persistence
                st.session_state['study_plan'] = study_plan
                
                st.success("✅ Study Plan Generated")
                
            except Exception as e:
                st.error(f"Error generating study plan: {str(e)}")
                st.info("Please check your internet connection and API key")

# ------------------ DISPLAY STUDY PLAN ------------------
if st.session_state['study_plan']:
    st.subheader("📅 Your AI Study Plan")
    st.write(st.session_state['study_plan'])
    
    # Auto-play TTS only once after generation
    if not st.session_state['tts_played']:
        with st.spinner("Reading study plan aloud..."):
            speak_text_async(st.session_state['study_plan'])
            st.session_state['tts_played'] = True
            st.info("🎙️ Study plan is being read aloud...")
    
    # ------------------ ACTION BUTTONS ------------------
    col1, col2 = st.columns(2)
    
    with col1:
        # PDF Download
        pdf_path = generate_pdf(st.session_state['study_plan'])
        if pdf_path and os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    "📄 Download as PDF",
                    f,
                    file_name="AI_Study_Plan.pdf",
                    mime="application/pdf",
                    key="pdf_download"
                )
    
    with col2:
        # Manual TTS button
        if st.button("🎙️ Read Aloud Again"):
            with st.spinner("Speaking..."):
                speak_text_async(st.session_state['study_plan'])
                st.info("🎙️ Reading study plan aloud...")
    
    # ------------------ CALENDAR VIEW ------------------
    st.subheader("📆 Calendar Ready Schedule")
    st.text_area(
        "Copy & paste this into Google Calendar",
        st.session_state['study_plan'],
        height=200,
        key="calendar_view"
    )

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built with Streamlit & Gemini ❤️")
st.caption("💡 Tip: Download your study plan as PDF and print it for offline reference!")
