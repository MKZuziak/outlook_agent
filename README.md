# 📬 Outlook Agent

A simple agentic framework that reads emails from Outlook, drafts intelligent responses using a language model (LLM), and optionally sends them upon user confirmation. The agent can be extended with a local GUI or served as an API.

---

## 🚀 Features

- ✅ Automatically reads the most recent unread email from Outlook.
- 🧠 Uses an LLM (e.g., OpenAI GPT) to generate polite and relevant responses.
- 🔐 Awaits explicit user confirmation before sending replies.
- 🖥️ Optional Gradio GUI for a user-friendly interface.
- 🌐 Optional FastAPI server to expose the agent via HTTP.

---

## 🛠 Installation

### Prerequisites

- Python `>=3.13`
- [Poetry](https://python-poetry.org/) (for dependency and virtual environment management)

### 1. Install Dependencies

Create the virtual environment and install required packages:

```
poetry install
```

### 2. Install with Optional Features

#### WITH GUI
```
poetry install --with gui
```
#### WITH API (FastAPI + Uvicorn)
```
poetry install --with api
```

### 3. Envrionment Configuration
Create a .env file by copying the template:

```
cp .env.example .env
```

Edit .env and fill in your credentials:

```
OPENAI_API_KEY=your-openai-api-key
EMAIL_ADDRESS=your.email@example.com
EMAIL_PASSWORD=your-app-password
```

ℹ️ Use an App Password if two-factor authentication is enabled on your Outlook account.
🚫 Do not commit your .env file to version control. It is ignored via .gitignore.