<#
.SYNOPSIS
Syncs the OrchestationAgentsSkillLike marketplace repo locally and (optionally) copies pack agents into a workspace.

.DESCRIPTION
- Ensures a local clone of the marketplace repository exists at -TargetDir (git clone or git pull).
- In -Mode agents, copies *.agent.md files from plugins/<pack>/agents/ into -WorkspaceAgentsDir.
- Prints recommended VS Code settings snippets for multiple consumption options.

This script never overwrites existing agent files unless -Force is provided.

.PARAMETER TargetDir
Local directory where the marketplace repo should be cloned/pulled.
Default: $env:USERPROFILE\.copilot\marketplaces\OrchestationAgentsSkillLike

.PARAMETER Mode
Sync mode:
- plugins: only ensures the repo is present locally and prints settings recommendations.
- agents: copies agent files from one or more packs into -WorkspaceAgentsDir.

.PARAMETER Pack
Optional pack name(s). If omitted, all packs found under <repo>/plugins are used.

.PARAMETER WorkspaceAgentsDir
Target directory (in the current working directory by default) for copied agent files when -Mode agents.
Default: .\.github\agents

.PARAMETER Force
Allows overwriting existing agent files in -WorkspaceAgentsDir.

.PARAMETER Help
Shows help.

.EXAMPLE
# Ensure local clone and print recommended settings
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agent_packs.ps1

# If you have PowerShell 7 installed, you can use `pwsh` instead of `powershell`.

.EXAMPLE
# Copy Atlas pack agents into the current workspace's .github/agents folder
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agent_packs.ps1 -Mode agents -Pack atlas-orchestration-team

.EXAMPLE
# Copy all pack agents, overwriting existing files
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/sync_agent_packs.ps1 -Mode agents -Force
#>

[CmdletBinding()]
param(
  [Parameter(Mandatory = $false)]
  [string]$TargetDir = (Join-Path $env:USERPROFILE ".copilot\marketplaces\OrchestationAgentsSkillLike"),

  [Parameter(Mandatory = $false)]
  [ValidateSet('plugins', 'agents')]
  [string]$Mode = 'plugins',

  [Parameter(Mandatory = $false)]
  [string[]]$Pack,

  [Parameter(Mandatory = $false)]
  [string]$WorkspaceAgentsDir = (Join-Path (Get-Location) ".github\agents"),

  [Parameter(Mandatory = $false)]
  [switch]$Force,

  [Parameter(Mandatory = $false)]
  [Alias('?')]
  [switch]$Help
)

$ErrorActionPreference = 'Stop'

if ($Help) {
  Get-Help -Detailed $MyInvocation.MyCommand.Path
  return
}

$RepoUrl = 'https://github.com/peluzzza/OrchestationAgentsSkillLike'
$RemoteMarketplaceId = 'peluzzza/OrchestationAgentsSkillLike'

function Assert-GitAvailable {
  if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git was not found on PATH. Install Git for Windows and try again."
  }
}

function Ensure-Directory {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Path
  )

  if (-not (Test-Path -LiteralPath $Path)) {
    New-Item -ItemType Directory -Path $Path -Force | Out-Null
  }
}

function Ensure-MarketplaceRepo {
  param(
    [Parameter(Mandatory = $true)]
    [string]$RepoDir
  )

  if (Test-Path -LiteralPath $RepoDir) {
    $gitDir = Join-Path $RepoDir '.git'
    if (Test-Path -LiteralPath $gitDir) {
      Push-Location $RepoDir
      try {
        Write-Host "Updating existing repo: $RepoDir"
        git pull
      }
      finally {
        Pop-Location
      }
      return
    }

    $childCount = @(Get-ChildItem -LiteralPath $RepoDir -Force -ErrorAction SilentlyContinue).Count
    if ($childCount -eq 0) {
      Write-Host "Cloning repo into existing empty directory: $RepoDir"
      git clone $RepoUrl $RepoDir
      return
    }

    throw "TargetDir exists but is not a git repo (and not empty): $RepoDir"
  }

  $parent = Split-Path -Parent $RepoDir
  if ($parent) {
    Ensure-Directory -Path $parent
  }

  Write-Host "Cloning repo: $RepoUrl -> $RepoDir"
  git clone $RepoUrl $RepoDir
}

