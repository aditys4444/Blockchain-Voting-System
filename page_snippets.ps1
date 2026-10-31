$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Get-Item "PROJECT_REPORT_75_PAGES.docx").FullName
$doc = $word.Documents.Open($docPath)
for ($i = 1; $i -le $doc.ComputeStatistics(2); $i++) {
    $pageRange = $doc.Range()
    # GoTo page $i
    $targetRange = $doc.GoTo([ref]1, [ref]1, [ref]$i) # wdGoToPage, wdGoToAbsolute, $i
    $textSnippet = $targetRange.Paragraphs[1].Range.Text.Trim()
    if ($textSnippet.Length -gt 60) { $textSnippet = $textSnippet.Substring(0, 60) + "..." }
    Write-Host "Page $i : $textSnippet"
}
$doc.Close([ref]$false)
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
