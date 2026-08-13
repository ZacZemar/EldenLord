# Development environments

EldenLord keeps source code in the repository and treats Python virtual environments as disposable machine-local state.

## Windows

The Windows development environment lives outside the repository by default:

```text
%LOCALAPPDATA%\EldenLord\venv
```

This keeps generated Python packages out of the OneDrive-backed source checkout.

### One-time / dependency setup

```powershell
.\setup.ps1
```

`setup.ps1` creates the venv if it does not exist and installs `requirements-dev.txt` into that exact interpreter. Running it again is safe and refreshes the declared development dependencies.

### Optional interactive activation

```powershell
.\activate.ps1
```

Activation is a developer convenience, not a runtime requirement. Use it when you want commands such as `python`, `pip`, or `pytest` in the current PowerShell session to resolve to EldenLord's venv.

If the environment does not exist yet, `activate.ps1` runs setup first.

### Run the CLI

```powershell
.\run.ps1
```

`run.ps1` does not require activation. It resolves `%LOCALAPPDATA%\EldenLord\venv\Scripts\python.exe` directly, creates the environment through `setup.ps1` if needed, changes to the repository root for the run, and starts `main.py`.

That means `run.ps1` behaves deterministically even from a fresh PowerShell session or when another Python environment is active.

### Optional venv location override

Set `ELDEN_LORD_VENV` before using any of the Windows scripts:

```powershell
$env:ELDEN_LORD_VENV = "D:\PythonEnvs\EldenLord"
.\setup.ps1
```

All three scripts use the same override.

## Linux

The existing Linux development workflow remains supported:

```bash
./scripts/setup_dev_env.sh
source .venv/bin/activate
```

The optional `.envrc.example` / `direnv` workflow remains just that: optional shell convenience. EldenLord itself does not depend on automatic activation when changing directories.

## Migrating an existing Windows `.venv`

Do not copy or move an existing repository-local `.venv` into LocalAppData. Virtual environments contain machine- and path-specific generated files and should be rebuilt.

From the EldenLord repository on Windows:

```powershell
.\setup.ps1
.\run.ps1
```

After the LocalAppData environment works, any old repository-local `.venv` can be deleted. The `.venv/` ignore rule remains because Linux still uses a repository-local environment and because legacy local environments should never be committed.
