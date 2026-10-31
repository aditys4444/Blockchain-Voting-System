$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = (Get-Item "PROJECT_REPORT_75_PAGES.docx").FullName
$doc = $word.Documents.Open($docPath)
foreach ($p in $doc.Paragraphs) {
    if ($p.Style.NameLocal -eq "Heading 1") {
        $pageNum = $p.Range.Information(1) # 1 = wdActiveEndPageNumber
        Write-Host "Heading 1: $($p.Range.Text.Trim()) -> Page $pageNum"
    }
}
$doc.Close([ref]$false)
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
