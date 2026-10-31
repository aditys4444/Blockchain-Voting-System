$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Get-Item "PROJECT_REPORT_75_PAGES.docx").FullName
$doc = $word.Documents.Open($docPath)
$pages = $doc.ComputeStatistics(2)
$words = $doc.ComputeStatistics(0)
$doc.Close([ref]$false)
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Host "PAGES_COUNT: $pages"
Write-Host "WORDS_COUNT: $words"
