Attribute VB_Name = "Dashboard"
Public SheetDashBoard As Object
Public Const StatusFirstCell  As String = "B4"
Public FirstCellRedStatus As Range
Public FirstCellBlueStatus As Range
Public FirstCellYelowStatus As Range
Public ArrDashboardHeader() As Variant
Public DefaultSheetHeader As Object
Public ArrDefaultSheetWidthColumns() As Variant
Public Const DefaultSheetHeaderHeight As Integer = 45
Public Const TitleSheetFirstCol As String = "A1"
Public Const HeaderSheetFirstCol As String = "A3"
Public TitleFontFormat As Object
Public HeaderFontFormat As Object
Public BodyFontFormat As Object
Public Const maxRow As Integer = 100

Public Const RedWarning As String = "ATENÇÃO!"
Public Const GreenWarning As String = "Completo"
Public Const YellowWarning As String = "Dentro do Prazo"
Public Const BlueWarning As String = "Prazo não definido"

Public Sub InitDashboard()
' Initialize the Dashboard variables
    Set SheetDashBoard = Sheets("Dashboard")
    Set FirstCellRedStatus = SheetDashBoard.Range("B4")
    Set FirstCellYelowStatus = SheetDashBoard.Range("G4")
    Set FirstCellBlueStatus = SheetDashBoard.Range("L4")
    
    Set TitleFontFormat = CreateObject("Scripting.Dictionary")
    Set HeaderFontFormat = CreateObject("Scripting.Dictionary")
    Set BodyFontFormat = CreateObject("Scripting.Dictionary")
    Set DefaultSheetHeader = CreateObject("Scripting.Dictionary")
    ' Set the Font format
    TitleFontFormat.Add "FontName", "Calibri Light"
    TitleFontFormat.Add "FontSize", 20
    TitleFontFormat.Add "FontBold", False
        
    HeaderFontFormat.Add "FontName", "Calibri Light"
    HeaderFontFormat.Add "FontSize", 11
    HeaderFontFormat.Add "FontBold", False
    HeaderFontFormat.Add "WrapText", True
        
    BodyFontFormat.Add "FontName", "Calibri Light"
    BodyFontFormat.Add "FontSize", 11
    BodyFontFormat.Add "FontBold", False
        
    
    ' The default header for each table (red, blue and yellow) in the dashboard
    ArrDashboardHeader = Array("Sheet", "Status", "Prazo Legal", "Documentos")
    
    ' The default header when a sheet is created
    DefaultSheetHeader.Add "País", 0
    DefaultSheetHeader.Add "Status", 1
    DefaultSheetHeader.Add "Caso", 2
    DefaultSheetHeader.Add "nº do pedido", 3
    DefaultSheetHeader.Add "Protocolo de Depósito", 4
    DefaultSheetHeader.Add "Invoice", 5
    DefaultSheetHeader.Add "Prazo Legal", 6
    DefaultSheetHeader.Add "Documentos", 7
    DefaultSheetHeader.Add "Doc. Assinados cliente", 8
    DefaultSheetHeader.Add "Enviados Correspondente", 9
    
    ' The default width for each column, the array ubound should be the same as the DefaultSheetHeader ubound
    ArrDefaultSheetWidthColumns = Array(11.3, 14.9, 25.5, 10.5, 9.8, 8.5, 9.9, 19.9, 7.1, 11.1)
    
    ' Before featch the data clear the table
    ClearTables
    
    ' Create the headers for each table
    CreateDashboardHeader
    
    ' Create the status tables in the dashborad
    CreateStatusTables
    
    ' Sort the tables by the deadline column
    SortByDate
    
End Sub

