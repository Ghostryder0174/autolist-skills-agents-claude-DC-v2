# Installs the autolist-skills-agents-claude-DC skill and its UserPromptSubmit hook for Claude Code on Windows.
#
# Requirements: Python 3 (the `py` launcher) and Node.js, used only to edit settings.json safely.
#
# Usage (PowerShell, from the repository folder):
#   powershell -ExecutionPolicy Bypass -File .\install.ps1
#   powershell -ExecutionPolicy Bypass -File .\install.ps1 -DisableSuperpowersHook

param([switch]$DisableSuperpowersHook)

$ErrorActionPreference = 'Stop'
$Here     = Split-Path -Parent $MyInvocation.MyCommand.Path
$Claude   = Join-Path $env:USERPROFILE '.claude'
$Backups  = Join-Path $Claude 'backups'
$Dest     = Join-Path $Claude 'skills\autolist-skills-agents-claude-DC'
$Settings = Join-Path $Claude 'settings.json'
$Stamp    = Get-Date -Format 'yyyyMMdd-HHmmss'

foreach ($cmd in 'py', 'node') {
  if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
    Write-Host "Missing: $cmd. Install it, then run this script again." -ForegroundColor Red; exit 1
  }
}
New-Item -ItemType Directory -Force $Backups, $Dest | Out-Null

# 1. Copy the skill. Keep an existing classes.json: it holds your own classification.
Write-Host '=== Skill'
$src = Join-Path $Here 'skills\autolist-skills-agents-claude-DC'
Copy-Item (Join-Path $src 'SKILL.md'), (Join-Path $src 'autolist.py') $Dest -Force
if (Test-Path (Join-Path $Dest 'classes.json')) {
  Write-Host '  classes.json already present, kept'
} else {
  Copy-Item (Join-Path $src 'classes.json') $Dest
}

# 2. Add the UserPromptSubmit hook to settings.json (backup first, no duplicate).
Write-Host '=== Hook'
if (-not (Test-Path $Settings)) { Set-Content -Path $Settings -Value '{}' -Encoding ascii }
Copy-Item $Settings (Join-Path $Backups "settings.json.$Stamp.bak")
$script = (Join-Path $Dest 'autolist.py') -replace '\\', '/'
$env:AUTOLIST_SETTINGS = $Settings
$env:AUTOLIST_CMD = "py -3 -I `"$script`""
node -e @'
const fs = require('fs');
const p = process.env.AUTOLIST_SETTINGS, cmd = process.env.AUTOLIST_CMD;
const s = JSON.parse(fs.readFileSync(p, 'utf8').replace(/^﻿/, '') || '{}');
s.hooks = s.hooks || {};
const ups = s.hooks.UserPromptSubmit = s.hooks.UserPromptSubmit || [];
const has = ups.some(g => (g.hooks || []).some(h => h.command === cmd));
if (!has) ups.push({ hooks: [{ type: 'command', command: cmd, timeout: 10 }] });
fs.writeFileSync(p, JSON.stringify(s, null, 2) + '\n');
console.log(has ? '  hook already present' : '  hook added');
'@

# 3. Optional: stop superpowers from injecting using-superpowers at every session start.
#    The plugin has no setting for this, so its hooks.json is emptied. A plugin update restores it.
if ($DisableSuperpowersHook) {
  Write-Host '=== superpowers SessionStart hook'
  $files = Get-ChildItem (Join-Path $Claude 'plugins\cache\superpowers-marketplace\superpowers') -Recurse -Filter hooks.json -ErrorAction SilentlyContinue |
    Where-Object { $_.Directory.Name -eq 'hooks' }
  foreach ($f in $files) {
    $ver = $f.Directory.Parent.Name
    Copy-Item $f.FullName (Join-Path $Backups "superpowers-$ver-hooks.json.$Stamp.bak")
    Set-Content -Path $f.FullName -Value "{`n  `"hooks`": {}`n}" -Encoding ascii
    Write-Host "  disabled for superpowers $ver"
  }
  if (-not $files) { Write-Host '  superpowers not installed, nothing to do' }
}

Write-Host "`nDone. Backups are in $Backups. Start a new Claude Code session to load the hook." -ForegroundColor Green
