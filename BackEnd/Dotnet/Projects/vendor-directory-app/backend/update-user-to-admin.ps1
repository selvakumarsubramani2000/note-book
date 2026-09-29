# Script to update a user's role to Admin in the SQLite database

param(
    [Parameter(Mandatory=$false)]
    [string]$Email = "admin@vendordir.com"
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Update User Role to Admin" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if database exists
if (-not (Test-Path "vendordirectory.db")) {
    Write-Host "❌ Error: Database file 'vendordirectory.db' not found!" -ForegroundColor Red
    Write-Host "   Make sure you're in the backend folder and the database has been created." -ForegroundColor Yellow
    exit 1
}

# Check if sqlite3 is available
$sqlite3Available = Get-Command sqlite3 -ErrorAction SilentlyContinue

if ($sqlite3Available) {
    Write-Host "📧 Updating user: $Email" -ForegroundColor Yellow
    Write-Host ""
    
    # Update the user role
    $query = "UPDATE Users SET Role = 'Admin' WHERE Email = '$Email';"
    sqlite3 vendordirectory.db $query
    
    # Verify the update
    Write-Host "✅ User role updated successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📋 Current user details:" -ForegroundColor Cyan
    $verifyQuery = "SELECT Id, Email, Name, Role FROM Users WHERE Email = '$Email';"
    sqlite3 vendordirectory.db $verifyQuery
    
} else {
    Write-Host "⚠️  SQLite3 command-line tool not found." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Alternative method:" -ForegroundColor Cyan
    Write-Host "1. Install DB Browser for SQLite: https://sqlitebrowser.org/" -ForegroundColor White
    Write-Host "2. Open 'vendordirectory.db' with DB Browser" -ForegroundColor White
    Write-Host "3. Go to 'Browse Data' tab" -ForegroundColor White
    Write-Host "4. Select 'Users' table" -ForegroundColor White
    Write-Host "5. Find the user with email: $Email" -ForegroundColor White
    Write-Host "6. Change the 'Role' column from 'User' to 'Admin'" -ForegroundColor White
    Write-Host "7. Click 'Write Changes'" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use this SQL query in any SQLite tool:" -ForegroundColor Cyan
    Write-Host "UPDATE Users SET Role = 'Admin' WHERE Email = '$Email';" -ForegroundColor White
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "⚠️  Important: After updating the role:" -ForegroundColor Yellow
Write-Host "1. Login again to get a new JWT token" -ForegroundColor White
Write-Host "2. The new token will include the Admin role" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan

