# 寻找 git 可执行文件路径
$gitPath = (Get-Command git -ErrorAction SilentlyContinue).Source

if (-not $gitPath) {
    Write-Host "错误: 找不到 git 命令，请确保 Git 已安装并添加到 PATH。" -ForegroundColor Red
    exit 1
}

Write-Host "找到 Git: $gitPath"

# 将路径从 ...\Git\cmd\git.exe 转换为 ...\Git\bin\bash.exe
# 注意：使用 -replace 正则替换，兼容反斜杠
$bashPath = $gitPath -replace '\\cmd\\git\.exe$', '\bin\bash.exe'

# 检查 bash.exe 是否存在
if (-not (Test-Path $bashPath)) {
    Write-Host "错误: 找不到 bash.exe，预期路径为 $bashPath" -ForegroundColor Red
    exit 1
}

Write-Host "使用 Bash: $bashPath"

# 执行 hack.sh（假设在当前目录）
$scriptPath = ".\hack.sh"
if (-not (Test-Path $scriptPath)) {
    Write-Host "错误: 找不到 $scriptPath，请确保它在当前目录。" -ForegroundColor Red
    exit 1
}

# 使用 bash 执行脚本
& $bashPath $scriptPath

# 检查执行结果
if ($LASTEXITCODE -ne 0) {
    Write-Host "执行 hack.sh 失败，退出码: $LASTEXITCODE" -ForegroundColor Red
    exit $LASTEXITCODE
}

Write-Host "执行 hack.sh 成功。" -ForegroundColor Green
exit 0