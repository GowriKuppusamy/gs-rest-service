# Jira MCP Server

Python MCP server for the Agentic SDLC **Requirements** phase. Exposes Jira REST API tools to Cursor Agent.

## Tools

| Tool | Description |
|------|-------------|
| `get_jira_issue(issue_key)` | Fetch issue summary, description, status, and metadata |
| `search_jira(jql)` | Search issues with JQL (up to 50 results) |
| `add_jira_comment(issue_key, comment)` | Add a comment to an issue |

## Prerequisites

- Python 3.10+
- Jira Cloud site with REST API access
- [Jira API token](https://id.atlassian.com/manage-profile/security/api-tokens)

## Environment variables

| Variable | Description |
|----------|-------------|
| `JIRA_URL` | Jira site URL, e.g. `https://your-domain.atlassian.net` |
| `JIRA_EMAIL` | Atlassian account email |
| `JIRA_API_TOKEN` | API token (never commit this) |

Copy `.env.example` to `.env` for local testing only. **Do not commit `.env`.**

## Local setup

```bash
cd jira-mcp
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

## Local test

Set environment variables, then run:

```bash
python server.py
```

Or inspect tools with the MCP CLI:

```bash
mcp dev server.py
```

## Error handling

Tools return JSON with an `error` field when something fails:

- **Missing configuration** — one or more env vars not set
- **Authentication failure** — invalid email or API token (HTTP 401)
- **Invalid issue key** — issue not found (HTTP 404)
- **API failure** — invalid JQL, permission errors, or other Jira errors
- **Network errors** — connection or timeout issues

Credentials are never logged or included in error responses.

## Configure in Cursor

Add the server to `.cursor/mcp.json` at the repository root. Use an absolute path to your Python executable in the virtual environment.

```json
{
  "mcpServers": {
    "jira": {
      "command": "C:\\path\\to\\cursor-agentic-sdlc\\jira-mcp\\.venv\\Scripts\\python.exe",
      "args": ["C:\\path\\to\\cursor-agentic-sdlc\\jira-mcp\\server.py"],
      "env": {
        "JIRA_URL": "https://your-domain.atlassian.net",
        "JIRA_EMAIL": "you@example.com",
        "JIRA_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

**macOS/Linux example:**

```json
{
  "mcpServers": {
    "jira": {
      "command": "/path/to/cursor-agentic-sdlc/jira-mcp/.venv/bin/python",
      "args": ["/path/to/cursor-agentic-sdlc/jira-mcp/server.py"],
      "env": {
        "JIRA_URL": "https://your-domain.atlassian.net",
        "JIRA_EMAIL": "you@example.com",
        "JIRA_API_TOKEN": "your-api-token"
      }
    }
  }
}
```

After saving, restart Cursor or reload MCP servers. The **jira** server should appear with the three tools.

### Security notes

- Store credentials in `.cursor/mcp.json` locally or in your OS environment — not in this repository.
- Add `.cursor/mcp.json` to `.gitignore` if it contains secrets, or use placeholder values in a committed template.
- Rotate API tokens if they are ever exposed.

## Usage with Requirements skill

Attach the **requirements** skill and ask Cursor to fetch a story:

```
Run Requirements for PROJ-123
```

The agent can call `get_jira_issue("PROJ-123")` to ingest the user story into `docs/requirements.md`.
