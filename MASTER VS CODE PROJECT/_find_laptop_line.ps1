$path='C:\Users\PCGAME\Desktop\MASTER VS CODE PROJECT\git_merge_summaries.txt'
$pattern='vs-code-projects-nexus-laptop'
$match = Select-String -Path $path -Pattern $pattern -SimpleMatch | Select-Object -First 1
if ($match -ne $null) { $match.LineNumber } else { Write-Host 'NOTFOUND' }
