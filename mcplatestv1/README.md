<div align="center">

```
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     ██████╗ ██████╗  ██████╗  ██████╗ ██╗     ███████╗     ║
║    ██╔════╝██╔════╝ ██╔═══██╗██╔════╝ ██║     ██╔════╝     ║
║    ██║  ███╗██║  ███╗██║   ██║██║  ███╗██║     █████╗       ║
║    ██║   ██║██║   ██║██║   ██║██║   ██║██║     ██╔══╝       ║
║    ╚██████╔╝╚██████╔╝╚██████╔╝╚██████╔╝███████╗███████╗     ║
║     ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝╚══════╝╚══════╝     ║
║                                                              ║
║            S E R V I C E S   M C P   S E R V E R            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

### 🤖 Give Claude superpowers over your Google Workspace & Databases

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/Protocol-MCP-blueviolet?style=for-the-badge)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-Desktop-D97757?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

> *"Talk to your data. Let Claude do the heavy lifting."*

</div>

---

## 🌐 What is This?

This is a local **MCP (Model Context Protocol) server** that bridges **Claude Desktop** with your real-world services — Google Sheets, Gmail, Google Calendar, and PostgreSQL. Once running, Claude can read, write, query, and act across all of them in a single natural-language conversation.

No switching tabs. No copy-pasting. No API wrangling by hand. Just ask Claude.

---

## ✨ Capabilities at a Glance

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   📊 Google Sheets   →   Read, write, append, inspect           │
│   📧 Gmail           →   List, search, read, send               │
│   📅 Google Calendar →   List, create, update, delete events    │
│   🐘 PostgreSQL      →   Query, write, inspect, custom SQL      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Architecture Overview

```
┌─────────────────────┐         stdio          ┌────────────────────────┐
│                     │ ◄────────────────────► │                        │
│   Claude Desktop    │                        │   mcp_server.py        │
│   (MCP Client)      │    JSON-RPC over pipe  │   (MCP Server)         │
│                     │ ◄────────────────────► │                        │
└─────────────────────┘                        └──────────┬─────────────┘
                                                          │
                              ┌───────────────────────────┼────────────────────────┐
                              │                           │                        │
                   ┌──────────▼──────────┐   ┌───────────▼────────┐  ┌────────────▼──────────┐
                   │  Google APIs        │   │  PostgreSQL         │  │  google_auth.py        │
                   │  ─────────────────  │   │  ────────────────── │  │  ──────────────────── │
                   │  Sheets  ✅         │   │  pg_list_tables ✅   │  │  OAuth 2.0 tokens      │
                   │  Gmail   ✅         │   │  pg_execute_*   ✅   │  │  credentials.json      │
                   │  Calendar✅         │   │  pg_describe_*  ✅   │  │  tokens.json           │
                   └─────────────────────┘   └────────────────────┘  └───────────────────────┘
