$files = Get-ChildItem -Path "D:\Content Creation\Navonmesh Tech\navonmesh-website-v2\navonmesh-site\*.html", "D:\Content Creation\Navonmesh Tech\navonmesh-website-v2\navonmesh-site\projects\*.html"
foreach ($f in $files) {
    $c = [System.IO.File]::ReadAllText($f.FullName)
    $c = $c -replace '(?s)<nav.*?</nav>', ''
    $c = $c -replace '(?s)<footer.*?</footer>', ''
    [System.IO.File]::WriteAllText($f.FullName, $c)
    Write-Host "Cleaned: $($f.FullName)"
}
