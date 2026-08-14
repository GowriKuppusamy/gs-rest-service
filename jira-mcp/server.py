"""Jira MCP server for the Agentic SDLC Requirements phase."""

from __future__ import annotations

import json
import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("jira")

REQUIRED_ENV_VARS = ("JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN")
REQUEST_TIMEOUT_SECONDS = 30


class JiraConfigError(Exception):
    """Raised when required Jira configuration is missing."""


class JiraAuthError(Exception):
    """Raised when Jira rejects credentials."""


class JiraNotFoundError(Exception):
    """Raised when a Jira issue is not found."""


class JiraAPIError(Exception):
    """Raised for other Jira API failures."""


def _get_config() -> tuple[str, str, str]:
    missing = [name for name in REQUIRED_ENV_VARS if not os.environ.get(name)]
    if missing:
        raise JiraConfigError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + ". Set them in .cursor/mcp.json or your shell environment."
        )

    base_url = os.environ["JIRA_URL"].rstrip("/")
    email = os.environ["JIRA_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    return base_url, email, token


def _auth_headers(email: str, token: str) -> dict[str, str]:
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def _auth(email: str, token: str) -> tuple[str, str]:
    return email, token


def _handle_response(response: requests.Response, issue_key: str | None = None) -> Any:
    if response.status_code == 401:
        raise JiraAuthError(
            "Jira authentication failed. Check JIRA_EMAIL and JIRA_API_TOKEN."
        )
    if response.status_code == 404 and issue_key:
        raise JiraNotFoundError(f"Jira issue not found: {issue_key}")
    if response.status_code == 400:
        detail = _safe_json(response)
        message = detail.get("errorMessages") or detail.get("errors") or response.text
        raise JiraAPIError(f"Invalid Jira request: {message}")
    if not response.ok:
        detail = _safe_json(response)
        messages = detail.get("errorMessages")
        if messages:
            raise JiraAPIError(f"Jira API error ({response.status_code}): {'; '.join(messages)}")
        raise JiraAPIError(
            f"Jira API error ({response.status_code}): {response.text or 'Unknown error'}"
        )
    if not response.text:
        return {}
    return response.json()


def _safe_json(response: requests.Response) -> dict[str, Any]:
    try:
        data = response.json()
        return data if isinstance(data, dict) else {}
    except ValueError:
        return {}


def _jira_request(
    method: str,
    path: str,
    *,
    issue_key: str | None = None,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
) -> Any:
    base_url, email, token = _get_config()
    url = f"{base_url}{path}"
    response = requests.request(
        method,
        url,
        params=params,
        json=json_body,
        auth=_auth(email, token),
        headers=_auth_headers(email, token),
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    return _handle_response(response, issue_key=issue_key)


def _adf_to_text(node: Any) -> str:
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if not isinstance(node, dict):
        return ""

    text = node.get("text", "") if node.get("type") == "text" else ""
    children = node.get("content") or []
    child_text = "".join(_adf_to_text(child) for child in children)
    if node.get("type") == "paragraph" and child_text:
        return text + child_text + "\n"
    return text + child_text


def _field_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return _adf_to_text(value).strip()
    return str(value)


def _format_issue(issue: dict[str, Any]) -> dict[str, Any]:
    fields = issue.get("fields") or {}
    return {
        "key": issue.get("key"),
        "summary": fields.get("summary"),
        "description": _field_text(fields.get("description")),
        "status": (fields.get("status") or {}).get("name"),
        "issue_type": (fields.get("issuetype") or {}).get("name"),
        "priority": (fields.get("priority") or {}).get("name"),
        "assignee": (fields.get("assignee") or {}).get("displayName"),
        "reporter": (fields.get("reporter") or {}).get("displayName"),
        "labels": fields.get("labels") or [],
        "components": [c.get("name") for c in fields.get("components") or [] if c.get("name")],
        "created": fields.get("created"),
        "updated": fields.get("updated"),
        "url": issue.get("self"),
    }


def _plain_text_to_adf(text: str) -> dict[str, Any]:
    paragraphs = text.splitlines() or [text]
    content = []
    for paragraph in paragraphs:
        if not paragraph:
            continue
        content.append(
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": paragraph}],
            }
        )
    if not content:
        content.append(
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": text or " "}],
            }
        )
    return {"type": "doc", "version": 1, "content": content}


