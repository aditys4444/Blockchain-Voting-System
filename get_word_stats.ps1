$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = Join-Path (Get-Location) "PROJECT_REPORT_75_PAGES.docx"
$doc = $word.Documents.Open($docPath)
$pages = $doc.ComputeStatistics(2)
$words = $doc.ComputeStatistics(0)
$doc.Close([ref]$false)
$word.Quit()
Write-Host "MS_WORD_PAGES: $pages"
Write-Host "MS_WORD_WORDS: $words"
