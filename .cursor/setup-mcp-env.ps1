# Sync MCP secrets from local env files into Windows User environment variables.
# Remote MCP servers (GitHub) only resolve ${env:NAME} from the process environment —
# envFile is NOT supported for remote HTTP/SSE servers in Cursor.
#
# Usage (run once after creating .cursor/mcp.env, then restart Cursor):
#   powershell -ExecutionPolicy Bypass -File .cursor/setup-mcp-env.ps1

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
$mcpEnv = Join-Path $PSScriptRoot "mcp.env"

if (-not (Test-Path $mcpEnv)) {
    Write-Error "Missing .cursor/mcp.env. Copy .cursor/mcp.env.example to .cursor/mcp.env and set GITHUB_TOKEN."
}

$token = $null
Get-Content $mcpEnv | ForEach-Object {
    if ($_ -match '^\s*GITHUB_TOKEN\s*=\s*(.+)\s*$') {
        $token = $Matches[1].Trim().Trim('"').Trim("'")
    }
}

if ([string]::IsNullOrWhiteSpace($token)) {
    Write-Error "GITHUB_TOKEN is empty in .cursor/mcp.env"
}

if ($token -match 'your-github|YOUR_GITHUB|\$\{env:') {
    Write-Error "GITHUB_TOKEN in .cursor/mcp.env is still a placeholder. Set your real GitHub PAT."
}

if ($token -match '^Bearer\s') {
    Write-Error "GITHUB_TOKEN should be the token only. Do not include Bearer prefix."
}

[Environment]::SetEnvironmentVariable("GITHUB_TOKEN", $token, "User")
$env:GITHUB_TOKEN = $token

Write-Host "GITHUB_TOKEN synced to Windows User environment (length: $($token.Length))."
Write-Host "Restart Cursor completely for GitHub MCP to pick up the token."
Write-Host "Project root: $projectRoot"
