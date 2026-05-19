# ✍️ AI Copywriter Pro (SaaS Prototype)

A full-stack AI Software-as-a-Service (SaaS) application built with Python. This application features a secure user registration and authentication architecture, session state management, and a dynamic backend freemium credit-gating ecosystem.

## 🚀 Features
* **User Authentication:** Cloud-hosted User sign-up, sign-in, and secure session management powered by Supabase Auth.
* **Freemium Credit Paywall:** Simulates a live enterprise tiering system by allocating 3 free tokens per user and gating generation capabilities upon consumption.
* **Context-Driven Marketing Inference:** Connects to Groq cloud APIs to generate targeted, high-converting ad copy dynamically based on product specifications and audience tone parameters.

## 🛠️ Tech Stack
* **Frontend Architecture:** [Streamlit](https://streamlit.io/)
* **Database & Auth Security:** [Supabase](https://supabase.com/) (PostgreSQL backend infrastructure)
* **LLM Engine:** [Groq Cloud](https://groq.com/) (Model: `llama-3.1-8b-instant`)

## 💻 Local Setup
1. Clone the repository and navigate inside.
2. Setup a virtual environment: `python -m venv venv` and activate it.
3. Install dependencies using pinned versions to bypass Python 3.14 system incompatibilities:
   ```bash
   pip install streamlit langchain-groq supabase==2.25.0
