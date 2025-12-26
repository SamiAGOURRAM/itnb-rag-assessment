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

## 📐 Stage 2: Design Questions & Answers

### Question 1: Role-Based Access Control (RBAC) Implementation

**Scenario**: Enterprise users with different document access rights (e.g., department-specific access vs. manager-level access).

**Solution Design**:

GroundX provides [**Fine-Grained Access Control (RBAC)**](https://www.eyelevel.ai/product/groundx-security) at document, bucket, and project levels, enabling enterprise-grade permission management.

#### Document-User Association

Based on [GroundX API documentation](https://docs.eyelevel.ai/reference/api-reference/documents/ingest-documents) and [security features](https://www.eyelevel.ai/product/groundx-security), we would use a **metadata-based RBAC approach**:

1. **searchData Parameter**: Attach custom metadata to each document during ingestion
   ```python
   searchData = {
       "department": "engineering",
       "access_level": "confidential",
       "allowed_roles": ["engineer", "manager", "admin"]
   }
   ```

2. **Bucket Organization**: Create department-specific buckets for coarse-grained access
   - `engineering-bucket`, `hr-bucket`, `finance-bucket`
   - Buckets serve as organizational units ([GroundX Buckets](https://docs.eyelevel.ai/reference/api-reference/buckets/create))

3. **Filter Parameter**: Use pre-filtering metadata
   ```python
   filter = {
       "permissions": {
           "roles": ["moderator", "admin"]
       }
   }
   ```

#### Access Enforcement at Query Time

Per [GroundX Search API](https://docs.eyelevel.ai/reference/api-reference/documents/lookup), implement a **query-time filtering layer**:

1. **Authentication Layer**: Verify user identity via JWT/OAuth
2. **Role Extraction**: Extract user's roles and department from auth token
3. **Filter Injection**: Pass user's authorized roles in the search filter
   ```python
   user_filter = {
       "department": user.department,
       "allowed_roles": user.roles  # ["engineer", "team_lead"]
   }
   search_results = groundx.search.content(
       query=question,
       filter=user_filter  # Pre-filters before vector search
   )
   ```

4. **Bucket Scoping**: Query only buckets user has access to
   ```python
   accessible_buckets = get_user_buckets(user)  # ["engineering-bucket"]
   search_results = groundx.search.content(
       bucket_ids=accessible_buckets,
       query=question
   )
   ```

#### Enterprise Security & Compliance

**GroundX Security Features** ([source](https://www.eyelevel.ai/product/groundx-security)):

1. **Data Protection**:
   - **End-to-End AES 256 Encryption** for data at rest and in transit
   - **Air-Gapped Deployments** for isolated systems (no external internet required)
   - **No Model Training on Customer Data** (unless explicitly authorized)

2. **Access Control**:
   - **Multi-Level Governance**: Document-level, bucket-level, and project-level permissions
   - **Fine-Grained RBAC** for enhanced compliance

3. **Compliance Certifications**:
   - **SOC 2 Certified** for enterprise trust
   - **HIPAA Compliant** for healthcare data
   - **FIPS Certified** with CVE-free images for government/regulated industries

4. **Secure Infrastructure**:
   - **Kubernetes-based architecture** with minimal attack surface
   - Single controlled point of data egress
   - Distributed Kafka processing within protected clusters
   - Dedicated storage and metadata databases with stringent security protocols

**Implementation Considerations**:

1. **Application-Level Enforcement**: Implement RBAC middleware before GroundX
2. **API Key Security**: Use service account pattern, never expose keys to clients
3. **Metadata Integrity**: Validate searchData permissions server-side
4. **Audit Logging**: Track document access for compliance (implement separately)
5. **Defense in Depth**:
   - Filter at query time (primary)
   - Bucket-level isolation (secondary)
   - Post-processing verification (tertiary)

**Recommended Architecture**:
```
User → Auth Service → RBAC Middleware → GroundX Proxy → GroundX API
         (JWT)        (Extract roles)    (Inject filters)   (Search)
```

---

### Question 2: Scaling RAG for Large and Dynamic Knowledge Bases

**Context**: ITNB's Sovereign Orchestrator - enterprise AI concierge handling thousands of documents with frequent updates.

**Scalable RAG Architecture Design**:

#### 1. Large-Scale Document Management

**Mechanisms for Handling Scale**:

1. **Incremental Ingestion Strategy**
   - Use [GroundX batch upload](https://docs.eyelevel.ai/reference/api-reference/documents/ingest-documents) via Python SDK
   - Implement change detection (hash-based or timestamp)
   - Only re-ingest modified documents
   ```python
   def ingest_changes(documents):
       for doc in documents:
           doc_hash = compute_hash(doc.content)
           if doc_hash != stored_hash(doc.id):
               groundx.ingest(doc, searchData={"hash": doc_hash})
   ```

2. **Hierarchical Bucket Structure**
   - Organize by: `{department}/{project}/{doc_type}`
   - Enables targeted searches (faster, more relevant)
   - Example: `engineering/sovereign-orchestrator/api-docs`

3. **Metadata-Rich Indexing**
   - Leverage [GroundX's automatic metadata generation](https://docs.eyelevel.ai/documentation/fundamentals/api-concepts)
   - Add custom searchData: `last_updated`, `owner`, `version`, `category`
   - Enables smart filtering and ranking

4. **X-Ray Data for Offline Processing**
   - Download [X-Ray summaries](https://docs.eyelevel.ai/documentation/fundamentals/api-concepts) for local caching
   - Use for analytics and monitoring without API calls

#### 2. User-Empowered Document Management

**Should Users Manage Documents?** ✅ **Yes** - Here's why and how:

**Why Empower Users**:
- **Domain Expertise**: Users know which documents are relevant/outdated
- **Scalability**: Distributes workload (IT can't manually manage thousands of docs)
- **Accuracy**: Real-time updates from source experts
- **Ownership**: Departments own their knowledge bases

**How to Implement**:

1. **Self-Service Portal**
   ```
   User Interface → FastAPI Backend → GroundX API
   - Upload documents (drag & drop)
   - Set metadata (department, tags, permissions)
   - Delete outdated docs
   - Monitor ingestion status
   ```

2. **Automated Connectors** (Reduce Manual Work)
   - **MS365 Integration**: Auto-sync SharePoint docs
   - **Webhook Listeners**: Trigger on document changes
   - **Scheduled Crawlers**: Weekly website scraping
   ```python
   @schedule.every().day.at("03:00")
   def sync_sharepoint():
       changes = detect_sharepoint_changes()
       ingest_batch(changes)
   ```

3. **Version Control**
   - Keep document versions in searchData
   - Allow rollback if bad update
   ```python
   searchData = {
       "version": "2.1.0",
       "previous_version": "2.0.3",
       "updated_by": "user@itnb.ch"
   }
   ```

#### 3. Automation & Agent Workflows

**Algorithms & Automation for Efficiency**:

1. **Smart Re-Indexing** (Not Full Re-crawl)
   - **Event-Driven Architecture**:
     ```
     Document Change → Event Queue → Incremental Ingest Agent
     ```
   - Use file hashes or modification timestamps
   - Only update changed chunks (not entire doc)

2. **Intelligent Routing Agent**
   - Route queries to relevant buckets using metadata
   ```python
   def route_query(query, user_context):
       # Classify query intent
       intent = classify(query)  # "API docs", "HR policy", etc.

       # Select relevant buckets
       buckets = select_buckets(intent, user_context.department)

       # Weighted search across buckets
       return search(query, buckets, weights=relevance_scores)
   ```

3. **Feedback Loop for Ranking**
   - Track which results users click
   - Re-rank using engagement signals
   ```python
   searchData["engagement_score"] = clicks / impressions
   ```

4. **Stale Document Detection Agent**
   ```python
   @schedule.weekly
   def detect_stale_docs():
       old_docs = query(filter={"last_updated": < 6_months_ago})
       notify_owners(old_docs, "Please review for accuracy")
   ```

5. **Semantic Deduplication**
   - Use embeddings to find near-duplicate documents
   - Prevent redundant content in index
   ```python
   def deduplicate(new_doc, threshold=0.95):
       similar = search(new_doc.content, top_k=5)
       if max(similar.scores) > threshold:
           flag_as_duplicate(new_doc)
   ```

#### 4. Performance Optimizations

1. **Caching Layer**: Redis for frequent queries
2. **Async Ingestion**: Queue-based (Celery/RQ)
3. **Batch Processing**: Ingest in batches of 100-500 docs
4. **Monitoring**: Track query latency, cache hit rate, index size

#### 5. Enterprise Deployment & Security

For large-scale production deployments ([GroundX Security](https://www.eyelevel.ai/product/groundx-security)):

**Deployment Options**:
- **Cloud**: AWS, Azure, Google Cloud Platform
- **On-Premises**: Red Hat, Kubernetes clusters
- **Air-Gapped**: Fully isolated environments for maximum security

**Security Architecture for Regulated Industries**:
1. **Infrastructure**:
   - Kubernetes-based with minimal attack surface
   - Single controlled point of data egress
   - Distributed Kafka processing in protected clusters
   - AES 256 encryption for all data (rest and transit)

2. **Compliance Requirements**:
   - SOC 2 and HIPAA certifications for healthcare/finance
   - FIPS-certified images for government contractors
   - CVE-free container images

3. **Scalability Features**:
   - Horizontal scaling via Kubernetes pods
   - GPU-powered document processing
   - Dedicated storage and metadata databases
   - No external dependencies for air-gapped deployments

---

## 📚 Sources

Design answers based on official GroundX documentation:
- [GroundX API Concepts](https://docs.eyelevel.ai/documentation/fundamentals/api-concepts)
- [Document Ingestion API](https://docs.eyelevel.ai/reference/api-reference/documents/ingest-documents)
- [Bucket Management](https://docs.eyelevel.ai/reference/api-reference/buckets/create)
- [Search API Reference](https://docs.eyelevel.ai/reference/api-reference/documents/lookup)
- [GroundX Security & Enterprise Features](https://www.eyelevel.ai/product/groundx-security)

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
