

# 📘 AI Study Buddy – Exam Planner

AI Study Buddy is a **Streamlit-based AI web application** that helps students prepare for exams by generating **personalized study plans** using **Generative AI (Gemini via LangChain)**.
It also includes **PDF download, reminders, voice assistant, progress tracking, and calendar-ready schedules**.

---

## 🚀 Features

* 🎯 **Personalized Study Plan**

  * Based on subject, exam date, weak topics, and daily study hours

* 📄 **Download Study Plan as PDF**

  * Offline access to generated plans

* 🔔 **Daily Study Reminders**

  * Save reminder time locally

* 🎙️ **Voice Assistant**

  * Reads the study plan aloud (Text-to-Speech)

* 📊 **Progress Tracking**

  * Track completed, skipped, or ongoing study sessions

* 📆 **Calendar-Ready Schedule**

  * Copy plan directly to Google Calendar or other planners

---

## 🛠️ Technologies Used

* **Python**
* **Streamlit** – Web interface
* **LangChain** – LLM orchestration
* **Google Gemini API** – AI model
* **FPDF** – PDF generation
* **pyttsx3** – Text-to-Speech
* **JSON** – Local data storage

---

## 📂 Project Structure

```
AI-STUDY-BUDDY/
│
├── app.py
├── reminders.json
├── progress.json
├── requirements.txt
├── .env
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/ai-study-buddy.git
cd ai-study-buddy
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Setup Environment Variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open browser at:

```
http://localhost:8501
```

---

## 📊 Data Storage

* **reminders.json**
  Stores daily reminder time and message

* **progress.json**
  Stores day-wise study progress and hours studied

> Note: JSON is used instead of a database to keep the project lightweight and suitable for academic use.

---

## 🎤 Viva Explanation (Short)

> “AI Study Buddy is an AI-powered web application that uses LangChain and Gemini to generate personalized exam study plans. It supports PDF downloads, voice assistance, reminders, progress tracking, and calendar integration using Streamlit.”

---

## 🔮 Future Enhancements

* User login system
* Email / notification reminders
* PDF timetable templates
* Progress charts and analytics
* Mobile app version

---

## 👨‍🎓 Project Details

* **Student Name:** Ritik
* **Project Type:** AI / Generative AI Mini Project
* **Use Case:** Exam preparation and time management

---

## 📜 License

This project is created for **educational purposes**.


