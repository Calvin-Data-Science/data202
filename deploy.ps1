Set-Location $PSScriptRoot

# 0 - Make sure the deploy key is unlocked in ssh-agent (avoids a passphrase
#     prompt on every single run - you'll only be asked once per login session,
#     or once per reboot since the agent's cache doesn't survive a restart).
if ((Get-Service ssh-agent).Status -ne 'Running') {
    Write-Host "Starting ssh-agent..." -ForegroundColor Cyan
    Start-Service ssh-agent
}
$loadedKeys = ssh-add -l 2>$null
if (-not ($loadedKeys -match 'session-916dcead6c07483f5d823-fs33')) {
    Write-Host "Deploy key not yet unlocked this session - enter its passphrase:" -ForegroundColor Cyan
    ssh-add "C:\Users\fs33\.ssh\calvin"
    if ($LASTEXITCODE -ne 0) { Write-Host "Could not unlock deploy key." -ForegroundColor Red; exit 1 }
}

# 1 - Generate per-student grade JSON files
if (Test-Path "grades\grades.xlsx") {
    Write-Host "Generating grade data..." -ForegroundColor Cyan
    python3 grades/generate.py
    if ($LASTEXITCODE -ne 0) { Write-Host "Grade generation failed." -ForegroundColor Red; exit 1 }
} else {
    Write-Host "No grades.xlsx found, skipping grade generation." -ForegroundColor Yellow
}

# 2 - Build Jekyll site
Write-Host "Building Jekyll site..." -ForegroundColor Cyan
bundle exec jekyll build
if ($LASTEXITCODE -ne 0) { Write-Host "Jekyll build failed." -ForegroundColor Red; exit 1 }

# 3 - Deploy to Calvin server
Write-Host "Deploying to server..." -ForegroundColor Cyan
scp -i "C:\Users\fs33\.ssh\calvin" -r "./_site/." "fs33@csweb.cs.calvin.edu:/webroot/courses/data/202/26fa/"
if ($LASTEXITCODE -ne 0) { Write-Host "Deployment failed." -ForegroundColor Red; exit 1 }

# 4 - Fix permissions on server (scp from Windows often lands files non-readable)
Write-Host "Fixing permissions..." -ForegroundColor Cyan
ssh -i "C:\Users\fs33\.ssh\calvin" fs33@csweb.cs.calvin.edu "find /webroot/courses/data/202/26fa/ -type d -exec chmod 755 {} + && find /webroot/courses/data/202/26fa/ -type f -exec chmod 644 {} +"
if ($LASTEXITCODE -eq 0) {
    Write-Host "Done." -ForegroundColor Green
} else {
    Write-Host "Permission fix failed - try running manually on the server." -ForegroundColor Yellow
}
