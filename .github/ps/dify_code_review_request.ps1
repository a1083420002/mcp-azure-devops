param(
  # App API keys (param > env > throw)
  [string]$CustomAppKey   = 'app-CzdjFhacdnhKZ9z3vGZdL9DL',
  [string]$StandardAppKey = 'app-ZiyaCPCjqiTaN8YEAsMTZU8e',

  # Endpoints
  [string]$CustomApiUrl   = 'https://dify.91app.biz/v1/chat-messages',
  [string]$StandardApiUrl = 'https://dify.91app.biz/v1/chat-messages',

  # Misc
  [string]$User = 'copilot-code-review-request',
  [int]$TimeoutSec    = 60,
  [int]$RetryCount    = 2,
  [int]$RetryDelaySec = 2,

  # Optional conversation ids
  [string]$CustomConversationId,
  [string]$StandardConversationId
)

$ErrorActionPreference = 'Stop'

function Get-ValueOrEnv {
  param(
    [string]$Value,
    [string]$EnvName,
    [string]$NameForError
  )
  if (-not [string]::IsNullOrWhiteSpace($Value)) { return $Value.Trim() }

  # Try to get environment variable from Process/User/Machine
  $envVal = [Environment]::GetEnvironmentVariable($EnvName)
  if ([string]::IsNullOrWhiteSpace($envVal)) {
    $envVal = [Environment]::GetEnvironmentVariable($EnvName, 'User')
    if ([string]::IsNullOrWhiteSpace($envVal)) {
      $envVal = [Environment]::GetEnvironmentVariable($EnvName, 'Machine')
    }
  }
  if ([string]::IsNullOrWhiteSpace($envVal)) {
    throw "Missing $NameForError. Provide -$NameForError or set env:$EnvName."
  }
  return $envVal.Trim()
}

# Resolve keys from param/env
$CustomAppKey   = Get-ValueOrEnv -Value $CustomAppKey   -EnvName 'DIFY_APP_KEY_CUSTOM'   -NameForError 'CustomAppKey'
$StandardAppKey = Get-ValueOrEnv -Value $StandardAppKey -EnvName 'DIFY_APP_KEY_STANDARD' -NameForError 'StandardAppKey'

# Network defaults
try { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12 } catch {}
try { [System.Net.WebRequest]::DefaultWebProxy.Credentials = [System.Net.CredentialCache]::DefaultCredentials } catch {}

# Ensure git is available
try {
  git --version *> $null
} catch {
  throw "Git is not available in PATH. Please install Git for Windows and ensure 'git' is in PATH."
}

# Get staged .cs files
$stagedCsFiles = @()
try {
  $stagedCsFiles = git diff --staged --name-only -- '*.cs' | Where-Object { $_ -and $_.Trim() -ne '' }
} catch {
  throw "Failed to list staged .cs files: $($_.Exception.Message)"
}

$fileCount = ($stagedCsFiles | Measure-Object).Count
Write-Host "Staged .cs files: $fileCount"
if ($fileCount -gt 0) {
  Write-Host "Files:`n$($stagedCsFiles -join "`n")"
}

# If no .cs changes, output empty JSON and exit 0 (CI friendly)
if ($fileCount -eq 0) {
  Write-Host "No staged .cs changes found. Skipping API calls."
  @{ answers = @() } | ConvertTo-Json -Compress | Write-Output
  exit 0
}

# Get diff only for staged .cs files
try {
  # Use -- to separate file list from options
  $queryText = git diff --staged -- $stagedCsFiles | Out-String
  if (-not $queryText.Trim()) {
    Write-Host "Staged .cs file list is non-empty but diff is empty."
    @{ answers = @() } | ConvertTo-Json -Compress | Write-Output
    exit 0
  }
} catch {
  throw "Failed to get staged .cs diff: $($_.Exception.Message)"
}

function Invoke-DifyRequest {
  [CmdletBinding()]
  param(
    [Parameter(Mandatory)][string]$AppKey,
    [Parameter(Mandatory)][string]$ApiUrl,
    [Parameter(Mandatory)][string]$Query,
    [Parameter(Mandatory)][string]$User,
    [int]$TimeoutSec = 60,
    [string]$ConversationId,
    [int]$RetryCount = 2,
    [int]$RetryDelaySec = 2
  )

  $body = [ordered]@{
    query         = $Query
    user          = $User
    inputs        = @{}
    response_mode = 'blocking'
  }
  if ($ConversationId) { $body['conversation_id'] = $ConversationId }

  $json    = $body | ConvertTo-Json -Depth 10
  $headers = @{ Authorization = "Bearer $AppKey" }

  for ($i = 0; $i -le $RetryCount; $i++) {
    try {
      $resp = Invoke-RestMethod -Uri $ApiUrl -Method POST -Headers $headers `
              -ContentType 'application/json; charset=utf-8' -Body $json -TimeoutSec $TimeoutSec

      if ($resp -and ($resp.PSObject.Properties.Name -contains 'answer')) {
        return [string]$resp.answer
      } else {
        return ($resp | ConvertTo-Json -Compress)
      }
    } catch {
      if ($i -lt $RetryCount) {
        Start-Sleep -Seconds $RetryDelaySec
      } else {
        return "[ERROR] $($_.Exception.Message)"
      }
    }
  }
}

# Call API twice synchronously (Custom → Standard)
$customAnswer   = Invoke-DifyRequest -AppKey $CustomAppKey   -ApiUrl $CustomApiUrl   -Query $queryText -User $User -TimeoutSec $TimeoutSec -ConversationId $CustomConversationId   -RetryCount $RetryCount -RetryDelaySec $RetryDelaySec
$standardAnswer = Invoke-DifyRequest -AppKey $StandardAppKey -ApiUrl $StandardApiUrl -Query $queryText -User $User -TimeoutSec $TimeoutSec -ConversationId $StandardConversationId -RetryCount $RetryCount -RetryDelaySec $RetryDelaySec

# Human-readable output
"Code Reviewer (Custom Rules): $customAnswer"
"Code Reviewer (Standard Rules): $standardAnswer"

# Output JSON for further processing
@{ answers = @(
    @{ reviewer = 'Code Reviewer (Custom Rules)';   answer = $customAnswer },
    @{ reviewer = 'Code Reviewer (Standard Rules)'; answer = $standardAnswer }
  )
} | ConvertTo-Json -Compress | Write-Output
