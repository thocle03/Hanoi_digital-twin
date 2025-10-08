$sumoVersion = "1.24.0"
$zipName = "sumo-win64-$sumoVersion.zip"
$downloadUrl = "https://sumo.dlr.de/releases/$sumoVersion/$zipName"
$outZip = Join-Path $env:TEMP $zipName
Invoke-WebRequest -Uri $downloadUrl -OutFile $outZip
$dest = Join-Path $env:USERPROFILE "sumo"
if (!(Test-Path $dest)) { New-Item -ItemType Directory -Path $dest | Out-Null }
Expand-Archive -Path $outZip -DestinationPath $dest -Force
$binPath = Join-Path (Join-Path $dest "sumo-win64-$sumoVersion") "bin"
$env:Path = $binPath + ";" + $env:Path
python -m pip install -r requirements.txt
Write-Output "Terminé. Vérifie avec 'sumo --version' et 'netconvert --version'"