```

---

## 🛠️ Tools Reference (27 tools)

<details>
<summary><b>📊 Google Sheets — 4 tools</b></summary>

| Tool | What it does | Required params |
|------|-------------|-----------------|
| `read_sheet` | Read data from any cell range | `spreadsheetId`, `range` |
| `write_sheet` | Write a 2D array of values | `spreadsheetId`, `range`, `values` |
| `append_sheet` | Append rows to the bottom | `spreadsheetId`, `range`, `values` |
| `get_sheet_info` | Get sheet names, row counts, metadata | `spreadsheetId` |

**Example prompts:**
```
"Read Sheet1!A1:D20 from my spreadsheet"
"Write [['Name','Score'],['Alice','95']] to Sheet2!A1"
"Append a new row with today's date and total sales"
```

</details>

<details>
<summary><b>📧 Gmail — 4 tools</b></summary>

| Tool | What it does | Required params |
|------|-------------|-----------------|
| `list_emails` | List recent emails with optional filter | — |
| `get_email_detail` | Get full content of an email | `messageId` |
| `send_email` | Send plain text or HTML email | `to`, `subject`, `body` |
| `search_emails` | Search using Gmail query syntax | `query` |

**Example prompts:**
```
"Show me my last 5 unread emails"
"Search for emails from boss@company.com this week"
"Send an email to team@company.com — subject: Update, body: Done!"
```

</details>

<details>
<summary><b>📅 Google Calendar — 5 tools</b></summary>

| Tool | What it does | Required params |
|------|-------------|-----------------|
| `list_calendar_events` | List upcoming events | — |
| `create_calendar_event` | Create event with title, time, location, attendees | `summary`, `start`, `end` |
| `update_calendar_event` | Modify an existing event | `eventId` |
| `delete_calendar_event` | Remove an event | `eventId` |
| `get_calendar_event` | Get full details of one event | `eventId` |

**Example prompts:**
```
"What's on my calendar this week?"
"Create a meeting called 'Sprint Review' tomorrow at 2pm for 1 hour"
"Add john@work.com as an attendee to my 3pm event"
```

</details>

<details>
<summary><b>🐘 PostgreSQL — 6 tools</b></summary>

| Tool | What it does | Required params |
|------|-------------|-----------------|
| `pg_list_tables` | List all tables in the connected DB | — |
| `pg_execute_query` | Run a SELECT query | `query` |
| `pg_execute_write` | Run INSERT / UPDATE / DELETE | `query` |
| `pg_describe_table` | Get column names, types, constraints | `table_name` |
| `pg_get_table_count` | Row count for a table | `table_name` |
| `pg_run_custom_sql` | Any SQL — auto-detects read vs write | `sql` |

**Example prompts:**
```
"List all tables in my database"
"Show me the 10 most recent orders from the orders table"
"How many users signed up this month?"
"Update the status to 'shipped' for order ID 4821"
```

</details>

---

## 📋 Prerequisites

Before you begin, make sure you have:

- [x] **Windows 10 / 11**
- [x] **Python 3.10** installed and on PATH
- [x] **Claude Desktop** installed
- [x] **Google Cloud Project** with these APIs enabled:
  - Google Sheets API
  - Gmail API
  - Google Calendar API
- [x] **`credentials.json`** downloaded from [Google Cloud Console](https://console.cloud.google.com/)
- [x] **PostgreSQL** running (local or remote)

---

## 🚀 Installation & Setup

### Step 1 — Clone & Enter the Project

```bash
git clone <your-repo-url>
cd mcplatestv1
```

### Step 2 — Create & Activate Virtual Environment

```bash
# Create
python -m venv mcpenv

# Activate (Windows)
mcpenv\Scripts\activate

