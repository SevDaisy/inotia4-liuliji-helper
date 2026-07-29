# 查找 git 可执行文件路径
$gitPath = (Get-Command git -ErrorAction SilentlyContinue).Source

if (-not $gitPath) {
    Write-Host "ERROR: git not found, please install Git and add to PATH." -ForegroundColor Red
    exit 1
}

Write-Host "Found Git: $gitPath"

# 将 ...\Git\cmd\git.exe 转换为 ...\Git\bin\bash.exe
$bashPath = $gitPath -replace '\\cmd\\git\.exe$', '\bin\bash.exe'

if (-not (Test-Path $bashPath)) {
    Write-Host "ERROR: bash.exe not found at $bashPath" -ForegroundColor Red
    exit 1
}

Write-Host "Using Bash: $bashPath"

# 获取脚本所在目录
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$shScript = Join-Path $scriptDir "hack.sh"

if (-not (Test-Path $shScript)) {
    Write-Host "ERROR: $shScript not found." -ForegroundColor Red
    exit 1
}

# 执行 hack.sh
& $bashPath $shScript

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to execute hack.sh, exit code: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "hack.sh executed successfully." -ForegroundColor Green
exit 0