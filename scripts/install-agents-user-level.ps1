<#
.SYNOPSIS
Instala todos los agentes del equipo Atlas en el directorio de usuario de VS Code.
Esto hace que los agentes estén disponibles en CUALQUIER workspace, sin necesidad
de clonar el repositorio ni configurar settings.json.

.DESCRIPTION
Copia los archivos .agent.md desde .github/agents/ al directorio global de prompts
de VS Code: %APPDATA%\Code\User\prompts\

Después de ejecutar este script, todos los agentes Atlas están disponibles
globalmente en VS Code Copilot Chat.

.PARAMETER Force
Sobreescribe archivos existentes en la carpeta de usuario.

.PARAMETER Uninstall
Elimina los agentes instalados del directorio de usuario.

.PARAMETER WhatIf
Muestra qué haría el script sin ejecutar nada.

.EXAMPLE
# Instalar (primera vez o actualización)
.\scripts\install-agents-user-level.ps1

.EXAMPLE
# Forzar sobreescritura de todos los archivos
.\scripts\install-agents-user-level.ps1 -Force

.EXAMPLE
# Ver qué haría sin ejecutar
.\scripts\install-agents-user-level.ps1 -WhatIf

.EXAMPLE
# Desinstalar todos los agentes Atlas del directorio de usuario
.\scripts\install-agents-user-level.ps1 -Uninstall
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [switch]$Force,
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

# ── Rutas ──────────────────────────────────────────────────────────────────────
$ScriptDir     = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot      = Split-Path -Parent $ScriptDir
$SourceAgents  = Join-Path $RepoRoot ".github\agents"
$UserPromptsDir = Join-Path $env:APPDATA "Code\User\prompts"

Write-Host ""
Write-Host "Atlas Agent Installer" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host "Fuente  : $SourceAgents"
Write-Host "Destino : $UserPromptsDir"
Write-Host ""

# ── Validar fuente ─────────────────────────────────────────────────────────────
if (-not (Test-Path $SourceAgents)) {
    Write-Error "No se encontró la carpeta de agentes: $SourceAgents"
    exit 1
}

$agentFiles = Get-ChildItem -Path $SourceAgents -Filter "*.agent.md" | Sort-Object Name

if ($agentFiles.Count -eq 0) {
    Write-Warning "No se encontraron archivos .agent.md en $SourceAgents"
    exit 0
}

# ── Modo Uninstall ─────────────────────────────────────────────────────────────
if ($Uninstall) {
    Write-Host "Modo: DESINSTALAR" -ForegroundColor Yellow
    $removed = 0
    foreach ($file in $agentFiles) {
        $dest = Join-Path $UserPromptsDir $file.Name
        if (Test-Path $dest) {
            if ($PSCmdlet.ShouldProcess($dest, "Eliminar")) {
                Remove-Item $dest -Force
                Write-Host "  [-] Eliminado: $($file.Name)" -ForegroundColor Red
                $removed++
            }
        }
    }
    Write-Host ""
    Write-Host "Desinstalación completa. $removed archivo(s) eliminado(s)." -ForegroundColor Green
    Write-Host "Recarga VS Code para aplicar los cambios:" -ForegroundColor Yellow
    Write-Host "  Ctrl+Shift+P → 'Developer: Reload Window'" -ForegroundColor Gray
    exit 0
}

# ── Modo Install ───────────────────────────────────────────────────────────────
Write-Host "Agentes encontrados: $($agentFiles.Count)" -ForegroundColor Green
Write-Host ""

# Crear directorio de destino si no existe
if (-not (Test-Path $UserPromptsDir)) {
    if ($PSCmdlet.ShouldProcess($UserPromptsDir, "Crear directorio")) {
        New-Item -ItemType Directory -Path $UserPromptsDir -Force | Out-Null
        Write-Host "Directorio creado: $UserPromptsDir" -ForegroundColor Gray
    }
}

$installed = 0
$skipped   = 0
$updated   = 0

foreach ($file in $agentFiles) {
    $dest = Join-Path $UserPromptsDir $file.Name
    $exists = Test-Path $dest

    if ($exists -and -not $Force) {
        # Comparar hash para detectar cambios
        $srcHash  = (Get-FileHash $file.FullName -Algorithm MD5).Hash
        $destHash = (Get-FileHash $dest -Algorithm MD5).Hash

        if ($srcHash -eq $destHash) {
            Write-Host "  [=] Sin cambios : $($file.Name)" -ForegroundColor Gray
            $skipped++
        } else {
            Write-Host "  [!] Desactualizado: $($file.Name) - usa -Force para actualizar" -ForegroundColor Yellow
            $skipped++
        }
    } else {
        $action = if ($exists) { "Actualizar" } else { "Instalar" }
        if ($PSCmdlet.ShouldProcess($dest, $action)) {
            Copy-Item $file.FullName $dest -Force
            if ($exists) {
                Write-Host "  [~] Actualizado : $($file.Name)" -ForegroundColor Blue
                $updated++
            } else {
                Write-Host "  [+] Instalado   : $($file.Name)" -ForegroundColor Green
                $installed++
            }
        }
    }
}

# ── Resumen ────────────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "-----------------------------------------" -ForegroundColor Gray
Write-Host "Instalados  : $installed" -ForegroundColor Green
Write-Host "Actualizados: $updated"   -ForegroundColor Blue
Write-Host "Sin cambios : $skipped"   -ForegroundColor Gray
Write-Host "-----------------------------------------" -ForegroundColor Gray
Write-Host ""

if ($installed -gt 0 -or $updated -gt 0) {
    Write-Host "OK: Agentes disponibles globalmente en VS Code." -ForegroundColor Green
    Write-Host ""
    Write-Host "SIGUIENTE PASO - Recarga VS Code:" -ForegroundColor Yellow
    Write-Host "  Ctrl+Shift+P -> 'Developer: Reload Window'" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "VERIFICACION - En Copilot Chat busca estos agentes:" -ForegroundColor Yellow
    Write-Host "  @Atlas          <- orquestador principal" -ForegroundColor Cyan
    Write-Host "  @Prometheus     <- pipeline Specify" -ForegroundColor Cyan
    Write-Host "  @Hermes         <- exploracion de codigo" -ForegroundColor Cyan
    Write-Host "  @Sisyphus       <- implementacion" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "NOTA: Los agentes estaran disponibles en CUALQUIER workspace" -ForegroundColor Gray
    Write-Host "      sin necesidad de clonar este repositorio." -ForegroundColor Gray
} elseif ($skipped -eq $agentFiles.Count) {
    Write-Host "OK: Todos los agentes ya estan instalados y actualizados." -ForegroundColor Green
    Write-Host "   Usa -Force para forzar la reinstalación." -ForegroundColor Gray
}

Write-Host ""
