param([Parameter(Mandatory = $true)][string]$InstallerPath)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$dist = Join-Path $projectRoot 'dist'
$staging = Join-Path $dist 'WeFlow微信聊天导出完整交付包'
if (-not (Test-Path -LiteralPath $InstallerPath -PathType Leaf)) { throw "未找到安装器：$InstallerPath" }
if (Test-Path -LiteralPath $dist) { Remove-Item -LiteralPath $dist -Recurse -Force }
New-Item -ItemType Directory -Path $staging -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $projectRoot 'skill') -Destination $staging -Recurse
Copy-Item -LiteralPath (Join-Path $projectRoot 'README.md') -Destination $staging
Copy-Item -LiteralPath (Join-Path $projectRoot 'SECURITY.md') -Destination $staging
Copy-Item -LiteralPath (Join-Path $projectRoot '安装Skill.ps1') -Destination $staging
Copy-Item -LiteralPath $InstallerPath -Destination $staging
Copy-Item -LiteralPath $InstallerPath -Destination $dist
$installerHash = (Get-FileHash -LiteralPath $InstallerPath -Algorithm SHA256).Hash
$signatureStatus = (Get-AuthenticodeSignature -FilePath $InstallerPath).Status
@("WeFlow 安装器：$(Split-Path $InstallerPath -Leaf)", "SHA-256：$installerHash", "数字签名状态：$signatureStatus") |
    Set-Content -LiteralPath (Join-Path $staging '安装器校验值.txt') -Encoding UTF8
$skillZip = Join-Path $dist 'WeFlow.Skill.zip'
$fullZip = Join-Path $dist 'WeFlow.zip'
Compress-Archive -LiteralPath (Join-Path $projectRoot 'skill\weflow-export-wechat') -DestinationPath $skillZip -CompressionLevel Optimal
Compress-Archive -Path (Join-Path $staging '*') -DestinationPath $fullZip -CompressionLevel Optimal
$installerCopy = Join-Path $dist (Split-Path $InstallerPath -Leaf)
Get-FileHash -LiteralPath $installerCopy, $skillZip, $fullZip -Algorithm SHA256 |
    ForEach-Object { "$($_.Hash)  $(Split-Path $_.Path -Leaf)" } |
    Set-Content -LiteralPath (Join-Path $dist 'SHA256SUMS.txt') -Encoding UTF8
Write-Output "发布包已生成：$dist"



