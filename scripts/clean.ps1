# SPDX-License-Identifier: MPL-2.0
Param(
    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$Args
)

$ErrorActionPreference = "Stop"
$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$bashScript = Join-Path $scriptRoot "$script"

if (-not (Test-Path $bashScript)) {
    Write-Error "Bash script '$bashScript' not found."
}

& bash $bashScript @Args
