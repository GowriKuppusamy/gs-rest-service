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

Write-Host "Cursor Agentic SDLC validation completed."