function Get-AvailablePacks {
  param(
    [Parameter(Mandatory = $true)]
    [string]$RepoDir
  )

  $pluginsDir = Join-Path $RepoDir 'plugins'
  if (-not (Test-Path -LiteralPath $pluginsDir)) {
    throw "Expected plugins directory not found: $pluginsDir"
  }

  return @(Get-ChildItem -LiteralPath $pluginsDir -Directory | Select-Object -ExpandProperty Name)
}

function Resolve-PackSelection {
  param(
    [Parameter(Mandatory = $true)]
    [string]$RepoDir,

    [Parameter(Mandatory = $false)]
    [string[]]$Pack
  )

  $available = Get-AvailablePacks -RepoDir $RepoDir
  if (-not $Pack -or $Pack.Count -eq 0) {
    return $available
  }

  $missing = @($Pack | Where-Object { $_ -notin $available })
  if ($missing.Count -gt 0) {
    $availableList = ($available | Sort-Object) -join ', '
    $missingList = ($missing | Sort-Object) -join ', '
    throw "Unknown pack(s): $missingList. Available packs: $availableList"
  }

  return $Pack
}

function Sync-PackAgentsToWorkspace {
  param(
    [Parameter(Mandatory = $true)]
    [string]$RepoDir,

    [Parameter(Mandatory = $true)]
    [string[]]$Packs,

    [Parameter(Mandatory = $true)]
    [string]$WorkspaceAgentsDir,

    [Parameter(Mandatory = $true)]
    [switch]$Force
  )

  Ensure-Directory -Path $WorkspaceAgentsDir
  $workspaceAgentsDirResolved = (Resolve-Path -LiteralPath $WorkspaceAgentsDir).Path

  foreach ($packName in $Packs) {
    $sourceAgentsDir = Join-Path $RepoDir ("plugins\\{0}\\agents" -f $packName)
    if (-not (Test-Path -LiteralPath $sourceAgentsDir)) {
      Write-Warning "Pack '$packName' has no agents directory: $sourceAgentsDir"
      continue
    }

    $agentFiles = @(Get-ChildItem -LiteralPath $sourceAgentsDir -Filter '*.agent.md' -File -ErrorAction SilentlyContinue)
    if ($agentFiles.Count -eq 0) {
      Write-Warning "No .agent.md files found in: $sourceAgentsDir"
      continue
    }

    foreach ($agentFile in $agentFiles) {
      $destination = Join-Path $workspaceAgentsDirResolved $agentFile.Name
      if ((Test-Path -LiteralPath $destination) -and (-not $Force)) {
        Write-Warning "Skipping existing agent file (use -Force to overwrite): $destination"
        continue
      }

      Copy-Item -LiteralPath $agentFile.FullName -Destination $destination -Force:$Force | Out-Null
      Write-Host ("Copied {0} -> {1}" -f $agentFile.Name, $destination)
    }
  }
}