Private Sub FormatCell(ByVal cell As Range, Optional ByVal style As String = "")
    ' Format the cell acording to the style
    
    Select Case style
    Case "red"
        cell.Interior.Color = RGB(247, 191, 199)
        With cell.Borders(xlEdgeBottom)
            .Weight = xlThin
            .LineStyle = xlContinuous
        End With
        
    Case "blue"
        cell.Interior.Color = RGB(217, 225, 242)
        With cell.Borders(xlEdgeBottom)
            .Weight = xlThin
            .LineStyle = xlContinuous
        End With
        
    Case "yellow"
        cell.Interior.Color = RGB(255, 230, 153)
        With cell.Borders(xlEdgeBottom)
            .Weight = xlThin
            .LineStyle = xlContinuous
        End With
    
    Case "header"
        With cell
            .Borders(xlEdgeLeft).LineStyle = xlContinuous
            .Borders(xlEdgeTop).LineStyle = xlContinuous
            .Borders(xlEdgeBottom).LineStyle = xlContinuous
            .Borders(xlEdgeRight).LineStyle = xlContinuous
            
            .WrapText = HeaderFontFormat.Item("WrapText")
            .Font.name = HeaderFontFormat.Item("FontName")
            .Font.Size = HeaderFontFormat.Item("FontSize")
            .Font.Bold = HeaderFontFormat.Item("FontBold")
            
            .HorizontalAlignment = xlCenter
            .VerticalAlignment = xlCenter
            
        End With
    
    Case "title"
        With cell
            .Merge
            .Font.name = TitleFontFormat.Item("FontName")
            .Font.Size = TitleFontFormat.Item("FontSize")
            .Font.Bold = TitleFontFormat.Item("FontBold")
            
            .HorizontalAlignment = xlCenter
            .VerticalAlignment = xlCenter
            
            .Borders(xlEdgeLeft).LineStyle = xlContinuous
            .Borders(xlEdgeTop).LineStyle = xlContinuous
            .Borders(xlEdgeBottom).LineStyle = xlContinuous
            .Borders(xlEdgeRight).LineStyle = xlContinuous
    
        End With
    
    Case "status"
        ' RedWarning rule
        cell.FormatConditions.Add Type:=xlCellValue, Operator:=xlEqual, Formula1:="=""" & RedWarning & """"
        cell.FormatConditions(cell.FormatConditions.Count).SetFirstPriority
        With cell.FormatConditions(1)
            .Font.Color = RGB(156, 0, 6)
            .Font.TintAndShade = 0
            
            .Interior.PatternColorIndex = xlAutomatic
            .Interior.Color = RGB(247, 191, 199)
            .Interior.TintAndShade = 0
            
            .StopIfTrue = False
        End With
          
        ' YellowWarning rule
        cell.FormatConditions.Add Type:=xlCellValue, Operator:=xlEqual, Formula1:="=""" & YellowWarning & """"
        cell.FormatConditions(cell.FormatConditions.Count).SetFirstPriority
        With cell.FormatConditions(1)
            .Font.Color = RGB(156, 87, 0)
            .Font.TintAndShade = 0
            
            .Interior.PatternColorIndex = xlAutomatic
            .Interior.Color = RGB(255, 235, 156)
            .Interior.TintAndShade = 0
            
            .StopIfTrue = False
        End With
        
        ' BlueWarning rule
        cell.FormatConditions.Add Type:=xlCellValue, Operator:=xlEqual, Formula1:="=""" & BlueWarning & """"
        cell.FormatConditions(cell.FormatConditions.Count).SetFirstPriority
        With cell.FormatConditions(1)
            .Font.Color = RGB(32, 55, 100)
            .Font.TintAndShade = 0
            
            .Interior.PatternColorIndex = xlAutomatic
            .Interior.Color = RGB(180, 198, 231)
            .Interior.TintAndShade = 0
            
            .StopIfTrue = False
        End With
        
        ' GreenWarning rule
        cell.FormatConditions.Add Type:=xlCellValue, Operator:=xlEqual, Formula1:="=""" & GreenWarning & """"
        cell.FormatConditions(cell.FormatConditions.Count).SetFirstPriority
        With cell.FormatConditions(1)
            .Font.Color = RGB(0, 97, 0)
            .Font.TintAndShade = 0
            
            .Interior.PatternColorIndex = xlAutomatic
            .Interior.Color = RGB(198, 239, 206)
            .Interior.TintAndShade = 0
            
            .StopIfTrue = False
        End With

    Case Else
        cell.Interior.Color = RGB(255, 255, 255)
    
    End Select
        
End Sub

Private Sub CreateDashboardHeader()
' Create the header for each table in the dashboard sheet
    Dim offset As Integer
    
    offset = 0
    For Each col In ArrDashboardHeader
        FirstCellRedStatus.offset(0, offset) = col
        FormatCell FirstCellRedStatus.offset(0, offset), "red"
        
        FirstCellYelowStatus.offset(0, offset) = col
        FormatCell FirstCellYelowStatus.offset(0, offset), "yellow"
        
        FirstCellBlueStatus.offset(0, offset) = col
        FormatCell FirstCellBlueStatus.offset(0, offset), "blue"
        
        offset = offset + 1
        
    Next col

End Sub

Private Function GetHeaderOffsetColumns(ByVal sheetFirstCell As Range) As Long()
' Get the offset based on the sheetFirstCell of the column containing the data to writes in the dashboard table, such as "Documentos" and "Prazo Legal"
' it match the string in the sheet table to get the column index
'   sheetFirstCell should be the first cell in the sheet table
    Dim headerName As Variant
    Dim index As Integer
    Dim arr(0 To 1) As Long
    
    index = 0
    For Each headerName In Range(sheetFirstCell.offset(-1, -1), sheetFirstCell.offset(-1, 0).End(xlToRight))
        If headerName.Value = ArrDashboardHeader(2) Or headerName.Value = ArrDashboardHeader(3) Then
            ' get the offset based on the sheetFirstCell
            arr(index) = headerName.Column - sheetFirstCell.Column
            index = index + 1
            
        End If
        
    Next headerName
    
    GetHeaderOffsetColumns = arr

End Function

Private Sub CreateStatusTables()
' Create the status table in the dashsboard sheet
    Dim company As Variant
    Dim sheet As Object
    Dim sheetFirstCell As Range
    Dim sheetLastRow  As Integer
    Dim status As Variant
    Dim arrOffset() As Long
    Dim offsetRedAlert As Integer
    Dim offsetYellowAlert As Integer
    Dim offsetBlueAlert As Integer
    
    offsetRedAlert = 1
    offsetYellowAlert = 1
    offsetBlueAlert = 1
    
    For Each company In Companies.keys
        ' Get the sheet to search the status
        Set sheet = Sheets(company)
        ' Set the status column first cell
        Set sheetFirstCell = sheet.Range(StatusFirstCell)
        
        ' Get the offset of the column to get data based on the first cell
        arrOffset = GetHeaderOffsetColumns(sheetFirstCell)
        
        sheetLastRow = GetTableLastRow(sheetFirstCell) - sheetFirstCell.row
        
        ' If the table is empty
        If sheetLastRow <= 0 Then GoTo skipCompany
        
        ' Go through the table to get the data
        For Each status In sheet.Range(sheetFirstCell, sheetFirstCell.offset(sheetLastRow, 0))
            ' if the status value match the value get the cell value and add to the sheet dashboard
            If status.Value = RedWarning Then
                FirstCellRedStatus.offset(offsetRedAlert, 0) = company
                FirstCellRedStatus.offset(offsetRedAlert, 1) = status.Value
                FirstCellRedStatus.offset(offsetRedAlert, 2) = status.offset(0, arrOffset(0)).Value
                FirstCellRedStatus.offset(offsetRedAlert, 3) = status.offset(0, arrOffset(1)).Value
                                
                offsetRedAlert = offsetRedAlert + 1
                
            ElseIf status.Value = BlueWarning Then
                FirstCellBlueStatus.offset(offsetBlueAlert, 0) = company
                FirstCellBlueStatus.offset(offsetBlueAlert, 1) = status
                FirstCellBlueStatus.offset(offsetBlueAlert, 2) = status.offset(0, arrOffset(0)).Value
                FirstCellBlueStatus.offset(offsetBlueAlert, 3) = status.offset(0, arrOffset(1)).Value
                
                offsetBlueAlert = offsetBlueAlert + 1
            
            ElseIf status.Value = YellowWarning Then
                FirstCellYelowStatus.offset(offsetYellowAlert, 0) = company
                FirstCellYelowStatus.offset(offsetYellowAlert, 1) = status
                FirstCellYelowStatus.offset(offsetYellowAlert, 2) = status.offset(0, arrOffset(0)).Value
                FirstCellYelowStatus.offset(offsetYellowAlert, 3) = status.offset(0, arrOffset(1)).Value
                
                offsetYellowAlert = offsetYellowAlert + 1
            
            End If
            
        Next status

skipCompany:
    
    Next company
    
    
End Sub

Private Sub ClearTables()
    ' For each status table (red, blue and yellow) cleat the contents
    SheetDashBoard.Range(FirstCellRedStatus.offset(1, 0), _
                         FirstCellRedStatus.offset(GetTableLastRow(FirstCellRedStatus) - FirstCellRedStatus.row, _
                                                   UBound(ArrDashboardHeader))).ClearContents
                                                   
    SheetDashBoard.Range(FirstCellBlueStatus.offset(1, 0), _
                         FirstCellBlueStatus.offset(GetTableLastRow(FirstCellBlueStatus) - FirstCellBlueStatus.row, _
                                                      UBound(ArrDashboardHeader))).ClearContents
                                                      
    SheetDashBoard.Range(FirstCellYelowStatus.offset(1, 0), _
                         FirstCellYelowStatus.offset(GetTableLastRow(FirstCellYelowStatus) - FirstCellYelowStatus.row, _
                                                     UBound(ArrDashboardHeader))).ClearContents


End Sub

Private Sub SortByDate()
    ' Get each status table range and sort by the deadline column
    SheetDashBoard.Range(FirstCellRedStatus.offset(1, 0), _
                         FirstCellRedStatus.offset(GetTableLastRow(FirstCellRedStatus), UBound(ArrDashboardHeader))).Sort Key1:=FirstCellRedStatus.offset(0, 2), Order1:=xlAscending
    SheetDashBoard.Range(FirstCellBlueStatus.offset(1, 0), _
                         FirstCellBlueStatus.offset(GetTableLastRow(FirstCellBlueStatus), UBound(ArrDashboardHeader))).Sort Key1:=FirstCellBlueStatus.offset(0, 2), Order1:=xlAscending
    SheetDashBoard.Range(FirstCellYelowStatus.offset(1, 0), _
                         FirstCellYelowStatus.offset(GetTableLastRow(FirstCellYelowStatus), UBound(ArrDashboardHeader))).Sort Key1:=FirstCellYelowStatus.offset(0, 2), Order1:=xlAscending
    
End Sub
Private Function ValidateSheetName(ByVal sheetName As String) As Boolean
' Validate the sheetName return True if the given name can be a sheet name, else return False
    ValidateSheetName = False
    
    If sheetName = "" Then
        MsgBox "Nome invalido, o planilha não pode ser vazio"
        Exit Function
        
    ElseIf Len(sheetName) > 31 Then
        MsgBox "Nome inválido, insira um nome com 30 caracteres ou menos"
        Exit Function
        
    ElseIf InStr("'", sheetName) Then
        MsgBox "Nome inválido, o caracter ' não é aceito como caracter valido no nome da planilha"
        Exit Function
        
    ElseIf InStr("\", sheetName) Then
        MsgBox "Nome inválido, o caracter \ não é aceito como caracter valido no nome da planilha"
        Exit Function
        
    ElseIf InStr("/", sheetName) Then
        MsgBox "Nome inválido, o caracter / não é aceito como caracter valido no nome da planilha"
        Exit Function
        
    ElseIf InStr("?", sheetName) Then
        MsgBox "Nome inválido, o caracter ? não é aceito como caracter valido no nome da planilha"
        Exit Function
        
    ElseIf InStr("*", sheetName) Then
        MsgBox "Nome inválido, o caracter * não é aceito como caracter valido no nome da planilha"
        Exit Function
        
    ElseIf Companies.exists(sheetName) Then
        MsgBox "Nome inválido, já existe um planilha com esse nome"
        Exit Function
        
    End If
    
    ValidateSheetName = True

End Function

Private Sub CreateTableTitle(ByVal sheet As Object)
' Create the default title, with the default format, in the table when a sheet is created
    Dim defaultTitle As Range
    
    ' Get the title range based on the DefaultSheetHeader
    Set defaultTitle = sheet.Range(sheet.Range(TitleSheetFirstCol), sheet.Range(TitleSheetFirstCol).offset(1, DefaultSheetHeader.Count - 1)) ' the first index is 0 while the first count is 1, then count -1 should be equal to the index
    
    FormatCell defaultTitle, "title"
    
    defaultTitle.Value = sheet.name
    
End Sub

Private Sub CreateSheetDefaultHeader(ByVal sheet As Object)
' Create the default header in the new sheet
    Dim index As Integer
    Dim firstCell As Range
    Dim name As Variant
    Dim columnLetter As String
    Dim cell As Range
        
    Set firstCell = sheet.Range(HeaderSheetFirstCol)
    
    For Each name In DefaultSheetHeader.keys
        Set cell = firstCell.offset(0, DefaultSheetHeader(name))
        cell.Value = name
        
        FormatCell cell, "header"
        
        ' Set the width
        columnLetter = Split(cell.Cells.Address, "$")(1)
        Columns(columnLetter & ":" & columnLetter).ColumnWidth = ArrDefaultSheetWidthColumns(DefaultSheetHeader(name))
        
    Next name
    
    ' Set the header row height
    Rows(firstCell.row & ":" & firstCell.row).RowHeight = DefaultSheetHeaderHeight
    
End Sub

Public Sub CreateTableBody(ByVal sheet As Object)
    Dim tableBody As Range
    Dim firstStatusRow As Range
    Dim statusCell  As Variant
    Dim row As Integer
    Dim documentCell As Range
    Dim documentWasSentCell As Range
    Dim deadlineCell As Range
    Dim firstCell As Range
    
    Set firstCell = sheet.Range(HeaderSheetFirstCol)
    
    ' get the cells under the header, the same number of columns of the header, and go down
    Set tableBody = sheet.Range(sheet.Range(firstCell.offset(1, 0), firstCell.offset(1, DefaultSheetHeader.Count)), _
                                sheet.Range(firstCell.offset(1, 0), firstCell.offset(maxRow, DefaultSheetHeader.Count)))
    
    FormatCell tableBody
    
    For row = 1 To maxRow
        Set statusCell = firstCell.offset(row, DefaultSheetHeader("Status"))
        Set documentCell = statusCell.offset(0, DefaultSheetHeader("Documentos") - DefaultSheetHeader("Status"))
        Set documentWasSentCell = statusCell.offset(0, DefaultSheetHeader("Enviados Correspondente") - DefaultSheetHeader("Status"))
        Set deadlineCell = statusCell.offset(0, DefaultSheetHeader("Prazo Legal") - DefaultSheetHeader("Status"))
        
        statusCell.Formula = "=IF(ISBLANK(" & documentCell.Address & "), """"," & _
                                  "IF(" & documentWasSentCell.Address & "=""ok"",""" & GreenWarning & """," & _
                                      "IF(OR(ISBLANK(" & deadlineCell.Address & ")," & deadlineCell.Address & "=""-""), """ & BlueWarning & """," & _
                                          "IF(NETWORKDAYS(TODAY," & deadlineCell.Address & ")<=8,""" & RedWarning & """,""" & YellowWarning & """))))"
    Next row
    
    columnLetter = Split(firstCell.offset(0, DefaultSheetHeader("Status")).Address, "$")(1)
    Set statusColumn = Columns(columnLetter & ":" & columnLetter)
    
    FormatCell statusColumn, "status"
    
    
End Sub

Public Sub CreatSheet()
' Create a new sheet with the default header
    Dim sheetName As String
    Dim sheet As Object
    
     ' Ask for a sheet name
    sheetName = InputBox("Insira o nome da planilha")
    
    ' Validate the inputed name
    If Not ValidateSheetName(sheetName) Then
        Exit Sub
        
    End If
    
    ' Create the sheet before the search sheet (this one should be the last one)
    Sheets.Add Before:=SheetSearch
    ' Search the new sheet in the sheets to rename it
    For i = 1 To Sheets.Count:
        If Companies.exists(Sheets(i).name) = False And Sheets(i).name <> "Search" And Sheets(i).name <> "Dashboard" Then
            Sheets(i).name = sheetName
            Exit For
            
        End If
        
    Next i
    
    Set sheet = Sheets(sheetName)
    ' Set the default header and title
    CreateTableTitle sheet
    CreateSheetDefaultHeader sheet
    CreateTableBody sheet
    
    ' Update the Company dict
    UpdateCompaniesName
    
End Sub
