param([switch]$CreateRepository)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$repoName = 'Zhuyyyan/agentic-payment-authorization'
$repoUrl = 'https://github.com/' + $repoName + '.git'
if (-not (Test-Path -LiteralPath '.git')) {
    git init -b main
    if ($LASTEXITCODE -ne 0) { throw 'Failed to initialize local Git repository.' }
}
git add -- .gitignore CITATION.cff README.md PUBLICATION.md publish.ps1 claims_audit.md config.json data/examples experiment_manifest.csv literature outputs paper progress.md quality_review.md requirements-lock.txt requirements.txt research src tests tools
if ($LASTEXITCODE -ne 0) { throw 'Failed to stage the prepared public files.' }
git diff --cached --quiet
if ($LASTEXITCODE -eq 1) {
    git -c user.name=Zhuyyyan -c user.email=Zhuyyyan@users.noreply.github.com commit -m 'Publish research proposal and reproducible authorization simulation'
    if ($LASTEXITCODE -ne 0) { throw 'Failed to create publication commit.' }
}
git branch -M main
if ($LASTEXITCODE -ne 0) { throw 'Failed to set the main branch.' }
if ($CreateRepository) {
    $ghCommand = Get-Command gh -ErrorAction SilentlyContinue
    if (-not $ghCommand) { throw 'GitHub CLI is unavailable. Create the empty PUBLIC repository in GitHub first, then rerun without -CreateRepository.' }
    gh repo create $repoName --public --description 'Consumer-delegated agentic payment authorization: research proposal and reproducible synthetic Python simulations'
    if ($LASTEXITCODE -ne 0) { throw 'Repository creation failed. Check the GitHub account and repository name.' }
}
$remotes = git remote
if ($remotes -contains 'origin') {
    $currentRemote = git remote get-url origin
    if ($currentRemote -ne $repoUrl -and $currentRemote -ne ('https://github.com/' + $repoName)) {
        throw ('Origin points to a different repository: ' + $currentRemote)
    }
} else {
    git remote add origin $repoUrl
    if ($LASTEXITCODE -ne 0) { throw 'Failed to add origin.' }
}
git push -u origin main
if ($LASTEXITCODE -ne 0) { throw 'Push failed. Complete GitHub sign-in if requested, then rerun this script.' }
Write-Host ('Published repository: https://github.com/' + $repoName)
