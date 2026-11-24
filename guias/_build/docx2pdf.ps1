# Converte DOCX -> PDF usando o Microsoft Word (COM) e atualiza sumário/campos antes.
# Uso: powershell -File docx2pdf.ps1 "C:\caminho\Guia.docx" [outro.docx ...]
param([Parameter(Mandatory = $true, ValueFromRemainingArguments = $true)][string[]]$Files)

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    foreach ($f in $Files) {
        $full = (Resolve-Path $f).Path
        $pdf = [System.IO.Path]::ChangeExtension($full, ".pdf")
        $doc = $word.Documents.Open($full, $false, $false)
        $doc.Repaginate()
        foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
        $doc.Fields.Update() | Out-Null
        foreach ($toc in $doc.TablesOfContents) { $toc.Update() }
        $doc.Repaginate()
        $doc.Save()                       # grava o DOCX com o sumário já atualizado
        $doc.ExportAsFixedFormat($pdf, 17, $false, 0, 0, 0, 0, 0, $true, $true, 1)  # 17 = PDF; cria marcadores dos títulos
        Write-Host ("OK  {0}  ({1} páginas)" -f $pdf, $doc.ComputeStatistics(2))
        $doc.Close($false)
    }
}
finally {
    $word.Quit()
}
