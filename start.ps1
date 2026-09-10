Write-Host ""
Write-Host "  ===================================================" -ForegroundColor Cyan
Write-Host "   Aria - AI Travel Planner (IBM Granite)" -ForegroundColor Cyan
Write-Host "  ===================================================" -ForegroundColor Cyan
Write-Host ""

# Install deps if missing
if (-not (Test-Path "node_modules")) {
    Write-Host "  Installing dependencies..." -ForegroundColor Yellow
    & "C:\Program Files\nodejs\node.exe" "C:\Program Files\nodejs\node_modules\npm\bin\npm-cli.js" install
}

Write-Host "  Starting server at http://localhost:3000" -ForegroundColor Green
Write-Host "  Press Ctrl+C to stop." -ForegroundColor Gray
Write-Host ""

# Open browser after 2 seconds in background
Start-Job -ScriptBlock {
    Start-Sleep 2
    Start-Process "http://localhost:3000"
} | Out-Null

# Start Node server
& "C:\Program Files\nodejs\node.exe" server.js
