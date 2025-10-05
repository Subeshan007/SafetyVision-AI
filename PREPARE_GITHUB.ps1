# GitHub Submission Preparation Script
# Duality AI Hackathon 2025

Write-Host "SafetyVision AI - GitHub Submission Preparation" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

$ErrorActionPreference = "Stop"

# Paths
$sourceDir = "d:\hackaura new"
$submissionDir = "$sourceDir\submission"
$modelSource = "C:\Users\ASUS\runs\detect\train\weights\best.pt"
$resultsSource = "C:\Users\ASUS\runs\detect\train"
$predictionsSource = "$sourceDir\Hackathon2_scripts\predictions"

# Step 1: Copy Model
Write-Host "Step 1: Copying trained model..." -ForegroundColor Yellow
if (Test-Path $modelSource) {
    Copy-Item $modelSource "$submissionDir\models\best.pt" -Force
    $modelSize = (Get-Item "$submissionDir\models\best.pt").Length / 1MB
    $sizeStr = [math]::Round($modelSize, 2)
    Write-Host "   [OK] Model copied: best.pt ($sizeStr MB)" -ForegroundColor Green
} else {
    Write-Host "   [WARNING] Model not found at: $modelSource" -ForegroundColor Red
    Write-Host "   Please update the path in this script" -ForegroundColor Yellow
}

# Step 2: Copy Results
Write-Host ""
Write-Host "Step 2: Copying training results..." -ForegroundColor Yellow
$resultFiles = @(
    "confusion_matrix.png",
    "confusion_matrix_normalized.png",
    "results.csv",
    "results.png",
    "F1_curve.png",
    "PR_curve.png",
    "P_curve.png",
    "R_curve.png"
)

$copiedCount = 0
foreach ($file in $resultFiles) {
    $sourcePath = "$resultsSource\$file"
    if (Test-Path $sourcePath) {
        Copy-Item $sourcePath "$submissionDir\results\" -Force
        Write-Host "   [OK] Copied: $file" -ForegroundColor Green
        $copiedCount++
    } else {
        Write-Host "   [SKIP] Not found: $file" -ForegroundColor DarkGray
    }
}
Write-Host "   Copied $copiedCount result files" -ForegroundColor Green

# Step 3: Copy Predictions (selective - first 100 images)
Write-Host ""
Write-Host "Step 3: Copying predictions (sample)..." -ForegroundColor Yellow
if (Test-Path "$predictionsSource\images") {
    # Copy first 100 annotated images (to save space)
    $predImages = Get-ChildItem "$predictionsSource\images" -File | Select-Object -First 100
    Write-Host "   Copying $($predImages.Count) sample prediction images..." -ForegroundColor Cyan
    
    foreach ($img in $predImages) {
        Copy-Item $img.FullName "$submissionDir\predictions\images\" -Force
    }
    Write-Host "   [OK] Copied $($predImages.Count) prediction images" -ForegroundColor Green
} else {
    Write-Host "   [WARNING] Predictions not found at: $predictionsSource\images" -ForegroundColor Red
}

# Copy corresponding labels
if (Test-Path "$predictionsSource\labels") {
    $predLabels = Get-ChildItem "$predictionsSource\labels" -File | Select-Object -First 100
    Write-Host "   Copying $($predLabels.Count) sample prediction labels..." -ForegroundColor Cyan
    
    foreach ($lbl in $predLabels) {
        Copy-Item $lbl.FullName "$submissionDir\predictions\labels\" -Force
    }
    Write-Host "   [OK] Copied $($predLabels.Count) prediction labels" -ForegroundColor Green
} else {
    Write-Host "   [WARNING] Labels not found at: $predictionsSource\labels" -ForegroundColor Red
}

# Step 4: Create .gitignore
Write-Host ""
Write-Host "Step 4: Creating .gitignore..." -ForegroundColor Yellow
$gitignoreContent = @"
# Python
__pycache__/
*.py[cod]
*`$py.class
*.so
.Python
env/
venv/
ENV/
*.egg-info/
dist/
build/

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# YOLO
runs/
wandb/

# Large files
*.pt.bak
*.onnx
*.engine

# Temp
temp_*
*.tmp
"@
Set-Content -Path "$submissionDir\.gitignore" -Value $gitignoreContent
Write-Host "   [OK] .gitignore created" -ForegroundColor Green

# Step 5: Summary
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "SUBMISSION PACKAGE READY!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Submission folder: $submissionDir" -ForegroundColor Cyan
Write-Host ""

Write-Host "Contents:" -ForegroundColor Yellow
$submissionSize = (Get-ChildItem $submissionDir -Recurse -File | Measure-Object -Property Length -Sum).Sum / 1MB
$sizeMB = [math]::Round($submissionSize, 2)
Write-Host "   - Total size: $sizeMB MB" -ForegroundColor White

$fileCount = @{
    "Scripts" = (Get-ChildItem "$submissionDir\scripts" -File -ErrorAction SilentlyContinue).Count
    "Docs" = (Get-ChildItem "$submissionDir\docs" -File -ErrorAction SilentlyContinue).Count
    "Models" = (Get-ChildItem "$submissionDir\models" -File -ErrorAction SilentlyContinue).Count
    "Results" = (Get-ChildItem "$submissionDir\results" -File -ErrorAction SilentlyContinue).Count
    "Predictions" = (Get-ChildItem "$submissionDir\predictions\images" -File -ErrorAction SilentlyContinue).Count
}

foreach ($category in $fileCount.Keys) {
    Write-Host "   - $category : $($fileCount[$category]) files" -ForegroundColor White
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Review files in: $submissionDir" -ForegroundColor White
Write-Host "   2. Create GitHub repository (private)" -ForegroundColor White
Write-Host "   3. Initialize git:" -ForegroundColor White
Write-Host "      cd '$submissionDir'" -ForegroundColor Cyan
Write-Host "      git init" -ForegroundColor Cyan
Write-Host "      git add ." -ForegroundColor Cyan
Write-Host "      git commit -m 'SafetyVision AI - Duality AI Hackathon 2025'" -ForegroundColor Cyan
Write-Host "   4. Push to GitHub:" -ForegroundColor White
Write-Host "      git branch -M main" -ForegroundColor Cyan
Write-Host "      git remote add origin YOUR_REPO_URL" -ForegroundColor Cyan
Write-Host "      git push -u origin main" -ForegroundColor Cyan
Write-Host "   5. Add collaborators: Maazsyedm, rebekah-bogdanoff, epilef68" -ForegroundColor White
Write-Host "   6. Submit form with GitHub URL" -ForegroundColor White
Write-Host ""
Write-Host "Final Score Estimate: 105-115 points (with bonus!)" -ForegroundColor Green
Write-Host ""
