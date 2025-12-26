# ITNB RAG Assessment

> **AI Engineering Internship Technical Assessment**
> A production-ready Retrieval-Augmented Generation (RAG) system for the ITNB website knowledge base.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Key Components](#key-components)
- [Advanced Features](#advanced-features)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

This project implements a complete RAG pipeline that:
1. **Crawls** the ITNB website using intelligent BFS (Breadth-First Search)
2. **Ingests** content into GroundX vector database for semantic search
3. **Answers** user questions with accurate, cited responses
4. **Monitors** system health and LLM performance with observability tools

**Built with**: Python 3.12+ | crawl4ai | GroundX | OpenAI-compatible LLM | Langfuse

---

## ✨ Features

### Core Functionality
- ✅ **Intelligent Web Crawler**: BFS-based with domain filtering and politeness policies
- ✅ **Vector Knowledge Base**: GroundX integration for semantic search
- ✅ **RAG Question Answering**: Context-aware responses with source citations
- ✅ **Interactive CLI**: Clean, user-friendly chat interface
- ✅ **Source Attribution**: Every answer cites actual ITNB website URLs
---

## 🚀 Quick Start

### For New Users (Starting from Scratch)

**Step 1: Get Your API Keys**

1. **GroundX** (Required - Vector Database)
   - Sign up at [groundx.ai](https://www.groundx.ai/)
   - Get your API key from dashboard

2. **LLM API** (Required - provided by assessment or use OpenAI)
   - Use the credentials provided in the technical assessment
   - OR get OpenAI API key from [platform.openai.com](https://platform.openai.com/)

3. **Langfuse** (Optional - Observability)
   - Sign up at [cloud.langfuse.com](https://cloud.langfuse.com/)
   - Create a project and get public/secret keys
   - ⚠️ Can be skipped - leave empty in .env to disable

**Step 2: Install Dependencies**

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browser for web crawling
playwright install chromium
```

**Step 3: Configure Your Environment**

```bash
# Copy the example configuration
cp .env.example .env

# Edit .env and add YOUR API keys
# nano .env   (or use any text editor)
```

Update `.env` with your credentials:
```bash
GROUNDX_API_KEY=your_actual_groundx_key_here
OPENAI_API_KEY=your_actual_llm_key_here
LANGFUSE_SECRET_KEY=your_langfuse_key_or_leave_empty
LANGFUSE_PUBLIC_KEY=your_langfuse_key_or_leave_empty
```

**Step 4: Crawl the ITNB Website**

```bash
# This will scrape ~32 pages from itnb.ch and save them as Markdown
python main.py --crawl-only
```

Expected output: `✅ 32 pages crawled successfully → data/scraped/`

**Step 5: Ingest Documents to GroundX**

```bash
# Upload the scraped pages to your GroundX vector database
python main.py --ingest-only
```

Expected output: `✅ 32 documents ingested to GroundX`

**Step 6: Start Chatting!**

```bash
# Launch the interactive RAG chatbot
python main.py --chat-only
```

Now you can ask questions about ITNB! 🎉

---

### Alternative: Run All Steps at Once

If you want to do everything in one command (first-time setup):

```bash
# Complete pipeline: Crawl → Ingest → Chat
python main.py --full-pipeline
```

### Daily Use (Data Already Exists)

Once you've crawled and ingested once, just chat:

```bash
# Chat only (assumes data already in GroundX)
python main.py
```

**Note**: `python main.py` does NOT re-crawl or re-ingest. It only starts the chat interface.

### Update Website Content

If ITNB website changed and you want fresh data:

```bash
# Re-crawl and re-ingest, then chat
python main.py --crawl --ingest
```

---

### Configuration Options

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROUNDX_API_KEY` | GroundX API key | - | ✅ Yes |
| `OPENAI_API_KEY` | LLM API key | - | ✅ Yes |
| `OPENAI_MODEL_NAME` | Model identifier | `inference-llama4-maverick` | ✅ Yes |
| `OPENAI_API_BASE` | LLM API endpoint | - | ✅ Yes |
| `USE_CONVERSATION_MEMORY` | Enable conversational memory | `true` | ❌ No |
| `LANGFUSE_SECRET_KEY` | Langfuse secret key | - | ❌ No |
| `LANGFUSE_PUBLIC_KEY` | Langfuse public key | - | ❌ No |

---

## 💻 Usage

### Interactive Chat (Recommended)

Start the chat interface with health checks:

```bash
python main.py
```

**Output:**
```
============================================================
  🏥 SYSTEM HEALTH CHECK
============================================================

Checking GroundX Vector Database...
✓ GroundX API: Connected (1 buckets found)

Checking LLM API Endpoint...
✓ LLM API: Connected (model: inference-llama4-maverick)

Checking Langfuse Observability...
✓ Langfuse: Configured (https://cloud.langfuse.com)

------------------------------------------------------------
✓ All critical systems operational
============================================================

  ██╗████████╗███╗   ██╗██████╗      █████╗ ██╗
  ██║╚══██╔══╝████╗  ██║██╔══██╗    ██╔══██╗██║
  ██║   ██║   ██╔██╗ ██║██████╔╝    ███████║██║
  ██║   ██║   ██║╚██╗██║██╔══██╗    ██╔══██║██║
  ██║   ██║   ██║ ╚████║██████╔╝    ██║  ██║██║
  ╚═╝   ╚═╝   ╚═╝  ╚═══╝╚═════╝     ╚═╝  ╚═╝╚═╝

Welcome! I can answer questions about ITNB AG based on
the company's website content.

Commands:
  - Type your question and press Enter
  - Type '/health' to check system health
  - Type 'exit' or 'quit' to end the session
  - Type 'clear' to clear conversation history
============================================================

💬 You: What does ITNB do?

🤖 Assistant: ITNB is a Swiss cybersecurity and IT company...

📚 Sources:
  1. https://www.itnb.ch/en/company/about-itnb
  2. https://www.itnb.ch/en/products-and-services

⚡ Response Time: 2.58s | Chunks: 5 | Model: inference-llama4-maverick
```

### Available Commands

| Command | Description |
|---------|-------------|
| `<your question>` | Ask any question about ITNB |
| `/health` | Check system health (no LLM call) |
| `clear` | Clear conversation history |
| `help` or `?` | Show help message |
| `exit` or `quit` | Exit chat |

### Individual Phases

**Phase 1: Crawl Website**
```bash
python main.py --crawl-only
```
- Crawls ITNB website using BFS
- Saves pages as Markdown files to `data/scraped/`
- Preserves metadata (source URL, title, timestamp)

**Phase 2: Ingest Documents**
```bash
python main.py --ingest-only
```
- Uploads Markdown files to GroundX
- Extracts source URLs from frontmatter
- Creates/updates vector embeddings

**Phase 3: Chat Only**
```bash
python main.py --chat-only
```
- Starts chat interface without crawling/ingestion
- Uses existing GroundX bucket

---

## 🔑 Key Components

### 1. Web Crawler ([src/crawler.py](src/crawler.py))

**Features:**
- BFS traversal with queue-based exploration
- Domain filtering (only `itnb.ch/en`)
- Duplicate URL detection
- Rate limiting (politeness policy)
- Metadata preservation in Markdown frontmatter

**Usage:**
```python
from src.crawler import ITNBCrawler

crawler = ITNBCrawler(start_url="https://www.itnb.ch/en")
crawler.crawl()
# Saves to data/scraped/*.md
```

### 2. GroundX Client ([src/groundx_client.py](src/groundx_client.py))

**Features:**
- Bucket management (create/get)
- Document ingestion with metadata
- Semantic search with source URL extraction
- Clean bucket deletion for fresh starts

**Usage:**
```python
from src.groundx_client import GroundXClient

client = GroundXClient()
client.get_or_create_bucket()
client.ingest_documents()  # Uploads all .md files

results = client.search(query="What is Sovereign Cloud?", n=5)
```

### 3. RAG Engine ([src/rag_engine.py](src/rag_engine.py))

**Features:**
- Context retrieval from GroundX
- Prompt construction with conversation history
- LLM answer generation
- Langfuse observability integration
- Source URL extraction

**Usage:**
```python
from src.rag_engine import RAGEngine

engine = RAGEngine()

# Stateless query
result = engine.query("What does ITNB do?")

# With conversation memory
history = [{"question": "...", "answer": "..."}]
result = engine.query("Tell me more", conversation_history=history)
```

### 4. Health Check System ([src/health_check.py](src/health_check.py))

**Features:**
- Validates GroundX connection
- Checks LLM endpoint availability
- Verifies Langfuse configuration
- Distinguishes critical vs optional components

**Usage:**
```python
from src.health_check import run_health_check

healthy = run_health_check()
if not healthy:
    print("System not ready")
```

---

## 🎯 Additional Features

### Conversational Memory

Enable context retention across queries for natural follow-up questions.

**Enable:**
```bash
# In .env
USE_CONVERSATION_MEMORY=true
```

**Example:**
```
💬 You: What does ITNB do?
🤖 Assistant: ITNB is a Swiss cybersecurity company...

💬 You: Tell me more about their cloud services
🤖 Assistant: [Understands "their" refers to ITNB from previous context]
```

**How it works:**
- Keeps last 5 message pairs (sliding window)
- Passes conversation history to LLM
- In-memory storage (no external dependencies)
- Can be disabled for stateless queries

### Health Check Command

Monitor system status during chat without LLM calls.

**Usage:**
```
💬 You: /health

============================================================
  🏥 SYSTEM HEALTH CHECK
============================================================

Checking GroundX Vector Database...
✓ GroundX API: Connected (1 buckets found)

Checking LLM API Endpoint...
✓ LLM API: Connected (model: inference-llama4-maverick)

Checking Langfuse Observability...
✓ Langfuse: Configured (https://cloud.langfuse.com)

------------------------------------------------------------
✓ All critical systems operational
============================================================
```

### Langfuse Observability

Track LLM performance, costs, and latency.

**Setup:**
1. Sign up at [cloud.langfuse.com](https://cloud.langfuse.com)
2. Create a project
3. Add keys to `.env`:
   ```bash
   LANGFUSE_SECRET_KEY=sk-lf-...
   LANGFUSE_PUBLIC_KEY=pk-lf-...
   ```

**Features:**
- Automatic trace generation for each query
- Latency tracking
- Token usage monitoring
- Error logging
- View traces at Langfuse dashboard

## 📁 Project Structure

```
itnb-rag-assessment/
├── config.py                  # Centralized configuration
├── main.py                    # Main orchestrator
├── requirements.txt           # Python dependencies
├── .env                       # Environment variables (create from .env.example)
├── .env.example              # Example configuration
├── README.md                 # This file
│
├── src/                      # Source code
│   ├── __init__.py
│   ├── crawler.py            # Web crawler (BFS)
│   ├── groundx_client.py     # GroundX API client
│   ├── rag_engine.py         # RAG pipeline
│   ├── cli.py                # CLI chat interface
│   └── health_check.py       # System health validation
│
├── data/                     # Data storage
│   └── scraped/              # Crawled Markdown files (*.md)
│
└── tests/                    # Test scripts
    ├── test_system.py        # End-to-end test
    ├── test_queries.py       # Multiple query test
    ├── test_memory.py        # Conversation memory test
    └── clean_reingest.py     # Clean bucket re-ingestion
```

## 📐 Stage 2: Design Questions & Answers

### Question 1: Role-Based Access Control (RBAC) Implementation

**Strategy: Application-Layer Metadata Filtering**
GroundX is a vector database, not an identity provider. Therefore, RBAC must be enforced by the application backend **before** the query reaches the search index.

**1. Ingestion (Tagging)**
During the ingestion phase, every document is tagged with strict `allowed_roles` metadata.

```python
# Ingest with security tags
client.ingest(
    documents=[{
        "blob": file_data,
        "metadata": { 
            "allowed_roles": ["finance_manager", "admin"], # Security Tag
            "department": "finance" 
        }
    }]
)

```

**2. Retrieval (Enforcement)**
When a user queries the system, the backend extracts their role from the session (e.g., JWT) and **forcibly injects** a filter into the GroundX search call. This guarantees the LLM never receives context the user isn't authorized to see.

```python
# Backend logic (not visible to user)
user_roles = auth_service.get_current_user_roles() # e.g. ["intern"]

results = groundx.search(
    query=user_query,
    filter={ "allowed_roles": { "$in": user_roles } } # Hard filter
)

```

---

### Question 2: Scaling RAG for Large and Dynamic Knowledge Bases

**1. Managing Large-Scale Documents**

* **Incremental Ingestion:** I would avoid full site re-crawls, and only use content hashing (SHA-256) to detect changes to only upload modified documents to GroundX.
* **Virtual Hierarchy:** GroundX buckets are flat, thus, to scale, I would simulate a folder structure using naming conventions (e.g., bucket name `engineering-sovereign-v1`) to scope searches narrowly and improve retrieval latency.

**2. User-Empowered Management**
**Yes, users must manage their own documents.**

* **Why:** IT/Admin teams become bottlenecks. Only domain experts know when a document is obsolete.
* **How:** Build a lightweight internal portal (Next.js/FastAPI) wrapping the GroundX API, this will allow authorized users to upload, tag, and—crucially delete outdated files without touching the codebase.

**3. Automation & Workflows**

* **Event-Driven Sync:** Instead of daily batch jobs, use Webhooks from source systems (SharePoint/Jira). When a file changes in SharePoint, a Lambda function triggers an immediate single-file update in GroundX.
* **Staleness Agents:** Run a weekly background job that flags documents older than 6 months and emails the document "owner" to verify if it is still accurate.

## 📚 Sources

Design answers based on GroundX documentation:
- [GroundX API Concepts](https://docs.eyelevel.ai/documentation/fundamentals/api-concepts)
- [Document Ingestion API](https://docs.eyelevel.ai/reference/api-reference/documents/ingest-documents)
- [Bucket Management](https://docs.eyelevel.ai/reference/api-reference/buckets/create)
- [Search API Reference](https://docs.eyelevel.ai/reference/api-reference/documents/lookup)
- [GroundX Security & Enterprise Features](https://www.eyelevel.ai/product/groundx-security)

---

**Built with ❤️ for the ITNB AI Engineering Internship**
