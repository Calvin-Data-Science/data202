Set-Location $PSScriptRoot

# 1 — Generate per-student grade JSON files
if (Test-Path "grades\grades.xlsx") {
    Write-Host "Generating grade data..." -ForegroundColor Cyan
    python3 grades/generate.py
    if ($LASTEXITCODE -ne 0) { Write-Host "Grade generation failed." -ForegroundColor Red; exit 1 }
} else {
    Write-Host "No grades.xlsx found, skipping grade generation." -ForegroundColor Yellow
}

# 2 — Build Jekyll site
Write-Host "Building Jekyll site..." -ForegroundColor Cyan
bundle exec jekyll build
if ($LASTEXITCODE -ne 0) { Write-Host "Jekyll build failed." -ForegroundColor Red; exit 1 }

# 3 — Deploy to Calvin server
Write-Host "Deploying to server..." -ForegroundColor Cyan
scp -i "C:\Users\fs33\.ssh\calvin" -r "./_site/." "fs33@csweb.cs.calvin.edu:/webroot/courses/data/202/26fa/"
if ($LASTEXITCODE -ne 0) { Write-Host "Deployment failed." -ForegroundColor Red; exit 1 }

# 4 — Fix permissions on server (scp from Windows often lands files non-readable)
Write-Host "Fixing permissions..." -ForegroundColor Cyan
ssh -i "C:\Users\fs33\.ssh\calvin" fs33@csweb.cs.calvin.edu "find /webroot/courses/data/202/26fa/ -type d -exec chmod 755 {} + && find /webroot/courses/data/202/26fa/ -type f -exec chmod 644 {} +"
if ($LASTEXITCODE -eq 0) {
    Write-Host "Done." -ForegroundColor Green
} else {
    Write-Host "Permission fix failed - try running manually on the server." -ForegroundColor Yellow
}
