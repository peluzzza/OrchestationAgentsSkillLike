Set-Location "c:\Users\daniel.leyva\OneDrive - European Medicines Agency\Desktop\Projects"

$base = ".\plugins"

$assignments = @{
    "backend-workflow"        = @{
        comment = "<!-- layer: 2 | parent: Backend-Atlas > Sisyphus -->"
        skip    = "Backend-Atlas.agent.md"
    }
    "data-workflow"           = @{
        comment = "<!-- layer: 2 | parent: Data-Atlas > Sisyphus -->"
        skip    = "Data-Atlas.agent.md"
    }
    "devops-workflow"         = @{
        comment = "<!-- layer: 2 | parent: DevOps-Atlas > Hephaestus -->"
        skip    = "DevOps-Atlas.agent.md"
    }
    "automation-mcp-workflow" = @{
        comment = "<!-- layer: 2 | parent: Automation-Atlas > Hephaestus -->"
        skip    = "Automation-Atlas.agent.md"
    }
    "frontend-workflow"       = @{
        comment = "<!-- layer: 2 | parent: Afrodita > Afrodita-UX -->"
        skip    = "Afrodita.agent.md"
    }
    "ux-enhancement-workflow" = @{
        comment = "<!-- layer: 2 | parent: UX-Atlas > Afrodita-UX -->"
        skip    = "UX-Atlas.agent.md"
    }
}

$total = 0
foreach ($pack in $assignments.Keys) {
    $info = $assignments[$pack]
    $files = Get-ChildItem "$base\$pack\agents\*.agent.md" | Where-Object { $_.Name -ne $info.skip }
    foreach ($file in $files) {
        $lines = Get-Content $file.FullName
        $dashes = @(($lines | Select-String "^---$") | Select-Object -ExpandProperty LineNumber)
        if ($dashes.Count -ge 2) {
            $closeIdx = $dashes[1] - 1
            if ($closeIdx + 1 -lt $lines.Count -and $lines[$closeIdx + 1] -like "<!-- layer:*") {
                Write-Host "  [SKIP already tagged] $($file.Name)"
                continue
            }
            $newLines = $lines[0..$closeIdx] + $info.comment + $lines[($closeIdx + 1)..($lines.Count - 1)]
            Set-Content $file.FullName $newLines -Encoding UTF8
            $total++
            Write-Host "  [OK] $($file.Name)"
        }
        else {
            Write-Host "  [WARN no closing ---] $($file.Name)"
        }
    }
}
Write-Host "Total files updated: $total"
