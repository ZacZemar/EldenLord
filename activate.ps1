$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Setup = Join-Path $Root "setup.ps1"

if ($env:ELDEN_LORD_VENV) {
    $Venv = $env:ELDEN_LORD_VENV
} else {
    $Base = if ($env:LOCALAPPDATA) { $env:LOCALAPPDATA } else { Join-Path $HOME "AppData\Local" }
    $Venv = Join-Path $Base "EldenLord\venv"
}

$Activate = Join-Path $Venv "Scripts\Activate.ps1"

if (-not (Test-Path $Activate)) {
    & $Setup
}

if (-not (Test-Path $Activate)) {
    throw "EldenLord virtual environment was not created successfully."
}

. $Activate
Write-Host "EldenLord virtual environment activated: $Venv"
