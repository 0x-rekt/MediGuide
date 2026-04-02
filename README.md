# MediGuide AI 🏥

**AI-Powered Medical Assistant for Tourists in India**

An intelligent multi-agent system that helps international tourists get fast, reliable medical assistance — from symptom checking to hospital discovery, cost estimation, and document generation. Built with Claude AI, FastAPI, and Next.js.

**[Jump to Setup](#-quick-start) | [API Docs](#-api-endpoints) | [Architecture](#-architecture)**

---

## ✨ Features

### 🤖 Six Specialized Agents

| Agent       | Purpose                                     | Technology                         |
| ----------- | ------------------------------------------- | ---------------------------------- |
| **Agent 1** | Multilingual Symptom Intake                 | Google Gemini (multilingual)       |
| **Agent 2** | Intelligent Triage & Severity Assessment    | Claude AI (medical reasoning)      |
| **Agent 3** | Real-time Nearest Hospital Finder           | Google Places API + Claude         |
| **Agent 4** | Smart Booking & Coordination                | Claude AI (with tool use)          |
| **Agent 5** | Transparent Cost Estimator                  | Claude AI (financial calculations) |
| **Agent 6** | Medical Summary & Insurance Claim Generator | CraftMyPDF + Claude                |

### 💡 Key Capabilities

- **🌍 Multilingual Support**: English, Hindi, Bengali, Spanish, French, and more
- **🏥 Real-time Hospital Discovery**: Nearest facilities with ratings and contact info
- **💰 Transparent Pricing**: Insurance-aware cost estimates and breakdowns
- **📋 Professional Documentation**: Auto-generated medical summaries and claim letters
- **🚨 Emergency Triage**: Intelligent severity assessment and guidance
- **🔄 End-to-End Workflow**: From intake to booking to documentation in one pipeline

---

## 🛠️ Tech Stack

### Backend

- **Framework**: FastAPI + Uvicorn
- **AI Models**:
  - Anthropic Claude 3 (primary agent logic)
  - Google Generative AI (multilingual support)
- **Database**: MongoDB with Motor (async driver)
- **External APIs**:
  - Google Places API (hospital search & details)
  - CraftMyPDF (PDF generation)
  - Clerk API (authentication)
  - Svix (webhook handling)

### Frontend

- **Framework**: Next.js 16.2 with TypeScript
- **UI Components**: Shadcn/ui with Radix UI
- **Authentication**: Clerk
- **Styling**: Tailwind CSS v4
- **Icons**: Lucide React

### Deployment & Infrastructure

- Backend: FastAPI server (Docker-ready)
- Frontend: Next.js (Vercel-ready)
- Database: MongoDB Atlas (cloud)

---

## 📁 Project Structure

```bash
MediGuide/
├── backend/
│   ├── agent1.py              # Multilingual chat & intake
│   ├── agent2.py              # Triage & severity assessment
│   ├── agent3.py              # Hospital finder & matching
│   ├── agent4.py              # Booking coordination
│   ├── agent5.py              # Cost estimation
│   ├── agent6.py              # Document generation
│   ├── orchestrator.py        # Main pipeline orchestrator
│   ├── main.py                # FastAPI server
│   ├── requirements.txt       # Python dependencies
│   ├── .env                   # Environment variables
│   └── src/
│       ├── utils.py           # Utility functions
│       └── routes/
│           └── webhooks.py    # Webhook handlers
│
├── frontend/
│   ├── app/
│   │   ├── layout.tsx         # Root layout with auth
│   │   ├── page.tsx           # Home page
│   │   └── globals.css        # Global styles
│   ├── components/
│   │   └── ui/                # Shadcn UI components
│   ├── lib/
│   │   └── utils.ts           # Client utilities
│   ├── public/                # Static assets
│   ├── package.json
│   ├── next.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   └── README.md
│
├── README.md                  # This file
└── .gitignore
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- MongoDB Atlas account (or local MongoDB)
- API Keys:
  - Anthropic Claude API
  - Google Generative AI API
  - Google Places API
  - Clerk API
  - CraftMyPDF API

### Backend Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file with required variables
cat > .env << EOF
ANTHROPIC_API_KEY=sk-...
GOOGLE_API_KEY=...
GOOGLE_PLACES_API_KEY=...
MONGODB_URI=mongodb+srv://user:password@cluster.mongodb.net/mediguide
CLERK_SECRET_KEY=...
CRAFT_MY_PDF_API_KEY=...
EOF

# 5. Run the FastAPI server
uvicorn main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`

### Frontend Setup

```bash
# 1. Navigate to frontend
cd frontend

# 2. Install dependencies
npm install
# or
yarn install

# 3. Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

# 4. Run development server
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`

---

## 🏗️ Architecture

### Agent Pipeline Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input (Web/Mobile)                   │
└────────────────────────────┬────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │    AGENT 1      │
                    │  Multilingual   │
                    │  Chat & Intake  │
                    │  (Google Gemini)│
                    └────────┬────────┘
                             │ (symptoms, duration, allergies)
                    ┌────────▼─────────┐
                    │    AGENT 2       │
                    │  Triage &        │
                    │  Severity Assess │
                    │  (Claude AI)     │
                    └────────┬─────────┘
                             │ (severity level, flags)
          ┌──────────────────┼──────────────────┐
          │                  │                  │
      ┌───▼────┐       ┌─────▼──────┐    ┌────▼────┐
      │AGENT 3 │       │ EMERGENCY? │    │AGENT 4  │
      │Hospital│       │    YES     │    │ Booking │
      │ Finder │       │    →→→     │    │  Coord  │
      │        │       │   112      │    │         │
      └───┬────┘       └────────────┘    └────┬────┘
          │                                    │
          │            ┌──────────────────────┘
          │            │
      ┌───▼────────────▼─┐
      │    AGENT 5       │
      │  Cost Estimator  │
      │ (Insurance aware)│
      └────────┬─────────┘
               │
      ┌────────▼────────┐
      │    AGENT 6      │
      │  Doc Generator  │
      │  (Medical PDF)  │
      └────────┬────────┘
               │
      ┌────────▼────────────────┐
      │  Final Report/Booking   │
      │  + Estimated Costs      │
      │  + Medical Documents    │
      └─────────────────────────┘
```

### Key Design Decisions

1. **Sequential Agent Chain**: Each agent passes its output to the next, building context progressively
2. **Tool-Calling**: Agents use Claude's function calling for precise API interactions
3. **Multilingual First**: Agent 1 detects language and maintains context throughout
4. **Insurance Awareness**: Cost calculations account for tourist insurance plans
5. **Async Operations**: FastAPI with Motor for non-blocking database operations

---

## 🔌 API Endpoints

### Health Check

```
GET /health
Response: { "status": "ok" }
```

### Webhook Integration (Clerk, Svix)

```
POST /webhooks/clerk
POST /webhooks/events
Content-Type: application/json
```

### Usage Example with cURL

```bash
# Health check
curl http://localhost:8000/health

# (Additional endpoints depend on frontend implementation)
```

---

## 🔑 Environment Variables

### Backend (.env)

| Variable                | Description               | Example             |
| ----------------------- | ------------------------- | ------------------- |
| `ANTHROPIC_API_KEY`     | Claude API key            | `sk-ant-...`        |
| `GOOGLE_API_KEY`        | Google Generative AI key  | `AIzaSy...`         |
| `GOOGLE_PLACES_API_KEY` | Google Places API key     | `AIzaSy...`         |
| `MONGODB_URI`           | MongoDB connection string | `mongodb+srv://...` |
| `CLERK_SECRET_KEY`      | Clerk backend secret      | `sk_test_...`       |
| `CRAFT_MY_PDF_API_KEY`  | CraftMyPDF API key        | `api_...`           |

### Frontend (.env.local)

| Variable                            | Description        | Example                 |
| ----------------------------------- | ------------------ | ----------------------- |
| `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` | Clerk frontend key | `pk_test_...`           |
| `CLERK_SECRET_KEY`                  | Clerk backend key  | `sk_test_...`           |
| `NEXT_PUBLIC_API_URL`               | Backend API URL    | `http://localhost:8000` |

---

## 🎯 Agent Details

### Agent 1: Multilingual Chat Agent

- **Purpose**: Initial symptom intake and language detection
- **AI Model**: Google Generative AI (Gemini)
- **Inputs**: User description of symptoms
- **Outputs**: Structured symptom data, detected language, duration, severity self-report
- **Features**: Supports 20+ languages, friendly conversation style

### Agent 2: Triage & Severity Assessment

- **Purpose**: Clinical triage and risk assessment
- **AI Model**: Claude 3 (high reasoning capability)
- **Inputs**: Symptom structure, medical history, allergies
- **Outputs**: Severity level (low/medium/high/emergency), recommended action
- **Features**: Red flag detection, emergency protocol activation

### Agent 3: Hospital Finder

- **Purpose**: Locate and match appropriate medical facilities
- **AI Model**: Claude 3 + Google Places API
- **Inputs**: Patient severity, location, medical needs
- **Outputs**: List of 3-5 nearest hospitals with details
- **Features**: Real-time ratings, contact info, estimated distance

### Agent 4: Booking Coordination

- **Purpose**: Facilitate appointments and admissions
- **AI Model**: Claude 3 (with booking tools)
- **Inputs**: Selected hospital, patient details, medical urgency
- **Outputs**: Booking confirmation, appointment details
- **Features**: Multi-language communication templates

### Agent 5: Cost Estimator

- **Purpose**: Transparent financial planning
- **AI Model**: Claude 3 (financial reasoning)
- **Inputs**: Hospital, procedures, insurance plan, home currency
- **Outputs**: Cost breakdown, insurance coverage, final estimate
- **Features**: Multi-currency support, insurance claim pre-calculation

### Agent 6: Document Generator

- **Purpose**: Professional medical and legal documentation
- **AI Model**: Claude 3 + CraftMyPDF
- **Inputs**: Complete patient journey, medical findings, costs
- **Outputs**: PDF medical summary, insurance claim letter, prescription
- **Features**: HIPAA-aware formatting, professional templates

---

## 🧪 Running the Pipeline

### Interactive Mode

```bash
cd backend
python orchestrator.py
```

This launches an interactive terminal experience where users input information step-by-step.

### Demo Mode

To test with sample data:

```python
python -c "from orchestrator import run_pipeline; run_pipeline(demo_mode=True)"
```

---

## 🔐 Security Considerations

1. **API Keys**: Never commit `.env` files to git (included in `.gitignore`)
2. **Authentication**: Clerk handles user authentication on the frontend
3. **Data Privacy**: Medical data is encrypted in MongoDB
4. **CORS**: Frontend is allowed only from whitelisted origins
5. **Rate Limiting**: Implement rate limiting for API calls (recommended)
6. **HIPAA**: PDF generation follows HIPAA compliance guidelines

---

## 📊 Database Schema (MongoDB)

### Collections

- **users**: Tourist profiles and preferences
- **consultations**: Medical consultation records
- **bookings**: Hospital appointment bookings
- **documents**: Generated medical documents
- **costs**: Cached cost estimates

---

## 🚀 Deployment

### Backend (FastAPI)

Option 1: Docker

```bash
# In backend directory
docker build -t mediguide-backend .
docker run -p 8000:8000 --env-file .env mediguide-backend
```

Option 2: Cloud Platforms

- **Heroku**: `git push heroku main`
- **Railway**: Connect GitHub repo
- **AWS/GCP**: Use managed container services

### Frontend (Next.js)

Option 1: Vercel (Recommended)

```bash
npm install -g vercel
vercel
```

Option 2: Docker

```bash
npm run build
npm start
```

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'agent1'`

- **Solution**: Ensure you're in the `backend/` directory and Python path includes the current directory

**Problem**: `anthropic.APIConnectionError`

- **Solution**: Verify `ANTHROPIC_API_KEY` is set in `.env` file

**Problem**: `pymongo.errors.ServerSelectionTimeoutError`

- **Solution**: Check MongoDB URI is correct and network allows connections

### Frontend Issues

**Problem**: Clerk authentication not working

- **Solution**: Verify `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` matches your Clerk app

**Problem**: API calls failing with CORS error

- **Solution**: Ensure `NEXT_PUBLIC_API_URL` matches backend URL in `.env.local`

---

## 📈 Future Enhancements

- [ ] SMS/WhatsApp integration via Twilio
- [ ] Video consultation capability
- [ ] Prescription fulfillment integration
- [ ] Real-time chat websocket support
- [ ] Multi-language email templates
- [ ] Insurance company API integrations
- [ ] Patient medical history database
- [ ] Analytics dashboard for hospitals

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add new feature'`
4. Push to branch: `git push origin feature/your-feature`
5. Submit a Pull Request

---

## 📝 License

This project is proprietary. All rights reserved.

---

## 👥 Support

For issues, questions, or feedback:

- 📧 Create an issue on GitHub
- 💬 Contact the development team

---

## 🙏 Acknowledgments

- **Google** for Places API and Generative AI
- **Clerk** for authentication infrastructure
- **Vercel** for Next.js framework and deployment
