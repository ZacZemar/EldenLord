$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Requirements = Join-Path $Root "requirements-dev.txt"

if ($env:ELDEN_LORD_VENV) {
    $Venv = $env:ELDEN_LORD_VENV
} else {
    $Base = if ($env:LOCALAPPDATA) { $env:LOCALAPPDATA } else { Join-Path $HOME "AppData\Local" }
    $Venv = Join-Path $Base "EldenLord\venv"
}

$Python = Join-Path $Venv "Scripts\python.exe"

if (-not (Test-Path $Python)) {
    Write-Host "Creating EldenLord virtual environment at $Venv"
    if (Get-Command py -ErrorAction SilentlyContinue) {
        py -3 -m venv $Venv
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        python -m venv $Venv
    } else {
        throw "Python 3 was not found."
    }
}

if (-not (Test-Path $Python)) {
    throw "Virtual environment creation failed."
}

if (Test-Path $Requirements) {
    & $Python -m pip install -r $Requirements
    if ($LASTEXITCODE -ne 0) { throw "Dependency installation failed." }
}

Write-Host ""
Write-Host "EldenLord development environment is ready."
Write-Host "Virtual environment: $Venv"
Write-Host "Run: .\run.ps1"
Write-Host "Activate: . .\activate.ps1"
