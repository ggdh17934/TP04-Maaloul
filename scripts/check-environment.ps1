$ErrorActionPreference = 'Stop'
Get-CimInstance Win32_OperatingSystem | Select-Object Caption,Version,BuildNumber
Get-PSDrive C | Select-Object Name,Free
wsl --version
if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker version
    docker compose version
    docker info
} else {
    Write-Host 'Docker is not on PATH. Install the downloaded installer, start Docker Desktop, and reopen PowerShell.'
}
$dataset = Join-Path $PSScriptRoot '../../TP2-MALOUL/data/raw/HIGGS.csv'
Get-Item -LiteralPath $dataset | Select-Object FullName,Length
