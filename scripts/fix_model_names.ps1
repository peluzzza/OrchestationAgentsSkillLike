Set-Location "c:\Users\daniel.leyva\OneDrive - European Medicines Agency\Desktop\Projects"

$files = Get-ChildItem -Path "." -Recurse -Filter "*.agent.md" | Where-Object { $_.FullName -notlike "*\.git\*" }
$fixed = 0
foreach ($file in $files) {
    $content = [System.IO.File]::ReadAllText($file.FullName, [System.Text.Encoding]::UTF8)
    if ($content -match "GPT-5\.4 \(copilot\)") {
        if ($content -match "GPT-5\.2 \(copilot\)") {
            $new = [System.Text.RegularExpressions.Regex]::Replace($content, "  - GPT-5\.4 \(copilot\)\r?\n", "")
        } else {
            $new = $content -replace "GPT-5\.4 \(copilot\)", "GPT-5.2 (copilot)"
        }
        [System.IO.File]::WriteAllText($file.FullName, $new, [System.Text.UTF8Encoding]::new($false))
        $fixed++
        Write-Host "[OK] $($file.Name)"
    }
}
Write-Host "Fixed: $fixed files"
