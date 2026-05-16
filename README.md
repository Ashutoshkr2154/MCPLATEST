<div align="center">

<!-- CAPSULE RENDER HEADER -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f0c29,50:302b63,100:24243e&height=200&section=header&text=google-services-mcp&fontSize=42&fontColor=ffffff&fontAlignY=38&desc=Model%20Context%20Protocol%20Server%20for%20Claude%20Desktop&descAlignY=58&descSize=16&animation=fadeIn" width="100%"/>

<!-- TYPING SVG BANNER -->
<a href="https://github.com/yourusername/google-services-mcp">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=22&duration=3500&pause=800&color=A78BFA&center=true&vCenter=true&multiline=false&width=700&lines=Connect+Claude+to+Your+Entire+Digital+Life;Gmail+%7C+Calendar+%7C+Sheets+%7C+MongoDB+%7C+PostgreSQL;25%2B+MCP+Tools.+One+Server.+Zero+Friction." alt="Typing SVG" />
</a>

<br/>
<br/>

<!-- BADGES -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/MCP-0.9%2B-A78BFA?style=for-the-badge&logo=anthropic&logoColor=white"/>
  <img src="https://img.shields.io/badge/Claude%20Desktop-Compatible-FF6B35?style=for-the-badge&logo=anthropic&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-22c55e?style=for-the-badge"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Google%20Sheets-34A853?style=for-the-badge&logo=googlesheets&logoColor=white"/>
  <img src="https://img.shields.io/badge/Gmail-EA4335?style=for-the-badge&logo=gmail&logoColor=white"/>
  <img src="https://img.shields.io/badge/Google%20Calendar-4285F4?style=for-the-badge&logo=googlecalendar&logoColor=white"/>
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
</p>

<p align="center">
  <img src="https://img.shields.io/github/stars/yourusername/google-services-mcp?style=for-the-badge&color=A78BFA&labelColor=1a1a2e"/>
  <img src="https://img.shields.io/github/forks/yourusername/google-services-mcp?style=for-the-badge&color=818cf8&labelColor=1a1a2e"/>
  <img src="https://img.shields.io/github/issues/yourusername/google-services-mcp?style=for-the-badge&color=f87171&labelColor=1a1a2e"/>
  <img src="https://img.shields.io/github/last-commit/yourusername/google-services-mcp?style=for-the-badge&color=34d399&labelColor=1a1a2e"/>
</p>

<br/>

> **Give Claude Desktop superpowers.** This MCP server bridges Claude to your Google Workspace and databases — enabling natural language control over Gmail, Calendar, Sheets, MongoDB, and PostgreSQL from a single, plug-and-play server.

<br/>

