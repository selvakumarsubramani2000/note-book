# Environment Setup Verification Script
# Run this script to check if all required tools are installed

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Vendor Directory - Environment Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check .NET SDK
Write-Host "Checking .NET SDK..." -ForegroundColor Yellow
try {
    $dotnetVersion = dotnet --version
    Write-Host "  ✅ .NET SDK installed: $dotnetVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ .NET SDK not found" -ForegroundColor Red
    Write-Host "     Install from: https://dotnet.microsoft.com/download" -ForegroundColor Yellow
    $allGood = $false
}

Write-Host ""

# Check Node.js
Write-Host "Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "  ✅ Node.js installed: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Node.js not found" -ForegroundColor Red
    Write-Host "     Install from: https://nodejs.org/" -ForegroundColor Yellow
    $allGood = $false
}

Write-Host ""

# Check npm
Write-Host "Checking npm..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "  ✅ npm installed: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ npm not found (comes with Node.js)" -ForegroundColor Red
    $allGood = $false
}

Write-Host ""

# Check Git
Write-Host "Checking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version
    Write-Host "  ✅ Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "  ❌ Git not found" -ForegroundColor Red
    Write-Host "     Install from: https://git-scm.com/downloads" -ForegroundColor Yellow
    $allGood = $false
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

if ($allGood) {
    Write-Host "  🎉 All required tools are installed!" -ForegroundColor Green
    Write-Host "  You're ready to start coding!" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  Some tools are missing" -ForegroundColor Yellow
    Write-Host "  Please install the missing tools above" -ForegroundColor Yellow
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Pause to see results
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

