param(
  [Parameter(Mandatory = $false)]
  [string]$DbScript,

  [Parameter(Mandatory = $false)]
  [string]$OutDir
)

$ErrorActionPreference = "Stop"

$scriptRoot = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Path }

if (-not $DbScript) {
  $DbScript = Join-Path $scriptRoot "..\database\db.script"
}

if (-not $OutDir) {
  $OutDir = Join-Path $scriptRoot "..\dashboard\data"
}

if (-not (Test-Path -LiteralPath $DbScript)) {
  $nested = Join-Path $scriptRoot "..\FinalCCNProject\database\db.script"
  if (Test-Path -LiteralPath $nested) {
    $DbScript = $nested
  } else {
    throw "db.script not found: $DbScript"
  }
}

$insertRe = [regex]"^INSERT INTO MQTT_READY VALUES\((\d+),([^,]+),([^,]+),([^,]+),'([^']+)'\)\s*$"

$rows = New-Object System.Collections.Generic.List[object]

Get-Content -LiteralPath $DbScript | ForEach-Object {
  if (-not $_.StartsWith("INSERT INTO MQTT_READY VALUES(")) { return }

  $m = $insertRe.Match($_.Trim())
  if (-not $m.Success) { return }

  $rows.Add([pscustomobject]@{
      id               = [int]$m.Groups[1].Value
      packetSize       = [double]$m.Groups[2].Value
      interArrival     = [double]$m.Groups[3].Value
      flowDuration     = [double]$m.Groups[4].Value
      arrivalTimestamp = $m.Groups[5].Value
    })
}

$rows = $rows | Sort-Object id

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

$generatedAt = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# repo-relative source path for readability
try {
  $repoRoot = (Resolve-Path (Join-Path $PSScriptRoot ".." )).Path
  $sourceRel = (Resolve-Path -LiteralPath $DbScript).Path.Replace($repoRoot + "\\", "")
} catch {
  $sourceRel = $DbScript
}

$payload = [pscustomobject]@{
  generatedAt = $generatedAt
  source      = ($sourceRel -replace "\\", "/")
  rowCount    = $rows.Count
  rows        = $rows
}

$jsonPath = Join-Path $OutDir "mqtt_ready.json"
$csvPath = Join-Path $OutDir "mqtt_ready.csv"

$payload | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $jsonPath -Encoding UTF8
$rows | Export-Csv -LiteralPath $csvPath -NoTypeInformation -Encoding UTF8

$first = if ($rows.Count -gt 0) { $rows[0].arrivalTimestamp } else { "-" }
$last = if ($rows.Count -gt 0) { $rows[$rows.Count - 1].arrivalTimestamp } else { "-" }

Write-Host "Extracted $($rows.Count) rows"
Write-Host "Time range: $first → $last"
Write-Host "Wrote: $jsonPath"
Write-Host "Wrote: $csvPath"
