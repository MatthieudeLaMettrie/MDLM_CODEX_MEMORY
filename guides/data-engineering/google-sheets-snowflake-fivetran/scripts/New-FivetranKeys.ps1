<#
.SYNOPSIS
Generates a local RSA key pair for the FIVETRAN_USER Snowflake login.
.DESCRIPTION
Writes keys outside the repository, refuses to overwrite files, and never prints
private-key contents. -Encrypt prompts locally for a passphrase. No network calls.
The public-key SQL uses RSA_PUBLIC_KEY; see GUIDE.md for rotation and configuration.
#>
[CmdletBinding()]
param(
    [string]$OutputDirectory = (Join-Path $env:USERPROFILE '.snowflake\keys\fivetran'),
    [string]$OpenSslPath,
    [switch]$Encrypt
)
$ErrorActionPreference = 'Stop'

if (-not $OpenSslPath) {
    $command = Get-Command openssl -ErrorAction SilentlyContinue
    if ($command) { $OpenSslPath = $command.Source }
    elseif (Test-Path -LiteralPath 'C:\Program Files\Git\mingw64\bin\openssl.exe') {
        $OpenSslPath = 'C:\Program Files\Git\mingw64\bin\openssl.exe'
    }
    else { throw 'OpenSSL not found. Supply -OpenSslPath to an installed executable.' }
}
if (-not (Test-Path -LiteralPath $OpenSslPath -PathType Leaf)) {
    throw 'The OpenSSL executable does not exist.'
}
$outputPath = [IO.Path]::GetFullPath($OutputDirectory)
$repoPath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\..\..'))
if ($outputPath.Equals($repoPath, [StringComparison]::OrdinalIgnoreCase) -or
    $outputPath.StartsWith($repoPath + [IO.Path]::DirectorySeparatorChar,
                          [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Choose an output directory outside this repository.'
}
$privatePath = Join-Path $outputPath 'rsa_key.p8'
$publicPath = Join-Path $outputPath 'rsa_key.pub'
$sqlPath = Join-Path $outputPath 'assign_public_key.sql'
foreach ($path in @($privatePath, $publicPath, $sqlPath)) {
    if (Test-Path -LiteralPath $path) { throw "Refusing to overwrite: $path" }
}
New-Item -ItemType Directory -Path $outputPath -Force | Out-Null

# genpkey emits PKCS#8; this avoids a PowerShell pipeline carrying key material.
$generateArgs = @('genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:2048',
                  '-out', $privatePath)
if ($Encrypt) { $generateArgs += '-aes-256-cbc' }
& $OpenSslPath @generateArgs
if ($LASTEXITCODE -ne 0) { throw 'Private-key generation failed. Inspect local output files.' }
& $OpenSslPath pkey -in $privatePath -pubout -out $publicPath
if ($LASTEXITCODE -ne 0) { throw 'Public-key export failed. Inspect local output files.' }

$publicBody = ((Get-Content -LiteralPath $publicPath |
    Where-Object { $_ -notmatch '^-----' }) -join '') -replace '\s', ''
if ($publicBody -notmatch '^[A-Za-z0-9+/]+={0,2}$') { throw 'Unexpected public-key format.' }
$sqlText = "USE ROLE ACCOUNTADMIN;`r`nALTER USER FIVETRAN_USER SET RSA_PUBLIC_KEY = '$publicBody';`r`nDESCRIBE USER FIVETRAN_USER;`r`n"
Set-Content -LiteralPath $sqlPath -Value $sqlText -Encoding ascii
Write-Output "Private key (keep secret): $privatePath"
Write-Output "Public key: $publicPath"
Write-Output "Run this public-key SQL in Snowflake: $sqlPath"
Write-Output "Encrypted private key: $($Encrypt.IsPresent)"
Write-Output 'Review folder access permissions. Paste the private key only into Fivetran.'