# You should see (mcpenv) in your terminal prompt
```

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Add Google Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **APIs & Services → Credentials**
3. Create **OAuth 2.0 Client ID** (type: Desktop App)
4. Click **Download JSON** and save it as `credentials.json` in the project root

### Step 5 — Authenticate with Google

```bash
python src/setup.py
```

A browser window will open. Sign in and authorize all three scopes (Sheets, Gmail, Calendar). This generates `tokens.json` — **do not delete it**.

> 💡 If your token ever expires, just re-run `python src/setup.py`

### Step 6 — Configure `config.json`

Copy the example config and fill in your details:

```bash
copy config.example.json config.json
```

```json
{
  "google": {
    "clientId": "your-client-id-here",
    "clientSecret": "your-client-secret-here",
    "redirectUri": "http://localhost",
    "spreadsheetId": "optional-default-spreadsheet-id",
    "calendarId": "primary"
  },
  "database": {
    "url": "postgresql://username:password@localhost:5432/your_database"
  }
}
```

> `spreadsheetId` and `calendarId` are optional defaults — you can pass them directly in any tool call.

---

## 🖥️ Claude Desktop Integration

### Locate the Config File

```
C:\Users\<YourName>\AppData\Roaming\Claude\claude_desktop_config.json
```

> 💡 Shortcut: Press `Win + R`, type `%APPDATA%\Claude`, hit Enter

### Edit the Config

Open the file in any text editor and add:

```json
{
  "mcpServers": {
    "google-services": {
      "command": "D:\\mcplatestv1\\mcpenv\\Scripts\\python.exe",
      "args": [
        "D:\\mcplatestv1\\src\\mcp_server.py"
      ],
      "env": {}
    }
  }
}
```

> ⚠️ Use **double backslashes** (`\\`) in all Windows paths.
> ⚠️ Use the **full path** to `python.exe` inside your `mcpenv` — not the system Python.

### Restart Claude Desktop

```
Fully quit Claude Desktop → Relaunch it
(Don't just close the window — right-click the tray icon → Quit)
```

### Verify Connection

Ask Claude: **"What tools do you have available?"**

You should see all 27 tools listed across Sheets, Gmail, Calendar, and PostgreSQL.

---

## 📁 Project Structure

```
mcplatestv1/
│
├── 📂 src/
│   ├── 🔧 mcp_server.py          ← Main server entry point (run this)
│   ├── 🔐 google_auth.py          ← OAuth 2.0 token management
│   ├── 📊 google_sheets.py        ← Sheets API functions
│   ├── 📧 google_gmail.py         ← Gmail API functions
│   ├── 📅 google_calendar.py      ← Calendar API functions
│   ├── 🐘 postgres_db.py          ← PostgreSQL query functions
│   ├── 🤖 agent.py                ← Tool routing / decision logic
│   └── ⚙️  setup.py               ← First-time Google auth script
│
├── 🔒 config.json                 ← Your credentials (git-ignored)
├── 📄 config.example.json         ← Template — copy this to config.json
├── 🔑 credentials.json            ← From Google Cloud Console (git-ignored)
├── 🎫 tokens.json                 ← Generated by setup.py (git-ignored)
├── 📦 requirements.txt            ← Python dependencies
├── 🖥️  claude_desktop_config.json ← Example Claude Desktop config snippet
└── 📖 README.md                   ← You are here
```

---

## 🔒 Security

The following files contain sensitive credentials. They are already in `.gitignore` — **never commit them**.

```
⛔  credentials.json    →  Google OAuth client credentials
⛔  tokens.json         →  Your personal auth tokens
⛔  config.json         →  Database URLs and client secrets
```

---

## 🩺 Troubleshooting

<details>
<summary><b>❌ Tools not appearing in Claude Desktop</b></summary>

1. **Fully quit Claude Desktop** — right-click tray icon → Quit (don't just close the window)
2. Relaunch and check again
3. Test the server manually:
   ```bash
   D:\mcplatestv1\mcpenv\Scripts\python.exe src/mcp_server.py
   ```
   If it crashes, you'll see the error here.
4. Double-check paths in `claude_desktop_config.json` — both the `command` and `args` must use absolute paths with `\\`

</details>

<details>
<summary><b>❌ Google authentication errors</b></summary>

1. Re-run the auth script:
   ```bash
   python src/setup.py
   ```
2. Make sure all three APIs are enabled in your Google Cloud Console:
   - Google Sheets API
   - Gmail API
   - Google Calendar API
3. Check that `credentials.json` is in the **project root**, not inside `src/`

</details>

<details>
<summary><b>❌ PostgreSQL connection errors</b></summary>

1. Check your connection string in `config.json`:
   ```
   postgresql://username:password@localhost:5432/database_name
   ```
2. Make sure your PostgreSQL service is running:
   ```bash
   # Check in Windows Services or run:
   pg_isready -h localhost -p 5432
   ```
3. Verify the database name and user credentials are correct

</details>

<details>
<summary><b>❌ Python not found or wrong version</b></summary>

Always use the full path to the venv Python in your Claude Desktop config:
```json
"command": "D:\\mcplatestv1\\mcpenv\\Scripts\\python.exe"
```
Never rely on `"command": "python"` — Claude Desktop may not inherit your PATH.

</details>

---

## 💡 Example Conversations with Claude

Once everything is running, here are some things you can ask:

```
📊 Sheets
  → "Read my budget spreadsheet Sheet1!A1:E50 and summarize expenses by category"
  → "Write a header row [Date, Amount, Category] to Sheet1!A1"

📧 Gmail
  → "Search for emails with subject containing 'invoice' from last month"
  → "Send a follow-up email to client@email.com about the proposal"

📅 Calendar
  → "What meetings do I have tomorrow?"
  → "Block 9am–11am this Friday as 'Deep Work' with no attendees"

🐘 PostgreSQL
  → "How many rows are in the users table?"
  → "Show me all orders where status = 'pending' placed in the last 7 days"
  → "What columns does the products table have?"
```

---

<div align="center">

```
╔══════════════════════════════════════╗
║   Built for personal use             ║
║   Windows · Python 3.10 · MCP        ║
║   Keep credentials.json private ⚠️   ║
╚══════════════════════════════════════╝
```

*Made with ☕ and too many API calls*

</div>