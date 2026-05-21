# ⚖️ SuaraRakyat — Malaysian Rights Explainer

> **Snap a letter. Ask a law. Know your rights.**
>
> An AI-powered multilingual civic assistant that helps every Malaysian understand government documents and their legal rights — in BM, English, Mandarin, Tamil, and local dialects like Kelantan and Sarawak.

---

## 🏆 V HACK 2026 — Varsity Hackathon

| | |
|---|---|
| **Track** | Natural Language Processing (NLP) |
| **SDG** | SDG 10: Reduced Inequalities (Target 10.2) |
| **Team** | VHACK2026-LawChat |
| **University** | Universiti Sains Malaysia (USM) |
| **Deadline** | 19 March 2026 |

---

## 📱 Screenshots

<!-- Add your screenshots here after building -->
| Home Screen | Document Explainer | Law Chat |
|---|---|---|
| ![Home](assets/screenshots/home.png) | ![Explain](assets/screenshots/explain.png) | ![Law](assets/screenshots/law.png) |

---

## 🎯 Problem Statement

ASEAN is a mosaic of thousands of languages and dialects. However, digital government portals (e-Gov) often use a single dominant national language and complex official terminology. This creates a barrier for:

- 👴 **Elderly users** who cannot understand formal BM or English
- 👷 **Migrant workers** unfamiliar with local legal language
- 🏘️ **Rural B40 communities** excluded from welfare and legal services
- 📋 **SMEs and freelancers** confused by LHDN and JKM letters

> *"In Malaysia, 1,001 undang-undang exist. Most rakyat don't know a single one."*

---

## 💡 Solution

**SuaraRakyat** is a web application powered by **Gemini 2.5 Flash** that:

1. 📷 **Snaps or uploads any government document** (LHDN notice, JKM letter, hospital bill, welfare form)
2. 🤖 **Gemini AI reads and explains it** in simple BM, English, Mandarin, Tamil, or local dialects
3. ✅ **Gives clear action steps** the user must take
4. ✍️ **Drafts a reply letter** if needed
5. ⚖️ **Answers legal questions** about tenancy, employment, consumer, family, road, and welfare rights
6. 🔊 **Supports voice input** for elderly and low-literacy users
7. 👤 **Guest mode** — no account needed to start immediately

---

## ✨ Key Features

### 📄 Document Explainer
| Feature | Description |
|---|---|
| Snap & Explain | Camera photo or PDF upload → Gemini extracts meaning in plain language |
| Instant Summary | Long letters condensed into simple bullet points |
| Action Guide | Clear steps of what to do next |
| Reply Draft | Auto-generates a formal reply letter |

### ⚖️ LawChat
| Feature | Description |
|---|---|
| Law Categories | Tenancy · Employment · Consumer · Family · Road · Welfare |
| Ask Anything | Open-ended legal Q&A in any language or dialect |
| Quick Prompts | Pre-built common questions per category |
| Chat History | Saved per user account via Firestore |

### 🌏 Multilingual AI
| Feature | Description |
|---|---|
| 5 Languages | English, Malay, Indonesian, Tagalog + local dialects |
| Local Dialects | Kelantan and Sarawak dialect support |
| Semantic NLP | Gemini turns complex legal jargon into plain language |
| Voice Input | Web Speech API for text-to-speech accessibility |

### 🛡️ Safety & Trust
| Feature | Description |
|---|---|
| RAG Grounded | All answers grounded in national statutes via System Instructions |
| Hallucination Control | Gemini is grounded in real Malaysian legal frameworks |
| User Auth | Firebase Auth for secure account management |
| Guest Mode | Instant access without creating an account |

---

## 🏗️ Application Architecture

