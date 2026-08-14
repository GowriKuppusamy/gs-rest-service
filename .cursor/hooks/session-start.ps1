Write-Host "========================================"
Write-Host "Cursor Agentic SDLC Hook Started"
Write-Host "========================================"

Write-Host "Checking project..."

if (Test-Path ".cursor/mcp.json") {
    Write-Host "MCP configuration found."
}
else {
    Write-Host "WARNING: MCP configuration not found."
}

if (Test-Path ".cursor/rules/sdlc-core.mdc") {
    Write-Host "SDLC governance rule found."
}
else {
    Write-Host "WARNING: SDLC governance rule not found."
}

if (Test-Path ".cursor/skills") {
    Write-Host "Skills directory found."
}
else {
    Write-Host "WARNING: Skills directory not found."
}

if (-not (Test-Path "jira-mcp/.env")) {
    Write-Host "WARNING: jira-mcp/.env missing — Jira MCP will fail until configured."
}

if (-not (Test-Path ".cursor/mcp.env")) {
    Write-Host "WARNING: .cursor/mcp.env missing — GitHub MCP will fail until configured."
}
elseif (-not $env:GITHUB_TOKEN) {
    Write-Host "WARNING: GITHUB_TOKEN not in Cursor process env. Run: powershell -ExecutionPolicy Bypass -File .cursor/setup-mcp-env.ps1 then restart Cursor."
}

Write-Host "Cursor Agentic SDLC validation completed."
