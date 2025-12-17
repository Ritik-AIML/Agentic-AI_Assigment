import streamlit as st
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from fpdf import FPDF
import pyttsx3

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage

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

# ------------------ UTIL FUNCTIONS ------------------
def clean_text(text):
    replacements = {
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "•": "-",
        "→": "->"
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text


def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    cleaned = clean_text(content)
    for line in cleaned.split("\n"):
        pdf.multi_cell(0, 8, line)

    file_path = "AI_Study_Plan.pdf"
    pdf.output(file_path)
    return file_path


def speak_text(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def save_reminder(time):
    data = {
        "reminder_time": time,
        "message": "Time to start your study session",
        "created_at": str(datetime.now())
    }
    with open("reminders.json", "w") as f:
        json.dump(data, f, indent=4)


def save_progress(day, topic, status, hours):
    data = {}
    if os.path.exists("progress.json"):
        with open("progress.json") as f:
            data = json.load(f)

    data[day] = {
        "topic": topic,
        "status": status,
        "hours_studied": hours
    }

    with open("progress.json", "w") as f:
        json.dump(data, f, indent=4)


# ------------------ SIDEBAR INPUT ------------------
st.sidebar.header("📌 Exam Details")

subject = st.sidebar.text_input("Subject")
exam_date = st.sidebar.text_input("Exam Date")
weak_topics = st.sidebar.text_area("Weak Topics (comma separated)")
study_hours = st.sidebar.slider("Daily Study Hours", 1, 12, 4)

generate_btn = st.sidebar.button("🚀 Generate Study Plan")

# ------------------ MODEL ------------------
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

system_prompt = SystemMessage(content="""
You are an AI Study Buddy.
Create realistic, stress-free exam study plans.
Focus more on weak topics.
Include breaks, revision, and exam-day tips.
Use simple language.
""")

# ------------------ MAIN LOGIC ------------------
response = None

if generate_btn:
    if not subject or not exam_date or not weak_topics:
        st.warning("⚠️ Please fill all fields")
    else:
        with st.spinner("Generating your study plan..."):
            user_prompt = HumanMessage(content=f"""
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
""")

            response = model.invoke([system_prompt, user_prompt])

        st.success("✅ Study Plan Generated")
        st.subheader("📅 Your AI Study Plan")
        st.write(response.content)

        # ------------------ PDF DOWNLOAD ------------------
        pdf_path = generate_pdf(response.content)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "📄 Download as PDF",
                f,
                file_name="AI_Study_Plan.pdf",
                mime="application/pdf"
            )

        # ------------------ VOICE ASSISTANT ------------------
        if st.button("🎙️ Read Study Plan Aloud"):
            speak_text(response.content)

        # ------------------ CALENDAR VIEW ------------------
        st.subheader("📆 Calendar Ready Schedule")
        st.text_area(
            "Copy & paste this into Google Calendar",
            response.content,
            height=200
        )

# ------------------ REMINDERS ------------------
st.markdown("---")
st.subheader("🔔 Daily Study Reminder")

reminder_time = st.time_input("Set reminder time")

if st.button("Save Reminder"):
    save_reminder(str(reminder_time))
    st.success("Reminder saved locally")

# ------------------ PROGRESS TRACKING ------------------
st.markdown("---")
st.subheader("📊 Progress Tracking")

day = st.text_input("Study Day (e.g., Day 1)")
topic = st.text_input("Topic Studied")
status = st.selectbox("Status", ["Completed", "In Progress", "Skipped"])
hours = st.number_input("Hours Studied", 0.0, 12.0, 1.0)

if st.button("Save Progress"):
    save_progress(day, topic, status, hours)
    st.success("Progress saved")

if os.path.exists("progress.json"):
    st.subheader("📈 Your Progress")
    with open("progress.json") as f:
        st.json(json.load(f))

# ------------------ FOOTER ------------------
st.markdown("---")
st.caption("Built using Streamlit, LangChain & Gemini ❤️")