```
┌─────────────────────────────────────────────────────┐
│         React 18 + TypeScript (SPA)                  │
│              Tailwind CSS                            │
│                                                     │
│  ┌──────────────┐        ┌────────────────────────┐  │
│  │  LawChat Tab  │        │  Document Explainer    │  │
│  │  Legal Q&A    │        │  PDF / Photo Upload    │  │
│  └──────┬───────┘        └────────────┬───────────┘  │
│         └──────────────┬──────────────┘              │
│                        │                             │
│           ┌────────────▼────────────┐                │
│           │     Firebase Auth        │                │
│           │   (User Identity)        │                │
│           └────────────┬────────────┘                │
└────────────────────────│────────────────────────────-┘
                         │ HTTPS
          ┌──────────────┴──────────────┐
          │                             │
          ▼                             ▼
┌──────────────────┐         ┌─────────────────────┐
│  Gemini 2.5 Flash │         │  Cloud Firestore     │
│  (AI Engine)      │         │  (Real-time DB)      │
│                  │         │                     │
│ • Legal reasoning │         │ • Chat history      │
│ • Doc parsing    │         │ • Analysed docs     │
│ • NLP & dialect  │         │ • User preferences  │
│ • RAG grounding  │         └─────────────────────┘
└──────────────────┘
         │
         ▼
┌──────────────────┐
│   Google Cloud    │
│      Run          │
│  (Hosted via AI   │
│  Studio Build)    │
└──────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Role |
|---|---|---|
| **Frontend** | React 18 + TypeScript | Responsive Single Page Application (SPA) styled with Tailwind CSS |
| **Backend** | Firebase (Serverless) | Firebase Auth for user identity and Cloud Firestore for real-time data storage |
| **AI Engine** | Gemini 2.5 Flash | Core "brain" for legal reasoning, document parsing, and multi-dialect translation |
| **Environment** | Cloud Run | Hosted on Google Cloud via the AI Studio Build environment |
| **NLP** | Natural Language Processing | Gemini handles semantic analysis to turn complex legal jargon into plain language |
| **RAG** | Grounded Context | Uses System Instructions to ground the AI in national statutes and legal frameworks |
| **Storage** | Firestore | Stores chat history, analysed documents, and user preferences |
| **Sharing** | HTTPS Preview | Shared via a secure URL that allows others to interact with your specific build |
| **Voice** | Web Speech API | Text-to-speech accessibility for elderly and low-literacy users |

---

## 📋 CS4 Technical Requirements — Coverage

| Requirement | Implementation |
|---|---|
| ✅ Dialect-Aware Translation | Gemini handles BM, English, Indonesian, Tagalog, Kelantan and Sarawak dialects |
| ✅ Text Simplification | Gemini converts legal jargon to plain everyday language (5th-grade level) |
| ✅ Recursive Summarisation | Long policy documents condensed into 3–5 actionable bullet points |
| ✅ Cross-Lingual Retrieval | Ask in any dialect → Gemini retrieves from national-language statute |
| ✅ Hallucination Control | RAG via System Instructions grounds all answers in official Malaysian acts |
| ✅ Low-Resource Languages | Covers local dialects not supported by standard translation tools |
| ✅ Inclusivity UI | Guest mode, voice input, simple layout designed for low digital literacy |

---

## 🚀 Getting Started

### Method 1 — Use the Live App

1. **Access the Platform** — Open the App URL in your browser
2. **Set Your Language** — Click the Language icon in the sidebar to choose from English, Malay, Indonesian, Tagalog, or local dialects like Kelantan and Sarawak
3. **Authentication**
   - 🔐 **Sign In** — Create an account to save your history and documents
   - 👤 **Guest Mode** — Click *"Continue as Guest"* to start immediately without an account
4. **Choose Your Tool**
   - 💬 **LawChat Tab** — Type any legal question (e.g. *"What are my rights as a tenant?"*)
   - 📄 **Document Explainer** — Upload a PDF or snap a photo of a legal letter to get an instant simplified summary

---

### Method 2 — Run Locally

#### Prerequisites
- Node.js 18+
- Firebase account
- Google AI Studio API Key (Gemini)

#### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Gohpeijia/VHACK2026-LawChat.git
cd VHACK2026-LawChat

# 2. Install dependencies
npm install

# 3. Set up environment variables
cp .env.example .env
# Add your keys to .env:
# VITE_GEMINI_API_KEY=your_gemini_key
# VITE_FIREBASE_API_KEY=your_firebase_key
# VITE_FIREBASE_PROJECT_ID=your_project_id

# 4. Start development server
npm run dev
```

#### Firebase Setup

```bash
# Install Firebase CLI
npm install -g firebase-tools

# Login and initialise
firebase login
firebase init

# Deploy
firebase deploy
```

---

## 📁 Project Structure

```
VHACK2026-LawChat/
├── src/
│   ├── components/
│   │   ├── LawChat.tsx              # Legal Q&A chat interface
│   │   ├── DocumentExplainer.tsx    # PDF/photo upload + AI result
│   │   ├── LanguageSelector.tsx     # Dialect and language picker
│   │   └── AuthModal.tsx            # Sign in / Guest mode
│   ├── services/
│   │   ├── geminiService.ts         # All Gemini API calls
│   │   └── firebaseService.ts       # Firestore + Auth
│   ├── hooks/
│   │   └── useAuth.ts               # Firebase auth hook
│   └── App.tsx                      # Root component
├── public/
├── .env                             # API keys (not committed)
├── firebase.json                    # Firebase config
└── package.json
```

---

## 🎬 Demo Script

| Step | Action | Expected Result |
|---|---|---|
| 1 | Open app in browser | Home with LawChat + Document Explainer tabs |
| 2 | Click *"Continue as Guest"* | Instant access, no login needed |
| 3 | Click Language icon → select **BM** | UI switches to Bahasa Malaysia |
| 4 | Go to **Document Explainer** | Upload / camera interface appears |
| 5 | Upload a LHDN letter PDF | Gemini explains in simple BM in ~5 seconds |
| 6 | Switch to **LawChat** tab | Chat interface opens |
| 7 | Type: *"Boleh ke landlord halau saya dalam 3 hari?"* | Gemini explains tenant rights + cites Akta |
| 8 | Switch to Kelantan dialect | Same answer in Kelantan dialect |

**Total demo time: ~90 seconds**

---

## 📚 Malaysian Laws Referenced

| Category | Acts |
|---|---|
| Tenancy | Specific Relief Act 1950, Distress Act 1951, National Land Code 1965 |
| Employment | Employment Act 1955, Industrial Relations Act 1967, Minimum Wages Order 2022 |
| Consumer | Consumer Protection Act 1999, Sale of Goods Act 1957 |
| Family | Law Reform (Marriage and Divorce) Act 1976, Guardianship of Infants Act 1961 |
| Road | Road Transport Act 1987, Motor Vehicles (Third Party Risks) Act 1960 |
| Welfare | SOCSO Act 1969, EPF Act 1991, JKM Assistance Guidelines |

---

## 👥 Team

| Name | Role |
|---|---|
| Person 1 | Frontend — React UI/UX, Tailwind, component design |
| Person 2 | AI Engine — Gemini prompts, RAG, NLP, dialect handling |
| Person 3 | Backend + Pitch — Firebase, auth, demo script, slides, video |

---

## 📄 License

This project was built for **V HACK 2026** at Universiti Sains Malaysia.

---

<div align="center">

**SuaraRakyat** — *Snap a letter. Ask a law. Know your rights.*

Built with ❤️ for every Malaysian who deserves to understand their rights.

</div>
#   F i n H a c k 2 0 2 6  
 