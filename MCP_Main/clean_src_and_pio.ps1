# Navigate to project
Set-Location -Path D:\MCP\esp32_project

# Step 1: Delete ALL .cpp files in src
Remove-Item -Path .\src\*.cpp -Force
Write-Output "Deleted all .cpp files"

# Step 2: Delete build cache
Remove-Item -Path .\.pio -Recurse -Force -ErrorAction SilentlyContinue
Write-Output "Deleted .pio build cache"

# Step 3: Verify src is empty
$files = Get-ChildItem -Path .\src -File
if ($files.Count -eq 0) {
    Write-Output "SUCCESS: src folder is now completely empty (0 files)"
} else {
    Write-Output "WARNING: Found $($files.Count) files still in src:"
    $files | ForEach-Object { Write-Output "  - $($_.Name)" }
}
