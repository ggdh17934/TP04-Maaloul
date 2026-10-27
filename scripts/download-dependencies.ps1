$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath (Split-Path $PSScriptRoot -Parent)
New-Item -ItemType Directory -Force vendor/linux-wheels, vendor/windows-wheels | Out-Null
python -m pip download --disable-pip-version-check --only-binary=:all: --platform manylinux_2_17_x86_64 --python-version 312 --implementation cp --abi cp312 --dest vendor/linux-wheels -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Linux wheel download failed' }
python -m pip download --disable-pip-version-check --only-binary=:all: --dest vendor/windows-wheels -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw 'Windows wheel download failed' }
