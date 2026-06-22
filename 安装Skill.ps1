param(
    [string]$Source = (Join-Path $PSScriptRoot 'skill\weflow-export-wechat'),
    [string]$SkillsRoot = (Join-Path $HOME '.codex\skills')
)

$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath (Join-Path $Source 'SKILL.md'))) { throw "未找到 Skill：$Source" }
$destination = Join-Path $SkillsRoot 'weflow-export-wechat'
New-Item -ItemType Directory -Path $SkillsRoot -Force | Out-Null
if (Test-Path -LiteralPath $destination) {
    $backup = "$destination.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
    Move-Item -LiteralPath $destination -Destination $backup
    Write-Output "已备份旧版本：$backup"
}
Copy-Item -LiteralPath $Source -Destination $destination -Recurse
Write-Output "Skill 已安装：$destination"
Write-Output '请完全退出并重新启动 Codex，然后使用 $weflow-export-wechat。'



