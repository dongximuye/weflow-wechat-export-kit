param(
    [string]$RepositoryName = 'weflow-wechat-export-kit',
    [string]$Version = 'v1.0.0'
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path $PSScriptRoot -Parent
$dist = Join-Path $projectRoot 'dist'
$releaseNotes = Join-Path $projectRoot 'RELEASE_NOTES.md'
$assets = @(
    (Join-Path $dist 'WeFlow-4.5.1-x64-Setup.exe'),
    (Join-Path $dist 'WeFlow.Skill.zip'),
    (Join-Path $dist 'WeFlow.zip'),
    (Join-Path $dist 'SHA256SUMS.txt')
)

$ghCommand = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghCommand) {
    $standardGh = 'C:\Program Files\GitHub CLI\gh.exe'
    if (Test-Path -LiteralPath $standardGh -PathType Leaf) { $ghCommand = Get-Item -LiteralPath $standardGh }
}
if (-not $ghCommand) {
    throw '未安装 GitHub CLI。请先执行：winget install --id GitHub.cli'
}
$gh = if ($ghCommand.Source) { $ghCommand.Source } elseif ($ghCommand.Path) { $ghCommand.Path } else { $ghCommand.FullName }
if (-not $gh) { throw '无法确定 GitHub CLI 的可执行文件路径。' }

& $gh auth status
if ($LASTEXITCODE -ne 0) { throw 'GitHub 尚未登录。请先执行：gh auth login' }

foreach ($asset in $assets) {
    if (-not (Test-Path -LiteralPath $asset -PathType Leaf)) { throw "缺少发布文件：$asset" }
}

Push-Location $projectRoot
try {
    $remoteNames = @(& git remote)
    if ($remoteNames -notcontains 'origin') {
        & $gh repo create $RepositoryName --private --source $projectRoot --remote origin --push
        if ($LASTEXITCODE -ne 0) { throw '创建或推送 GitHub 私有仓库失败。' }
    } else {
        & git push -u origin main
        if ($LASTEXITCODE -ne 0) { throw '推送 main 分支失败。' }
    }

    & git rev-parse --verify $Version 2>$null | Out-Null
    if ($LASTEXITCODE -ne 0) {
        & git tag -a $Version -m "WeFlow 微信聊天导出套件 $Version"
    }
    & git push origin $Version
    if ($LASTEXITCODE -ne 0) { throw '推送版本标签失败。' }

    & $gh release view $Version 1>$null 2>$null
    if ($LASTEXITCODE -eq 0) {
        & $gh release upload $Version @assets --clobber
    } else {
        & $gh release create $Version @assets --title "WeFlow 微信聊天导出套件 $Version" --notes-file $releaseNotes
    }
    if ($LASTEXITCODE -ne 0) { throw '创建或更新 GitHub Release 失败。' }

    $repositoryUrl = & $gh repo view --json url --jq '.url'
    $releaseUrl = & $gh release view $Version --json url --jq '.url'
    Write-Output "仓库：$repositoryUrl"
    Write-Output "下载：$releaseUrl"
}
finally {
    Pop-Location
}







