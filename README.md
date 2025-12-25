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

### Production-Grade Features
- 🏥 **Health Check System**: Pre-flight validation of all components
- 💬 **Conversational Memory**: Optional context retention across queries
- 📊 **Langfuse Observability**: LLM monitoring and performance tracking
- 🛡️ **Robust Error Handling**: Graceful failures with clear error messages
- 🔧 **Modular Architecture**: Clean separation of concerns
- ⚡ **Performance Optimized**: Average response time 2-3 seconds

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure API keys
cp .env.example .env
# Edit .env with your API keys

# 3. Install browser for crawler
playwright install chromium

# 4. Run the complete pipeline
python main.py

# Or run individual phases:
python main.py --crawl-only      # Phase 1: Crawl website
python main.py --ingest-only     # Phase 2: Ingest to GroundX
python main.py --chat-only       # Phase 3: Chat interface
```

---

## 📦 Installation

### Prerequisites

- **Python 3.9+** (tested with 3.12)
- **pip** package manager
- **GroundX account** ([free trial](https://www.groundx.ai/))
- **Internet connection** for API calls

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Install Playwright Browser

```bash
playwright install chromium
```

### Step 3: Configure Environment

```bash
# Copy example configuration
cp .env.example .env

# Edit .env and add your API keys
```

---

## ⚙️ Configuration

Edit `.env` file with your credentials:

```bash
# GroundX API (Required)
GROUNDX_API_KEY=your_groundx_api_key_here

# LLM API (Required - OpenAI-compatible)
OPENAI_MODEL_NAME=inference-llama4-maverick
OPENAI_API_BASE=https://maas.ai-2.kvant.cloud
OPENAI_API_KEY=your_llm_api_key_here

# Conversational Memory (Optional)
USE_CONVERSATION_MEMORY=true  # Enable context retention (default: true)

# Langfuse Observability (Optional)
LANGFUSE_SECRET_KEY=your_secret_key  # Leave empty to disable
LANGFUSE_PUBLIC_KEY=your_public_key
LANGFUSE_HOST=https://cloud.langfuse.com
```

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

## 🎯 Advanced Features

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

### Clean Bucket Re-ingestion

Remove all old data and start fresh:

```bash
python clean_reingest.py
```

This will:
1. Delete existing GroundX bucket
2. Create fresh bucket
3. Re-ingest all documents with proper metadata

---

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

---

## 🐛 Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Install all dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium
```

**2. GroundX Connection Failed**
```bash
# Check API key in .env
GROUNDX_API_KEY=your_actual_key_here

# Test connection
python -c "from src.health_check import run_health_check; run_health_check()"
```

**3. LLM Connection Failed**
```bash
# Verify API endpoint and key
OPENAI_API_BASE=https://maas.ai-2.kvant.cloud
OPENAI_API_KEY=your_actual_key_here

# Check model name (no "openai/" prefix)
OPENAI_MODEL_NAME=inference-llama4-maverick
```

**4. Langfuse Not Working**
```bash
# Langfuse is optional - check config
LANGFUSE_SECRET_KEY=sk-lf-...
LANGFUSE_PUBLIC_KEY=pk-lf-...

# Leave empty to disable observability
LANGFUSE_SECRET_KEY=
LANGFUSE_PUBLIC_KEY=
```

**5. Empty or Wrong Sources**
```bash
# Re-ingest with clean bucket
python clean_reingest.py

# This removes old data and re-uploads with correct metadata
```

**6. Conversation Memory Not Working**
```bash
# Check config flag
USE_CONVERSATION_MEMORY=true

# Restart chat to apply changes
python main.py
```

### Debug Mode

Enable verbose logging:
```python
# Add to main.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Issues

- **Slow responses**: Check LLM API endpoint latency
- **Out of memory**: Reduce `max_history_messages` in config.py
- **Crawler timeout**: Increase timeout in src/crawler.py

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| **Crawl Speed** | ~2-3 pages/second |
| **Documents Indexed** | 32 pages |
| **Average Query Time** | 2-3 seconds |
| **Vector Search** | Top 5 chunks |
| **Context Window** | Last 5 message pairs |
| **Uptime** | Health checks ensure 99%+ readiness |

---

## 🎓 Technical Highlights

### Best Practices Implemented

✅ **Configuration Management**: Centralized config with environment variables
✅ **Error Handling**: Graceful failures with user-friendly messages
✅ **Type Safety**: Type hints throughout codebase
✅ **Documentation**: Comprehensive docstrings and README
✅ **Modular Design**: Clear separation of concerns
✅ **Observability**: Production-ready monitoring with Langfuse
✅ **Health Checks**: Pre-flight validation before user interaction
✅ **Source Attribution**: Accurate citation of information sources
✅ **Memory Management**: Efficient sliding window for conversation history
✅ **Clean Architecture**: Easy to test, maintain, and extend

### Design Decisions

- **In-memory conversation storage**: No Redis needed for CLI application
- **Sliding window**: Prevents context overflow while maintaining relevance
- **Optional features**: Memory and observability can be toggled via config
- **Health checks first**: Fail fast with clear error messages
- **Clean CLI**: Minimal noise, maximum clarity
- **Source URL extraction**: Frontmatter metadata for accurate attribution

---

## 📝 License

This project is part of the ITNB AI Engineering Internship Technical Assessment.

---

## 🙏 Acknowledgments

- **ITNB AG** for the internship opportunity
- **GroundX** for vector database infrastructure
- **Langfuse** for LLM observability tools
- **crawl4ai** for web scraping capabilities

---

**Built with ❤️ for the ITNB AI Engineering Internship**
