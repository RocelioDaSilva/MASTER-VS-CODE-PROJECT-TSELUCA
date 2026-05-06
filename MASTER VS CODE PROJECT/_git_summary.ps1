$summaryPath = 'C:\Users\PCGAME\Desktop\MASTER VS CODE PROJECT\git_merge_summaries.txt'
Remove-Item -Force -ErrorAction SilentlyContinue $summaryPath
$repos = @('C:\Users\PCGAME\Desktop\MASTER VS CODE PROJECT\vs-code-projects-nexus-desktop','C:\Users\PCGAME\Desktop\MASTER VS CODE PROJECT\vs-code-projects-nexus-laptop')
foreach ($r in $repos) {
  if (Test-Path $r) {
    $untracked = (git -C $r ls-files --others --exclude-standard 2>$null | Measure-Object).Count
    $status = (git -C $r status -sb 2>$null)
    $head = (git -C $r rev-parse --short HEAD 2>$null)
    $last = (git -C $r log -1 --pretty=format:'%h %ad %an %s' --date=iso 2>$null)
    $remotes = (git -C $r remote -v 2>$null)
    Add-Content $summaryPath "=== $r ==="
    Add-Content $summaryPath "untracked_count: $untracked"
    Add-Content $summaryPath $status
    Add-Content $summaryPath "HEAD: $head"
    Add-Content $summaryPath "last: $last"
    Add-Content $summaryPath $remotes
  } else {
    Add-Content $summaryPath "Missing: $r"
  }
}
Write-Host "WROTE $summaryPath"
