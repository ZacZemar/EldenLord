$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Setup = Join-Path $Root "setup.ps1"
$Main = Join-Path $Root "main.py"

if ($env:ELDEN_LORD_VENV) {
    $Venv = $env:ELDEN_LORD_VENV
} else {
    $Base = if ($env:LOCALAPPDATA) { $env:LOCALAPPDATA } else { Join-Path $HOME "AppData\Local" }
    $Venv = Join-Path $Base "EldenLord\venv"
}

$Python = Join-Path $Venv "Scripts\python.exe"

if (-not (Test-Path $Python)) {
    & $Setup
}

if (-not (Test-Path $Python)) {
    throw "EldenLord virtual environment was not created successfully."
}

Push-Location $Root
try {
    & $Python $Main
}
finally {
    Pop-Location
}
