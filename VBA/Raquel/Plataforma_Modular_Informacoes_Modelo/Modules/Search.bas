Attribute VB_Name = "Search"
Public SheetSearch As Object
Public Const CompanyFirstCell As String = "A3"
Public Const SearchFirstCell As String = "B5"

Public Sub InitSearch()
' initialize the global variables
    Set SheetSearch = Sheets("Search")
       
    ' Fill the company cmb and get the dictionary containing the sheets name
    UpdateCompaniesName
    
End Sub

Private Sub ClearTable(ByVal sheet As Object, ByVal tableFirstCell As Range)
' Clear the table content and the merged cells
    Dim rangeToClear As Range
    Dim lastColumn As String
    Dim lastRow As Integer
    
    ' If the first column is empty, the entry table should be empty than do not need to clear
    If tableFirstCell.End(xlDown).Row = 1048576 Then
        Exit Sub
        
    End If
    
    ' get the last column based in the header
    lastColumn = GetTableLastColumnLetter(tableFirstCell)
    ' get the last row based in the first column
    lastRow = GetTableLastRow(tableFirstCell)
    
    Set rangeToClear = sheet.Range(tableFirstCell, sheet.Range(lastColumn & lastRow))
    ' unmerge the cells
    rangeToClear.UnMerge
    'finally clear the range content and the format
    rangeToClear.Clear
    
End Sub

Public Sub ClearSearchTable()
'Clear the search table
    ' Clear the cell conataining the company name
    SheetSearch.Range("COMPANYNAME") = ""
    'Clear the table
    ClearTable SheetSearch, SheetSearch.Range(SearchFirstCell)
    
End Sub

Private Sub CopyAndPasteTable(ByVal tableName As String, ByVal FirstCell As String, ByVal cellToPaste As Range)
' Copy the table from the sheet tableName and paste to the cellToPaste
    Dim sheet As Object
    Dim sheetFirstCell As Range
    Dim tableLastColumn As String
    Dim tableLastRow As Integer
    
    Set sheet = Sheets(tableName)
    Set tableFirstCell = sheet.Range(FirstCell)
    ' If it go donw and reach the last row then the table is empty
    If tableFirstCell.End(xlDown).Row = 1048576 Then
        MsgBox "A tabela para empresa " & table & " esta vazia."
        Exit Sub
        
    End If
    
    tableLastColumn = GetTableLastColumnLetter(tableFirstCell)
    tableLastRow = GetTableLastRow(tableFirstCell)
    
    ' copy the table range
    sheet.Range(tableFirstCell, sheet.Range(tableLastColumn & tableLastRow)).Copy
    ' paste to the destiny
    cellToPaste.PasteSpecial Paste:=xlPasteColumnWidths
    cellToPaste.PasteSpecial
    'remove the copy selection
    Application.CutCopyMode = False
        
End Sub
Public Sub DisplayCompanyName(ByVal companyName As String)
' Correct merged cell to display the company name to fit the table lenght and writes the company name
    Dim lastColum As String
    Dim companyNameCell As Range
    Dim newRange As Range
    Dim oldRange As Range
    Dim oldLastColumn As String
    
    Set companyNameCell = SheetSearch.Range("COMPANYNAME")
    
    ' Get the last column index to remove the format
    oldLastColumn = companyNameCell.MergeArea.Cells(companyNameCell.MergeArea.Rows.Count, companyNameCell.MergeArea.Columns.Count).Address
    
    ' Unmerge the cell containing the company name
    companyNameCell.UnMerge
    
    ' Get the range where the company name was
    Set oldRange = SheetSearch.Range(companyNameCell, SheetSearch.Range(oldLastColumn))
    
    ' Remove the borders
    With oldRange
        .Borders(xlEdgeLeft).LineStyle = xlNone
        .Borders(xlEdgeTop).LineStyle = xlNone
        .Borders(xlEdgeBottom).LineStyle = xlNone
        .Borders(xlEdgeRight).LineStyle = xlNone
    End With
    
    ' Get the last column index from the new table
    lastColum = GetTableLastColumnLetter(SheetSearch.Range(SearchFirstCell))
    
    Set newRange = SheetSearch.Range(companyNameCell, SheetSearch.Range(lastColum & companyNameCell.Row))
    
    ' Merge the new range of cell
    newRange.Merge
    
    ' Give the new company name to the merged cell
    companyNameCell = companyName
    
    ' Add the borders to the merged cell
    With newRange
        .Borders(xlEdgeLeft).LineStyle = xlContinuous
        .Borders(xlEdgeLeft).Weight = xlThin
        .Borders(xlEdgeTop).LineStyle = xlContinuous
        .Borders(xlEdgeTop).Weight = xlThin
        .Borders(xlEdgeBottom).LineStyle = xlContinuous
        .Borders(xlEdgeBottom).Weight = xlThin
        .Borders(xlEdgeRight).LineStyle = xlContinuous
        .Borders(xlEdgeRight).Weight = xlThin
    End With


End Sub


Public Sub CreateReport()
' Trigged when the search button is clicked return the company table searched in the Search sheet
    Dim companyName As String
    Dim table As Range
    Dim cellToPaste As Range
    ' first clear the table in the Search sheet
    ClearSearchTable
    ' get the company sheet name select in the combobox
    companyName = SheetSearch.CmbCompaniesName.Value
    
    If companyName = "" Then
        MsgBox "Escolha o nome de uma aba para buscar a tabela  Modular Informações."
        Exit Sub
        
    End If
    ' Display the company name
        
    CopyAndPasteTable companyName, CompanyFirstCell, SheetSearch.Range(SearchFirstCell & SearchFirstRow)
    DisplayCompanyName (companyName)
    
    SheetSearch.Shapes.Range(Array("RefreshButton", "SearchButton", "SaveButton")).Height = 34.0157480315
    
End Sub

Public Sub UpdateTable()
' Copy the changes from the search sheet to the original sheet
    Dim companyName As String
    Dim sheet As Object
    Dim result As VbMsgBoxResult
    
    If IsEmpty(SheetSearch.Range("COMPANYNAME")) Then
        MsgBox "Informe o nome da planilha em que os dados serão atualizados."
        Exit Sub
        
    End If
    ' Get the sheet to capy the changes to
    companyName = SheetSearch.Range("COMPANYNAME")
    ' Ask if the user is sure about the change
    result = MsgBox("Deseja atualizar a tabela original (" & companyName & ")?", vbYesNo)
    
    If result = vbNo Then
        Exit Sub
        
    End If
    
    Set sheet = Sheets(companyName)
    ' Clear the original table
    ClearTable sheet, sheet.Range(CompanyFirstCell)
    ' Copy the table from search sheet and paste it to the original sheet
    CopyAndPasteTable SheetSearch.Name, SearchFirstCell, sheet.Range(CompanyFirstCell)
    
    MsgBox "Tabela (" & companyName & ") atualizada com sucesso!"
    
End Sub

