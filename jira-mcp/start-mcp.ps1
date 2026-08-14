$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$envFile = Join-Path $root ".env"
$python = Join-Path $root ".venv\Scripts\python.exe"
$server = Join-Path $root "server.py"

if (-not (Test-Path $python)) {
    Write-Error "Jira MCP: Python venv not found at $python. Run: cd jira-mcp; python -m venv .venv; .venv\Scripts\pip install -r requirements.txt"
    exit 1
}

if (-not (Test-Path $envFile)) {
    Write-Error "Jira MCP: Missing jira-mcp/.env. Copy jira-mcp/.env.example to jira-mcp/.env and set JIRA_URL, JIRA_EMAIL, JIRA_API_TOKEN."
    exit 1
}

$required = @("JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN")
$missing = @()

foreach ($name in $required) {
    $found = Select-String -Path $envFile -Pattern "^\s*$name\s*=" -Quiet
    if (-not $found) {
        $missing += $name
    }
}

if ($missing.Count -gt 0) {
    Write-Error ("Jira MCP: Missing keys in jira-mcp/.env: " + ($missing -join ", "))
    exit 1
}

& $python $server
