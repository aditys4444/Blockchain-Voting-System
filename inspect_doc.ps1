$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Get-Item "PROJECT_REPORT_75_PAGES.docx").FullName
$doc = $word.Documents.Open($docPath)
Write-Host "Total Pages: $($doc.ComputeStatistics(2))"
Write-Host "Total Paragraphs: $($doc.Paragraphs.Count)"
Write-Host "Total Tables: $($doc.Tables.Count)"
Write-Host "Total InlineShapes: $($doc.InlineShapes.Count)"
$doc.Close([ref]$false)
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
