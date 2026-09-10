# ✈️ Aria — AI Travel Agent

An AI-powered travel agent chat application built with **Node.js/Express** backend and a modern **HTML/CSS/JS** frontend, powered by **IBM watsonx AI**.

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
npm install
```

### 2. Configure credentials
Copy the example env file and fill in your IBM credentials:
```bash
copy .env.example .env
```

Edit `.env`:
```
WATSONX_API_KEY=your_actual_ibm_api_key
WATSONX_PROJECT_ID=your_actual_project_id
WATSONX_URL=https://us-south.ml.cloud.ibm.com/ml/v1/text/chat?version=2023-05-29
IAM_TOKEN_URL=https://iam.cloud.ibm.com/identity/token
PORT=3000
```

### 3. Run the server
```bash
npm start
```
Open your browser at **http://localhost:3000**

For development with auto-reload:
```bash
npm run dev
```

---

## 📁 Project Structure

```
travel-agent/
├── server.js          # Express backend + watsonx proxy
├── package.json
├── .env.example       # Environment variable template
├── public/
│   └── index.html     # Chat UI frontend (self-contained)
└── README.md
```

---

## 🔑 Getting IBM watsonx Credentials

1. Go to [IBM Cloud](https://cloud.ibm.com)
2. Create or open a **watsonx.ai** project
3. Generate an **API key** under Manage → Access → API Keys
4. Copy your **Project ID** from the project settings

---

## 🏗️ Architecture

```
Browser (public/index.html)
        │  POST /api/chat  { messages: [...] }
        ▼
Express Server (server.js)
        │  Fetches IBM IAM token (cached)
        │  POST https://us-south.ml.cloud.ibm.com/ml/v1/text/chat
        ▼
IBM watsonx AI (meta-llama/llama-3-3-70b-instruct)
```

- The backend acts as a secure proxy — your API key never reaches the browser
- IAM tokens are cached for ~55 minutes and refreshed automatically
- Full conversation history is sent with each request for context

---

## 🤖 Features

- 💬 Streaming-style chat UI with typing indicator
- 🗺️ Quick-start destination chips
- 📝 Markdown rendering (headers, lists, bold, code blocks)
- 🔐 Secure API key proxying via backend
- 📱 Responsive design (mobile-friendly)
- ⚡ Auto-growing textarea input
- 🟢 Live health check / configuration status