def _tool_error(message: str) -> str:
    return json.dumps({"error": message}, indent=2)


@mcp.tool()
def get_jira_issue(issue_key: str) -> str:
    """Fetch a Jira issue by key (e.g. PROJ-123) for Requirements analysis."""
    key = issue_key.strip().upper()
    if not key:
        return _tool_error("issue_key is required.")

    try:
        data = _jira_request(
            "GET",
            f"/rest/api/3/issue/{key}",
            issue_key=key,
            params={"fields": "summary,description,status,issuetype,priority,assignee,reporter,labels,components,created,updated"},
        )
        return json.dumps(_format_issue(data), indent=2)
    except JiraConfigError as exc:
        return _tool_error(str(exc))
    except JiraAuthError as exc:
        return _tool_error(str(exc))
    except JiraNotFoundError as exc:
        return _tool_error(str(exc))
    except JiraAPIError as exc:
        return _tool_error(str(exc))
    except requests.RequestException as exc:
        return _tool_error(f"Network error while contacting Jira: {exc}")


@mcp.tool()
def search_jira(jql: str) -> str:
    """Search Jira issues using JQL and return matching issue summaries."""
    query = jql.strip()
    if not query:
        return _tool_error("jql is required.")

    try:
        data = _jira_request(
            "POST",
            "/rest/api/3/search/jql",
            json_body={
                "jql": query,
                "maxResults": 50,
                "fields": ["summary", "status", "issuetype", "updated"],
            },
        )
        issues = [
            {
                "key": issue.get("key"),
                "summary": (issue.get("fields") or {}).get("summary"),
                "status": ((issue.get("fields") or {}).get("status") or {}).get("name"),
                "issue_type": ((issue.get("fields") or {}).get("issuetype") or {}).get("name"),
                "updated": (issue.get("fields") or {}).get("updated"),
            }
            for issue in data.get("issues") or []
        ]
        return json.dumps(
            {
                "jql": query,
                "total": data.get("total", len(issues)),
                "issues": issues,
            },
            indent=2,
        )
    except JiraConfigError as exc:
        return _tool_error(str(exc))
    except JiraAuthError as exc:
        return _tool_error(str(exc))
    except JiraAPIError as exc:
        return _tool_error(str(exc))
    except requests.RequestException as exc:
        return _tool_error(f"Network error while contacting Jira: {exc}")


@mcp.tool()
def add_jira_comment(issue_key: str, comment: str) -> str:
    """Add a comment to a Jira issue (e.g. requirements notes or clarifications)."""
    key = issue_key.strip().upper()
    body = comment.strip()
    if not key:
        return _tool_error("issue_key is required.")
    if not body:
        return _tool_error("comment is required.")

    try:
        data = _jira_request(
            "POST",
            f"/rest/api/3/issue/{key}/comment",
            issue_key=key,
            json_body={"body": _plain_text_to_adf(body)},
        )
        return json.dumps(
            {
                "issue_key": key,
                "comment_id": data.get("id"),
                "created": data.get("created"),
                "message": "Comment added successfully.",
            },
            indent=2,
        )
    except JiraConfigError as exc:
        return _tool_error(str(exc))
    except JiraAuthError as exc:
        return _tool_error(str(exc))
    except JiraNotFoundError as exc:
        return _tool_error(str(exc))
    except JiraAPIError as exc:
        return _tool_error(str(exc))
    except requests.RequestException as exc:
        return _tool_error(f"Network error while contacting Jira: {exc}")


if __name__ == "__main__":
    try:
        _get_config()
    except JiraConfigError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)
    mcp.run()
