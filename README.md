🎓 AI Studybot

AI Studybot is an educational AI assistant designed to help students understand academic concepts through structured explanations, step-by-step guidance, and conversational learning.

The project provides a FastAPI backend that connects a large language model with persistent chat memory using MongoDB, enabling interactive tutoring experiences.

✨ Features

* 📚 AI tutor for academic topics
* 🧠 Conversation memory stored in MongoDB
* ⚡ FastAPI backend with REST endpoints
* 🌐 Deployed on Render
* 🔐 Environment-based configuration (.env)
* 🧩 Structured markdown responses (tables, math, steps)
* 🔄 Chat history retrieval per user

---

## 🏗️ Tech Stack

* **Backend:** FastAPI
* **LLM:** Groq (via LangChain)
* **Database:** MongoDB Atlas
* **Deployment:** Render
* **Validation:** Pydantic
* **Environment Management:** python-dotenv

---

## 📂 Project Structure

```
AI_Studybot/
│── main.py / app.py
│── .env
│── requirements.txt
│── .gitignore
│── README.md
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/Likith-HR/AI_Studybot.git
cd AI_Studybot
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file:

```
Groq_api_key=YOUR_GROQ_API_KEY
Mongo_url=YOUR_MONGODB_CONNECTION_STRING
```

---

## ▶️ Run locally

```bash
uvicorn app:app --reload
```

Open:

```
http://127.0.0.1:8000/docs
```

---

## 🧠 API Usage

### POST `/chat`

Request:

```json
{
  "user_id": "user123",
  "question": "Explain Newton’s laws"
}
```

Response:

```json
{
  "response": "AI generated explanation..."
}
```

---

## 💡 How It Works

1. User sends a question
2. Previous messages are retrieved from MongoDB
3. LangChain builds prompt with history
4. Groq model generates structured answer
5. Both user and assistant messages are stored

---

## 🔒 Security Notes

* `.env` is ignored via `.gitignore`
* Database credentials are not committed
* CORS enabled for frontend integration

---



⭐ Acknowledgment

Built as a learning project exploring AI tutoring systems, conversational memory, and modern API deployment.
