Attribute VB_Name = "Commun"
Public Companies As Object

Public Function GetTableLastColumnLetter(ByVal sheetFirstCell As Range) As String
' get the table last column letter based on the header
    GetTableLastColumnLetter = Split(sheetFirstCell.End(xlToRight).Cells.Address, "$")(1)
    
End Function

Public Function GetTableLastRow(ByVal sheetFirstCell As Range) As Integer
' Get the table last column based on the first column
    Dim auxRange As Range
    Set auxRange = sheetFirstCell
    
    ' the table is grouped by the value in the first column, for each contry in there is an block and then there is an empty row
    Do
        ' If it goes down to the last row then the auxRange is the last cell containing value
        If auxRange.End(xlDown).Row = 1048576 Then Exit Do
        Set auxRange = auxRange.End(xlDown)
                
    Loop
    ' if the cell is merged get the last cell in the merged cells
    Set auxRange = auxRange.MergeArea.Cells(auxRange.MergeArea.Rows.Count, auxRange.MergeArea.Columns.Count)
    
    GetTableLastRow = auxRange.Row
    
End Function

Private Sub ClearCombobox(ByVal cmb As Object)
' clear the bombobox options and the choosed value
    cmb.Clear
    cmb.Value = ""
    
End Sub

Public Sub UpdateCompaniesName()
' Fill the Company Name combobox and update the companies dictionary
    Dim i As Integer
    Dim CmbCompaniesName As Object
    
    Set CmbCompaniesName = SheetSearch.CmbCompaniesName
    Set Companies = CreateObject("Scripting.Dictionary")
    
    ' First cleat the combobox before add the Companies opitions
    ClearCombobox CmbCompaniesName
    
    ' Go through all the sheets
    For i = 1 To Sheets.Count:
        ' Get all the sheets name except for the "Search" and "Dashboard" sheet because its not a company
        If Sheets(i).Name <> "Search" And Sheets(i).Name <> "Dashboard" Then
            Companies(Sheets(i).Name) = i
            CmbCompaniesName.AddItem Sheets(i).Name
            
        End If
        
    Next i
    
End Sub