[**Quick Start**](#-quick-start) · [**MCP Tools**](#-mcp-tools-reference) · [**Architecture**](#-architecture) · [**Configuration**](#-configuration) · [**Troubleshooting**](#-troubleshooting)

</div>

---

## ⚡ What Is This?

**google-services-mcp** is a production-grade [Model Context Protocol](https://modelcontextprotocol.io/) server that supercharges Claude Desktop with direct, authenticated access to:

| Service | Capability |
|---|---|
| 📧 **Gmail** | List, read, search, and send emails |
| 📅 **Google Calendar** | Create, update, delete, and query events |
| 📊 **Google Sheets** | Read, write, and append spreadsheet data |
| 🍃 **MongoDB Atlas** | Full CRUD + aggregation pipeline execution |
| 🐘 **PostgreSQL (Neon)** | SELECT, INSERT, UPDATE, DELETE, schema inspection |

Instead of switching between apps, you just **talk to Claude** — and Claude does the work.

```
You:    "Find emails from my manager about the Q3 report, add a task to my spreadsheet,
         and schedule a review meeting for Friday at 2 PM."

Claude: ✅ Found 3 emails  →  ✅ Task added to Sheet1  →  ✅ Event created on Friday
```

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🤖 AI-Native Tool Design
Every tool is engineered with semantic descriptions so Claude selects the right one automatically — no prompt engineering required.

### 🔌 Plug-and-Play Setup
Three config changes and a `python src/setup.py` run is all it takes. Works on Windows, macOS, and Linux.

### 🧩 Modular Architecture
Each service (Gmail, Calendar, Sheets, MongoDB, PostgreSQL) is isolated in its own module. Add or remove integrations without touching the core server.

</td>
<td width="50%">

### 🔁 Autonomous Agent Mode
`agent.py` provides a standalone AI loop that reads emails, infers intent, and autonomously creates calendar events, spreadsheet tasks, and email replies.

### 🛡️ OAuth2 + Token Refresh
Full Google OAuth2 flow with automatic token refresh. Credentials never expire silently.

### 🗄️ Dual Database Support
MongoDB Atlas (document) and Neon PostgreSQL (relational) work simultaneously — query across both from a single Claude conversation.

</td>
</tr>
</table>

---

## 🏗️ Architecture

```mermaid
graph TB
    subgraph Claude["🤖 Claude Desktop"]
        UI["Chat Interface"]
        AI["Claude AI Engine"]
    end

    subgraph MCP["⚡ MCP Layer (stdio / JSON-RPC 2.0)"]
        SERVER["mcp_server.py\n(25+ tools registered)"]
        POSTGRES_MCP["postgres_mcp.py"]
        MONGO_MCP["mongodb_mcp.py"]
    end

    subgraph Google["☁️ Google Workspace"]
        AUTH["google_auth.py\n(OAuth2 + Token Refresh)"]
        SHEETS["google_sheets.py"]
        GMAIL["google_gmail.py"]
        GCAL["google_calendar.py"]
    end

    subgraph Databases["🗄️ Databases"]
        PG["postgres_db.py\n→ Neon PostgreSQL"]
        MONGO["mongodb_db.py\n→ MongoDB Atlas"]
    end

    subgraph Config["⚙️ Configuration"]
        CFG["config.json"]
        CREDS["credentials.json"]
        TOKENS["tokens.json"]
    end

    UI -->|Natural Language| AI
    AI -->|Tool Selection| SERVER
    SERVER -->|stdio JSON-RPC| POSTGRES_MCP
    SERVER -->|stdio JSON-RPC| MONGO_MCP
    SERVER --> AUTH
    AUTH --> SHEETS & GMAIL & GCAL
    SHEETS & GMAIL & GCAL -->|Google APIs| Google
    POSTGRES_MCP --> PG
    MONGO_MCP --> MONGO
    CFG & CREDS & TOKENS --> AUTH
    CFG --> PG & MONGO
```

### Request Lifecycle

```mermaid
sequenceDiagram
    participant U as 👤 User
    participant C as 🤖 Claude Desktop
    participant M as ⚡ mcp_server.py
    participant S as 🔧 Service Module
    participant A as ☁️ External API/DB

    U->>C: "Send John an email about Friday's meeting"
    C->>C: Semantic tool selection → send_email
    C->>M: JSON-RPC: tools/call {name: "send_email", args: {...}}
    M->>S: gmail.send_email(to, subject, body)
    S->>A: Google Gmail API (OAuth2 Bearer token)
    A-->>S: {messageId: "abc123", threadId: "xyz"}
    S-->>M: {success: true, messageId: "abc123"}
    M-->>C: TextContent JSON response
    C-->>U: "Email sent successfully to john@example.com ✅"
```

---

## 📁 Folder Structure

```
google-services-mcp/
│
├── 📄 config.json                  # Active configuration (gitignored)
├── 📄 config.example.json          # Template — safe to commit
├── 📄 credentials.json             # Google OAuth2 client secrets (gitignored)
├── 📄 tokens.json                  # Refreshable OAuth2 access tokens (gitignored)
├── 📄 claude_desktop_config.json   # Claude Desktop MCP registration template
├── 📄 requirements.txt             # Python dependencies
├── 📄 .gitignore
│
├── 📚 HOW_CLAUDE_SELECTS_TOOLS.md  # Deep-dive: MCP tool selection mechanics
├── 📚 MCP_FLOW_EXPLAINED.md        # Full request lifecycle walkthrough
├── 📚 SETUP.md                     # Quick setup guide
│
└── src/
    ├── 🚀 mcp_server.py            # Primary MCP server (25+ tools)
    ├── 🤖 agent.py                 # Autonomous email→action agent
    ├── 🔐 google_auth.py           # OAuth2 authentication manager
    ├── 📊 google_sheets.py         # Sheets API wrapper
    ├── 📧 google_gmail.py          # Gmail API wrapper
    ├── 📅 google_calendar.py       # Calendar API wrapper
    ├── 🐘 postgres_db.py           # PostgreSQL query engine
    ├── 🐘 postgres_mcp.py          # PostgreSQL standalone MCP server
    ├── 🍃 mongodb_db.py            # MongoDB operations engine
    ├── 🍃 mongodb_mcp.py           # MongoDB standalone MCP server
    ├── ⚙️  setup.py                # Interactive setup wizard
    └── __init__.py
```

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|---|---|---|
| **Protocol** | `mcp >= 0.9.0` | Model Context Protocol (stdio transport) |
| **Language** | Python 3.10+ | Core runtime |
| **Google Auth** | `google-auth-oauthlib`, `google-auth-httplib2` | OAuth2 flow + token management |
| **Google APIs** | `google-api-python-client` | Sheets, Gmail, Calendar |
| **PostgreSQL** | `psycopg2-binary` | Neon (or any PG) connection |
| **MongoDB** | `pymongo`, `bson` | Atlas connection + BSON serialization |
| **Transport** | stdio (JSON-RPC 2.0) | Claude Desktop ↔ MCP Server |
| **Config** | JSON | `config.json`, `credentials.json`, `tokens.json` |

</div>

---

## 📦 Installation

### Prerequisites

- Python **3.10+**
- [Claude Desktop](https://claude.ai/download) installed
- A [Google Cloud Console](https://console.cloud.google.com) project with OAuth2 credentials
- *(Optional)* A MongoDB Atlas cluster URI
- *(Optional)* A PostgreSQL connection URL (Neon recommended)

### Step 1 — Clone the Repository

```bash
git clone https://github.com/yourusername/google-services-mcp.git
cd google-services-mcp
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary>📋 Full dependency list</summary>

```
mcp>=0.9.0
google-api-python-client>=2.100.0
google-auth-httplib2>=0.2.0
google-auth-oauthlib>=1.2.0
python-dotenv>=1.0.0
psycopg2-binary>=2.9.0
pymongo>=4.6.0
```

</details>

### Step 3 — Configure Google OAuth2

1. Go to [Google Cloud Console → APIs & Services → Credentials](https://console.cloud.google.com/apis/credentials)
2. Create an **OAuth 2.0 Client ID** (Desktop application)
3. Download the JSON file and save it as **`credentials.json`** in the project root
4. Enable these APIs in your Google Cloud project:
   - Google Sheets API
   - Gmail API
   - Google Calendar API

### Step 4 — Run the Setup Wizard

```bash
python src/setup.py
```

The wizard will:
- Guide you through the Google OAuth2 browser flow
- Save tokens to `tokens.json`
- Prompt for your Spreadsheet ID and Calendar ID
- Write your configuration to `config.json`

### Step 5 — Register with Claude Desktop

Find your Claude Desktop config file:

| OS | Path |
|---|---|
| **Windows** | `%APPDATA%\Claude\claude_desktop_config.json` |
| **macOS** | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| **Linux** | `~/.config/Claude/claude_desktop_config.json` |

Add the following (update paths to match your system):

```json
{
  "mcpServers": {
    "google-services": {
      "command": "python",
      "args": ["/absolute/path/to/google-services-mcp/src/mcp_server.py"],
      "env": {}
    },
    "postgresql-db": {
      "command": "python",
      "args": ["/absolute/path/to/google-services-mcp/src/postgres_mcp.py"],
      "env": {}
    },
    "mongodb": {
      "command": "python",
      "args": ["/absolute/path/to/google-services-mcp/src/mongodb_mcp.py"],
      "env": {}
    }
  }
}
```

> **Windows users:** Use double backslashes: `"C:\\Users\\you\\google-services-mcp\\src\\mcp_server.py"`

### Step 6 — Restart Claude Desktop

Fully quit and relaunch Claude Desktop. Ask:

```
"What tools do you have access to?"
```

Claude should list 25+ tools across Gmail, Calendar, Sheets, MongoDB, and PostgreSQL.

---

## ⚙️ Configuration

### `config.json` Reference

```json
{
  "google": {
    "clientId": "your-client-id.apps.googleusercontent.com",
    "clientSecret": "your-client-secret",
    "redirectUri": "http://localhost",
    "spreadsheetId": "your-default-spreadsheet-id",
    "calendarId": "primary"
  },
  "database": {
    "url": "postgresql://user:password@host/dbname?sslmode=require"
  },
  "mongodb": {
    "uri": "mongodb+srv://user:password@cluster.mongodb.net/?appName=YourApp"
  }
}
```

| Key | Description | Required |
|---|---|---|
| `google.clientId` | OAuth2 Client ID from Google Cloud | ✅ For Google tools |
| `google.clientSecret` | OAuth2 Client Secret | ✅ For Google tools |
| `google.spreadsheetId` | Default Google Spreadsheet ID | ⚠️ Optional (can pass per-call) |
| `google.calendarId` | Default calendar (`primary` for main) | ⚠️ Optional |
| `database.url` | Full PostgreSQL connection URL | ⚠️ For PostgreSQL tools |
| `mongodb.uri` | MongoDB Atlas connection string | ⚠️ For MongoDB tools |

> 🔒 **Security:** Never commit `config.json`, `credentials.json`, or `tokens.json` to version control. They are pre-listed in `.gitignore`.

---

## 🚀 Quick Start

Once Claude Desktop is running with the MCP server registered, try these prompts:

### 📧 Gmail
```
"Show me my last 5 unread emails"
"Search for emails from sarah@company.com this week"
"Send an email to team@company.com with subject 'Sprint Review' and body 'Meeting at 3 PM Friday'"
```

### 📅 Google Calendar
```
"What events do I have this week?"
"Create a meeting called 'Product Sync' on Thursday at 2 PM for 1 hour"
"Cancel the event with ID abc123xyz"
```

### 📊 Google Sheets
```
"Read cells A1 to D10 from spreadsheet 1BxiMVs0XRA..."
"Write 'Done' to cell B5 in my spreadsheet"
"Append a new row with today's date, 'Task completed', and 'John' to Sheet1"
```

### 🍃 MongoDB
```
"List all my MongoDB databases"
"Find the first 10 documents in the users collection where status is active"
"Count orders placed in the last 30 days"
"Run this aggregation: group orders by status and count each"
```

### 🐘 PostgreSQL
```
"Show me all tables in the database"
"How many users are in the users table?"
"Describe the schema of the orders table"
"Run: SELECT name, email FROM users WHERE created_at > '2024-01-01' LIMIT 20"
```

---

## 🧰 MCP Tools Reference

### 📊 Google Sheets (4 Tools)

| Tool | Description | Required Args |
|---|---|---|
| `read_sheet` | Read data from a range | `spreadsheetId`, `range` |
| `write_sheet` | Write a 2D array to a range | `spreadsheetId`, `range`, `values` |
| `append_sheet` | Append rows to a sheet | `spreadsheetId`, `range`, `values` |
| `get_sheet_info` | Get spreadsheet metadata | `spreadsheetId` |

### 📧 Gmail (4 Tools)

| Tool | Description | Required Args |
|---|---|---|
| `list_emails` | List inbox emails with optional query | *(none required)* |
| `get_email_detail` | Get full email content | `messageId` |
| `send_email` | Send an email (plain or HTML) | `to`, `subject`, `body` |
| `search_emails` | Search with Gmail query syntax | `query` |

### 📅 Google Calendar (5 Tools)

| Tool | Description | Required Args |
|---|---|---|
| `list_calendar_events` | List upcoming events | *(none required)* |
| `create_calendar_event` | Create a new event | `summary`, `start`, `end` |
| `update_calendar_event` | Modify an existing event | `eventId` |
| `delete_calendar_event` | Remove an event | `eventId` |
| `get_calendar_event` | Get event details | `eventId` |

### 🍃 MongoDB (8 Tools)

| Tool | Description | Required Args |
|---|---|---|
| `mongo_list_databases` | List all databases | *(none)* |
| `mongo_list_collections` | List collections in a database | `database_name` |
| `mongo_find_documents` | Query with filter, limit, skip | `database_name`, `collection_name` |
| `mongo_insert_document` | Insert a single document | `database_name`, `collection_name`, `document` |
| `mongo_update_document` | Update matching documents | `database_name`, `collection_name`, `filter_query`, `update_data` |
| `mongo_delete_document` | Delete matching documents | `database_name`, `collection_name`, `filter_query` |
| `mongo_count_documents` | Count with optional filter | `database_name`, `collection_name` |
| `mongo_aggregate` | Run aggregation pipeline | `database_name`, `collection_name`, `pipeline` |

### 🐘 PostgreSQL (6 Tools)

| Tool | Description | Required Args |
|---|---|---|
| `pg_list_tables` | List all tables | *(none)* |
| `pg_execute_query` | Run a SELECT query | `query` |
| `pg_execute_write` | Run INSERT/UPDATE/DELETE | `query` |
| `pg_describe_table` | Get column schema | `table_name` |
| `pg_get_table_count` | Count rows in a table | `table_name` |
| `pg_run_custom_sql` | Auto-detect SELECT vs write | `sql` |

---

## 🤖 Autonomous Agent Mode

`agent.py` is a standalone decision-making loop that operates independently of Claude Desktop. It:

1. **Fetches** your last 10 inbox emails via Gmail
2. **Analyzes** email subjects and bodies for intent signals
3. **Routes** each email to an appropriate action:

```mermaid
flowchart TD
    A[📥 Fetch 10 Inbox Emails] --> B{Analyze Each Email}
    B -->|'meeting', 'schedule'| C[📅 Check Calendar]
    B -->|'task', 'todo', 'please add'| D[📋 Append to Google Sheet]
    B -->|'urgent' in sender/subject| E[🚨 Mark as Priority Task]
    C -->|Has date + time info| F[📅 Create Calendar Event]
    D --> G[📧 Send Confirmation Reply]
    E --> D
    F --> G
    G --> H[✅ Done]
```

**Run the agent:**

```bash
python src/agent.py
```

**Example output:**
```
Initializing MCP Client...
Fetching available tools...
Connected. Available tools: 27

Step 1: Checking emails...
Found 10 emails

Step 2: Analyzing emails for actions...
Identified 3 potential actions

Step 3: Processing decisions...
Processing: Email mentions meeting - checking calendar
  → Creating calendar event: "Q3 Review Meeting" on 2024-01-25 10:00 AM

Processing: Email mentions task - adding to sheet
  → Task added to spreadsheet successfully
  → Email reply sent to sender@company.com

Step 4: Checking calendar status...
Calendar has 5 upcoming events

Automatic decision-making process completed
```

---

## 🔐 Authentication Deep Dive

The auth system (`google_auth.py`) implements a full OAuth2 lifecycle:

```mermaid
flowchart LR
    A[App Start] --> B{tokens.json exists?}
    B -->|Yes| C{Token valid?}
    B -->|No| D[Open Browser OAuth Flow]
    C -->|Yes| G[✅ Authenticated]
    C -->|Expired| E[Auto Refresh Token]
    E --> G
    D --> F[User Authorizes in Browser]
    F --> G
    G --> H[Save tokens.json]
```

**Google OAuth2 Scopes requested:**

| Scope | Access Level |
|---|---|
| `spreadsheets` | Read + Write Google Sheets |
| `gmail.readonly` | Read emails |
| `gmail.send` | Send emails |
| `calendar` | Full Calendar read/write |

---

## 🔒 Security

> ⚠️ **Critical:** The following files contain sensitive credentials and **must never be committed to version control.**

| File | Contains | Action |
|---|---|---|
| `config.json` | OAuth secrets, DB connection strings | ✅ In `.gitignore` |
| `credentials.json` | Google OAuth2 client credentials | ✅ In `.gitignore` |
| `tokens.json` | Live access + refresh tokens | ✅ In `.gitignore` |

**Best Practices:**

- Store secrets in environment variables for production deployments
- Rotate your Google OAuth2 client secret periodically
- Use IAM roles with minimum required permissions for MongoDB Atlas and PostgreSQL
- For Neon PostgreSQL: use branch-specific credentials, not the root user
- Enable `sslmode=require` (already the default in this project)
- Never log the contents of `config.json` or `tokens.json`

---

## 🧪 Usage Examples

### Multi-Step Workflow (Single Prompt)

```
You: "Check my emails for anything from the design team, create calendar events 
      for any mentioned meetings, and add all action items to my spreadsheet."

Claude:
  1. list_emails(query="from:design team")     → 3 emails found
  2. create_calendar_event("Design Review")     → Event created: Thu 3 PM
  3. append_sheet([[date, task, source, status]]) → 2 tasks logged
```

### Database Query Chain

```
You: "Count users in Postgres and compare with MongoDB customers collection"

Claude:
  1. pg_execute_query("SELECT COUNT(*) FROM users") → 1,247 users
  2. mongo_count_documents("mydb", "customers")     → 1,189 customers
  → "PostgreSQL has 1,247 users vs 1,189 MongoDB customers (58 difference)"
```

### Smart Email + Sheet Integration

```
You: "Find all emails with invoices and log the sender and subject to Sheet1"

Claude:
  1. search_emails("invoice")          → 7 emails found
  2. get_email_detail(id) × 7          → Extract sender + subject
  3. append_sheet(rows) → 7 rows added to Sheet1
```

---

## 🔧 How Claude Selects Tools

Claude uses **semantic matching** — not hardcoded routing — to select the right tool. The `description` field on each `Tool` object is what Claude reads.

```python
# This description is what Claude's AI sees and matches against your words
Tool(
    name="send_email",
    description="Send an email via Gmail",   # ← Claude matches user intent here
    inputSchema={...}
)
```

**Matching examples:**

| You say | Claude selects |
|---|---|
| "Give me all the tables" | `pg_list_tables` |
| "Show me users table structure" | `pg_describe_table(table_name="users")` |
| "How many users are there?" | `pg_execute_query("SELECT COUNT(*) FROM users")` |
| "Find emails about project alpha" | `search_emails(query="project alpha")` |
| "Add a new document to the orders collection" | `mongo_insert_document(...)` |

See [`HOW_CLAUDE_SELECTS_TOOLS.md`](HOW_CLAUDE_SELECTS_TOOLS.md) for the complete semantic matching breakdown.

---

## 🚧 Troubleshooting

<details>
<summary><strong>❌ Tools not appearing in Claude Desktop</strong></summary>

1. Verify your absolute path in `claude_desktop_config.json` — it must be exact
2. On Windows, escape backslashes: `"C:\\Users\\you\\project\\src\\mcp_server.py"`
3. Test the server runs standalone: `python src/mcp_server.py` (should block without error)
4. Fully quit Claude Desktop (not just close window) and relaunch
5. Check Claude Desktop logs (Help → Open Logs)

</details>

<details>
<summary><strong>❌ Google authentication fails</strong></summary>

1. Ensure `credentials.json` is in the project **root** (not `src/`)
2. Re-run `python src/setup.py` to regenerate `tokens.json`
3. Verify these APIs are enabled in Google Cloud Console:
   - Google Sheets API
   - Gmail API
   - Google Calendar API
4. Check that your OAuth2 app is not in "Testing" mode with restricted testers

</details>

<details>
<summary><strong>❌ PostgreSQL connection error</strong></summary>

1. Verify `database.url` in `config.json` is correct
2. Ensure `sslmode=require` is in the connection string for Neon
3. Test connectivity: `python -c "import psycopg2; psycopg2.connect('your-url')"`
4. Check that your IP is allowlisted in Neon's dashboard

</details>

<details>
<summary><strong>❌ MongoDB connection error</strong></summary>

1. Verify `mongodb.uri` in `config.json` includes `?appName=YourApp`
2. Ensure your IP address is in MongoDB Atlas → Network Access → IP Allowlist
3. Test: `python -c "from pymongo import MongoClient; MongoClient('your-uri').admin.command('ping')"`

</details>

<details>
<summary><strong>❌ "Python not found" on Windows</strong></summary>

Use the full path to your Python executable:

```json
{
  "mcpServers": {
    "google-services": {
      "command": "C:\\Python312\\python.exe",
      "args": ["C:\\path\\to\\src\\mcp_server.py"]
    }
  }
}
```

</details>

---

## ❓ FAQ

**Q: Can I use this without MongoDB or PostgreSQL?**
> Yes. The server gracefully returns an error message if those URIs aren't configured. Google tools work independently.

**Q: Does this work with Claude.ai (web) or only Claude Desktop?**
> Currently, MCP via stdio is a Claude Desktop feature. Claude.ai (web) does not support local MCP servers.

**Q: Can I run multiple MCP servers simultaneously?**
> Yes — this is the recommended approach. The `claude_desktop_config.json` shows three servers registered at once: `google-services`, `postgresql-db`, and `mongodb`.

**Q: Are my emails/data sent to Anthropic?**
> Tool results are passed to Claude's context window for the current conversation. Anthropic's standard data handling policies apply. No data is permanently stored by the MCP server itself.

**Q: Can I add more Google services (Drive, Docs, etc.)?**
> Absolutely. Add a new module in `src/`, register new `Tool` objects in `mcp_server.py`, and add the corresponding OAuth scope to `SCOPES` in `google_auth.py`.

**Q: Is `agent.py` the same as the MCP server?**
> No. `agent.py` is a standalone script that uses an MCP client to call the server programmatically. The MCP server (`mcp_server.py`) is what Claude Desktop connects to via stdio.

---

## 🗺️ Roadmap

| Status | Feature |
|---|---|
| ✅ Done | Gmail read/send/search |
| ✅ Done | Google Calendar CRUD |
| ✅ Done | Google Sheets read/write/append |
| ✅ Done | MongoDB Atlas full CRUD + aggregation |
| ✅ Done | PostgreSQL full CRUD + schema inspection |
| ✅ Done | Autonomous email agent |
| 🔜 Planned | Google Drive integration (list, read, upload) |
| 🔜 Planned | Google Docs read/write |
| 🔜 Planned | Slack integration |
| 🔜 Planned | Docker + docker-compose setup |
| 🔜 Planned | Web-based OAuth setup UI |
| 🔜 Planned | Environment variable support (no `config.json`) |
| 🔜 Planned | GitHub Actions CI for automated testing |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get involved:

```bash
# 1. Fork the repository and clone your fork
git clone https://github.com/yourusername/google-services-mcp.git
cd google-services-mcp

# 2. Create a feature branch
git checkout -b feat/google-drive-integration

# 3. Make your changes and test locally
python src/mcp_server.py  # Should start without errors

# 4. Commit with a clear message
git commit -m "feat: add Google Drive list_files and download_file tools"

# 5. Push and open a Pull Request
git push origin feat/google-drive-integration
```

**Contribution Guidelines:**
- Follow the existing module pattern: `service_db.py` (logic) + `service_mcp.py` (MCP wrapper) or integrate into `mcp_server.py`
- Write descriptive `Tool.description` values — Claude depends on them for tool selection
- Return consistent `{"success": bool, ...}` response shapes
- Never commit `config.json`, `credentials.json`, or `tokens.json`

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full terms.

```
MIT License — free to use, modify, and distribute with attribution.
```

---

## 🙏 Acknowledgements

<div align="center">

| Project | Role |
|---|---|
| [Anthropic MCP](https://modelcontextprotocol.io/) | The protocol that makes this possible |
| [Claude Desktop](https://claude.ai/download) | The AI client |
| [Google APIs Python Client](https://github.com/googleapis/google-api-python-client) | Google Workspace integration |
| [psycopg2](https://www.psycopg.org/) | PostgreSQL adapter |
| [PyMongo](https://pymongo.readthedocs.io/) | MongoDB driver |
| [Neon](https://neon.tech/) | Serverless PostgreSQL hosting |
| [MongoDB Atlas](https://www.mongodb.com/atlas) | Managed MongoDB hosting |

</div>

---

<div align="center">

<!-- FOOTER WAVE -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:24243e,50:302b63,100:0f0c29&height=120&section=footer" width="100%"/>

**Built with ❤️ for the Claude + MCP community**

<br/>

<img src="https://img.shields.io/badge/Made%20with-Python-3776AB?style=flat-square&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Powered%20by-Claude-FF6B35?style=flat-square&logo=anthropic&logoColor=white"/>
<img src="https://img.shields.io/badge/Protocol-MCP-A78BFA?style=flat-square"/>

<br/><br/>

⭐ **Star this repo if it saved you time** · 🐛 **[Report a Bug](https://github.com/yourusername/google-services-mcp/issues)** · 💡 **[Request a Feature](https://github.com/yourusername/google-services-mcp/issues)**

</div>