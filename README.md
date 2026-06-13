# Svelte RAG Chatbot

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and Docker Compose
- [Groq API key](https://console.groq.com)
- [Google OAuth credentials](https://console.cloud.google.com)

## Google OAuth Setup

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create a new project
3. Go to **APIs & Services** → **OAuth consent screen** → External → Create
4. Go to **APIs & Services** → **Credentials** → **+ Create Credentials** → **OAuth 2.0 Client ID**
5. Application type: **Web application**
6. Authorized JavaScript origins: `http://localhost:3000`
7. Authorized redirect URIs: `http://localhost:3000/api/auth/callback/google`
8. Copy the Client ID and Client Secret

## Setup

1. Clone the repository and enter the directory:
```bash
git clone <repo-url>
cd svelte-rag
```

2. Create your `.env` file:
```env
DATABASE_URL=postgresql://svelte:svelte@db:5432/svelte-rag
GROQ_API_KEY=your_groq_api_key
BETTER_AUTH_SECRET=your_random_string_min_32_chars
BETTER_AUTH_URL=http://localhost:3000
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

> Generate a secure secret with: `openssl rand -base64 32`

3. Start the app:
```bash
docker compose up
```

4. Open [http://localhost:3000](http://localhost:3000)

> First run takes a few minutes — Ollama needs to pull the embedding model.