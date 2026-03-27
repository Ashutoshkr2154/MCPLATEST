#!/usr/bin/env python3
"""
Pure MCP Server - Standard Implementation
Works with any MCP client via stdio
Includes: Google Sheets, Gmail, Google Calendar, MongoDB, PostgreSQL
"""

import sys
import json
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp.server import Server
from mcp.types import Tool, TextContent
import src.google_sheets as sheets
import src.google_gmail as gmail
import src.google_calendar as calendar
import src.mongodb_db as mongo
import src.postgres_db as db

def load_config():
    try:
        config_path = Path(__file__).parent.parent / 'config.json'
        with open(config_path, 'r') as f:
            return json.load(f)
    except:
        return {'google': {}, 'mongodb': {}, 'database': {}}

config = load_config()

server = Server("google-services-mcp-server")

@server.list_tools()
async def list_tools():
    return [

        # ─────────────────────────────────────────
        # GOOGLE SHEETS TOOLS
        # ─────────────────────────────────────────
        Tool(
            name="read_sheet",
            description="Read data from a Google Sheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheetId": {"type": "string", "description": "The ID of the spreadsheet"},
                    "range": {"type": "string", "description": "The range to read (e.g., 'Sheet1!A1:B10')"}
                },
                "required": ["spreadsheetId", "range"]
            }
        ),
        Tool(
            name="write_sheet",
            description="Write data to a Google Sheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheetId": {"type": "string"},
                    "range": {"type": "string"},
                    "values": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "string"}},
                        "description": "2D array of values to write"
                    }
                },
                "required": ["spreadsheetId", "range", "values"]
            }
        ),
        Tool(
            name="append_sheet",
            description="Append data to a Google Sheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheetId": {"type": "string"},
                    "range": {"type": "string"},
                    "values": {
                        "type": "array",
                        "items": {"type": "array", "items": {"type": "string"}}
                    }
                },
                "required": ["spreadsheetId", "range", "values"]
            }
        ),
        Tool(
            name="get_sheet_info",
            description="Get information about a Google Sheet",
            inputSchema={
                "type": "object",
                "properties": {
                    "spreadsheetId": {"type": "string"}
                },
                "required": ["spreadsheetId"]
            }
        ),

        # ─────────────────────────────────────────
        # GMAIL TOOLS
        # ─────────────────────────────────────────
        Tool(
            name="list_emails",
            description="List emails from Gmail",
            inputSchema={
                "type": "object",
                "properties": {
                    "maxResults": {"type": "integer", "description": "Maximum number of emails", "default": 10},
                    "query": {"type": "string", "description": "Gmail search query", "default": ""}
                }
            }
        ),
        Tool(
            name="get_email_detail",
            description="Get detailed information about a specific email",
            inputSchema={
                "type": "object",
                "properties": {
                    "messageId": {"type": "string", "description": "The Gmail message ID"}
                },
                "required": ["messageId"]
            }
        ),
        Tool(
            name="send_email",
            description="Send an email via Gmail",
            inputSchema={
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "Recipient email address"},
                    "subject": {"type": "string", "description": "Email subject"},
                    "body": {"type": "string", "description": "Email body content"},
                    "isHtml": {"type": "boolean", "description": "Whether the body is HTML", "default": False}
                },
                "required": ["to", "subject", "body"]
            }
        ),
        Tool(
            name="search_emails",
            description="Search emails in Gmail",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Gmail search query"}
                },
                "required": ["query"]
            }
        ),

        # ─────────────────────────────────────────
        # GOOGLE CALENDAR TOOLS
        # ─────────────────────────────────────────
        Tool(
            name="list_calendar_events",
            description="List upcoming calendar events",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendarId": {"type": "string", "default": "primary"},
                    "maxResults": {"type": "integer", "default": 10},
                    "timeMin": {"type": "string", "description": "Minimum time (ISO 8601 format)"}
                }
            }
        ),
        Tool(
            name="create_calendar_event",
            description="Create a new calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendarId": {"type": "string", "default": "primary"},
                    "summary": {"type": "string", "description": "Event title"},
                    "description": {"type": "string"},
                    "start": {"type": "string", "description": "Start time (ISO 8601)"},
                    "end": {"type": "string", "description": "End time (ISO 8601)"},
                    "location": {"type": "string"},
                    "attendees": {"type": "array", "items": {"type": "string"}},
                    "timeZone": {"type": "string", "default": "America/Los_Angeles"}
                },
                "required": ["summary", "start", "end"]
            }
        ),
        Tool(
            name="update_calendar_event",
            description="Update an existing calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendarId": {"type": "string", "default": "primary"},
                    "eventId": {"type": "string"},
                    "summary": {"type": "string"},
                    "description": {"type": "string"},
                    "start": {"type": "string"},
                    "end": {"type": "string"},
                    "location": {"type": "string"},
                    "attendees": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["eventId"]
            }
        ),
        Tool(
            name="delete_calendar_event",
            description="Delete a calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendarId": {"type": "string", "default": "primary"},
                    "eventId": {"type": "string"}
                },
                "required": ["eventId"]
            }
        ),
        Tool(
            name="get_calendar_event",
            description="Get details of a specific calendar event",
            inputSchema={
                "type": "object",
                "properties": {
                    "calendarId": {"type": "string", "default": "primary"},
                    "eventId": {"type": "string"}
                },
                "required": ["eventId"]
            }
        ),

        # ─────────────────────────────────────────
        # MONGODB TOOLS
        # ─────────────────────────────────────────
        Tool(
            name="mongo_list_databases",
            description="List all MongoDB databases",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="mongo_list_collections",
            description="List all collections in a MongoDB database",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_name": {"type": "string", "description": "Database name"}
                },
                "required": ["database_name"]
            }
        ),
        Tool(
            name="mongo_find_documents",
            description="Find documents in a MongoDB collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_name": {"type": "string"},
                    "collection_name": {"type": "string"},
                    "query": {"type": "string", "description": "JSON query string e.g. '{\"name\": \"John\"}'"},
                    "limit": {"type": "integer", "default": 100},
                    "skip": {"type": "integer", "default": 0}
                },
                "required": ["database_name", "collection_name"]
            }
        ),
        Tool(
            name="mongo_insert_document",
            description="Insert a single document into MongoDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_name": {"type": "string"},
                    "collection_name": {"type": "string"},
                    "document": {"type": "string", "description": "JSON document string to insert"}
                },
                "required": ["database_name", "collection_name", "document"]
            }
        ),
        Tool(
            name="mongo_update_document",
            description="Update a document in MongoDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_name": {"type": "string"},
                    "collection_name": {"type": "string"},
                    "filter_query": {"type": "string", "description": "JSON filter query"},
                    "update_data": {"type": "string", "description": "JSON update data"},
                    "upsert": {"type": "boolean", "default": False}
                },
                "required": ["database_name", "collection_name", "filter_query", "update_data"]
            }
        ),
        Tool(
            name="mongo_delete_document",
            description="Delete a document from MongoDB",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_name": {"type": "string"},
                    "collection_name": {"type": "string"},
                    "filter_query": {"type": "string", "description": "JSON filter query"}
                },
                "required": ["database_name", "collection_name", "filter_query"]
            }
        ),
        Tool(
            name="mongo_count_documents",
            description="Count documents in a MongoDB collection",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_name": {"type": "string"},
                    "collection_name": {"type": "string"},
                    "query": {"type": "string", "description": "Optional JSON filter query"}
                },
                "required": ["database_name", "collection_name"]
            }
        ),
        Tool(
            name="mongo_aggregate",
            description="Run a MongoDB aggregation pipeline",
            inputSchema={
                "type": "object",
                "properties": {
                    "database_name": {"type": "string"},
                    "collection_name": {"type": "string"},
                    "pipeline": {"type": "string", "description": "JSON aggregation pipeline array"}
                },
                "required": ["database_name", "collection_name", "pipeline"]
            }
        ),

        # ─────────────────────────────────────────
        # POSTGRESQL TOOLS
        # ─────────────────────────────────────────
        Tool(
            name="pg_list_tables",
            description="List all tables in the PostgreSQL database",
            inputSchema={"type": "object", "properties": {}}
        ),
        Tool(
            name="pg_execute_query",
            description="Execute a SELECT query on PostgreSQL",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL SELECT query"},
                    "params": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="pg_execute_write",
            description="Execute INSERT, UPDATE, or DELETE on PostgreSQL",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "SQL write query"},
                    "params": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="pg_describe_table",
            description="Get schema/column info for a PostgreSQL table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string"}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="pg_get_table_count",
            description="Get row count for a PostgreSQL table",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string"}
                },
                "required": ["table_name"]
            }
        ),
        Tool(
            name="pg_run_custom_sql",
            description="Run any SQL query on PostgreSQL (auto-detects SELECT vs write)",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string"},
                    "params": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["sql"]
            }
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        current_config = load_config()
        result = None

        # ─────────────────────────────────────────
        # GOOGLE SHEETS
        # ─────────────────────────────────────────
        if name == "read_sheet":
            spreadsheet_id = arguments.get("spreadsheetId") or current_config.get("google", {}).get("spreadsheetId")
            result = sheets.read_sheet_data(spreadsheet_id, arguments["range"])

        elif name == "write_sheet":
            spreadsheet_id = arguments.get("spreadsheetId") or current_config.get("google", {}).get("spreadsheetId")
            result = sheets.write_sheet_data(spreadsheet_id, arguments["range"], arguments["values"])

        elif name == "append_sheet":
            spreadsheet_id = arguments.get("spreadsheetId") or current_config.get("google", {}).get("spreadsheetId")
            result = sheets.append_sheet_data(spreadsheet_id, arguments["range"], arguments["values"])

        elif name == "get_sheet_info":
            spreadsheet_id = arguments.get("spreadsheetId") or current_config.get("google", {}).get("spreadsheetId")
            result = sheets.get_sheet_info(spreadsheet_id)

        # ─────────────────────────────────────────
        # GMAIL
        # ─────────────────────────────────────────
        elif name == "list_emails":
            result = gmail.list_emails(arguments.get("maxResults", 10), arguments.get("query", ""))

        elif name == "get_email_detail":
            result = gmail.get_email_detail(arguments["messageId"])

        elif name == "send_email":
            result = gmail.send_email(
                arguments["to"],
                arguments["subject"],
                arguments["body"],
                arguments.get("isHtml", False)
            )

        elif name == "search_emails":
            result = gmail.search_emails(arguments["query"])

        # ─────────────────────────────────────────
        # GOOGLE CALENDAR
        # ─────────────────────────────────────────
        elif name == "list_calendar_events":
            result = calendar.list_events(
                arguments.get("calendarId") or current_config.get("google", {}).get("calendarId", "primary"),
                arguments.get("maxResults", 10),
                arguments.get("timeMin")
            )

        elif name == "create_calendar_event":
            result = calendar.create_event(
                arguments.get("calendarId") or current_config.get("google", {}).get("calendarId", "primary"),
                {
                    "summary": arguments["summary"],
                    "description": arguments.get("description", ""),
                    "start": arguments["start"],
                    "end": arguments["end"],
                    "location": arguments.get("location", ""),
                    "attendees": arguments.get("attendees", []),
                    "timeZone": arguments.get("timeZone", "America/Los_Angeles")
                }
            )

        elif name == "update_calendar_event":
            result = calendar.update_event(
                arguments.get("calendarId") or current_config.get("google", {}).get("calendarId", "primary"),
                arguments["eventId"],
                {
                    "summary": arguments.get("summary"),
                    "description": arguments.get("description"),
                    "start": arguments.get("start"),
                    "end": arguments.get("end"),
                    "location": arguments.get("location"),
                    "attendees": arguments.get("attendees"),
                    "timeZone": arguments.get("timeZone", "America/Los_Angeles")
                }
            )

        elif name == "delete_calendar_event":
            result = calendar.delete_event(
                arguments.get("calendarId") or current_config.get("google", {}).get("calendarId", "primary"),
                arguments["eventId"]
            )

        elif name == "get_calendar_event":
            result = calendar.get_event(
                arguments.get("calendarId") or current_config.get("google", {}).get("calendarId", "primary"),
                arguments["eventId"]
            )

        # ─────────────────────────────────────────
        # MONGODB
        # ─────────────────────────────────────────
        elif name.startswith("mongo_"):
            mongo_uri = current_config.get('mongodb', {}).get('uri', '')
            if not mongo_uri:
                result = {"success": False, "error": "MongoDB URI not configured. Add 'mongodb.uri' to config.json"}

            elif name == "mongo_list_databases":
                result = mongo.list_databases(mongo_uri)

            elif name == "mongo_list_collections":
                result = mongo.list_collections(mongo_uri, arguments["database_name"])

            elif name == "mongo_find_documents":
                result = mongo.find_documents(
                    mongo_uri,
                    arguments["database_name"],
                    arguments["collection_name"],
                    arguments.get("query"),
                    arguments.get("limit", 100),
                    arguments.get("skip", 0)
                )

            elif name == "mongo_insert_document":
                result = mongo.insert_document(
                    mongo_uri,
                    arguments["database_name"],
                    arguments["collection_name"],
                    arguments["document"]
                )

            elif name == "mongo_update_document":
                result = mongo.update_document(
                    mongo_uri,
                    arguments["database_name"],
                    arguments["collection_name"],
                    arguments["filter_query"],
                    arguments["update_data"],
                    arguments.get("upsert", False)
                )

            elif name == "mongo_delete_document":
                result = mongo.delete_document(
                    mongo_uri,
                    arguments["database_name"],
                    arguments["collection_name"],
                    arguments["filter_query"]
                )

            elif name == "mongo_count_documents":
                result = mongo.count_documents(
                    mongo_uri,
                    arguments["database_name"],
                    arguments["collection_name"],
                    arguments.get("query")
                )

            elif name == "mongo_aggregate":
                result = mongo.aggregate(
                    mongo_uri,
                    arguments["database_name"],
                    arguments["collection_name"],
                    arguments["pipeline"]
                )

        # ─────────────────────────────────────────
        # POSTGRESQL
        # ─────────────────────────────────────────
        elif name.startswith("pg_"):
            pg_url = current_config.get('database', {}).get('url', '')
            if not pg_url:
                result = {"success": False, "error": "PostgreSQL URL not configured. Add 'database.url' to config.json"}

            elif name == "pg_list_tables":
                result = db.list_tables(pg_url)

            elif name == "pg_execute_query":
                result = db.execute_query(pg_url, arguments["query"], arguments.get("params"))

            elif name == "pg_execute_write":
                result = db.execute_write(pg_url, arguments["query"], arguments.get("params"))

            elif name == "pg_describe_table":
                result = db.describe_table(pg_url, arguments["table_name"])

            elif name == "pg_get_table_count":
                result = db.get_table_count(pg_url, arguments["table_name"])

            elif name == "pg_run_custom_sql":
                result = db.run_custom_sql(pg_url, arguments["sql"], arguments.get("params"))

        else:
            result = {"success": False, "error": f"Unknown tool: {name}"}

        return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]

    except Exception as error:
        return [TextContent(type="text", text=json.dumps({"success": False, "error": str(error)}, indent=2))]


async def main():
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())