function Print-RecommendedSettings {
  param(
    [Parameter(Mandatory = $true)]
    [string]$LocalRepoDir,

    [Parameter(Mandatory = $true)]
    [string]$RemoteMarketplaceId,

    [Parameter(Mandatory = $true)]
    [string]$WorkspaceAgentsDir
  )

  function Convert-ToSettingsPath {
    param(
      [Parameter(Mandatory = $true)]
      [string]$Path
    )

    $resolved = $null
    try {
      $resolved = (Resolve-Path -LiteralPath $Path -ErrorAction SilentlyContinue)
    }
    catch {
      $resolved = $null
    }

    $absolutePath = if ($resolved) { $resolved.Path } else { $Path }
    $cwd = (Resolve-Path -LiteralPath (Get-Location).Path).Path
    $relative = $null

    $cwdPrefix = $cwd.TrimEnd('\') + '\'
    if ($absolutePath.StartsWith($cwdPrefix, [System.StringComparison]::OrdinalIgnoreCase)) {
      $candidate = $absolutePath.Substring($cwdPrefix.Length)
      if ($candidate) {
        return ($candidate -replace '\\', '/')
      }
    }

    try {
      function Convert-ToFileUri {
        param(
          [Parameter(Mandatory = $true)]
          [string]$Path,

          [Parameter(Mandatory = $false)]
          [switch]$AsDirectory
        )

        if ($Path.StartsWith('\\')) {
          $unc = $Path.TrimStart('\\')
          $parts = $unc.Split('\\', 2)
          $host = $parts[0]
          $rest = if ($parts.Count -gt 1) { $parts[1] } else { '' }
          $rest = ($rest -replace '\\', '/')
          if ($AsDirectory -and $rest -and -not $rest.EndsWith('/')) {
            $rest += '/'
          }
          return New-Object System.Uri(("file://{0}/{1}" -f $host, $rest))
        }

        $normalized = ($Path -replace '\\', '/')
        if ($AsDirectory -and -not $normalized.EndsWith('/')) {
          $normalized += '/'
        }

        return New-Object System.Uri(("file:///{0}" -f $normalized))
      }

      $fromUri = Convert-ToFileUri -Path ($cwd.TrimEnd('\') + '\') -AsDirectory
      $toUri = Convert-ToFileUri -Path $absolutePath
      $relative = [System.Uri]::UnescapeDataString($fromUri.MakeRelativeUri($toUri).ToString())
    }
    catch {
      $relative = $null
    }

    $isActuallyRelative = $relative -and
      -not ($relative.StartsWith('..')) -and
      -not ($relative -match '^[a-zA-Z]+:') -and
      -not ($relative.StartsWith('/'))

    if ($isActuallyRelative) {
      return ($relative -replace '\\', '/')
    }

    return ($absolutePath -replace '\\', '/')
  }

  $localPluginsPath = Join-Path $LocalRepoDir 'plugins'
  $localPluginsPathJson = Convert-ToSettingsPath -Path $localPluginsPath
  $workspaceAgentsDirJson = Convert-ToSettingsPath -Path $WorkspaceAgentsDir
  $localRepoDirJson = ($LocalRepoDir -replace '\\', '/')

  Write-Output ""
  Write-Output "============================"
  Write-Output "Recommended VS Code settings"
  Write-Output "============================"
  Write-Output "Pick ONE of the following consumption approaches (do not paste all at once)."
  Write-Output ""

  Write-Output "A) Marketplace (remote)"
  Write-Output "----------------------"
  Write-Output "{"
  Write-Output '  "chat.plugins.enabled": true,'
  Write-Output ('  "chat.plugins.marketplaces": ["{0}"]' -f $RemoteMarketplaceId)
  Write-Output "}"
  Write-Output ""

  Write-Output "B) Local plugin path (no marketplace UI)"
  Write-Output "---------------------------------------"
  Write-Output "{"
  Write-Output '  "chat.plugins.enabled": true,'
  Write-Output '  "chat.plugins.paths": {'
  Write-Output ('    "{0}": true' -f $localPluginsPathJson)
  Write-Output '  }'
  Write-Output "}"
  Write-Output ""

  Write-Output "C) Agents-only (copy/sync into this workspace)"
  Write-Output "---------------------------------------------"
  Write-Output "{"
  Write-Output '  "chat.agentFilesLocations": {'
  Write-Output ('    "{0}": true' -f $workspaceAgentsDirJson)
  Write-Output '  }'
  Write-Output "}"
  Write-Output ""

  Write-Output "(Optional) Marketplace (local clone)"
  Write-Output "-----------------------------------"
  Write-Output "{"
  Write-Output '  "chat.plugins.enabled": true,'
  Write-Output ('  "chat.plugins.marketplaces": ["{0}"]' -f $localRepoDirJson)
  Write-Output "}"
  Write-Output ""
}

$scriptRepoRoot = Split-Path -Parent $PSScriptRoot
$localPluginsDir = Join-Path $scriptRepoRoot 'plugins'
$localMarketplaceJson = Join-Path $scriptRepoRoot '.github\plugin\marketplace.json'

if ((Test-Path -LiteralPath $localPluginsDir) -and (Test-Path -LiteralPath $localMarketplaceJson)) {
  Write-Host "Using local marketplace repo: $scriptRepoRoot"
  $resolvedRepoDir = (Resolve-Path -LiteralPath $scriptRepoRoot).Path
}
else {
  Assert-GitAvailable
  Ensure-MarketplaceRepo -RepoDir $TargetDir
  $resolvedRepoDir = (Resolve-Path -LiteralPath $TargetDir).Path
}

if ($Mode -eq 'agents') {
  $selectedPacks = Resolve-PackSelection -RepoDir $resolvedRepoDir -Pack $Pack
  Sync-PackAgentsToWorkspace -RepoDir $resolvedRepoDir -Packs $selectedPacks -WorkspaceAgentsDir $WorkspaceAgentsDir -Force:$Force
}

Print-RecommendedSettings -LocalRepoDir $resolvedRepoDir -RemoteMarketplaceId $RemoteMarketplaceId -WorkspaceAgentsDir $WorkspaceAgentsDir
